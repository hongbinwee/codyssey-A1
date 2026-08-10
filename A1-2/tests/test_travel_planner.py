import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from urllib.error import HTTPError

import travel_planner


VALID_RECOMMENDATION = {
    "recommended_city": "서울",
    "weather": "선선하고 맑습니다.",
    "events": ["전시 관람"],
    "reason": "도심 이동이 편리합니다. 봄 행사를 함께 즐길 수 있습니다.",
}


class TravelPlannerTests(unittest.TestCase):
    def test_call_openai_chat_omits_temperature_for_gpt5_models(self):
        response = {"choices": [{"message": {"content": "{}"}}]}

        with patch.object(travel_planner, "call_json_api", return_value=response) as call:
            travel_planner.call_openai_chat("key", "gpt-5.6-luna", [], temperature=0.2)

        payload = call.call_args.kwargs["payload"]
        self.assertNotIn("temperature", payload)

    def test_validate_recommendation_rejects_empty_events(self):
        recommendation = dict(VALID_RECOMMENDATION, events=[])

        with self.assertRaisesRegex(ValueError, "events must contain 1-3"):
            travel_planner.validate_recommendation(recommendation)

    def test_validate_recommendation_rejects_reason_with_wrong_sentence_count(self):
        recommendation = dict(VALID_RECOMMENDATION, reason="한 문장입니다.")

        with self.assertRaisesRegex(ValueError, "reason must contain 2-4"):
            travel_planner.validate_recommendation(recommendation)

    def test_generate_recommendation_does_not_retry_http_error(self):
        errors = []
        http_error = HTTPError(
            "https://api.openai.com/v1/chat/completions",
            401,
            "Unauthorized",
            hdrs=None,
            fp=None,
        )

        with patch.object(travel_planner, "call_openai_chat", side_effect=http_error) as call:
            with self.assertRaises(HTTPError):
                travel_planner.generate_recommendation("key", "gpt-5.6-luna", "2026-03-15", errors)

        self.assertEqual(call.call_count, 1)
        self.assertEqual(errors[0]["type"], "AUTH_ERROR")

    def test_generate_recommendation_retries_invalid_json_once(self):
        errors = []
        responses = ["not json", json.dumps(VALID_RECOMMENDATION, ensure_ascii=False)]

        with patch.object(travel_planner, "call_openai_chat", side_effect=responses) as call:
            result = travel_planner.generate_recommendation(
                "key", "gpt-5.6-luna", "2026-03-15", errors
            )

        self.assertEqual(result, VALID_RECOMMENDATION)
        self.assertEqual(call.call_count, 2)
        self.assertEqual(errors[0]["type"], "JSON_PARSE_RETRY")

    def test_generate_report_falls_back_when_required_section_is_missing(self):
        errors = []

        with patch.object(travel_planner, "call_openai_chat", return_value="# incomplete report"):
            report = travel_planner.generate_report(
                "key", "gpt-5.6-luna", "2026-03-15", VALID_RECOMMENDATION, [], errors
            )

        self.assertIn("## 오류 요약(errors)", report)
        self.assertEqual(errors[0]["type"], "REPORT_GENERATION_FALLBACK")

    def test_normalize_city_name_handles_common_suffixes(self):
        self.assertEqual(travel_planner.normalize_city_name(" 서울특별시 "), "서울")
        self.assertEqual(travel_planner.normalize_city_name("부산시"), "부산")

    def test_kakao_provider_receives_normalized_city(self):
        errors = []
        with patch.object(travel_planner, "call_json_api", return_value={"documents": []}) as call:
            provider = travel_planner.KakaoPlaceSearchProvider("key")
            provider.search("서울시", errors)

        self.assertIn("query=%EC%84%9C%EC%9A%B8+%EB%A7%9B%EC%A7%91", call.call_args.args[0])

    def test_load_cached_outputs_accepts_complete_same_date_result(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            base_dir = Path(temp_dir)
            results_dir = base_dir / "results"
            results_dir.mkdir()
            (results_dir / "2026-03-15_raw.json").write_text(
                json.dumps(
                    {
                        "date": "2026-03-15",
                        "recommendation": VALID_RECOMMENDATION,
                        "restaurants": [],
                        "errors": [],
                    },
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )
            (results_dir / "2026-03-15_travel_plan.md").write_text("# cached", encoding="utf-8")

            cached = travel_planner.load_cached_outputs(base_dir, "2026-03-15", [])

        self.assertIsNotNone(cached)
        self.assertEqual(cached[0], VALID_RECOMMENDATION)

    def test_load_cached_outputs_accepts_raw_json_without_report(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            base_dir = Path(temp_dir)
            results_dir = base_dir / "results"
            results_dir.mkdir()
            (results_dir / "2026-03-15_raw.json").write_text(
                json.dumps(
                    {
                        "date": "2026-03-15",
                        "recommendation": VALID_RECOMMENDATION,
                        "restaurants": [],
                        "errors": [],
                    },
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )

            cached = travel_planner.load_cached_outputs(base_dir, "2026-03-15", [])

        self.assertIsNotNone(cached)
        self.assertIsNone(cached[3])

    def test_load_cached_outputs_ignores_incomplete_cache(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            base_dir = Path(temp_dir)
            results_dir = base_dir / "results"
            results_dir.mkdir()
            (results_dir / "2026-03-15_raw.json").write_text("{}", encoding="utf-8")
            (results_dir / "2026-03-15_travel_plan.md").write_text("# cached", encoding="utf-8")

            cached = travel_planner.load_cached_outputs(base_dir, "2026-03-15", [])

        self.assertIsNone(cached)

    def test_save_outputs_records_write_error(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            base_dir = Path(temp_dir)
            (base_dir / "results").write_text("not a directory", encoding="utf-8")
            errors = []

            paths = travel_planner.save_outputs(
                base_dir,
                "2026-03-15",
                VALID_RECOMMENDATION,
                [],
                errors,
                "# report\n",
            )

        self.assertEqual(paths, (None, None))
        self.assertEqual(errors[0]["type"], "OUTPUT_WRITE_ERROR")


if __name__ == "__main__":
    unittest.main()
