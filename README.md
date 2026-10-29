# littlecoinapp

A Python CLI starter for identifying coins from photos with OpenAI vision and
returning a cautious, approximate value range.

## Requirements

- Python 3.10 or later
- An OpenAI API key with access to a vision-capable model

## Setup

From this directory, create and activate the virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .
```

Create your local configuration file and add your API key:

```bash
cp .env.example .env
```

Edit `.env` and set `OPENAI_API_KEY`. The default model is `gpt-4.1-mini`;
override it by setting `OPENAI_MODEL` in `.env`.

## Usage

```bash
littlecoinapp analyze path/to/coin.jpg
```

The command prints JSON with a possible identification, visible condition,
estimated USD value range, confidence, and caveats. Supported image formats are
JPEG, PNG, WEBP, and GIF. A clear photo of both sides generally helps
identification; this starter currently analyzes one image per invocation.

## Valuation notes

The value is an AI-generated estimate, not a verified market quote or
professional appraisal. Coin value can depend on details that are difficult to
judge from a photo, including authenticity, grade, mint errors, provenance, and
recent sales. Verify important findings with a reputable numismatist or
up-to-date sold-price data before buying, selling, or insuring a coin.
