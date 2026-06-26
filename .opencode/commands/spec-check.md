# Command: /spec-check

Validate that an implementation matches its spec.

## Usage
```
/spec-check <demo-folder>
```

Example: `/spec-check demos/01-spec-to-api`

## What this command does
1. Reads `<demo-folder>/SPEC.md`
2. Reads the main Python script in `<demo-folder>/`
3. Reads the committed artifact(s) in `<demo-folder>/output/`
4. Activates the `output-validator` skill (`.agents/skills/output-validator/SKILL.md`)
5. Compares the spec's Acceptance Criteria against the actual implementation and output
6. Returns a checklist: each criterion marked as `pass`, `fail`, or `unverifiable`

## Example output (in chat)

```
## Spec Check: demos/01-spec-to-api

| Criterion | Status |
|---|---|
| output/main.py is valid Python | pass |
| All resources have a Pydantic model | pass |
| All endpoints described in spec exist | pass |
| File includes uvicorn.run entrypoint | pass |
| No undocumented endpoints | pass |

Result: 5/5 criteria passing
```

## Notes
- `unverifiable` means the criterion requires running the code or human judgment
- This command is read-only — it does not modify specs or implementation files
- Run this before marking a feature spec status as `done`
