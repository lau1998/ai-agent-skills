---
name: create-skill
description: Create, classify, register, validate, or update AI Agent Skills managed in this repository. Use when the user asks to add, create, scaffold, organize, categorize, verify, or modify a project Skill.
---

# Create And Register Skills

Create repository Skills through the installed `skill-creator` workflow, place them in one of the two approved categories, and keep `catalog.yaml` consistent.

## Workflow

1. Locate the repository root with `git rev-parse --show-toplevel`.
2. Read the root `AGENTS.md`, `catalog.yaml`, and any existing Skill with a similar purpose.
3. Understand the requested behavior through concrete usage examples. Do not ask redundant questions when the request already defines the triggers and outputs.
4. Choose `development` or `other` using the classification rules below. Tell the user the selected category and the reason. Ask for confirmation only when the primary deliverable is genuinely ambiguous.
5. Generate a short, verb-led name using lowercase letters, digits, and hyphens. Keep it under 64 characters.
6. Check both `catalog.yaml` and the target directory before creating files. Never overwrite an existing Skill.
7. Invoke the installed `skill-creator` Skill and use its `scripts/init_skill.py` generator. Set the output path to `skills/<category>` and request only the resource directories the Skill actually needs.
8. Replace every generated placeholder. Keep `SKILL.md` concise, put detailed material in one-level `references/` files, and do not add auxiliary documentation inside the Skill.
9. Add document comments to every function or method. Add short comments around important logic that is not self-explanatory.
10. Run every bundled script on a representative case. Then run the installed `skill-creator/scripts/quick_validate.py` against the completed Skill directory.
11. Register a new Skill only after all checks pass. Run `scripts/register_skill.py` as shown below from the repository root.
12. Report the created path, selected category, validation commands, and results.

## Classification

Classify by the primary deliverable rather than the subject name.

Use `development` when the main result is any of the following:

- Source code, scripts, tests, APIs, database schemas, or migrations.
- Build, dependency, continuous integration, deployment, or infrastructure configuration.
- Code debugging, review, refactoring, performance work, or software engineering procedures.

Use `other` when the main result is not code, including writing, translation, learning, research, office work, design guidance, travel, health, or daily-life workflows.

For mixed requests, use `development` when implementing software is the core goal. Use `other` when code is only an internal helper used to produce a non-code result.

## Register A New Skill

Run from the repository root after validation succeeds:

```bash
.venv/bin/python skills/development/create-skill/scripts/register_skill.py \
  --catalog catalog.yaml \
  --root . \
  --name <skill-name> \
  --category <development-or-other> \
  --path skills/<development-or-other>/<skill-name> \
  --description '<concise-description>'
```

The script rejects malformed records, unsupported categories, nonstandard paths, missing directories, duplicate names, and duplicate paths. Do not edit around these failures; fix the Skill or resolve the conflict first.

## Update An Existing Skill

Preserve the existing name, category, and path unless the user explicitly requests a rename or category change. Read the current Skill and its catalog record before editing. Regenerate `agents/openai.yaml` when its UI metadata no longer matches `SKILL.md`, rerun bundled script tests, and run `quick_validate.py` after the change.

When a rename or category change is requested, treat it as a migration: verify that the destination is unused, move the complete Skill directory, update the existing catalog record without creating a second record, and validate repository integrity before reporting completion.

## Failure Rules

- Stop before writing when the target directory or catalog name already exists and the request is not clearly an update.
- Do not register a Skill whose validator or bundled tests fail.
- Do not add a third category. Place non-development work in `other`.
- Do not silently choose a category when both possible primary deliverables remain equally plausible after reading the request.
