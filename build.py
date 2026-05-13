#!/usr/bin/env python3
"""
build.py — Study Notes Static Site Builder
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Author:  Muhd Aiman (MAb839N)
GitHub:  https://github.com/MAb839N

A zero-dependency static site generator that converts structured Markdown
module files into a single portable HTML study notes application.

Zero external dependencies. Requires Python 3.6+
Works on Windows, macOS, Linux — no Python packages required.

Usage:
  python build.py        (Windows)
  python3 build.py       (macOS / Linux)

Reads:   template.html + modules/*.md
Writes:  study-notes.html
"""
import re
from pathlib import Path

# ─── PATHS ────────────────────────────────────────────────────────────────────
MODULES_DIR = Path('modules')
TEMPLATE    = Path('template.html')
OUTPUT      = Path('study-notes.html')

# ─── CONSTANTS ────────────────────────────────────────────────────────────────
ALLOWED_COLORS = {'blue', 'green', 'gold', 'rose', 'purple', 'teal', 'orange', 'slate'}
REQUIRED_MODES = ('NOTES', 'MINDMAP', 'FLASHCARDS')


# ─── UTILITIES ────────────────────────────────────────────────────────────────
def js_escape(s):
    """Escape a value for safe embedding in a JS single-quoted string."""
    return str(s).replace('\\', '\\\\').replace("'", "\\'")


# ─── FRONTMATTER PARSER ───────────────────────────────────────────────────────
_ATTR_RE = re.compile(r'(\w[\w-]*)=["\']([^"\']*)["\']')

def _parse_inline_attrs(s):
    return dict(_ATTR_RE.findall(s))

def parse_frontmatter(raw):
    """
    Parse YAML-like frontmatter into a dict.
    Supports: key: value, key: "value", list with - items,
    pill shorthand: - Label | target-id
    """
    data = {}
    current_list_key = None

    for line in raw.splitlines():
        stripped = line.lstrip()
        if not stripped:
            continue

        if stripped.startswith('- '):
            if current_list_key is None:
                continue
            item_raw = stripped[2:].strip().strip('"\'')
            if '|' in item_raw:
                parts = item_raw.split('|', 1)
                data[current_list_key].append({
                    'label':  parts[0].strip(),
                    'target': parts[1].strip()
                })
            else:
                data[current_list_key].append(item_raw)
            continue

        if ':' in line and not line.startswith(' '):
            key, _, rest = line.partition(':')
            key = key.strip()
            val = rest.strip().strip('"\'')
            if val == '':
                data[key] = []
                current_list_key = key
            else:
                data[key] = val
                current_list_key = None

    return data


# ─── MODULE FILE LOADER ───────────────────────────────────────────────────────
def load_module(filepath):
    """
    Parse a module .md file.
    Returns: (frontmatter_dict, notes_raw, mindmap_raw, flashcards_raw)
    Raises ValueError for structural problems.
    """
    text = Path(filepath).read_text(encoding='utf-8')

    fm_match = re.match(r'^---\s*\n(.*?)\n---', text, re.DOTALL)
    if not fm_match:
        raise ValueError("No frontmatter block (--- delimiters) found.")

    fm   = parse_frontmatter(fm_match.group(1))
    body = text[fm_match.end():].strip()

    for req in ('id', 'course', 'course-full', 'label', 'title'):
        if req not in fm:
            raise ValueError(f"Missing required frontmatter field: '{req}'")

    marker_re = re.compile(r'<!--\s*(NOTES|MINDMAP|FLASHCARDS)\s*-->', re.IGNORECASE)
    parts = marker_re.split(body)

    sections = {}
    for i in range(1, len(parts), 2):
        key     = parts[i].strip().upper()
        content = parts[i + 1].strip() if i + 1 < len(parts) else ''
        sections[key] = content

    return (
        fm,
        sections.get('NOTES',      ''),
        sections.get('MINDMAP',    ''),
        sections.get('FLASHCARDS', ''),
    )


# ─── SECTION PARSER ───────────────────────────────────────────────────────────
_SECTION_OPEN_RE = re.compile(r'<!--\s*SECTION\s+(.*?)\s*-->', re.DOTALL)
_SECTION_CLOSE   = '<!-- /SECTION -->'

