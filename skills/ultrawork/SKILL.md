---
name: ultrawork
description: Parallel execution workflow for independent subtasks
---

# Ultrawork

Use this skill when a task can be split into multiple independent lanes that should run in parallel.

## Purpose

Improve throughput by running independent work concurrently while keeping dependencies explicit and verification disciplined.

## When To Use

- Several subtasks can proceed independently
- One lane can research while another implements
- Verification can run in parallel with non-overlapping execution work
- The task is large enough that serial execution would waste time

## When Not To Use

- The work is mostly sequential
- Every next step depends on the previous result
- Splitting the task would create coordination overhead larger than the benefit

## Workflow

1. Break the task into independent and dependent parts.
2. Keep the immediate critical path local when needed.
3. Delegate bounded parallel-safe subtasks.
4. Avoid overlapping ownership when multiple lanes may edit code.
5. Integrate results.
6. Verify the combined outcome before declaring completion.

## Good Parallel Lanes

- search or mapping work
- documentation lookup
- one implementation lane plus one verification lane
- disjoint code changes in separate files or modules

## Bad Parallel Lanes

- two agents editing the same small file without clear ownership
- delegating work whose result is needed immediately for the very next step
- splitting trivial work that is faster to do directly

## Rules

- Parallelize only when it materially improves speed or quality.
- Keep each delegated task concrete and bounded.
- Make ownership explicit for code changes.
- Integrate and verify centrally after parallel work returns.

## Output

Report:
- which lanes ran in parallel
- what each lane produced
- how the results were integrated
- what verification was performed
