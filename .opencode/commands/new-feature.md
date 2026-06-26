# Command: /new-feature

Scaffold a new feature spec file from a plain-English description.

## Usage
```
/new-feature <description>
```

## What this command does
1. Reads `SPEC/features/_template.md` to load the canonical spec template
2. Activates the `spec-writer` agent (`.opencode/agents/spec-writer.md`)
3. Passes the user's description to the agent
4. The agent fills every section of the template
5. Suggests a filename based on the feature name (kebab-case, e.g., `my-new-feature.md`)
6. Writes the completed spec to `SPEC/features/<suggested-name>.md`

## Example
```
/new-feature An agent that reads a CSV file and detects anomalies in numeric columns
```

Expected output: a fully populated `SPEC/features/csv-anomaly-detector.md` with status `draft`.

## Notes
- Review the generated spec before writing any code
- Change status from `draft` to `ready` only after the spec has been reviewed
- If the description is ambiguous, the agent will ask a clarifying question before writing
