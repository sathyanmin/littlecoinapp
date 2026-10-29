import io
import json
import sys
import unittest
from contextlib import redirect_stderr, redirect_stdout
from unittest.mock import patch

from littlecoinapp.cli import main


class CliTests(unittest.TestCase):
    def test_prints_analysis_as_json(self):
        analysis = {"identification": {"year": "1900"}}
        with (
            patch.object(sys, "argv", ["littlecoinapp", "analyze", "coin.jpg"]),
            patch("littlecoinapp.cli.analyze_coin", return_value=analysis),
            redirect_stdout(io.StringIO()) as stdout,
        ):
            result = main()

        self.assertEqual(result, 0)
        self.assertEqual(json.loads(stdout.getvalue()), analysis)

    def test_reports_invalid_input(self):
        with (
            patch.object(sys, "argv", ["littlecoinapp", "analyze", "coin.jpg"]),
            patch(
                "littlecoinapp.cli.analyze_coin",
                side_effect=ValueError("Invalid image"),
            ),
            redirect_stderr(io.StringIO()) as stderr,
        ):
            result = main()

        self.assertEqual(result, 1)
        self.assertIn("Error: Invalid image", stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
