# AI_MODULE_GUIDE.md
# Study Notes — Module Generation Rules

## How to use this file

When generating a new module, give the AI (Claude or any other LLM):
1. This file as a reference
2. Your raw course notes or lecture material
3. The instruction below

**Instruction to include in your prompt:**
> "Generate a module .md file strictly following AI_MODULE_GUIDE.md.
> Do not deviate from the schema, component names, or file structure.
> Use only the HTML components listed. Do not invent new classes or tags."

---

## Output: One .md File

The AI must output a single `.md` file.
Save it to the `modules/` folder.
Run `python build.py` (or `python3 build.py`) to rebuild the site.

The build script validates every file before generating output.
If any rule is violated, the build will **abort with a clear error message**.
Fix the error and re-run. The site is never updated with invalid input.

---

## File Structure — Mandatory

Every module file has exactly this structure, in this order:

```
---
[FRONTMATTER]
---

<!-- NOTES -->
[NOTES CONTENT — sections using comment markers]

<!-- MINDMAP -->
[ONE SVG element]

<!-- FLASHCARDS -->
[One or more .fc-sec blocks]
```

No other top-level markers. No extra sections. No deviation from this order.
All three modes (Notes, Mindmap, Flashcards) are **mandatory**. The build will fail if any are missing.

---

## Part 1: Frontmatter Schema

All fields are required unless marked optional.

```yaml
---
id: course-lesson
course: SHORT
course-full: Full Course Name
label: Lesson N
title: Full Lesson Title
description: One sentence. What this lesson covers.
reference: "Author (Year). Title. Publisher."   # OPTIONAL
pills:
  - Pill Label Text | section-id
  - Pill Label Text | section-id
---
```

### Field rules

| Field | Rule |
|---|---|
| `id` | Lowercase, no spaces. Format: `web-l1`, `py-l2`. **Must match the filename stem exactly.** Must be unique across all modules. |
| `course` | Short uppercase abbreviation. e.g. `WEB`, `PY`. No institution name or code. |
| `course-full` | Full course title. No institution name or code. |
| `label` | Always `Lesson N` (e.g. `Lesson 1`, `Lesson 2`). Shown in sidebar and breadcrumb. |
| `title` | Full lesson title shown in the hero banner. |
| `description` | One sentence summary. Shown in hero and home card. |
| `reference` | Optional. Textbook citation. HTML allowed inside (e.g. `<em>`). |
| `pills` | 3–8 entries. Each is `Pill label | section-id`. Quick-jump links in the hero. Every target must match a real section id in NOTES. |

### Label convention
Every lesson uses `Lesson N` — not `Topic N`, not `Week N`. The build has no enforcement for this yet, but consistency is required for the sidebar and breadcrumb to make sense to the reader.

---

## Part 2: NOTES Section

Content is divided into sections using **comment marker pairs**. The build script parses these and wraps each section in the correct collapsible HTML shell.

### Section syntax — MANDATORY FORMAT

```
<!-- SECTION id="UNIQUE-ID" icon="EMOJI" color="COLOR" title="Section Title" num="N" -->
[section body HTML here]
<!-- /SECTION -->
```

The opening marker is a single HTML comment containing all attributes.
The closing marker is always exactly `<!-- /SECTION -->`.

### ⚠️ Critical rules for section markers

- The **opening** marker: `<!-- SECTION` followed by attributes, then `-->`
- The **closing** marker: always exactly `<!-- /SECTION -->` — no variation
- Never use `</section>` anywhere in the file — it has no meaning in this format
- Never nest section markers inside each other
- The build will not produce output if a `<!-- /SECTION -->` is missing

### Section attributes

| Attribute | Rule |
|---|---|
| `id` | Unique within the module. Prefix with a short module code. e.g. `w-intro`, `p-vars`, `g-setup`. |
| `icon` | One emoji. See colour conventions below. |
| `color` | One of: `blue`, `green`, `gold`, `rose`, `purple`, `teal`, `orange`, `slate` — **no other values accepted**. |
| `title` | Section header text. |
| `num` | Integer. Section number shown as `§ N`. Count up from 1 with no gaps. |

