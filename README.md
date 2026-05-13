# Study Notes — Static Site Builder

**A personal static study notes system built with AI assistance.**

Converts structured Markdown module files into a single portable HTML application — no server, no install, no internet connection required after generation.

Built by [Muhd Aiman — MAb839N](https://github.com/MAb839N)

---

## What it does

Running one command (`python3 build.py`) reads all `.md` files in the `modules/` folder and generates `study-notes.html` — a fully self-contained study application with:

- **Notes mode** — collapsible sections with structured conceptual content
- **Mindmap mode** — interactive SVG diagram; hover to preview, click to navigate
- **Flashcard mode** — flip cards for active recall practice
- **Sidebar** — collapsible course groups, search scoped to the current page
- **Responsive** — works on desktop, tablet, and mobile

The generated HTML file works completely offline. Sync it to any device and open in any browser.

See [AI_MODULE_GUIDE.md](./AI_MODULE_GUIDE.md) for the full module authoring specification.

---

## Project structure

```
project/
├── build.py              ← run this to generate the site
├── template.html         ← shell: CSS, JS, layout — never edited for content
├── AI_MODULE_GUIDE.md    ← format specification for AI-generated modules
├── modules/
│   ├── sample-gpt.md     ← sample: using GPT to generate modules
│   ├── sample-git.md     ← sample: GitHub setup and device syncing
│   └── your-module.md    ← add your own modules here
└── study-notes.html      ← generated output (rebuild anytime)
```

---

## How to run

**Requirements:** Python 3.6+ — no packages, no install beyond Python itself.

```bash
# macOS / Linux
python3 build.py

# Windows
python build.py
```

The builder validates every module before generating output. If any file has a structural error, the build aborts with a clear error message indicating exactly what to fix.

---

## How to add a module

1. Create a `.md` file in `modules/` following the schema in `AI_MODULE_GUIDE.md`
2. Run `python3 build.py`
3. Open `study-notes.html` in a browser

The included sample modules (`sample-gpt.md`, `sample-git.md`) are working examples of the full format — sections, mindmap, and flashcards all included.

---

## Module format overview

Each module file has three parts separated by markers:

```
---
id: web-l1
course: WEB
course-full: Web Development
label: Lesson 1
title: How the Web Works
description: One sentence summary.
pills:
  - Section Name | section-id
---

<!-- NOTES -->
<!-- SECTION id="section-id" icon="📌" color="blue" title="Section Title" num="1" -->
[HTML content]
<!-- /SECTION -->

<!-- MINDMAP -->
<svg viewBox="0 0 1000 500" ...> ... </svg>

<!-- FLASHCARDS -->
<div class="fc-sec"> ... </div>
```

See `AI_MODULE_GUIDE.md` for the complete specification including all available components, colour conventions, mindmap rules, and validation requirements.

---

## Build validation

The builder runs 7 checks on every module before generating output:

1. Filename stem matches frontmatter `id`
2. Module `id` is unique across all files
3. All three modes (Notes, Mindmap, Flashcards) are present
4. No duplicate section IDs within a module
5. Section `color` values are from the allowed set
6. Every pill target matches an existing section ID
7. Every `goSec()` call in the mindmap uses valid section and module IDs

Any failure aborts the build cleanly with a descriptive error message.

---

## Motivation

This project started as a personal study tool and became a milestone in learning to build structured systems with GPT assistance. The AI generates module content; the pipeline enforces structure and validates output. The goal was a system where adding new study material is as simple as a conversation.

---

*Built with Python 3 · Zero external dependencies · Works fully offline*
