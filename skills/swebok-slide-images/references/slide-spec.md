# SWEBOK Slide Image Specification

Use this reference when creating Japanese study/reference slide images from SWEBOK Guide V4.0a.

## Role

Act as:

- SWEBOK reader: read the target text, figures/tables, parent heading, and nearby related sections accurately.
- Instructional designer: reorganize the content for learning and later reference.
- Slide designer: create quiet, intellectual, spacious, diagram-centered slides.
- UI/UX designer: make the topic understandable in 3 seconds and the key points in 15 seconds.

## Target Inference

Infer Knowledge Area / chapter, section number, English title, Japanese title, parent topic, and related sections from the user input. Use supporting sections only when the requested section is too short or explicitly points forward. Ask only when ambiguity materially affects the result.

## Section-Type Patterns

Use the closest pattern:

- Definition: importance, formal definition decomposition, key terms, practical meaning, source, misunderstandings, summary.
- Classification: reason for classification, full category diagram, upper/lower categories, differences, benefits, next-section connection, summary.
- Activity/process: purpose, whole flow, activity roles, relation to management/development, cautions, related KA, summary.
- Technique/tool: purpose, category organization, main techniques/tools, selection viewpoint, use context, cautions, summary.
- Introduction: chapter position, covered viewpoints, main issues, core concepts, related KAs, topic structure, reading guide, summary.

## Fixed Design System

Apply these specifications to every slide. Do not introduce alternative styles.

### Canvas and Layout

- 16:9 slide ratio.
- Use a 12-column alignment grid.
- Keep generous outer margins.
- Basic structure: top = title, center = main content, bottom = note/source.
- Fixed slide number in the upper right.
- Fixed small source note at the bottom.
- Enforce one message per slide.
- Give each slide one visual protagonist. Split crowded information.

### Color Palette

Use only:

- Background: `#F7F5F2`
- Surface / Card Background: `#FFFFFF`
- Primary Text: `#1F2937`
- Secondary Text: `#475569`
- Accent: `#0F766E`
- Divider / Border: `#D8DEE6`

Rules:

- Use Accent for headings, emphasis, diagram lines, and important card headings.
- Use Primary Text for main body text.
- Use Secondary Text for notes and secondary information.
- Use Divider for rules and card borders.
- Background must be `#F7F5F2`; card interiors must be `#FFFFFF`.
- Do not use other strong colors or gradients.

### Typography

Assume Noto Sans JP and matching sans-serif for English.

- Slide Title: 30pt, Bold, `#1F2937`
- Section Subtitle / One-line message: 18pt, Medium, `#0F766E`
- Body Text: 18pt, Regular, `#1F2937`
- Supporting Text: 15pt, Regular, `#475569`
- Caption / Source / Slide Number: 11pt, Medium, `#475569`
- Card Title: 18pt, Bold, `#1F2937`
- Card Body: 15pt, Regular, `#1F2937`

Rules:

- No long paragraphs.
- Body content: 3-5 items maximum.
- Keep each item short.
- The heading sequence alone should reveal the slide flow.
- Japanese is primary; English terms are supporting labels.

### Shapes and Lines

- Card background: `#FFFFFF`
- Card border: 1.5px `#D8DEE6`
- Card radius: 12px
- No shadows.
- Divider line: 1px `#D8DEE6`
- Arrows/connectors: 2px `#0F766E`
- Icons, if used, must be simple flat line icons.
- No 3D, dimensional icons, or decorative illustrations.

### Reusable Components

Use consistent appearances for:

- Header Title
- Slide Number
- Definition Card
- Comparison Block
- Hierarchy Tree
- Process Flow
- Relation Map
- Insight Card
- Summary Cards
- Source Note, e.g. `Source: SWEBOK Guide V4.0a, Ch.01 §1.2`

## Layout Rules

- Title in the upper left.
- Optional one-line message directly under the title.
- Main content centered in the middle region.
- Comparisons use two columns.
- Classifications use a tree or category diagram.
- Flows use arrows.
- Relations use a central map.
- Summaries use 3-5 Summary Cards in a row or two rows.
- Avoid large tables; convert them to cards or maps.
- Use proximity, alignment, and repetition so the viewer's eye does not wander.

## Diagram Rules

- Definition: Definition Card.
- Classification: tree or category diagram.
- Comparison: two-column block.
- Flow: arrow process flow.
- Relation: relation map.
- Structure: hierarchy diagram.
- Caution: calm Insight Card.
- Summary: 3-5 Summary Cards.
- Icons must support meaning, not decorate.
- Reuse the same visual treatment for the same semantic role across chapters.

## Image Prompt Requirements

Each image prompt must specify:

- `Create one 16:9 slide image`.
- Japanese text exactly as intended for the slide.
- Section number, slide number, and source note.
- Fixed colors, typography, card borders, no shadows, no gradients.
- The chosen component type: Definition Card, Comparison Block, Hierarchy Tree, Process Flow, Relation Map, Insight Card, or Summary Cards.
- Layout with top title, central diagram/cards, and bottom source note.
- No dense paragraphs, no table dumps, no decorative illustration, no invented facts.

## Final Quality Criteria

The result must make clear:

- requested section's subject
- relation to the parent topic
- important concepts
- meaning of figures/tables
- connection to following sections

Japanese must be natural, English terms must be accurate, each slide must have one clear message, diagrams must carry the explanation, and the design must remain consistent, quiet, spacious, and readable when projected.