### Colour conventions (follow consistently)

| Color | Use for |
|---|---|
| `blue` | Definitions, core concepts |
| `green` | Processes, functions, steps, how-to |
| `gold` | Examples, applied steps, frameworks |
| `rose` | Warnings, skills, critical distinctions |
| `purple` | Structure, hierarchy, classification |
| `teal` | Rationale, why it matters, significance |
| `orange` | Types, categories, varieties |
| `slate` | Summary, key takeaways |

### Section example

```
<!-- SECTION id="w-intro" icon="📌" color="blue" title="Introduction to the Web" num="1" -->
<div class="def-box">
  <div class="def-lbl">Core Definition</div>
  <p><strong>Management</strong> is the attainment of organisational goals...</p>
</div>
<!-- /SECTION -->

<!-- SECTION id="p-func" icon="⚙️" color="green" title="The Four Functions (POLC)" num="2" -->
<p>Content for section 2 goes here.</p>
<!-- /SECTION -->
```

---

## Part 3: HTML Components Available

Use ONLY the components below. Do not invent new class names.

---

### Definition Box
Use for: core definitions, key concepts.
```html
<div class="def-box">
  <div class="def-lbl">Core Definition</div>
  <p><strong>Term</strong> is the definition text here.</p>
</div>
```
For non-standard label: replace "Core Definition" with e.g. "Legal Requirement", "Key Concept".
For alternate accent colour: add `style="background:linear-gradient(135deg,#f0fdf8,#e6faf4);border-left-color:var(--c-green);"` to `.def-box`.

---

### 2-Column Grid
Use for: paired comparisons, two related concepts.
```html
<div class="g2">
  <div class="card-g CARD-CLASS">
    <h4><span class="f-badge BADGE-CLASS">Letter</span><span class="clr-XX">Label</span></h4>
    <p>Content.</p>
  </div>
  <div class="card-g CARD-CLASS"> ... </div>
</div>
```

### 3-Column Grid
Use for: three concepts side by side (e.g. skill types, three categories).
```html
<div class="g3">
  <div class="card-g CARD-CLASS"> ... </div>
  <div class="card-g CARD-CLASS"> ... </div>
  <div class="card-g CARD-CLASS"> ... </div>
</div>
```

### Card background classes (pick the most appropriate)
| Class | Colour | Use for |
|---|---|---|
| `cg-plan` | Green | Planning / first item |
| `cg-org` | Blue | Organising / second item |
| `cg-lead` | Yellow | Leading / third item |
| `cg-ctrl` | Red | Controlling / fourth item |
| `cg-inc` | Blue | Incidents / definitions |
| `cg-acc` | Red | Accidents / warnings |
| `cg-near` | Yellow | Near-miss / caution |
| `cg-safe` | Green | Safety / positive |
| `cg-type` | Purple | Types / categories |

### Badge + colour-label classes
```html
<span class="f-badge bg-gr">P</span><span class="clr-gr">Planning</span>
```
| Badge class | Colour |
|---|---|
| `bg-gr` | Green |
| `bg-bl` | Blue |
| `bg-go` | Gold |
| `bg-ro` | Rose |
| `bg-or` | Orange |
| `bg-pu` | Purple |

Matching text colour classes: `clr-gr` `clr-bl` `clr-go` `clr-ro` `clr-te` `clr-or` `clr-pu`

---

### Tip Box (light background, general note)
```html
<div class="tip-box">💡 <strong>Note:</strong> Content here.</div>
```

### Warning Box (yellow background, important distinction)
```html
<div class="warn-box">⚠️ <strong>Key rule:</strong> Content here. <strong>Emphasise key terms.</strong></div>
```

### Info Box (blue background, supplementary information)
```html
<div class="info-box">ℹ️ Content here.</div>
```

