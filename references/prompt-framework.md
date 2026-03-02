# Prompt Framework

Use this structure to turn repository findings into reliable logo prompts.

## 1. Brand Brief Template

```markdown
# Brand Brief

## Product
- Name:
- One-line value proposition:
- Primary users:

## Functional Context
- Core features:
- Domain:
- Personality signals from docs/copy:

## Visual Guardrails
- Must communicate:
- Must avoid:
- Color constraints:
- Shape constraints:
- Accessibility constraints:
```

## 2. Prompt Block Template

Write one block per direction in `logo-prompts.txt`. Separate blocks with a line containing `---`.

```text
Direction name: [name]
Style intent: [minimal / bold / abstract / etc]
Primary motifs: [2-4 motifs]
Palette direction: [specific color cues or monochrome]
Composition: [centered icon, simple silhouette, no tiny details]
Favicon constraints: readable at 16x16 and 32x32
Negative constraints: no text, no watermark, no mockup background, no trademark imitation
```

## 3. Quality Prompt Add-Ons

Add one or more:
- "single icon mark on transparent background"
- "geometric simplicity with strong silhouette"
- "high contrast edges, vector-like clarity"
- "avoid photoreal textures"
- "avoid intricate gradients"

## 4. Evaluation Rubric

Score each generated concept 1-5 on:
1. Relevance to product context
2. Distinctiveness
3. Favicon legibility
4. Scalability
5. Brand fit
