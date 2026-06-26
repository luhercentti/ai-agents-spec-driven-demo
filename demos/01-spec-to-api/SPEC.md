# Demo: Spec to API

## What this demo does
Reads a plain-language API specification (`SPEC.md`, this file) and generates a complete,
runnable FastAPI application using the OpenAI API.

The generated application is committed to `output/main.py`. You do not need to run anything
to see the result.

## The spec (input to the generator)

Build a task management REST API with the following resources and behavior:

**Resource: Task**
- Fields: `id` (int), `title` (str), `description` (str, optional), `status` (enum: todo/in_progress/done), `created_at` (datetime)

**Endpoints:**
- `GET /tasks` — return a list of all tasks
- `POST /tasks` — create a new task; `title` is required; `status` defaults to `todo`
- `GET /tasks/{task_id}` — return a single task by ID; 404 if not found
- `PATCH /tasks/{task_id}` — update `title`, `description`, or `status`; 404 if not found
- `DELETE /tasks/{task_id}` — delete a task; return 204 on success; 404 if not found

**Behavior:**
- Use an in-memory list as the data store (no database)
- IDs are auto-incremented integers starting at 1
- Return `422` for validation errors (FastAPI default behavior is acceptable)

## How to run
```sh
pip install openai
export OPENAI_API_KEY=sk-...
python generate.py
# output/main.py will be written
```

The output is already committed — running is optional.
