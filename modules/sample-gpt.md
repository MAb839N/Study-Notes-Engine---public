---
id: sample-gpt
course: GUIDE
course-full: Project Guide
label: Guide 1
title: Using GPT to Generate Study Modules
description: How to use GPT to convert raw course material into structured study module files for this system.
pills:
  - What This System Produces | sg-what
  - The AI Module Guide | sg-guide
  - Preparing Your Material | sg-material
  - Writing the Prompt | sg-prompt
  - Reviewing & Validating | sg-review
  - Complete Workflow | sg-workflow
---

<!-- NOTES -->

<!-- SECTION id="sg-what" icon="📋" color="blue" title="What This System Produces" num="1" -->
<div class="def-box">
  <div class="def-lbl">The Output</div>
  <p>Running <code>python3 build.py</code> generates a <strong>single portable HTML file</strong> — <code>study-notes.html</code>. Open it in any browser, on any device, with no internet connection required. Every module you add becomes a fully functional page with Notes, Mindmap, and Flashcards modes.</p>
</div>
<div class="g3" style="margin-top:12px">
  <div class="card-g cg-inc">
    <h4 class="clr-bl">📝 Notes Mode</h4>
    <p>Collapsible sections with structured content — definitions, comparisons, steps, and examples. Searchable within the current page.</p>
  </div>
  <div class="card-g cg-near">
    <h4 class="clr-go">🗺 Mindmap Mode</h4>
    <p>Interactive SVG diagram linking all sections. Hover any node to preview content; click to jump directly to that section in Notes.</p>
  </div>
  <div class="card-g cg-type">
    <h4 class="clr-pu">🃏 Flashcard Mode</h4>
    <p>Flip cards for active recall practice. Grouped by topic. Questions test conceptual understanding, not rote memorisation.</p>
  </div>
</div>
<div class="info-box" style="margin-top:12px">ℹ️ The module <code>.md</code> files are the source of truth. The HTML is always regenerated — never edit <code>study-notes.html</code> directly.</div>
<!-- /SECTION -->

<!-- SECTION id="sg-guide" icon="📖" color="green" title="The AI Module Guide" num="2" -->
<div class="def-box" style="background:linear-gradient(135deg,#f0fdf4,#e6faf0);border-left-color:var(--c-green);">
  <div class="def-lbl" style="color:var(--c-green)">Why It Matters</div>
  <p><code>AI_MODULE_GUIDE.md</code> is the contract between you and the AI. It tells GPT exactly what format to produce, what components to use, and what rules to follow. Without it, GPT guesses — and guesses wrong.</p>
</div>
<p style="font-size:.87rem;color:#555;margin:12px 0 10px;">The guide defines:</p>
<ul class="why-list">
  <li><span class="why-chk">✓</span><span>The <strong>frontmatter schema</strong> — all required fields and what each does</span></li>
  <li><span class="why-chk">✓</span><span>The <strong>section marker format</strong> — <code>&lt;!-- SECTION ... --&gt;</code> syntax and allowed attributes</span></li>
  <li><span class="why-chk">✓</span><span>The <strong>HTML component library</strong> — every card, box, grid, and list class available</span></li>
  <li><span class="why-chk">✓</span><span>The <strong>mindmap rules</strong> — layout, node structure, <code>goSec()</code> call format</span></li>
  <li><span class="why-chk">✓</span><span>The <strong>flashcard structure</strong> — group format, card format, label types</span></li>
  <li><span class="why-chk">✓</span><span>The <strong>content rules</strong> — what the build validates and what you must check manually</span></li>
</ul>
<div class="warn-box" style="margin-top:10px">⚠️ Always pass <code>AI_MODULE_GUIDE.md</code> to GPT in the same conversation as your raw material. GPT cannot follow rules it has not been shown.</div>
<!-- /SECTION -->

