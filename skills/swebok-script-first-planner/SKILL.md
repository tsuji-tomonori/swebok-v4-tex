---
name: swebok-script-first-planner
description: Create Japanese presentation scripts and a non-overlapping global slide design before generating SWEBOK Guide V4.0a slide images or image prompts. Use with SWEBOK slide-generation workflows whenever slides should be based on a prior Japanese talk track, when the user wants speaker notes/manuscripts, or when duplicate content across slides/sections must be prevented.
---

# SWEBOK Script First Planner

## Overview

Plan SWEBOK slide sets by writing the Japanese presentation script first, then deriving the slide images from that script. Use this skill before image prompt creation in `swebok-slide-images` and `swebok-chapter-orchestrator`.

Always read [references/script-first-workflow.md](references/script-first-workflow.md) before planning slides.

## Core Rule

Do not create slide prompts directly from source notes. First create:

1. a global design map for the whole requested range;
2. a duplicate-control map assigning each concept to exactly one primary slide;
3. Japanese presentation scripts for each slide;
4. slide prompts distilled from the scripts.

The script explains; the slide visualizes. Avoid putting the full script on the slide.

## Workflow

1. Read the SWEBOK source scope using the caller skill's source workflow.
2. Extract source-grounded concepts, figures, distinctions, dependencies, and section transitions.
3. Build a global design map with slide IDs, one-message statements, source anchors, visual component types, and concept ownership.
4. Check overlap before drafting: every important concept must have one primary slide; later mentions must be marked as recap, bridge, or synthesis.
5. Draft Japanese presentation scripts slide by slide. Keep the script natural for speaking, source-grounded, and free of unsupported examples.
6. Derive each slide's visible text and diagram from the script. Keep visible text short and diagram-centered.
7. Run a final overlap check across titles, one-line messages, bullets, and diagram labels.
8. If the user requested prompt-only output, include the global design map and scripts before the image prompts. Otherwise, use the scripts internally unless the user asked to receive them.

## Script Requirements

- Write in natural Japanese for oral presentation.
- Use 120-220 Japanese characters per normal slide as a default; use less for title/summary slides.
- Include English technical terms only where they help learners map back to SWEBOK.
- Avoid long direct quotations from SWEBOK.
- Do not introduce facts, numbers, benefits, examples, or evaluation claims absent from the source.
- Make the slide's role clear: introduce, define, compare, classify, connect, caution, summarize, or synthesize.

## Slide Derivation Rules

- Convert each script into one slide message, 3-5 short visible items at most, and one main diagram/component.
- Put details in the presentation script, not on the slide.
- If two scripts say the same thing, merge, split responsibilities, or mark one as recap.
- If a concept must recur, change its function: first occurrence explains, later occurrence connects or summarizes.
- Preserve the fixed visual system from `swebok-slide-images/references/slide-spec.md`.

## Output Formats

For internal image generation, use this hidden working order:

```text
Global Design Map
Duplicate-Control Map
Presentation Scripts
Slide Image Prompts
Image Generation
```

For prompt-only or manuscript-request output, return:

```text
全体設計
重複管理
発表用原稿
画像生成プロンプト
```

Keep the final user-facing explanation short after image generation.
