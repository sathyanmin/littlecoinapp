import base64
import json
import mimetypes
import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI


_SUPPORTED_IMAGE_TYPES = {"image/jpeg", "image/png", "image/webp", "image/gif"}
_ANALYSIS_SCHEMA = {
    "type": "object",
    "properties": {
        "identification": {
            "type": "object",
            "properties": {
                "country": {"type": ["string", "null"]},
                "denomination": {"type": ["string", "null"]},
                "year": {"type": ["string", "null"]},
                "mint_mark": {"type": ["string", "null"]},
                "composition": {"type": ["string", "null"]},
            },
            "required": [
                "country",
                "denomination",
                "year",
                "mint_mark",
                "composition",
            ],
            "additionalProperties": False,
        },
        "condition_assessment": {"type": "string"},
        "estimated_value": {
            "type": "object",
            "properties": {
                "low": {"type": "number"},
                "high": {"type": "number"},
                "currency": {"type": "string"},
            },
            "required": ["low", "high", "currency"],
            "additionalProperties": False,
        },
        "valuation_basis": {"type": "string"},
        "confidence": {"type": "string", "enum": ["low", "medium", "high"]},
        "caveats": {"type": "array", "items": {"type": "string"}},
    },
    "required": [
        "identification",
        "condition_assessment",
        "estimated_value",
        "valuation_basis",
        "confidence",
        "caveats",
    ],
    "additionalProperties": False,
}


def analyze_coin(image_path: Path) -> dict:
    load_dotenv()

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or api_key == "your-openai-api-key":
        raise ValueError(
            "Set OPENAI_API_KEY in your .env file before analyzing a coin."
        )

    if not image_path.is_file():
        raise ValueError(f"Image file does not exist: {image_path}")

    media_type, _ = mimetypes.guess_type(image_path.name)
    if media_type not in _SUPPORTED_IMAGE_TYPES:
        raise ValueError("Use a JPEG, PNG, WEBP, or GIF image.")

    encoded_image = base64.b64encode(image_path.read_bytes()).decode("ascii")
    image_url = f"data:{media_type};base64,{encoded_image}"

    client = OpenAI(api_key=api_key)
    response = client.responses.create(
        model=os.getenv("OPENAI_MODEL", "gpt-4.1-mini"),
        input=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": (
                            "Identify the coin from the visible evidence and provide "
                            "a cautious, approximate value range in USD. Do not invent "
                            "details that cannot be read; use null for unknown "
                            "identification fields. Assess visible condition, explain "
                            "the basis of the estimate, and list important caveats. "
                            "This is an informational estimate, not a professional "
                            "appraisal."
                        ),
                    },
                    {"type": "input_image", "image_url": image_url, "detail": "high"},
                ],
            }
        ],
        text={
            "format": {
                "type": "json_schema",
                "name": "coin_analysis",
                "strict": True,
                "schema": _ANALYSIS_SCHEMA,
            }
        },
    )
    return json.loads(response.output_text)
