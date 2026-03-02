# PM Brand Identity

Codex skill for generating project logos and icon packs from repository context using Gemini image models.

## What It Does

- Reads code and documentation to extract brand signals.
- Produces a structured brand context and prompt directions.
- Generates logo concepts with Gemini (`gemini-3-pro-image-preview` by default).
- Exports production-ready assets:
  - favicon (`16/32/48` + `.ico`)
  - extension icons (`16/32/48/128`)
  - high-resolution logos (`256/512/1024`)
  - web assets (`apple-touch-icon`, Android icons, OG image, web manifest)

## Repository Structure

- `SKILL.md`: Core skill instructions and trigger description.
- `agents/openai.yaml`: Skill UI metadata.
- `scripts/`: Automation scripts.
- `references/`: Prompt framework, asset specs, and publishing checklist.
- `LICENSE` / `LICENSE.txt`: MIT license text.

## Requirements

- Python 3.10+
- `Pillow` for image packaging:
  - `python -m pip install pillow`
- Gemini API key:
  - `GEMINI_API_KEY` environment variable, or
  - `--api-key` CLI flag, or
  - interactive hidden prompt when not provided.

## Quick Start

1. Extract repo context:

```bash
python scripts/extract_project_brand_context.py \
  --project-root . \
  --output-file brand-output/brand-context.md
```

2. Prepare:
- `brand-brief.md`
- `logo-prompts.txt` (prompt blocks separated by `---`)

3. Generate concepts:

```bash
python scripts/generate_logos_gemini.py \
  --brief-file brand-brief.md \
  --prompt-file logo-prompts.txt \
  --output-dir brand-output/raw
```

4. Package selected concept:

```bash
python scripts/build_logo_assets.py \
  --input brand-output/raw/logo-01.png \
  --name my-product \
  --output-dir brand-output/final
```

## Security Notes

- Never hardcode API keys in files.
- Do not commit `.env` or generated outputs containing secrets.

## License

MIT. See `LICENSE`.
