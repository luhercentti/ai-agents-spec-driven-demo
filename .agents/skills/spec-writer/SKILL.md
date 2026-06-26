# Skill: spec-writer

## Description
Turns plain-English requirements into structured feature specs following the project template.
This skill is the reusable capability underlying the `/new-feature` command.

## When to use
Load this skill when:
- A user describes a feature in natural language and wants a spec written
- A spec needs to be rewritten for clarity or completeness
- You need to check whether an existing spec is complete and properly structured

## Inputs
- A plain-English description of a feature (required)
- The canonical template from `SPEC/features/_template.md` (loaded automatically)
- Existing specs from `SPEC/features/` for style reference (optional)

## Outputs
- A fully populated Markdown spec following the template structure
- All sections filled: Status, Summary, Problem, Inputs, Outputs, Behavior, Constraints, Acceptance Criteria
- Status set to `draft` unless told otherwise

## Instructions

### Step 1 — Understand the requirement
Read the input carefully. If any of the following are unclear, ask before writing:
- What does this feature take as input?
- What does it produce as output?
- What should NOT happen (constraints)?

### Step 2 — Fill the template
Follow these rules:
- **Summary**: exactly one sentence, present tense ("Reads X and produces Y")
- **Problem**: explain *why* this exists, not *what* it does
- **Behavior**: numbered steps in plain language — no code, no pseudocode
- **Acceptance Criteria**: verifiable checkbox statements a reviewer could check off
- **Constraints**: things that must NOT happen, plus edge cases and failure modes

### Step 3 — Review for completeness
Before returning the spec, verify:
- [ ] No section is empty or contains only "N/A"
- [ ] Behavior steps are numbered and sequential
- [ ] Every acceptance criterion is verifiable (not vague like "works correctly")
- [ ] Constraints are specific (not vague like "should be fast")

## Example usage

**Input:**
> An agent that reads a CSV file and detects anomalies in numeric columns using z-score.

**Expected output:** A fully populated spec at `SPEC/features/csv-anomaly-detector.md`
with concrete inputs (CSV file path), outputs (JSON report), behavior steps (read → parse →
compute z-scores → flag → write), constraints (handle missing values, non-numeric columns),
and verifiable acceptance criteria.
