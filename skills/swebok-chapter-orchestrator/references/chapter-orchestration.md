# SWEBOK Chapter Orchestration

Use this reference with the sibling `swebok-slide-images` skill to create chapter-level SWEBOK slide image sets.

## Purpose

Chapter-level requests need more than concatenated section slides. Add:

- an opening frame that tells the learner where the chapter sits in SWEBOK;
- a map of the chapter's topics and dependencies;
- section-level slide groups generated with the existing section skill;
- synthesis slides that connect the sections back into one chapter-level understanding.

Create the chapter-wide design map and Japanese presentation scripts before creating slide prompts. Use the sibling `swebok-script-first-planner` skill to prevent chapter-opening, section, bridge, and closing slides from repeating the same explanation.

## Chapter-Level Reading Checklist

Read these before planning slides:

- chapter / Knowledge Area title and introduction;
- topic headings and nesting;
- chapter figures/tables that define structure;
- Matrix of Topics vs. Reference Material;
- Further Readings and References;
- first paragraph of each major section;
- neighboring chapter links only when SWEBOK explicitly connects them.

## Chapter Opening Slides

Use 3-5 slides:

1. **Title**: chapter number, English/Japanese title, and what the chapter helps the learner understand.
2. **Positioning**: relation to SWEBOK and software engineering practice as stated by the source.
3. **Scope Map**: major topics as a hierarchy or relation map.
4. **Reading Route**: recommended order implied by section dependencies.
5. **Key Questions**: 3-5 learning questions derived from the chapter introduction and topic headings.

Keep these slides source-grounded. Do not present opinions as SWEBOK claims.

## Section Group Orchestration

For each major section:

1. Treat the section title/number as input to `swebok-slide-images`.
2. Apply the section skill's source workflow, content rules, slide planning, and fixed design system.
3. Keep the section group's presentation scripts inside the chapter-wide duplicate-control map.
4. Choose fewer slides for simple subsections and more for dense subsections.
5. Preserve chapter-level numbering and grouping so learners can navigate later.
6. Include the same source note format, e.g. `Source: SWEBOK Guide V4.0a, Ch.01 §1.2`.

When the chapter has many tiny subsections, group them by parent topic and create one section group per parent topic. Do not create full 8-10 slide groups for every tiny heading unless the user requests exhaustive coverage.

## Bridge Slides

Add bridge slides only when a chapter changes conceptual mode, such as:

- fundamentals to processes;
- categories to activities;
- concepts to techniques/tools;
- requirements to design/test/management links.

Bridge slide format:

- one-line message: "ここから何が変わるか";
- 2-column comparison or small relation map;
- 3 short bullets maximum;
- no new claims beyond the source.

## Chapter Closing Slides

Use 4-7 slides:

1. **Synthesis Map**: show how major sections relate.
2. **Concept Comparison**: clarify the most important distinctions across sections.
3. **Practice Viewpoint**: source-grounded cautions or reading viewpoints.
4. **Chapter Summary**: 3-5 Summary Cards.
5. **Reference Map**: how matrix / further readings support deeper study.
6. **Related KAs**: only if explicitly supported by SWEBOK.
7. **Next Study Path**: next chapter or next topic flow, source-grounded.

## Prompt Grouping

For prompt-only output, group prompts as:

```text
Chapter Opening
- 01-01 ...
- 01-02 ...

Section 1.1 ...
- 1.1-01 ...

Section 1.2 ...
- 1.2-01 ...

Chapter Closing
- 99-01 ...
```

Each prompt must still satisfy the image prompt requirements from `swebok-slide-images/references/slide-spec.md`.

Include the Japanese presentation script for each prompt unless the user explicitly asks for prompts only without scripts.

## Part Splitting

Split large chapters into parts when the output would be too large or image generation would be unwieldy:

- Part 1: chapter opening + first conceptual group.
- Part 2+: subsequent section groups with one short recap slide.
- Final Part: remaining section groups + chapter closing.

Every part should include enough context to stand alone, but avoid repeating the full chapter overview.

## Quality Gate

Before output, check:

- chapter identity and section list are correct;
- chapter opening slides explain why the chapter exists;
- each section group follows the section skill;
- chapter closing slides synthesize rather than repeat;
- all claims are traceable to SWEBOK;
- no dense paragraphs, table dumps, unsupported examples, gradients, shadows, or extra colors appear in prompts.