<!-- SECTION id="sg-material" icon="📂" color="purple" title="Preparing Your Source Material" num="3" -->
<p style="font-size:.87rem;color:#555;margin-bottom:13px;">The quality of GPT's output depends entirely on the quality of what you give it. Raw, messy notes produce a poor module. Clean, structured source material produces an excellent one.</p>
<div class="g2">
  <div class="card-g cg-plan">
    <h4 class="clr-gr">✅ Good source material</h4>
    <ul>
      <li>Lecture slides or textbook chapter content</li>
      <li>Raw notes with headings and key terms visible</li>
      <li>Exercise or assignment content (stripped of step-by-step instructions)</li>
      <li>Module objectives or learning outcomes</li>
    </ul>
  </div>
  <div class="card-g cg-acc">
    <h4 class="clr-ro">❌ What to strip out first</h4>
    <ul>
      <li>Specific filenames, cell addresses, or computed values from exercises</li>
      <li>Submission instructions ("save as directed", "exit the application")</li>
      <li>Step-by-step lab procedures — extract the concept behind each step instead</li>
      <li>Institution names, course codes, or instructor-specific content</li>
    </ul>
  </div>
</div>
<div class="tip-box" style="margin-top:12px">💡 <strong>Best approach:</strong> Read through your raw material first and identify the key concepts. Write them as bullet points in plain language before passing to GPT. This pre-processing step consistently produces better module output than dumping raw text directly.</div>
<!-- /SECTION -->

<!-- SECTION id="sg-prompt" icon="💬" color="gold" title="Writing the Prompt" num="4" -->
<div class="def-box" style="background:linear-gradient(135deg,#fef9ec,#fef3c7);border-left-color:var(--c-gold-s);">
  <div class="def-lbl" style="color:var(--c-gold-s)">The Core Instruction</div>
  <p>The prompt must tell GPT three things: what format to follow, what content to use, and what to avoid. All three are required for a usable output.</p>
</div>
<p style="font-size:.87rem;font-weight:600;color:var(--navy);margin:14px 0 8px;">Prompt Template</p>
<div class="steps">
  <div class="step"><div class="step-num">1</div><div class="step-body"><h5>Pass the guide</h5><p>Start the conversation by pasting the full contents of <code>AI_MODULE_GUIDE.md</code> and saying: <em>"This is the format spec for a study notes system. Follow it strictly."</em></p></div></div>
  <div class="step"><div class="step-num">2</div><div class="step-body"><h5>Pass the raw material</h5><p>Paste your prepared source content and say: <em>"This is the raw course material for the next module."</em></p></div></div>
  <div class="step"><div class="step-num">3</div><div class="step-body"><h5>Give the instruction</h5><p><em>"Generate a module .md file following AI_MODULE_GUIDE.md strictly. Content must be conceptual reference — not step-by-step instructions. Do not invent new CSS classes or components. Do not include specific filenames, cell addresses, or computed values."</em></p></div></div>
  <div class="step"><div class="step-num">4</div><div class="step-body"><h5>Specify the module id and label</h5><p>Tell GPT exactly: <em>"id: web-l1, course: WEB, course-full: Web Development, label: Lesson 1, title: [your title]"</em> — otherwise GPT will invent them.</p></div></div>
</div>
<!-- /SECTION -->

<!-- SECTION id="sg-review" icon="🔍" color="rose" title="Reviewing and Validating Output" num="5" -->
<p style="font-size:.87rem;color:#555;margin-bottom:13px;">GPT output must always be reviewed before running the build. The build script catches structural errors — but it cannot catch content problems.</p>
<div class="g2">
  <div class="card-g cg-acc">
    <h4 class="clr-ro">🤖 What the build catches</h4>
    <ul>
      <li>Missing <code>&lt;!-- /SECTION --&gt;</code> closing markers</li>
      <li>Invalid section colour values</li>
      <li>Pill targets that don't match any section id</li>
      <li>Duplicate section ids within the module</li>
      <li><code>goSec()</code> calls with wrong module id or unknown section id</li>
      <li>Missing Notes, Mindmap, or Flashcards modes</li>
    </ul>
  </div>
  <div class="card-g cg-near">
    <h4 class="clr-go">👁️ What you must check manually</h4>
    <ul>
      <li>Content is conceptual, not step-by-step</li>
      <li>No invented CSS classes or components</li>
      <li>Flashcard questions test understanding, not exercise recall</li>
      <li>Mindmap covers all sections, no orphan nodes</li>
      <li>Section count and pill count make sense</li>
      <li>All facts are accurate — GPT can hallucinate details</li>
    </ul>
  </div>
