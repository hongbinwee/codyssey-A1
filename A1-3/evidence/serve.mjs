// 로컬 정적 서버 — A1-3 루트를 서빙한다.
// 사용: node evidence/serve.mjs [port]   (기본 포트 4317)
import http from "node:http";
import { readFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const port = Number(process.argv[2]) || 4317;
// /api 요청은 로컬 Python API 러너(evidence/run_api.py)로 전달한다.
// 배포 환경에서는 Vercel이 같은 경로를 Python Function으로 연결한다.
const apiTarget = process.env.AXG_API_ORIGIN || "http://127.0.0.1:4318";

const proxyApi = (req, res) => {
  const chunks = [];
  req.on("data", (c) => chunks.push(c));
  req.on("end", async () => {
    try {
      const upstream = await fetch(apiTarget + req.url, {
        method: req.method,
        headers: { "Content-Type": req.headers["content-type"] || "application/json" },
        body: req.method === "GET" || req.method === "HEAD" ? undefined : Buffer.concat(chunks),
      });
      const data = Buffer.from(await upstream.arrayBuffer());
      res.writeHead(upstream.status, {
        "Content-Type": upstream.headers.get("content-type") || "application/json; charset=utf-8",
        "Cache-Control": "no-store",
      });
      res.end(data);
    } catch {
      res.writeHead(502, { "Content-Type": "application/json; charset=utf-8" });
      res.end(JSON.stringify({ ok: false, error: { code: "API_DOWN", message: "로컬 API 서버에 연결할 수 없습니다. evidence/run_api.py를 실행했는지 확인하세요." } }));
    }
  });
};

const MIME = {
  ".html": "text/html; charset=utf-8",
  ".css": "text/css; charset=utf-8",
  ".js": "text/javascript; charset=utf-8",
  ".mjs": "text/javascript; charset=utf-8",
  ".json": "application/json; charset=utf-8",
  ".png": "image/png",
  ".jpg": "image/jpeg",
  ".jpeg": "image/jpeg",
  ".gif": "image/gif",
  ".svg": "image/svg+xml",
  ".webp": "image/webp",
  ".ico": "image/x-icon",
  ".woff": "font/woff",
  ".woff2": "font/woff2",
  ".mp4": "video/mp4",
  ".webm": "video/webm",
  ".m3u8": "application/vnd.apple.mpegurl",
  ".ts": "video/mp2t",
};

http
  .createServer(async (req, res) => {
    if (req.url.startsWith("/api/")) { proxyApi(req, res); return; }
    try {
      let pathname = decodeURIComponent(new URL(req.url, "http://localhost").pathname);
      if (pathname === "/" || pathname.endsWith("/")) pathname += "index.html";
      const file = path.normalize(path.join(root, pathname));
      if (!file.startsWith(root)) {
        res.writeHead(403).end("Forbidden");
        return;
      }
      const data = await readFile(file);
      res.writeHead(200, {
        "Content-Type": MIME[path.extname(file).toLowerCase()] || "application/octet-stream",
        "Cache-Control": "no-cache",
      });
      res.end(data);
    } catch {
      res.writeHead(404).end("Not found");
    }
  })
  .listen(port, "127.0.0.1", () => {
    console.log("AX Ground dev server: http://127.0.0.1:" + port + "/  (root: " + root + ")");
  });
