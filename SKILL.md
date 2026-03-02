---
name: pm-brand-identity
description: Analyze a project's code and documentation to generate brand direction, then create production-ready logos and favicon/app-icon assets with Gemini image generation (`gemini-3-pro-image-preview` by default, Nano Banana Pro). Use when the user asks to create or refresh a project logo, generate a favicon from code context, derive visual identity from a repository, or produce high-quality icon/logo assets for web and app use.
---

# PM Brand Identity

## Overview

Turn repository context into a coherent visual identity and export-ready brand assets. This skill reads project files, writes a brand brief, generates multiple logo concepts via Gemini, and packages polished favicon/logo outputs.

## Setup

Resolve the installed skill path before running scripts:
- PowerShell: ``$SKILL_DIR = Join-Path ($env:CODEX_HOME ?? "$HOME/.codex") "skills/pm-brand-identity"``
- Bash: ``SKILL_DIR="${CODEX_HOME:-$HOME/.codex}/skills/pm-brand-identity"``

## Core Workflow

### Step 1: Build Context From The Repository

Collect product and brand signals before writing prompts.

Run:
```bash
python "$SKILL_DIR/scripts/extract_project_brand_context.py" \
  --project-root . \
  --output-file brand-output/brand-context.md
```

Then:
- Read `brand-output/brand-context.md` plus key docs (`README.md`, docs, product copy).
- Summarize into a short brand brief (mission, audience, keywords, emotional tone, visual constraints).

Use `references/prompt-framework.md` to structure the brief.

### Step 2: Create 3 Concept Directions

Create 3 distinct but on-brand directions:
1. Clean geometric/minimal
2. Bold expressive/mascot-like
3. Abstract symbolic/monogram

For each direction, define:
- Shape language
- Palette direction
- Typography style cues (without embedding text unless requested)
- Scalability constraints (must read at 16x16)
- Negative constraints (no clutter, no detailed gradients, no trademark mimicry)

### Step 3: Generate Logos With Gemini (Nano Banana Pro)

Require API key as environment variable:
- `GEMINI_API_KEY=<user-provided-key>`
- Optional: `GEMINI_MODEL` (defaults to `gemini-3-pro-image-preview` in the script)
- If no key is passed via env or CLI, the script prompts interactively for a hidden key input.

Run:
```bash
python "$SKILL_DIR/scripts/generate_logos_gemini.py" \
  --brief-file brand-brief.md \
  --prompt-file logo-prompts.txt \
  --output-dir brand-output/raw
```

Use one prompt block per concept in `logo-prompts.txt`, separated by `---`.

### Step 4: Package Favicon And Logo Assets

Convert the selected master logo into deployable assets:
```bash
python "$SKILL_DIR/scripts/build_logo_assets.py" \
  --input brand-output/raw/logo-01.png \
  --name my-product \
  --output-dir brand-output/final
```

This script creates:
- `logos/` high-resolution PNGs
- `favicon/` PNG sizes + `favicon.ico`
- `web/` `apple-touch-icon.png`, Android icons, `site.webmanifest`

See `references/asset-specs.md` for required sizes and quality checks.

### Step 5: Quality Gate Before Delivery

Before finalizing:
- Verify legibility at `16x16`, `32x32`, and `48x48`.
- Verify silhouette remains recognizable on light and dark backgrounds.
- Check for accidental text artifacts from image generation.
- Provide 2-3 final options with rationale tied to repository context.

## Operational Notes

- Never hardcode API keys into scripts, prompts, or output files.
- Keep prompts deterministic and explicit; avoid "make it cool" style vagueness.
- If Gemini generation fails, retry with simplified prompts and stronger constraints.
- If `Pillow` is missing for asset packaging, install: `python -m pip install pillow`.

## Reference Files

- `references/prompt-framework.md` - prompt templates and direction scaffolding
- `references/asset-specs.md` - favicon/logo sizes and quality criteria
- `references/share-ready-checklist.md` - checks before publishing this skill to GitHub