def transform_sections(notes_html):
    """
    Parse <!-- SECTION attr="val" ... --> ... <!-- /SECTION --> blocks
    and wrap each in the full collapsible .sec HTML shell.

    Returns: (transformed_html, section_ids, section_colors)

    Attributes in the SECTION marker:
      id     → HTML id and toggleSec() argument
      icon   → emoji for the section icon circle
      color  → one of ALLOWED_COLORS
      title  → section header text
      num    → integer shown as § N
    """
    out        = []
    sec_ids    = []
    sec_colors = []
    pos        = 0
    counter    = 0

    while True:
        m = _SECTION_OPEN_RE.search(notes_html, pos)
        if not m:
            out.append(notes_html[pos:])
            break

        out.append(notes_html[pos:m.start()])
        attrs = _parse_inline_attrs(m.group(1))

        close_pos = notes_html.find(_SECTION_CLOSE, m.end())
        if close_pos == -1:
            out.append(notes_html[m.start():])
            break

        inner = notes_html[m.end():close_pos].strip()

        sid   = attrs.get('id',    f'sec-{counter}')
        icon  = attrs.get('icon',  '📄')
        color = attrs.get('color', 'slate')
        title = attrs.get('title', 'Section')
        num   = attrs.get('num',   str(counter + 1))
        counter += 1

        sec_ids.append(sid)
        sec_colors.append(color)

        out.append(f"""
        <div class="sec" id="{sid}">
          <div class="sec-hd" onclick="toggleSec('{sid}')">
            <div class="sec-ico ico-{color}">{icon}</div>
            <div class="sec-title">{title}</div>
            <span class="sec-num">§ {num}</span><span class="chevron">▾</span>
          </div>
          <div class="sec-bd">
            {inner}
          </div>
        </div>""")

        pos = close_pos + len(_SECTION_CLOSE)

    return ''.join(out), sec_ids, sec_colors


# ─── VALIDATION ───────────────────────────────────────────────────────────────
_GOSEC_RE = re.compile(r"goSec\s*\(\s*'([^']+)'\s*,\s*'([^']+)'\s*\)")

def validate_module(filepath, fm, section_ids, section_colors,
                    notes_raw, mm_raw, fc_raw, seen_module_ids):
    """
    Run all 7 validation checks against a loaded module.
    Returns a list of error strings. Empty list = valid.
    """
    errors = []
    mid    = fm.get('id', '')

    # 1. Filename stem must match frontmatter id
    stem = Path(filepath).stem
    if stem != mid:
        errors.append(
            f"Filename '{stem}.md' does not match frontmatter id '{mid}'. "
            f"Rename file or fix the id field."
        )

    # 2. Module id must be unique across all files in this build
    if mid in seen_module_ids:
        errors.append(f"Duplicate module id '{mid}'. Each module must have a unique id.")

    # 3. All 3 modes are mandatory
    mode_content = {'NOTES': notes_raw, 'MINDMAP': mm_raw, 'FLASHCARDS': fc_raw}
    for mode in REQUIRED_MODES:
        if not mode_content[mode].strip():
            errors.append(
                f"Missing required section: <!-- {mode} -->. "
                f"All three modes (Notes, Mindmap, Flashcards) are mandatory."
            )

    # 4. Duplicate section IDs within this module
    seen_sids = set()
    for sid in section_ids:
        if sid in seen_sids:
            errors.append(f"Duplicate section id within module: '{sid}'.")
        seen_sids.add(sid)

    # 5. Section colors must be from the allowed set
    for sid, color in zip(section_ids, section_colors):
        if color not in ALLOWED_COLORS:
            errors.append(
                f"Section '{sid}' has invalid color '{color}'. "
                f"Allowed: {sorted(ALLOWED_COLORS)}"
            )

    # 6. Pill targets must each match an existing section id
    for pill in fm.get('pills', []):
        if isinstance(pill, dict):
            target = pill.get('target', '')
            if target and target not in section_ids:
                errors.append(
                    f"Pill target '{target}' not found in any SECTION id. "
                    f"Defined ids: {section_ids}"
                )

    # 7. goSec() calls in mindmap: module id and section id must both be valid
    for match in _GOSEC_RE.finditer(mm_raw):
        sec_id, page_id = match.group(1), match.group(2)
        if page_id != mid:
            errors.append(
                f"goSec('{sec_id}', '{page_id}') uses wrong module id "
                f"(expected '{mid}')."
            )
        if sec_id not in section_ids:
            errors.append(
                f"goSec('{sec_id}', '{page_id}') references unknown section id. "
                f"Defined ids: {section_ids}"
            )

    return errors


