# Script-First SWEBOK Slide Workflow

Use this workflow before generating SWEBOK slide images or prompts.

## Planning Artifacts

Create these artifacts in order.

### 1. Global Design Map

Use a compact table or structured list:

- Slide ID
- Slide role: title, position, definition, classification, comparison, process, relation, caution, summary, synthesis
- One-message statement
- Source anchor: chapter/section/figure/table
- Primary concept owned by the slide
- Visual component: Definition Card, Comparison Block, Hierarchy Tree, Process Flow, Relation Map, Insight Card, Summary Cards

For chapter-level work, include group labels:

- Chapter Opening
- Section Group
- Bridge
- Chapter Closing

### 2. Duplicate-Control Map

Assign each important concept to one primary slide.

Use labels:

- `Primary`: the slide that explains the concept.
- `Recap`: short reminder only.
- `Bridge`: connects two concepts without re-explaining them.
- `Synthesis`: integrates earlier concepts at a higher level.

If two slides have the same one-message statement, revise the plan before writing scripts.

### 3. Presentation Scripts

Write Japanese speaker scripts after the global design map is stable.

Recommended length:

- title/opening slide: 80-140 Japanese characters;
- normal concept slide: 120-220 Japanese characters;
- dense comparison/structure slide: 180-260 Japanese characters;
- summary/synthesis slide: 120-200 Japanese characters.

Each script should:

- explain why the slide exists;
- say what the viewer should notice in the diagram;
- connect to the previous or next slide when useful;
- stay grounded in SWEBOK;
- avoid reading every visible bullet aloud.

### 4. Slide Prompts

Derive prompts from scripts.

Each prompt should include:

- slide ID and title;
- exact visible Japanese text;
- one-line message;
- selected component and layout;
- source note;
- fixed design system from `swebok-slide-images/references/slide-spec.md`;
- instruction that the full script is not visible on the slide.

## Anti-Duplication Rules

- A definition appears once as a definition. Later slides may use the term but must not redefine it.
- A category tree appears once as the full structure. Later slides may zoom into branches.
- A comparison appears once as a comparison. Later slides may apply the distinction.
- A figure/table from SWEBOK appears once as the main explanation. Later slides may reference its implication.
- Summary slides synthesize, not repeat all bullets.

## Review Checklist

Before image generation or prompt-only output, check:

- every slide has a unique one-message statement;
- no two slides have the same primary concept;
- every script has a matching visual role;
- visible text is shorter than the script;
- no slide depends on unsupported facts;
- source anchors are present;
- chapter-level opening/closing slides do not duplicate section-level slides.
