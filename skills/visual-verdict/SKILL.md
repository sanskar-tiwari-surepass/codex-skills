---
name: visual-verdict
description: Structured visual QA verdict for screenshot-to-reference comparisons
---

# Visual Verdict

Use this skill when you need a strict, reusable visual comparison between a generated screenshot and one or more reference images.

## When To Use

- The task has visual fidelity requirements
- You already have screenshots to compare
- You want a deterministic pass/revise/fail verdict before the next edit

## Inputs

- `reference_images[]`: one or more reference image paths
- `generated_screenshot`: the current output image
- Optional `category_hint`: short label for the intended UI style or page type

## Output Contract

Return **JSON only** with this exact shape:

```json
{
  "score": 0,
  "verdict": "revise",
  "category_match": false,
  "differences": ["..."],
  "suggestions": ["..."],
  "reasoning": "short explanation"
}
```

Rules:
- `score`: integer `0-100`
- `verdict`: `pass`, `revise`, or `fail`
- `category_match`: whether the result matches the intended UI category/style
- `differences[]`: concrete visual mismatches
- `suggestions[]`: specific next edits tied to those mismatches
- `reasoning`: 1-2 sentence summary

## Threshold

- Default visual pass threshold: `90+`
- If the score is below threshold, revise the UI and run this skill again before declaring success

## Debugging Rule

If mismatch diagnosis is hard, you may use pixel-diff tooling as a secondary aid, but this skill's JSON verdict remains the authoritative output.

## Example

```json
{
  "score": 87,
  "verdict": "revise",
  "category_match": true,
  "differences": [
    "Top nav spacing is tighter than reference",
    "Primary button uses smaller font weight"
  ],
  "suggestions": [
    "Increase nav item horizontal padding by 4px",
    "Set primary button font-weight to 600"
  ],
  "reasoning": "Core layout matches, but style details still diverge."
}
```