</div>
<div class="tip-box" style="margin-top:12px">💡 <strong>Fix errors iteratively:</strong> Run the build, read the error message, fix the specific line in the <code>.md</code> file, run again. Most errors are single-line fixes — a wrong section id, a missing closing marker, or a mismatched pill target.</div>
<!-- /SECTION -->

<!-- SECTION id="sg-workflow" icon="🔄" color="slate" title="Complete Workflow" num="6" -->
<ul class="why-list">
  <li><span class="why-chk">✓</span><span><strong>Prepare</strong> — read raw material, identify key concepts, strip lab-specific content</span></li>
  <li><span class="why-chk">✓</span><span><strong>Prompt</strong> — pass AI_MODULE_GUIDE.md + prepared material + explicit instruction to GPT</span></li>
  <li><span class="why-chk">✓</span><span><strong>Save</strong> — save GPT output as <code>modules/course-lesson.md</code></span></li>
  <li><span class="why-chk">✓</span><span><strong>Build</strong> — run <code>python3 build.py</code> and read the output for errors</span></li>
  <li><span class="why-chk">✓</span><span><strong>Review</strong> — open <code>study-notes.html</code> in a browser and check the rendered output</span></li>
  <li><span class="why-chk">✓</span><span><strong>Refine</strong> — fix any content or formatting issues directly in the <code>.md</code> file, rebuild</span></li>
  <li><span class="why-chk">✓</span><span><strong>Sync</strong> — commit and push the new module file to your private repo</span></li>
</ul>
<div class="quote-note">📌 The <code>.md</code> files are your investment. The HTML is always regeneratable. Protect the source files — they are what gets backed up and synced.</div>
<!-- /SECTION -->


<!-- MINDMAP -->

