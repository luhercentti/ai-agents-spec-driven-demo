"""
Demo 01 — Spec to API
Reads SPEC.md and generates a complete FastAPI application.
Output is written to output/main.py.
"""

import ast
import json
import os
import sys
from pathlib import Path

from openai import OpenAI

SPEC_PATH = Path(__file__).parent / "SPEC.md"
OUTPUT_PATH = Path(__file__).parent / "output" / "main.py"
MODEL = os.environ.get("OPENAI_MODEL", "gpt-4o")
# Claude models don't support response_format=json_object — the system prompt handles JSON output
SUPPORTS_JSON_MODE = not MODEL.startswith("claude")

SYSTEM_PROMPT = """
You are an expert Python developer. Your task is to read an API specification written
in plain English and generate a complete, runnable FastAPI application that implements it.

Rules:
- Use FastAPI and Pydantic v2
- Use an in-memory list as the data store (no database, no SQLAlchemy)
- Implement exactly the endpoints described — no more, no less
- Include a uvicorn.run entrypoint at the bottom guarded by if __name__ == "__main__"
- Add a short docstring to each route handler explaining what it does
- Do not add authentication, middleware, or features not mentioned in the spec

Return a JSON object with a single key "code" whose value is the complete Python source
code as a string. Do not include any explanation or commentary outside the JSON object.
""".strip()


def load_spec() -> str:
    if not SPEC_PATH.exists():
        print(f"Error: SPEC.md not found at {SPEC_PATH}", file=sys.stderr)
        sys.exit(1)
    content = SPEC_PATH.read_text().strip()
    if not content:
        print("Error: SPEC.md is empty", file=sys.stderr)
        sys.exit(1)
    return content


def generate_api(spec: str) -> str:
    client = OpenAI()
    print(f"Calling API (model: {MODEL})...")
    kwargs = {"response_format": {"type": "json_object"}} if SUPPORTS_JSON_MODE else {}
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": spec},
        ],
        **kwargs,
    )
    raw = response.choices[0].message.content
    parsed = json.loads(raw)
    if "code" not in parsed:
        print(f"Error: response missing 'code' key. Got: {list(parsed.keys())}", file=sys.stderr)
        sys.exit(1)
    return parsed["code"]


def validate_python(code: str) -> None:
    try:
        ast.parse(code)
    except SyntaxError as e:
        print(f"Error: generated code has a syntax error: {e}", file=sys.stderr)
        sys.exit(1)


def main() -> None:
    spec = load_spec()
    code = generate_api(spec)
    validate_python(code)
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(code)
    lines = code.count("\n") + 1
    print(f"Done. Written {lines} lines to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
