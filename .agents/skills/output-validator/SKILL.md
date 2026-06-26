# Skill: output-validator

## Description
Compares committed output artifacts against their source spec to verify that
acceptance criteria are met. This skill is the reusable capability underlying
the `/spec-check` command.

## When to use
Load this skill when:
- A demo has been implemented and you want to verify it matches its spec
- A spec's status is being changed from `in-progress` to `done`
- You want to audit existing demos for spec compliance

## Inputs
- A `SPEC.md` file for the demo being validated
- The implementation script(s) in the same folder
- The committed artifacts in `output/`

## Outputs
A validation report with:
- One row per acceptance criterion
- Status: `pass` | `fail` | `unverifiable`
- For `fail`: a brief explanation of what is missing or wrong
- A summary line: `N/M criteria passing`

## Instructions

### Step 1 — Parse the spec
Read the `SPEC.md` and extract:
- The **Inputs** section (what data the script expects)
- The **Outputs** section (what files/formats should be produced)
- The **Acceptance Criteria** checkboxes

### Step 2 — Check each criterion
For each criterion:

1. **Structural checks** (can be done by reading files):
   - Does the output file exist?
   - Is the format correct (valid Markdown, valid Python, valid JSON)?
   - Are required sections/fields present?

2. **Content checks** (requires reading the implementation):
   - Does the script read the inputs described in the spec?
   - Does the script write to the output path described in the spec?
   - Are constraints enforced in the code (e.g., error handling for missing files)?

3. **Unverifiable criteria** (mark as such, do not guess):
   - Criteria that require executing the script
   - Criteria that require human judgment ("output is accurate")

### Step 3 — Return the report
Format as a Markdown table:

```markdown
| Criterion | Status | Notes |
|---|---|---|
| output/main.py is valid Python | pass | |
| All endpoints described in spec exist | fail | /delete endpoint missing |
| Output is accurate | unverifiable | Requires execution |
```

Followed by: `Result: N/M criteria verified as passing (X unverifiable)`

## Constraints
- Do not execute any code — validation is static only
- Do not modify specs or implementation files
- Do not mark a criterion as `pass` based on assumption — if uncertain, mark `unverifiable`
