---
name: fde-workbench-flow
description: Develop or hand off a project using this FDE workbench or its generated starter, preserving goal constraints, executable evidence, and the user's ability to explain the result. Use for this kit's domain adaptation and reuse workflow, not unrelated application work.
---

# FDE workbench flow

Locate the user-selected project root containing kit.py and domain_packs. Do not assume this skill's folder is the project root. Read the root HANDOFF.md and README.md; use current code and execution results over historical completion claims.

## Define and adapt

- Preserve the user's actual objective. Record the target user action, input data, constraints, exclusions, and observable completion evidence in BRIEF.md and INTENT.md when starting or materially changing a project. If absent, the kit's templates provide these forms.
- Choose a relevant recipe and existing library from catalog/recipes.json and catalog/repos.json. Recheck source and license conditions before adopting a different version. Do not install all catalog entries.
- For overall improvements, create a source checkpoint before edits. If runtime-data/workbench.sqlite3 exists, back it up separately. The root checkpoint excludes work/; a generated project's changes require its own checkpoint.
- Keep domain policies in domain_packs and reusable execution rules in runtime. A new domain also needs representative inputs and expected outcomes; changing labels alone is not domain validation.

## Verify the right boundary

- The default UI has local-operator privileges. It is not production authentication. Do not expose the loopback demo as a hosted multi-user service without implementing and testing that boundary.
- Preserve the approval invariant: edits invalidate approval, execution checks the current version and approved proposal hash, and local results are committed atomically with completion. A remote connector needs its own idempotency and reconciliation design; the local transaction does not prove exactly-once remote execution.
- Distinguish rules, SDK TestModel, a real model, and local sandbox actions. Structural validation and valid policy IDs do not prove factual correctness. Provider failure usage may be unknown.
- Run checks relevant to changed behavior. scripts/verify.py records tests, capability examples, a category-only synthetic baseline, and source hashes. Do not count TODOs, copied evidence, or discovered tests as successful execution.
- For UI or runtime claims, also check the actual browser/API/process. Inspect an existing process before starting another. A timeout alone is not proof of termination.

## Explain and hand off

Use docs/HOW_IT_WORKS.md for the existing structure and docs/RUNBOOK.md for setup, model mode, and recovery. Read docs/AI_NATIVE.md when preparing for the user's technical/intent/cognition/communication criteria; do not invent official scores.

Record what changed, why, observed results, limits, and the next concrete step in HANDOFF.md. Include commands and evidence paths, not credentials. Distinguish source-kit evidence from current-copy evidence.

Help the user predict and explain behavior using UNDERSTANDING.md or its template. Do not fabricate human understanding, historical decisions, delegation, or successful model calls. The final explanation should let the user start the result, locate changed parts, and describe a real failure case.
