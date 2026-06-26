# Feature Spec: Changelog Agent

## Status
done

## Summary
Read a raw git log and produce a clean, grouped, human-readable CHANGELOG in Keep a Changelog format.

## Problem
Raw git logs are noisy and inconsistent. Turning them into a CHANGELOG requires reading every
commit, inferring intent, grouping related changes, and writing in a tone suitable for end users.
This is tedious for humans and well-suited for an LLM.

## Inputs
- A `git_log.txt` file containing the output of `git log --oneline` or `git log --pretty=format:"%h %s"`

## Outputs
- A Markdown file (`output/CHANGELOG.md`) following the Keep a Changelog format:
  - Grouped by: `Added`, `Changed`, `Fixed`, `Removed`
  - Each entry is a plain-language sentence, not a raw commit message
  - A version header (inferred or placeholder `[Unreleased]`)

## Behavior
1. Script reads `git_log.txt` from the same directory
2. Constructs a system prompt: act as a technical writer, group and rewrite commits for end users
3. Passes the raw log as the user message
4. Requests a JSON response with keys: `version`, `added`, `changed`, `fixed`, `removed`
   — each value is an array of strings
5. Formats the JSON into Keep a Changelog Markdown
6. Writes to `output/CHANGELOG.md`

## Constraints
- Must not include commit hashes in the output
- Must not invent changes not implied by the commit messages
- Empty sections (e.g., no `Removed` entries) must be omitted from the output
- Commit messages that are clearly noise (e.g., "fix typo", "wip") may be omitted or merged

## Acceptance Criteria
- [ ] Output follows Keep a Changelog structure
- [ ] No commit hashes appear in the output
- [ ] All meaningful commits are represented in at least one section
- [ ] Empty sections are not rendered

## Open Questions
- None