<svg viewBox="0 0 1000 500" xmlns="http://www.w3.org/2000/svg" aria-label="Guide 1 mindmap — Using GPT to Generate Study Modules">
  <path d="M408 245 C370 228,332 168,296 118" fill="none" stroke="#4a80cc" stroke-width="4" stroke-linecap="round"/>
  <path d="M408 252 C372 262,334 300,296 322" fill="none" stroke="#2d7a5f" stroke-width="4" stroke-linecap="round"/>
  <path d="M408 260 C374 278,336 388,298 432" fill="none" stroke="#5a3a8a" stroke-width="4" stroke-linecap="round"/>
  <path d="M572 245 C608 226,640 164,666 114" fill="none" stroke="#b45309" stroke-width="4" stroke-linecap="round"/>
  <path d="M572 252 C602 252,628 252,652 252" fill="none" stroke="#9b3a4a" stroke-width="4" stroke-linecap="round"/>
  <path d="M572 260 C606 278,640 386,666 430" fill="none" stroke="#3a5068" stroke-width="4" stroke-linecap="round"/>
  <path d="M288 112 C246 104,200 96,154 90"  fill="none" stroke="#4a80cc" stroke-width="2" stroke-linecap="round"/>
  <path d="M288 118 C246 118,200 118,154 118" fill="none" stroke="#4a80cc" stroke-width="2" stroke-linecap="round"/>
  <path d="M288 316 C246 308,200 300,154 294" fill="none" stroke="#2d7a5f" stroke-width="2" stroke-linecap="round"/>
  <path d="M288 322 C246 322,200 322,154 322" fill="none" stroke="#2d7a5f" stroke-width="2" stroke-linecap="round"/>
  <path d="M836 246 C858 234,876 218,886 204" fill="none" stroke="#9b3a4a" stroke-width="2" stroke-linecap="round"/>
  <path d="M836 254 C858 248,876 244,886 242" fill="none" stroke="#9b3a4a" stroke-width="2" stroke-linecap="round"/>
  <rect x="406" y="226" width="168" height="52" rx="8" fill="#7a7a8e"/>
  <text x="490" y="248" text-anchor="middle" fill="white" font-family="Arial,sans-serif" font-size="12" font-weight="600">Using GPT to</text>
  <text x="490" y="266" text-anchor="middle" fill="white" font-family="Arial,sans-serif" font-size="12" font-weight="600">Generate Modules</text>
  <g class="mm-node" onclick="goSec('sg-what','sample-gpt')" onmouseenter="showTip('What This System Produces','Single portable HTML. Notes, Mindmap, Flashcards. Never edit the HTML directly — rebuild from .md files.')" onmouseleave="hideTip()">
    <rect x="74" y="102" width="216" height="30" rx="5" fill="rgba(74,128,204,.09)"/>
    <text x="284" y="122" text-anchor="end" fill="#4a80cc" font-family="Arial,sans-serif" font-size="12.5" font-weight="700">What This System Produces</text>
  </g>
  <g class="mm-node" onclick="goSec('sg-what','sample-gpt')" onmouseenter="showTip('What This Produces','Notes · Mindmap · Flashcards — all from one .md file.')" onmouseleave="hideTip()"><text x="150" y="93"  text-anchor="end" fill="#4a80cc" font-family="Arial,sans-serif" font-size="11">Notes · Mindmap · Flashcards</text></g>
  <g class="mm-node" onclick="goSec('sg-what','sample-gpt')" onmouseenter="showTip('What This Produces','Single portable HTML — offline, no server.')" onmouseleave="hideTip()"><text x="150" y="122" text-anchor="end" fill="#4a80cc" font-family="Arial,sans-serif" font-size="11">Single portable HTML</text></g>
  <g class="mm-node" onclick="goSec('sg-guide','sample-gpt')" onmouseenter="showTip('The AI Module Guide','AI_MODULE_GUIDE.md is the format contract. Always pass it to GPT. Without it GPT guesses.')" onmouseleave="hideTip()">
    <rect x="68" y="306" width="222" height="30" rx="5" fill="rgba(45,122,95,.09)"/>
    <text x="284" y="326" text-anchor="end" fill="#2d7a5f" font-family="Arial,sans-serif" font-size="12.5" font-weight="700">The AI Module Guide</text>
  </g>
  <g class="mm-node" onclick="goSec('sg-guide','sample-gpt')" onmouseenter="showTip('The AI Module Guide','Pass AI_MODULE_GUIDE.md to GPT every time — defines format, components, rules.')" onmouseleave="hideTip()"><text x="150" y="297" text-anchor="end" fill="#2d7a5f" font-family="Arial,sans-serif" font-size="11">Format contract for GPT</text></g>
  <g class="mm-node" onclick="goSec('sg-guide','sample-gpt')" onmouseenter="showTip('The AI Module Guide','Defines sections, components, mindmap rules, flashcard format, content rules.')" onmouseleave="hideTip()"><text x="150" y="326" text-anchor="end" fill="#2d7a5f" font-family="Arial,sans-serif" font-size="11">Schema · components · rules</text></g>
  <g class="mm-node" onclick="goSec('sg-material','sample-gpt')" onmouseenter="showTip('Preparing Material','Strip lab steps, filenames, computed values. Identify concepts first.')" onmouseleave="hideTip()">
    <rect x="88" y="420" width="210" height="24" rx="4" fill="rgba(90,58,138,.09)"/>
    <text x="292" y="437" text-anchor="end" fill="#5a3a8a" font-family="Arial,sans-serif" font-size="12.5" font-weight="700">Preparing Source Material</text>
  </g>
  <g class="mm-node" onclick="goSec('sg-prompt','sample-gpt')" onmouseenter="showTip('Writing the Prompt','4 parts: pass the guide, pass material, give instruction, specify module id and label.')" onmouseleave="hideTip()">
    <rect x="664" y="100" width="188" height="30" rx="4" fill="rgba(180,83,9,.09)"/>
    <text x="668" y="120" text-anchor="start" fill="#b45309" font-family="Arial,sans-serif" font-size="12.5" font-weight="700">Writing the Prompt</text>
  </g>
  <g class="mm-node" onclick="goSec('sg-review','sample-gpt')" onmouseenter="showTip('Reviewing Output','Build catches structure errors. You check content, accuracy, and component usage.')" onmouseleave="hideTip()">
    <rect x="650" y="236" width="188" height="32" rx="4" fill="rgba(155,58,74,.09)"/>
    <text x="654" y="250" text-anchor="start" fill="#9b3a4a" font-family="Arial,sans-serif" font-size="12.5" font-weight="700">Reviewing &amp;</text>
    <text x="654" y="265" text-anchor="start" fill="#9b3a4a" font-family="Arial,sans-serif" font-size="12.5" font-weight="700">Validating</text>
  </g>
  <g class="mm-node" onclick="goSec('sg-review','sample-gpt')" onmouseenter="showTip('Reviewing Output','Build = structural errors. Manual = content accuracy, no hallucinations.')" onmouseleave="hideTip()"><text x="890" y="207" text-anchor="start" fill="#9b3a4a" font-family="Arial,sans-serif" font-size="11">Build catches structure</text></g>
  <g class="mm-node" onclick="goSec('sg-review','sample-gpt')" onmouseenter="showTip('Reviewing Output','Check: conceptual content, no invented classes, accurate facts, flashcard quality.')" onmouseleave="hideTip()"><text x="890" y="244" text-anchor="start" fill="#9b3a4a" font-family="Arial,sans-serif" font-size="11">You check content &amp; facts</text></g>
  <g class="mm-node" onclick="goSec('sg-workflow','sample-gpt')" onmouseenter="showTip('Complete Workflow','Prepare → Prompt → Save → Build → Review → Refine → Sync.')" onmouseleave="hideTip()">
    <rect x="664" y="418" width="188" height="24" rx="4" fill="rgba(58,80,104,.09)"/>
    <text x="668" y="435" text-anchor="start" fill="#3a5068" font-family="Arial,sans-serif" font-size="12.5" font-weight="700">Complete Workflow</text>
  </g>
