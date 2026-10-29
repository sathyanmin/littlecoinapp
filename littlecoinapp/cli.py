import argparse
import json
import sys
from pathlib import Path

from openai import OpenAIError

from littlecoinapp.analyzer import analyze_coin


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="littlecoinapp",
        description="Identify a coin from a photo and estimate its value.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    analyze_parser = subparsers.add_parser(
        "analyze", help="Analyze a coin image with OpenAI vision."
    )
    analyze_parser.add_argument("image", type=Path, help="Path to a coin image")
    args = parser.parse_args()

    try:
        result = analyze_coin(args.image)
    except (ValueError, OSError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    except OpenAIError as exc:
        print(f"OpenAI request failed: {exc}", file=sys.stderr)
        return 1

    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
