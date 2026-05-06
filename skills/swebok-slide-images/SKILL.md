---
name: swebok-slide-images
description: Convert SWEBOK Guide V4.0a chapters, sections, or topic names into Japanese study/reference slide images. Use when the user names a SWEBOK chapter/section/item such as "1.2 Categories of Software Requirements", asks for Japanese SWEBOK learning slides, asks for 16:9 slide images, or asks for only the completed slide-generation prompt without images.
---

# SWEBOK Slide Images

## Overview

Create quiet, diagram-centered Japanese study/reference slide images from SWEBOK Guide V4.0a. Treat the SWEBOK PDF as the primary source, infer the requested scope from a chapter/section/item name, design the slide sequence internally, and generate 16:9 slide images unless the user explicitly says "プロンプトだけ", "画像は不要", or equivalent.

Always read:

1. [references/slide-spec.md](references/slide-spec.md)
2. `../swebok-script-first-planner/SKILL.md`
3. `../swebok-script-first-planner/references/script-first-workflow.md`

Use the script-first planner before image prompt creation so Japanese presentation scripts and a duplicate-free global design exist before slides are generated.

## Source Workflow

1. Locate the SWEBOK Guide V4.0a PDF. Prefer `swebok-v4.pdf` in the current project, then uploaded files or user-provided paths.
2. Identify the target Knowledge Area / chapter, section number, English title, Japanese title if available, parent topic, and nearby related sections.
3. Read the target heading, body text, figures/tables, parent heading, surrounding relevant sections, Matrix of Topics vs. Reference Material, Further Readings, and References as needed.
4. If the target section is short but later subsections expand the same concept, use those later subsections as supporting scope while keeping the requested section as the main subject.
5. Ask a brief clarification only when multiple plausible targets remain, the title cannot be found, the PDF is unavailable, or the requested output format is unclear.

## Content Rules

- Base all claims on SWEBOK Guide V4.0a.
- Do not invent examples, numbers, effects, review results, or practices that are not supported by the source.
- Avoid long quotations. Prefer concise Japanese paraphrase, reconstruction, and diagramming.
- Preserve SWEBOK technical terms accurately; include English terms only where they help identification or later reference.
- Mark any added explanation as "学習上の補足" and keep it aligned with the text.
- Keep each slide to one message, with at most 3-5 short body items.

## Script-First Slide Planning

Build the full sequence internally before image generation, then apply the script-first workflow:

1. Title: English/Japanese title, section number, and what to understand.
2. Positioning: why the topic matters in its parent topic.
3. Core concept: definition, classification, claim, or purpose.
4. Structure diagram: hierarchy, category map, relation map, or flow.
5. Element explanation: cards for categories, activities, techniques, or concepts.
6. Comparison/relation: upper/lower concepts, similar concepts, or other KA links.
7. Practical reading: cautions, likely misunderstandings, or application viewpoints.
8. Next-section connection: what the following topic develops.
9. Summary: 3-5 memorable points.
10. Overall role: what the topic contributes inside the KA or SWEBOK.

Choose slide count from source density: small section 6-8, normal subsection 8-10, multi-concept section 10-12, chapter introduction 10-12. Split very broad introduction ranges into parts of about 10 slides each.

Before writing image prompts, create a global design map, duplicate-control map, and Japanese presentation script for each slide. The slide visible text must be distilled from the script, not copied from it.

## Output Workflow

1. Create the global design map with one unique message and primary concept per slide.
2. Create the duplicate-control map and revise until no slide owns the same concept twice.
3. Write Japanese presentation scripts for every slide.
4. Create the image-generation prompt for each slide using the fixed design system.
5. If the user requested prompt-only output, return the design map, duplicate-control map, scripts, and completed prompts; do not generate images.
6. Otherwise, generate the slide images as 16:9 images. Use the image generation capability directly when available.
7. After generation, keep explanation minimal: identify the target section and number of generated slides.

## Example Scope

For `1.2 Categories of Software Requirements`, target Ch.01 Software Requirements, `1. Software Requirements Fundamentals`, `1.2 Categories of Software Requirements`. Use Figure 1.2 and sections 1.3-1.8 as supporting scope. Plan about 8-10 slides including:

- requirements category tree
- Product Requirements vs. Project Requirements
- Functional vs. Nonfunctional Requirements
- Nonfunctional split into Technology Constraints and Quality of Service Constraints
- why classification helps elicitation, analysis, specification, validation, and impact understanding
- connection map to sections 1.3-1.8
