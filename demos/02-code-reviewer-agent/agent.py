"""
Demo 02 — Code Reviewer Agent
Reads sample_diff.txt and produces a structured code review.
Output is written to output/review.md.
"""

import json
import sys
from pathlib import Path

from openai import OpenAI

DIFF_PATH = Path(__file__).parent / "sample_diff.txt"
OUTPUT_PATH = Path(__file__).parent / "output" / "review.md"

SYSTEM_PROMPT = """
You are a senior software engineer performing a code review.

Review the provided unified diff against this rubric (in priority order):
1. Correctness — does the code do what it appears to intend?
2. Error handling — are failure modes (None values, missing env vars, exceptions) handled?
3. Security — are there credential leaks, insecure algorithms, or injection risks?
4. Clarity — is the code easy to understand?
5. Unnecessary complexity — is anything harder to read than it needs to be?

Do NOT comment on code style, formatting, whitespace, or architectural concerns
outside the scope of the diff.

Severity levels: critical | major | minor | info

Return a JSON object with this exact structure:
{
  "summary": "2-4 sentence overall assessment",
  "findings": [
    {
      "severity": "critical | major | minor | info",
      "file": "relative file path",
      "line": "line number or range",
      "issue": "what is wrong",
      "suggestion": "what to do instead"
    }
  ],
  "verdict": "approve | request-changes | needs-discussion"
}

If there are no findings, return an empty array and set verdict to "approve".
Return only the raw JSON object — no Markdown, no explanation.
""".strip()


def load_diff() -> str:
    if not DIFF_PATH.exists():
        print(f"Error: diff file not found at {DIFF_PATH}", file=sys.stderr)
        sys.exit(1)
    content = DIFF_PATH.read_text().strip()
    if not content:
        print("Error: diff file is empty", file=sys.stderr)
        sys.exit(1)
    return content


def review_diff(diff: str) -> dict:
    client = OpenAI()
    print("Calling OpenAI API...")
    response = client.chat.completions.create(
        model="gpt-4o",
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": diff},
        ],
    )
    return json.loads(response.choices[0].message.content)


def format_report(review: dict) -> str:
    lines = ["# Code Review\n"]
    verdict = review.get("verdict", "unknown")
    lines.append(f"**Verdict:** {verdict}\n")
    lines.append(f"**Summary:** {review.get('summary', '')}\n")

    findings = review.get("findings", [])
    if not findings:
        lines.append("\nNo issues found.\n")
    else:
        lines.append("\n## Findings\n")
        lines.append("| Severity | File | Line | Issue | Suggestion |")
        lines.append("|---|---|---|---|---|")
        for f in findings:
            row = "| {severity} | {file} | {line} | {issue} | {suggestion} |".format(**f)
            lines.append(row)

    return "\n".join(lines)


def main() -> None:
    diff = load_diff()
    review = review_diff(diff)
    report = format_report(review)
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(report)
    print(f"Done. Review written to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
