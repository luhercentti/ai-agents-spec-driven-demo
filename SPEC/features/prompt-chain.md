# Feature Spec: Prompt Chain Demo

## Status
done

## Summary
Implement a four-step prompt chain — plan, draft, critique, refine — that produces a
higher-quality output than a single-shot prompt, with each step's output visible.

## Problem
Single-shot prompting often produces shallow results for complex writing tasks.
Chaining prompts — where each step takes the previous step's output as input — produces
measurably better results and makes the reasoning process transparent.

## Inputs
- A task description hardcoded in the script:
  "Write a technical explanation of how vector embeddings work for a software engineer
   who has not worked with ML before."

## Outputs
- A Markdown file (`output/result.md`) showing all four chain steps:
  - Step 1: Outline (bullet list of key points to cover)
  - Step 2: Draft (full prose based on the outline)
  - Step 3: Critique (structured feedback on the draft: clarity, accuracy, gaps)
  - Step 4: Refined draft (final version incorporating the critique)

## Behavior
1. Script defines the task as a constant string
2. Step 1 — Plan: ask the model to produce a structured outline for the task
3. Step 2 — Draft: pass the outline + task, ask for a full draft
4. Step 3 — Critique: pass the draft, ask for a structured critique
   (JSON: `{ "clarity": "...", "accuracy": "...", "gaps": [...] }`)
5. Step 4 — Refine: pass the draft + critique, ask for a revised final version
6. Write all four outputs to `output/result.md` with clear section headers
7. Print each step's completion to stdout as it finishes

## Constraints
- Each step must use the previous step's output — no step ignores the chain
- The critique must be structured (JSON), not free-form, so it can be parsed
- The final output must be materially different from the Step 2 draft
- The script must print progress to stdout so the user can see it working

## Acceptance Criteria
- [ ] `output/result.md` contains all four sections
- [ ] Step 3 is valid JSON (parseable)
- [ ] Step 4 incorporates at least one point from the Step 3 critique
- [ ] The script prints step progress to stdout during execution

## Open Questions
- None