### Quote / Pull Note (gold left border, italic note)
```html
<div class="quote-note">📌 Italic note or memorable quote here.</div>
```

---

### Checklist (why-list)
Use for: summary points, bullet reasons, takeaways.
```html
<ul class="why-list">
  <li><span class="why-chk">✓</span><span><strong>Key term</strong> — explanation.</span></li>
  <li><span class="why-chk">✓</span><span><strong>Key term</strong> — explanation.</span></li>
</ul>
```

---

### Numbered Steps
Use for: ordered processes, numbered procedures.
```html
<div class="steps">
  <div class="step">
    <div class="step-num">1</div>
    <div class="step-body">
      <h5>Step Title</h5>
      <p>Step description.</p>
    </div>
  </div>
  <div class="step">
    <div class="step-num">2</div>
    <div class="step-body">
      <h5>Step Title</h5>
      <p>Step description.</p>
    </div>
  </div>
</div>
```

---

### Management Hierarchy
Use for: any 3-level hierarchy (Top / Middle / First-line or equivalent).
```html
<div class="hier">
  <div class="h-lvl h-top">
    <div class="h-bar"></div>
    <div class="h-body">
      <div class="h-title">Top Level Name</div>
      <div class="h-eg">e.g. Example Role</div>
      <div class="h-desc">Description of this level.</div>
    </div>
  </div>
  <div class="h-lvl h-mid">
    <div class="h-bar"></div>
    <div class="h-body">
      <div class="h-title">Middle Level Name</div>
      <div class="h-eg">e.g. Example Role</div>
      <div class="h-desc">Description.</div>
    </div>
  </div>
  <div class="h-lvl h-first">
    <div class="h-bar"></div>
    <div class="h-body">
      <div class="h-title">Bottom Level Name</div>
      <div class="h-eg">e.g. Example Role</div>
      <div class="h-desc">Description.</div>
    </div>
  </div>
</div>
```

---

### Skill Cards (3 types)
Use for: exactly 3 skill types or analogous triad.
```html
<div class="g3">
  <div class="sk-card sk-c">
    <div class="sk-ico">🔭</div>
    <h4>Skill Name One</h4>
    <p>Description.</p>
    <span class="sk-tag">Tag label</span>
  </div>
  <div class="sk-card sk-h">
    <div class="sk-ico">🤝</div>
    <h4>Skill Name Two</h4>
    <p>Description.</p>
    <span class="sk-tag">Tag label</span>
  </div>
  <div class="sk-card sk-t">
    <div class="sk-ico">🔧</div>
    <h4>Skill Name Three</h4>
    <p>Description.</p>
    <span class="sk-tag">Tag label</span>
  </div>
</div>
```
Classes: `sk-c` (purple) · `sk-h` (rose/red) · `sk-t` (green)

---

### Comparison Cards (Effectiveness / Efficiency style)
Use for: direct 2-way comparisons with a label pill.
```html
<div class="g2">
  <div class="p-card p-eff">
    <h4>Concept A</h4>
    <span class="p-tag">Tag A</span>
    <p>Description of A.</p>
  </div>
  <div class="p-card p-efcy">
    <h4>Concept B</h4>
    <span class="p-tag">Tag B</span>
    <p>Description of B.</p>
  </div>
</div>
```
Classes: `p-eff` (green) · `p-efcy` (blue). For rose: use `style="background:#fff1f2;border:1.5px solid #fca5a5;"` on `.p-card`.

---

### Dot Matrix Table
Use for: skill/attribute importance across levels.
```html
<div class="matrix">
  <div class="m-row hd">
    <div class="m-cell">Level</div>
    <div class="m-cell">Skill A</div>
    <div class="m-cell">Skill B</div>
    <div class="m-cell">Skill C</div>
  </div>
  <div class="m-row">
    <div class="m-cell" style="color:#7c3aed">Top</div>
    <div class="m-cell"><div class="dot-row"><div class="d on"></div><div class="d on"></div><div class="d on"></div></div></div>
    <div class="m-cell"><div class="dot-row"><div class="d on"></div><div class="d on"></div><div class="d off"></div></div></div>
    <div class="m-cell"><div class="dot-row"><div class="d on"></div><div class="d off"></div><div class="d off"></div></div></div>
  </div>
</div>
<p style="font-size:.74rem;color:#999;">●●● High · ●○○ Lower</p>
```
Max 3 dots per cell. `on` = filled, `off` = empty.

