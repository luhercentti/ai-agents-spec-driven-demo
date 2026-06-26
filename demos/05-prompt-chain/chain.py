"""
Demo 05 — Prompt Chain
Four-step chain: plan → draft → critique → refine.
Output is written to output/result.md.
"""

import json
from pathlib import Path

from openai import OpenAI

OUTPUT_PATH = Path(__file__).parent / "output" / "result.md"

TASK = (
    "Write a technical explanation of how vector embeddings work "
    "for a software engineer who has not worked with ML before."
)


def chat(client: OpenAI, system: str, user: str, json_mode: bool = False) -> str:
    kwargs = {}
    if json_mode:
        kwargs["response_format"] = {"type": "json_object"}
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        **kwargs,
    )
    return response.choices[0].message.content.strip()


def step1_plan(client: OpenAI) -> str:
    print("Step 1/4 — Planning outline...")
    system = (
        "You are a technical writer planning a structured explanation. "
        "Produce a concise bullet-point outline covering all key concepts needed. "
        "Focus on the concepts a software engineer without ML experience needs to understand. "
        "Do not write prose — only the outline."
    )
    return chat(client, system, f"Task: {TASK}")


def step2_draft(client: OpenAI, outline: str) -> str:
    print("Step 2/4 — Writing draft...")
    system = (
        "You are a technical writer. Write a full, clear prose explanation based on the outline. "
        "Use analogies where helpful. Avoid jargon without definition. "
        "Target audience: software engineers with no ML background."
    )
    user = f"Task: {TASK}\n\nOutline:\n{outline}"
    return chat(client, system, user)


def step3_critique(client: OpenAI, draft: str) -> dict:
    print("Step 3/4 — Critiquing draft...")
    system = (
        "You are a senior technical editor. Review the draft and identify weaknesses. "
        "Return a JSON object with three keys: "
        '"clarity" (string: what is unclear or confusing), '
        '"accuracy" (string: any technical inaccuracies or oversimplifications), '
        '"gaps" (array of strings: important concepts that are missing or underdeveloped). '
        "Be specific and constructive. Return only the JSON object."
    )
    raw = chat(client, system, f"Draft:\n{draft}", json_mode=True)
    return json.loads(raw)


def step4_refine(client: OpenAI, draft: str, critique: dict) -> str:
    print("Step 4/4 — Refining...")
    system = (
        "You are a technical writer revising a draft based on editorial feedback. "
        "Address every point in the critique. The final version should be noticeably "
        "better than the draft — clearer, more accurate, and more complete. "
        "Return only the revised explanation."
    )
    critique_text = (
        f"Clarity issues: {critique.get('clarity', 'none')}\n"
        f"Accuracy issues: {critique.get('accuracy', 'none')}\n"
        f"Gaps: {', '.join(critique.get('gaps', []))}"
    )
    user = f"Original draft:\n{draft}\n\nEditorial critique:\n{critique_text}"
    return chat(client, system, user)


def main() -> None:
    client = OpenAI()

    outline = step1_plan(client)
    draft = step2_draft(client, outline)
    critique = step3_critique(client, draft)
    refined = step4_refine(client, draft, critique)

    gaps_text = "\n".join(f"- {g}" for g in critique.get("gaps", []))
    critique_md = (
        f"**Clarity:** {critique.get('clarity', '')}\n\n"
        f"**Accuracy:** {critique.get('accuracy', '')}\n\n"
        f"**Gaps:**\n{gaps_text}"
    )

    output = "\n\n---\n\n".join([
        f"# Prompt Chain Output\n\n**Task:** {TASK}",
        f"## Step 1 — Outline\n\n{outline}",
        f"## Step 2 — Draft\n\n{draft}",
        f"## Step 3 — Critique\n\n{critique_md}",
        f"## Step 4 — Refined\n\n{refined}",
    ])

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(output)
    print(f"Done. Full chain written to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
