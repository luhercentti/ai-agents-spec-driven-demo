# Feature Spec: Code Reviewer Agent

## Status
done

## Summary
Read a unified diff and produce a structured, prioritized code review with concrete suggestions.

## Problem
Code review quality is uneven. Reviewers miss things under time pressure, and review comments
are often vague ("this could be better"). An agent given a diff and a clear rubric produces
consistent, actionable feedback every time.

## Inputs
- A `sample_diff.txt` file containing a unified diff (the kind produced by `git diff`)

## Outputs
- A Markdown file (`output/review.md`) containing:
  - A summary section (overall assessment, 2–4 sentences)
  - A findings table with columns: severity, file, line, issue, suggestion
  - A verdict: `approve` | `request-changes` | `needs-discussion`

## Behavior
1. Script reads `sample_diff.txt` from the same directory
2. Constructs a system prompt defining the reviewer's role and rubric:
   - Check for: logic errors, unhandled edge cases, naming clarity, missing error handling,
     security issues, unnecessary complexity
3. Passes the diff as the user message
4. Requests a JSON response with keys: `summary`, `findings` (array), `verdict`
5. Each finding: `{ severity, file, line, issue, suggestion }`
6. Formats the JSON response into a readable Markdown report
7. Writes the report to `output/review.md`

## Constraints
- Must not comment on code style or formatting (that's a linter's job)
- Must not suggest architectural rewrites — findings scope is the diff only
- Severity must be one of: `critical` | `major` | `minor` | `info`
- If no issues are found, the findings table must say so explicitly (not be empty/missing)

## Acceptance Criteria
- [ ] `output/review.md` is valid Markdown
- [ ] Every finding has all five fields populated
- [ ] Verdict is one of the three allowed values
- [ ] Summary is present and non-empty
- [ ] No finding references code outside the diff

## Open Questions
- None