</svg>


<!-- FLASHCARDS -->

<div class="fc-sec">
  <div class="fc-hd">🤖 GPT Prompting Essentials</div>
  <div class="fc-grid">
    <div class="flip-card" onclick="this.classList.toggle('flipped')"><div class="flip-in"><div class="fc-f"><div class="fc-lbl">Key Rule</div><div class="fc-q">What must you always pass to GPT before asking it to generate a module, and why?</div><div class="fc-tip">Tap to reveal ↗</div></div><div class="fc-b"><div class="fc-a">Always pass <strong>AI_MODULE_GUIDE.md</strong> — it is the format contract. Without it, GPT has no way to know the section marker syntax, allowed components, mindmap rules, or content standards. It will guess, and the output will not build.</div></div></div></div>
    <div class="flip-card" onclick="this.classList.toggle('flipped')"><div class="flip-in"><div class="fc-f"><div class="fc-lbl">Key Rule</div><div class="fc-q">What types of content should you strip from raw material before passing it to GPT?</div><div class="fc-tip">Tap to reveal ↗</div></div><div class="fc-b"><div class="fc-a">Strip: <strong>specific filenames</strong>, cell addresses, computed values, step-by-step lab procedures, submission instructions, institution names, and course codes. What remains should be the <em>concepts</em> — what something is, why it exists, how it works.</div></div></div></div>
    <div class="flip-card" onclick="this.classList.toggle('flipped')"><div class="flip-in"><div class="fc-f"><div class="fc-lbl">Concept</div><div class="fc-q">What does the build script validate, and what must you check manually?</div><div class="fc-tip">Tap to reveal ↗</div></div><div class="fc-b"><div class="fc-a"><strong>Build catches:</strong> missing section markers, invalid colours, wrong goSec() ids, mismatched pill targets, duplicate section ids, missing modes.<br><br><strong>You check:</strong> content is conceptual not procedural, no invented CSS classes, facts are accurate, flashcard questions test understanding.</div></div></div></div>
  </div>
</div>
