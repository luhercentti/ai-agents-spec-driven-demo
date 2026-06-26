"""
Demo 03 — Changelog Agent
Reads git_log.txt and produces a Keep a Changelog formatted CHANGELOG.md.
Output is written to output/CHANGELOG.md.
"""

import json
import os
import sys
from pathlib import Path

from openai import OpenAI

LOG_PATH = Path(__file__).parent / "git_log.txt"
OUTPUT_PATH = Path(__file__).parent / "output" / "CHANGELOG.md"
MODEL = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")
SUPPORTS_JSON_MODE = not MODEL.startswith("claude")

SYSTEM_PROMPT = """
You are a technical writer converting raw git commit messages into a clean changelog.

Rules:
- Group changes into: added, changed, fixed, removed
- Rewrite each entry as a clear past-tense sentence (e.g., "Added rate limiting to all API routes")
- Omit noise commits: "wip", "cleanup", "fix typo", "update dependencies", "temp"
- Do not include commit hashes
- Do not invent changes not implied by the commit messages
- Merge closely related commits into a single entry if appropriate
- Omit any category that has no entries

Return a JSON object with this structure:
{
  "version": "[Unreleased]",
  "added": ["...", "..."],
  "changed": ["...", "..."],
  "fixed": ["...", "..."],
  "removed": ["...", "..."]
}

Omit any key whose array would be empty.
Return only the raw JSON object — no Markdown, no explanation.
""".strip()


def load_log() -> str:
    if not LOG_PATH.exists():
        print(f"Error: git log file not found at {LOG_PATH}", file=sys.stderr)
        sys.exit(1)
    content = LOG_PATH.read_text().strip()
    if not content:
        print("Error: git log file is empty", file=sys.stderr)
        sys.exit(1)
    return content


def generate_changelog(log: str) -> dict:
    client = OpenAI()
    print(f"Calling API (model: {MODEL})...")
    kwargs = {"response_format": {"type": "json_object"}} if SUPPORTS_JSON_MODE else {}
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": log},
        ],
        **kwargs,
    )
    return json.loads(response.choices[0].message.content)


def format_changelog(data: dict) -> str:
    version = data.get("version", "[Unreleased]")
    lines = [
        "# Changelog\n",
        "All notable changes to this project will be documented in this file.\n",
        "Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).\n",
        f"## {version}\n",
    ]
    section_labels = {
        "added": "Added",
        "changed": "Changed",
        "fixed": "Fixed",
        "removed": "Removed",
    }
    for key, label in section_labels.items():
        entries = data.get(key, [])
        if entries:
            lines.append(f"### {label}\n")
            for entry in entries:
                lines.append(f"- {entry}")
            lines.append("")
    return "\n".join(lines)


def main() -> None:
    log = load_log()
    data = generate_changelog(log)
    changelog = format_changelog(data)
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(changelog)
    print(f"Done. Changelog written to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
