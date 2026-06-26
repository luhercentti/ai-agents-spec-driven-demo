# Constitution

These are the governing principles of this project. They take precedence over
convenience, speed, or personal preference. When a decision is unclear, return here.

---

## 1. Spec before code

No implementation begins without a written specification. The spec defines intent.
Code is an expression of that intent, not the source of truth.

If the spec is wrong, fix the spec first, then fix the code.

## 2. Agents have roles, not opinions

Every AI agent in this project is given a specific role with explicit constraints.
Agents are not asked to "help" or "improve things" in the abstract — they are given
a bounded task with defined inputs, outputs, and failure conditions.

## 3. Outputs are artifacts

The result of running any agent or script is a committed artifact. Outputs are not
ephemeral. They are versioned, reviewable, and treated the same as source code.

## 4. Clarity over cleverness

Scripts should be readable by someone unfamiliar with the codebase in under five
minutes. Abstractions are introduced only when they reduce real complexity, not
to demonstrate sophistication.

## 5. No hidden state

No agent reads from or writes to external state (databases, external APIs beyond
the LLM itself, file system paths outside the project) without that dependency
being declared in its definition.

## 6. Failures are documented

If a script fails, the failure is instructive. Error handling is explicit. Scripts
do not silently succeed with bad output.

## 7. Humans remain in the loop

AI agents in this project automate repetitive, well-defined tasks. They do not make
architectural decisions, merge code, or modify specs. Those actions require a human.