---

### Reference Box
Use at the end of NOTES if there is a textbook source.
```html
<div class="ref-box">📚 <strong>Reference:</strong> Author (Year). <em>Title</em>. Publisher.</div>
```
Note: the `reference` frontmatter field generates this automatically — do not double-up.

---

## Part 4: MINDMAP Section

The mindmap is a single `<svg>` element. No wrapping div — the build script handles that.

```html
<svg viewBox="0 0 1000 500" xmlns="http://www.w3.org/2000/svg" aria-label="COURSE Lesson N mindmap">

  <!-- Branch paths -->
  <path d="M fromX fromY C cp1X cp1Y, cp2X cp2Y, toX toY"
        fill="none" stroke="#COLOR" stroke-width="4" stroke-linecap="round"/>

  <!-- Centre node (always present) -->
  <rect x="408" y="223" width="164" height="54" rx="8" fill="#7a7a8e"/>
  <text x="490" y="245" text-anchor="middle" fill="white"
        font-family="Arial,sans-serif" font-size="13" font-weight="600">Lesson</text>
  <text x="490" y="263" text-anchor="middle" fill="white"
        font-family="Arial,sans-serif" font-size="13" font-weight="600">Title</text>

  <!-- Clickable node (repeat for each branch label) -->
  <g class="mm-node"
     onclick="goSec('section-id','module-id')"
     onmouseenter="showTip('Node Heading','Tooltip description text.')"
     onmouseleave="hideTip()">
    <rect x="X" y="Y" width="W" height="H" rx="4" fill="rgba(R,G,B,.09)"/>
    <text x="TX" y="TY" text-anchor="start" fill="#COLOR"
          font-family="Arial,sans-serif" font-size="12.5" font-weight="700">Label</text>
  </g>

</svg>
```

### Mindmap layout rules

- **ViewBox:** always `0 0 1000 500`
- **Centre node:** approximately `x=408 y=223 width=164 height=54`. Always `fill="#7a7a8e"`.
- **Left branch nodes:** `text-anchor="end"`. X coordinate ends around 278–300.
- **Right branch nodes:** `text-anchor="start"`. X coordinate starts around 636–660.
- **Main branch paths:** `stroke-width="4"`
- **Sub-branch paths (leaf labels):** `stroke-width="2"`
- **Sub-label text (leaves):** `font-size="11"`, no background rect
- **Node rects:** `fill="rgba(R,G,B,.09)"` — same hue as the branch colour, low opacity
- **`goSec()` args:** always `('section-id', 'module-id')` — **both must exactly match values in the frontmatter and NOTES sections**. The build validates every `goSec()` call and will abort if either argument is wrong.
- **Tooltip:** `showTip('Short Heading', 'One sentence description.')` — keep brief
- Use 4–6 main branches. Each should map to a section in NOTES.
- Sketch on paper first. Use Bezier C paths for smooth curves.

---

## Part 5: FLASHCARDS Section

One or more `.fc-sec` blocks. Each has a heading and a grid of flip cards.

```html
<div class="fc-sec">
  <div class="fc-hd">📌 Category Heading</div>
  <div class="fc-grid">

    <div class="flip-card" onclick="this.classList.toggle('flipped')">
      <div class="flip-in">
        <div class="fc-f">
          <div class="fc-lbl">Label (Definition / Apply / Distinction / Hierarchy)</div>
          <div class="fc-q">Question text?</div>
          <div class="fc-tip">Tap to reveal ↗</div>
        </div>
        <div class="fc-b">
          <div class="fc-a">Answer with <strong>key terms bolded</strong>.</div>
        </div>
      </div>
    </div>

  </div>
</div>
```

