import base64
import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from littlecoinapp.analyzer import analyze_coin


class AnalyzeCoinTests(unittest.TestCase):
    def setUp(self):
        dotenv = patch("littlecoinapp.analyzer.load_dotenv")
        dotenv.start()
        self.addCleanup(dotenv.stop)
        self.environment = patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}, clear=True)
        self.environment.start()
        self.addCleanup(self.environment.stop)

    def test_sends_image_to_openai_and_returns_analysis(self):
        analysis = {"confidence": "medium", "estimated_value": {"low": 1, "high": 5}}
        with tempfile.TemporaryDirectory() as directory:
            image_path = Path(directory) / "coin.jpg"
            image_path.write_bytes(b"coin image")

            with patch("littlecoinapp.analyzer.OpenAI") as openai:
                openai.return_value.responses.create.return_value.output_text = json.dumps(
                    analysis
                )

                result = analyze_coin(image_path)

        self.assertEqual(result, analysis)
        openai.assert_called_once_with(api_key="test-key")
        request = openai.return_value.responses.create.call_args.kwargs
        image = request["input"][0]["content"][1]
        self.assertEqual(image["type"], "input_image")
        self.assertEqual(
            image["image_url"],
            "data:image/jpeg;base64," + base64.b64encode(b"coin image").decode("ascii"),
        )
        self.assertEqual(request["text"]["format"]["type"], "json_schema")

    def test_rejects_missing_image(self):
        with self.assertRaisesRegex(ValueError, "does not exist"):
            analyze_coin(Path("missing-coin.jpg"))

    def test_rejects_unsupported_image_type(self):
        with tempfile.TemporaryDirectory() as directory:
            image_path = Path(directory) / "coin.bmp"
            image_path.write_bytes(b"coin image")

            with self.assertRaisesRegex(ValueError, "JPEG, PNG, WEBP, or GIF"):
                analyze_coin(image_path)

    def test_requires_api_key(self):
        with patch.dict(os.environ, {}, clear=True):
            with tempfile.TemporaryDirectory() as directory:
                image_path = Path(directory) / "coin.jpg"
                image_path.write_bytes(b"coin image")

                with self.assertRaisesRegex(ValueError, "OPENAI_API_KEY"):
                    analyze_coin(image_path)


if __name__ == "__main__":
    unittest.main()