# ─── PAGE HTML BUILDER ────────────────────────────────────────────────────────
def build_page(fm, notes_transformed, mm_raw, fc_raw):
    """Build the complete <div class="page"> block for one module."""
    mid   = fm['id']
    course = fm.get('course',      '')
    label  = fm.get('label',       '')
    title  = fm.get('title',       '')
    desc   = fm.get('description', '')
    pills  = fm.get('pills',       [])
    ref    = fm.get('reference',   '')

    pills_html = ''
    for p in pills:
        if isinstance(p, dict):
            t = p.get('target', '')
            l = p.get('label',  '')
            pills_html += (
                f'            <span class="hero-pill" data-sec="{t}"'
                f' onclick="goSec(\'{t}\',\'{mid}\')">✦ {l}</span>\n'
            )

    ref_html = (
        f'\n        <div class="ref-box">'
        f'📚 <strong>Reference:</strong> {ref}</div>'
    ) if ref else ''

    notes_div = f"""    <div id="{mid}-notes">
      <div class="hero">
        <div class="hero-tag">{course} · {label}</div>
        <h1>{title}</h1>
        <p>{desc}</p>
        <div class="hero-pills">
{pills_html}        </div>
      </div>
      {notes_transformed}
      {ref_html}
    </div>"""

    mm_div = ''
    if mm_raw.strip():
        mm_div = f"""
    <div id="{mid}-mm" style="display:none">
      <div class="hero">
        <div class="hero-tag">{course} · {label} · Mindmap</div>
        <h1>{title}</h1>
        <p>Click any node to jump to that section in the Notes.</p>
      </div>
      <div class="mm-wrap">
        <div class="mm-banner">🗺 <b>Interactive Mindmap</b> — tap any node to navigate to its notes section.</div>
        <div class="mm-scroll">
          {mm_raw}
        </div>
        <div class="mm-hint">💬 Hover any node to preview · Click to jump to the Notes section</div>
      </div>
    </div>"""

    fc_div = ''
    if fc_raw.strip():
        fc_div = f"""
    <div id="{mid}-fc" style="display:none">
      <div class="hero">
        <div class="hero-tag">{course} · {label} · Flashcards</div>
        <h1>Quick Review</h1>
        <p>Tap each card to reveal the answer.</p>
      </div>
      {fc_raw}
    </div>"""

    return f"""
  <div class="page" id="page-{mid}">
    <div class="pg">
      {notes_div}
      {mm_div}
      {fc_div}
    </div>
  </div>"""


# ─── SIDEBAR BUILDER ──────────────────────────────────────────────────────────
def build_sidebar(courses):
    html = ''
    first = True
    for cid, (cfull, modules) in courses.items():
        collapsed = '' if first else ' collapsed'
        first = False
        links = ''
        for fm in modules:
            mid   = fm['id']
            label = fm.get('label', '')
            title = fm.get('title', '')
            links += (
                f"      <div class=\"sb-link ind\" onclick=\"nav('{mid}',this,'notes')\">"
                f"<span class=\"sb-dot\"></span>{label} · {title}</div>\n"
            )
        links += '      <div class="sb-add">Add via modules/ + build.py</div>\n'
        html += (
            f'  <div class="sb-course{collapsed}" data-course="{cid}">\n'
            f'    <div class="sb-course-toggle" onclick="toggleCourse(this)">\n'
            f'      <span class="sb-course-name">{cfull}</span>\n'
            f'      <span class="sb-caret">&#9660;</span>\n'
            f'    </div>\n'
            f'    <div class="sb-links">\n'
            f'{links}'
            f'    </div>\n'
            f'  </div>\n'
        )
    html += (
        '  <div class="sb-sec">\n'
        '    <div class="sb-lbl" style="opacity:.45">More Courses</div>\n'
        '    <div class="sb-links">\n'
        '      <div class="sb-add">Add via modules/ + build.py</div>\n'
        '    </div>\n'
        '  </div>'
    )
    return html


# ─── HOME CARDS BUILDER ───────────────────────────────────────────────────────
def build_home_cards(all_modules):
    cards = ''
    for fm in all_modules:
        mid    = fm['id']
        course = fm.get('course',      '')
        label  = fm.get('label',       '')
        title  = fm.get('title',       '')
        desc   = fm.get('description', '')
        cards += (
            f'        <div class="home-card" onclick="nav(\'{mid}\',null,\'notes\')">\n'
            f'          <div class="hc-tag">{course} · {label}</div>\n'
            f'          <h3>{title}</h3>\n'
            f'          <p>{desc}</p>\n'
            f'        </div>\n'
        )
    cards += (
        '        <div class="home-card dim">\n'
        '          <div class="hc-tag">Coming Soon</div>\n'
        '          <h3>Add your next lesson</h3>\n'
        '          <p>Drop a .md file in modules/ and run build.py.</p>\n'
        '        </div>'
    )
    return cards


# ─── JS DATA BUILDERS ─────────────────────────────────────────────────────────
def build_topic_modes_js(all_modules, modes_map):
    lines = []
    for fm in all_modules:
        mid   = fm['id']
        modes = modes_map.get(mid, ['notes'])
        modes_s = ', '.join(f"'{m}'" for m in modes)
        lines.append(f"  '{js_escape(mid)}': [{modes_s}]")
    return ',\n'.join(lines)


