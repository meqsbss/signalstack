# Process

## Roles
- **PM** — grooms a task before anyone implements it. Follows `_docs/team/pm.md`.
- **Engineer** — implements one groomed task. Follows `_docs/team/software-engineer.md`.
- **QA** — checks the result against the acceptance criteria. Follows `_docs/team/qa-engineer.md`.

## Orchestrator
The main session is the orchestrator. It launches PM, Engineer, and QA as subagents.
It does not groom, implement, or test itself.

## Lifecycle
1. Pick the next open issue labeled `mvp` from the backlog.
2. PM grooms it (rewrites using `_docs/task-template.md`).
3. Engineer implements it.
4. QA verifies it.
5. On FAIL → back to step 3 with the QA comment as input.
6. On PASS → the orchestrator closes the issue.
7. Repeat until no open `mvp` issues remain.

## Rules
- Do not skip step 2 (grooming).
- The Engineer does not close the issue.
- QA does not fix code, only outputs PASS or FAIL.
- The orchestrator closes an issue only after QA outputs PASS.
- Bugs found during manual testing get a `user-test-bug` label and go
  through the same lifecycle (PM → Engineer → QA).

## Task tracker
GitHub Issues are the canonical backlog. `_docs/tasks.md` does not exist
and must not be created.