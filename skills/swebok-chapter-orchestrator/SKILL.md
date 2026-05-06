---
name: swebok-chapter-orchestrator
description: Orchestrate SWEBOK Guide V4.0a chapter-level Japanese slide image generation by creating chapter overview slides, invoking/reusing the swebok-slide-images section workflow for each section, and adding chapter summary/synthesis slides. Use when the user specifies a whole SWEBOK chapter, Knowledge Area, or broad chapter-like range and wants study/reference slide images or prompt-only output.
---

# SWEBOK Chapter Orchestrator

## Overview

Create a coherent Japanese study/reference slide set for a whole SWEBOK Guide V4.0a chapter or Knowledge Area. Build chapter-level overview and synthesis slides, then reuse the sibling `swebok-slide-images` skill for each major section so section-level slides stay consistent with the existing fixed design system.

Always read:

1. [references/chapter-orchestration.md](references/chapter-orchestration.md)
2. `../swebok-script-first-planner/SKILL.md`
3. `../swebok-script-first-planner/references/script-first-workflow.md`
4. `../swebok-slide-images/SKILL.md`
5. `../swebok-slide-images/references/slide-spec.md`

## Trigger Interpretation

Treat inputs such as `Ch.01 Software Requirements`, `Software Requirements`, `Chapter 1`, `要求`, or a Knowledge Area name as chapter-level requests. If the user specifies a subsection such as `1.2 Categories of Software Requirements`, use `swebok-slide-images` directly instead of this orchestrator.

Ask a brief clarification only when the chapter cannot be identified, multiple chapters match equally, or the user asks for an output form that conflicts with image generation.

## Orchestration Workflow

1. Locate `swebok-v4.pdf` in the project, then identify the target chapter / Knowledge Area.
2. Read the chapter title, introduction, topic list, Matrix of Topics vs. Reference Material, figures/tables that frame the chapter, Further Readings, and References.
3. Create a chapter-wide global design map before drafting any slide prompt.
4. Create a duplicate-control map across chapter opening slides, section groups, bridge slides, and chapter closing slides.
5. Create chapter opening slides that explain scope, position in SWEBOK, topic map, and how to read the chapter.
6. Divide the chapter into major sections. For each section, apply the `swebok-slide-images` workflow as if the user had requested that section by name.
7. Write Japanese presentation scripts for all slides before creating image prompts.
8. Insert short bridge slides only when they reduce confusion between major sections; do not add decorative interludes.
9. Create chapter closing slides that synthesize the chapter, compare major concepts, show cross-section relationships, and summarize the learning takeaways.
10. Generate 16:9 slide images unless the user explicitly asks for prompt-only output.

## Output Rules

- Keep chapter-level slides and section-level slides visually identical by using the `swebok-slide-images` design specification.
- Keep every slide source-grounded. Do not invent chapter themes, examples, outcomes, maturity claims, or practical recommendations not supported by SWEBOK.
- Create Japanese presentation scripts before image prompts. Visible slide text must be shorter than the script and must not duplicate the same explanation across slide groups.
- Use a hierarchical slide numbering scheme for large outputs, e.g. `01-03` for chapter-opening slide 3, `1.2-04` for section 1.2 slide 4, and `99-02` for chapter-closing slide 2.
- If the chapter is too large for one image-generation batch, split into Part 1 / Part 2 / Part 3 by major sections while preserving one chapter-level outline.
- If the user says "プロンプトだけ", "画像は不要", or equivalent, output the design map, duplicate-control map, scripts, and complete image prompts grouped by chapter opening, section groups, and chapter closing.

## Default Structure

Use this structure unless the source suggests a more natural grouping:

1. Chapter title slide
2. Chapter scope and SWEBOK position
3. Chapter topic map
4. Reading route / dependency map
5. Section group: section-level slides via `swebok-slide-images`
6. Optional bridge slide between large conceptual groups
7. Repeat section groups
8. Chapter synthesis relation map
9. Chapter summary cards
10. Next study path / related Knowledge Areas

## Size Guidance

- Short chapter or narrow Knowledge Area: 20-35 slides.
- Normal Knowledge Area chapter: 35-60 slides.
- Dense chapter: split into parts of about 20-30 slides each.
- Do not pad. If the source does not support a slide, omit it.

## Completion Note

After generation, keep the final explanation minimal: target chapter, number of parts if split, section groups included, and whether images or prompts were produced.