def build_breadcrumb_labels_js(all_modules):
    lines = ["  'home': 'Home'"]
    for fm in all_modules:
        mid    = fm['id']
        course = fm.get('course', '')
        label  = fm.get('label',  '')
        title  = fm.get('title',  '')
        val    = (
            f"{js_escape(course)} &rsaquo; "
            f"<b>{js_escape(label)} &middot; {js_escape(title)}</b>"
        )
        lines.append(f"  '{js_escape(mid)}': '{val}'")
    lines.append("  'guide': '<b>&#9881; Maintenance Guide</b>'")
    return ',\n'.join(lines)


def build_page_to_course_js(all_modules):
    lines = []
    for fm in all_modules:
        mid = fm['id']
        cid = fm.get('course', '')
        lines.append(f"  '{js_escape(mid)}': '{js_escape(cid)}'")
    return ',\n'.join(lines)


# ─── HOME STATS ───────────────────────────────────────────────────────────────
def build_home_stats(num_modules, num_lessons):
    return (
        f'          <div><div class="stat-n">{num_modules}</div>'
        f'<div class="stat-l">Courses</div></div>\n'
        f'          <div><div class="stat-n">{num_lessons}</div>'
        f'<div class="stat-l">Lessons</div></div>\n'
        f'          <div><div class="stat-n">3</div>'
        f'<div class="stat-l">Study Modes</div></div>'
    )


# ─── MAIN ─────────────────────────────────────────────────────────────────────
def main():
    print('\u2501' * 52)
    print('  Study Notes Builder')
    print('\u2501' * 52)

    if not MODULES_DIR.exists():
        print('\n  \u2717  modules/ folder not found.')
        return
    if not TEMPLATE.exists():
        print('\n  \u2717  template.html not found.')
        return

    md_files = sorted(MODULES_DIR.glob('*.md'))
    if not md_files:
        print('\n  \u2717  No .md files found in modules/')
        return

    print(f'\n  Loading {len(md_files)} module file(s):')

    all_modules     = []
    pages_html      = ''
    modes_map       = {}
    courses         = {}
    seen_module_ids = set()
    build_failed    = False

    for filepath in md_files:
        print(f'\n  \u2500\u2500 {filepath.name}')

        try:
            fm, notes_raw, mm_raw, fc_raw = load_module(filepath)
        except ValueError as e:
            print(f'     \u2717 LOAD ERROR: {e}')
            build_failed = True
            continue

        notes_transformed, section_ids, section_colors = transform_sections(notes_raw)

        errors = validate_module(
            filepath, fm, section_ids, section_colors,
            notes_raw, mm_raw, fc_raw, seen_module_ids
        )

        if errors:
            for e in errors:
                print(f'     \u2717 {e}')
            build_failed = True
            continue

        mid = fm['id']
        print(f'     \u2713 id: {mid}  |  '
              f'sections: {len(section_ids)}  |  '
              f'pills: {len(fm.get("pills", []))}')

        seen_module_ids.add(mid)

        modes = ['notes']
        if mm_raw.strip(): modes.append('mm')
        if fc_raw.strip(): modes.append('fc')
        modes_map[mid] = modes

        all_modules.append(fm)
        pages_html += build_page(fm, notes_transformed, mm_raw, fc_raw)

        cid   = fm.get('course',      'OTHER')
        cfull = fm.get('course-full', cid)
        if cid not in courses:
            courses[cid] = (cfull, [])
        courses[cid][1].append(fm)

    if build_failed:
        print('\n  \u2717  Build aborted. Fix all errors above before retrying.')
        print('\u2501' * 52)
        return

    if not all_modules:
        print('\n  \u2717  No valid modules loaded.')
        return

    sidebar_html    = build_sidebar(courses)
    home_cards_html = build_home_cards(all_modules)
    home_stats_html = build_home_stats(len(courses), len(all_modules))
    topic_modes_js  = build_topic_modes_js(all_modules, modes_map)
    breadcrumbs_js  = build_breadcrumb_labels_js(all_modules)
    page_to_course_js = build_page_to_course_js(all_modules)

    template = TEMPLATE.read_text(encoding='utf-8')
    output   = template
    output   = output.replace('{{SIDEBAR_SECTIONS}}',  sidebar_html)
    output   = output.replace('{{HOME_STATS}}',         home_stats_html)
    output   = output.replace('{{HOME_CARDS}}',         home_cards_html)
    output   = output.replace('{{MODULE_PAGES}}',       pages_html)
    output   = output.replace('{{TOPIC_MODES}}',        topic_modes_js)
    output   = output.replace('{{BREADCRUMB_LABELS}}',  breadcrumbs_js)
    output   = output.replace('{{PAGE_TO_COURSE}}',     page_to_course_js)

    OUTPUT.write_text(output, encoding='utf-8')

    print(f'\n  \u2713  Output: {OUTPUT}  ({len(output):,} bytes)')
    print(f'     {len(courses)} module(s) \u00b7 {len(all_modules)} lesson(s)')
    print('\u2501' * 52)


if __name__ == '__main__':
    main()