### Flashcard rules
- Minimum 2 `.fc-sec` blocks per module.
- Each `.fc-sec` has 3–5 `.flip-card` entries.
- **fc-lbl types:** `Definition` · `Distinction` · `Apply` · `Hierarchy` · `Skill` · `Key Rule` · `Concept` · `Reporting` · `Summary`
- Questions must be exam-style: specific, testable.
- Answers: concise, accurate. Use `<strong>` for key terms. `<br>` for line breaks.
- Total flashcards per module: 8–12.

---

## Part 6: Content Rules

These rules apply to all content. Non-negotiable. The build enforces most of these — violations abort the build.

| Rule | Requirement | Enforced by build? |
|---|---|---|
| **R1** | No institution names or course codes. Use course titles and short forms only. | No — author's responsibility |
| **R2** | Every module must have Notes + Mindmap + Flashcards. All three required. | **Yes — build aborts** |
| **R3** | Zero external dependencies. No CDN links, no external images, no web fonts. | No — author's responsibility |
| **R4** | All facts must be exact and accurate. Do not paraphrase loosely. | No — author's responsibility |
| **R5** | Use only CSS classes and components listed in this guide. No new classes. | No — author's responsibility |
| **R6** | Section IDs must be unique within the module. Prefix with module code. | **Yes — build aborts** |
| **R7** | Colour coding must follow the conventions table in Part 2. Unknown colours abort build. | **Yes — build aborts** |
| **R8** | Every pill target must match a real section id in NOTES. | **Yes — build aborts** |
| **R9** | The `id` in frontmatter must match the filename stem exactly. | **Yes — build aborts** |
| **R10** | Every `goSec('section-id', 'module-id')` call must use valid ids. | **Yes — build aborts** |
| **R11** | Module ids must be unique across all modules in the build. | **Yes — build aborts** |
| **R12** | Use `Lesson N` for the `label` field — not Topic N or Week N. | No — author's responsibility |

---

## Part 7: Naming Convention

| Item | Convention | Example |
|---|---|---|
| Module file | `course-lesson.md` | `web-l1.md`, `py-l2.md`, `git-l3.md` |
| Module id | `course-lesson` (must match filename without .md) | `web-l1`, `py-l2` |
| Section ids | `X-keyword` (X = 1–3 char prefix matching module) | `w-intro`, `p-vars`, `g-setup` |
| Course short | Uppercase 2–4 chars | `WEB`, `PY`, `GIT` |
| Label | Always `Lesson N` | `Lesson 1`, `Lesson 2` |

Files are sorted alphabetically by the build. Name them so that lessons appear in order:
`web-l1.md`, `web-l2.md`, `web-l3.md` ...

---

## Quick Checklist Before Submitting a Module

The build will catch most errors automatically. This checklist covers what it cannot catch.

**Build will enforce (fatal errors):**
- [ ] `id` in frontmatter matches the filename stem exactly
- [ ] Module `id` is unique (no other module uses the same id)
- [ ] All three modes present: `<!-- NOTES -->`, `<!-- MINDMAP -->`, `<!-- FLASHCARDS -->`
- [ ] No duplicate section ids within this module
- [ ] All section `color` values are from the allowed set
- [ ] Every pill target matches a real section id
- [ ] Every `goSec()` call uses correct module id and valid section id

**Author must verify manually:**
- [ ] `label` field uses `Lesson N` format (not Topic N or Week N)
- [ ] Every `<!-- SECTION ... -->` has a matching `<!-- /SECTION -->`
- [ ] Section numbers count from 1 with no gaps
- [ ] No institution names or external dependencies anywhere
- [ ] All facts are accurate — do not hallucinate content
- [ ] At least 2 `fc-sec` groups with 8–12 flashcards total
- [ ] No new CSS classes invented — only listed components used
