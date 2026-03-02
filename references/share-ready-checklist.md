# Share-Ready Checklist

Use this checklist before publishing the skill to GitHub.

## 1. Validate Structure

Run:

```bash
python ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py pm-brand-identity
```

Expected result: `Skill is valid!`

## 2. Confirm No Secrets

Scan for common key patterns:

```bash
rg -n "AIza|GEMINI_API_KEY|api[_-]?key|token|secret" pm-brand-identity
```

Expected result: no real credentials in files.

## 3. Keep API Key Usage Runtime-Only

- Pass credentials through environment variables (`GEMINI_API_KEY`).
- Do not commit `.env` files with real values.
- Do not store key values in prompt files, JSON metadata, or examples.

## 4. Verify Script Health

Run smoke checks:

```bash
python pm-brand-identity/scripts/extract_project_brand_context.py --help
python pm-brand-identity/scripts/generate_logos_gemini.py --help
python pm-brand-identity/scripts/build_logo_assets.py --help
```

## 5. Include Required Skill Files

- `SKILL.md`
- `agents/openai.yaml`
- `LICENSE.txt`
- required `scripts/` and `references/` files
