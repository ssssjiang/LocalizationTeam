---
name: task-workflow
description: >
  Structured workflow for any actionable task. Use when the agent receives a
  request to DO something — implement, fix, create, modify, send, run, or
  configure. Covers: Clarify (if ambiguous) → Plan → Execute → Verify.
  Skip Clarify if the requirement is already unambiguous in a single sentence.
---

# Task Workflow

Structured workflow for actionable tasks. Follow in order; do not skip phases.

## Phase 1: Clarify (skip if requirement is already clear)

**When to skip:** The user's request is a single, unambiguous sentence (e.g. "fix the typo in line 42 of foo.ts").

**When to run:** The request is vague, multi-interpretable, or missing key constraints.

**Rules:**
- Ask at most 2 questions per turn; prefer multiple-choice when possible
- Focus on: purpose, constraints, success criteria
- Once clear, proceed to Plan

## Phase 2: Plan

**Output format:**
- Numbered steps with exact file paths and commands
- Expected output for each step
- Final verification command(s) that prove success

**Gate:** Present the plan and wait for user approval before executing. Revise if requested.

## Phase 3: Execute

**Rules:**
- Execute steps in order; show actual output for each
- If output deviates from plan, pause and explain before continuing
- Do not claim completion until Verify has run

## Phase 4: Verify

**Rules:**
- Run the verification command(s) from the plan
- Paste actual output; state Pass or Fail with evidence
- Final status: **Verified** (command passed) / **Not verified** (command failed or not run) / **Blocked** (environment cannot run verification)

**Evidence requirement:** Do not claim "done" without running the verification command and showing its output.
