# Feature Spec: Spec to API Generator

## Status
done

## Summary
Read a plain-language feature spec and generate a working FastAPI application that implements it.

## Problem
Writing boilerplate API code from a spec is repetitive and mechanical. Given a well-structured
spec, an LLM can produce a correct first draft faster than a human — and the result is directly
traceable back to the spec that drove it.

## Inputs
- A `SPEC.md` file describing an API's resources, endpoints, and behavior in plain language

## Outputs
- A single Python file (`output/main.py`) containing a complete FastAPI application:
  - Pydantic models for all resources
  - Route handlers for all described endpoints
  - Inline docstrings derived from the spec
  - A runnable `uvicorn` entrypoint

## Behavior
1. Script reads `SPEC.md` from the same directory
2. Constructs a system prompt defining the LLM's role as a FastAPI code generator
3. Passes the full spec content as the user message
4. Requests structured output: a JSON object with a single key `code` containing the Python source
5. Parses the response and writes the value of `code` to `output/main.py`
6. Prints a confirmation with line count and output path

## Constraints
- Output must be a single self-contained Python file — no multi-file output
- Must not hallucinate endpoints not described in the spec
- Must not add authentication or middleware not mentioned in the spec
- Script must fail loudly if `SPEC.md` is missing or empty

## Acceptance Criteria
- [ ] `output/main.py` is valid Python (parseable by `ast.parse`)
- [ ] All resources described in the spec have a corresponding Pydantic model
- [ ] All endpoints described in the spec have a corresponding route handler
- [ ] The file includes a `uvicorn.run` entrypoint
- [ ] No endpoint exists in the output that is not described in the spec

## Open Questions
- None
