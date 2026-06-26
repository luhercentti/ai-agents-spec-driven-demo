# Command: /review

Run the code-reviewer agent on the current working diff.

## Usage
```
/review [file-or-folder]
```

If no argument is given, reviews the full `git diff HEAD` output.
If a path is given, reviews only changes to that file or folder.

## What this command does
1. Runs `git diff HEAD [path]` to get the current diff
2. Activates the `code-reviewer` agent (`.opencode/agents/code-reviewer.md`)
3. Passes the diff to the agent
4. The agent returns a JSON review object
5. Formats the result as a readable Markdown report in the chat

## Example
```
/review demos/02-code-reviewer-agent/agent.py
```

Expected output (in chat):

```
## Code Review

**Verdict:** approve

**Summary:** The script correctly reads the diff, constructs a well-scoped prompt,
and handles the API response. No critical issues found.

| Severity | File | Line | Issue | Suggestion |
|---|---|---|---|---|
| minor | agent.py | 34 | ... | ... |
```

## Notes
- This command does not write any files — output appears in the chat only
- To save a review to a file, copy the output to `output/review.md` manually
- The reviewer does not check style or formatting — run a linter separately
