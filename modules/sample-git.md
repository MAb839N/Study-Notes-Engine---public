---
id: sample-git
course: GUIDE
course-full: Project Guide
label: Guide 2
title: GitHub Setup & Device Syncing
description: Setting up Git and GitHub, managing a two-repo strategy, and keeping your project in sync across multiple devices.
pills:
  - Git & GitHub Concepts | gh-what
  - One-Time Setup | gh-setup
  - Two-Repo Strategy | gh-repos
  - Daily Workflow | gh-daily
  - Syncing Across Devices | gh-sync
---

<!-- NOTES -->

<!-- SECTION id="gh-what" icon="🐙" color="blue" title="Git and GitHub Concepts" num="1" -->
<div class="def-box">
  <div class="def-lbl">Two Separate Things</div>
  <p><strong>Git</strong> is version control software that runs on your machine — it tracks every change you make to files and lets you go back to any previous state. <strong>GitHub</strong> is a cloud platform where you store Git repositories — it acts as the remote backup and sync point between devices.</p>
</div>
<div class="g2" style="margin-top:12px">
  <div class="card-g cg-inc">
    <h4 class="clr-bl">📦 Repository (repo)</h4>
    <p>A folder tracked by Git. Every file change inside it is recorded. Repositories live locally on your machine and optionally on GitHub as a remote copy.</p>
  </div>
  <div class="card-g cg-type">
    <h4 class="clr-pu">📸 Commit</h4>
    <p>A saved snapshot of your files at a point in time. Every commit has a message describing what changed. Commits form a complete history of the project.</p>
  </div>
</div>
<div class="g2" style="margin-top:10px">
  <div class="card-g cg-safe">
    <h4 class="clr-gr">⬆️ Push</h4>
    <p>Sends your local commits to GitHub. After pushing, the remote repo reflects your latest work. Other devices can then pull these changes.</p>
  </div>
  <div class="card-g cg-near">
    <h4 class="clr-go">⬇️ Pull</h4>
    <p>Fetches the latest commits from GitHub and applies them to your local files. Run this before starting work on any device that hasn't been used recently.</p>
  </div>
</div>
<div class="info-box" style="margin-top:12px">ℹ️ <strong>.gitignore</strong> — a text file in the repo root listing files and folders that Git should never track. Anything listed here is invisible to Git — it will never be committed or pushed, even if you run <code>git add .</code></div>
<!-- /SECTION -->

<!-- SECTION id="gh-setup" icon="⚙️" color="green" title="One-Time Setup" num="2" -->
<p style="font-size:.87rem;color:#555;margin-bottom:13px;">These steps are done once. After setup, daily work is just three commands.</p>
<div class="steps">
  <div class="step"><div class="step-num">1</div><div class="step-body"><h5>Install Git</h5><p>Run <code>git --version</code> in CMD or Terminal. If it returns a version number, Git is already installed. If not, download from <strong>git-scm.com</strong> and install with default settings.</p></div></div>
  <div class="step"><div class="step-num">2</div><div class="step-body"><h5>Set your identity (global, once per machine)</h5><p><code>git config --global user.name "Your Name"</code><br><code>git config --global user.email "you@email.com"</code><br>This tags every commit with your name. Run on each device.</p></div></div>
  <div class="step"><div class="step-num">3</div><div class="step-body"><h5>Create repos on GitHub</h5><p>Go to github.com → <strong>New Repository</strong>. Create one Private and one Public. Do not initialise with a README — you will push from local.</p></div></div>
  <div class="step"><div class="step-num">4</div><div class="step-body"><h5>Initialise your local folders</h5><p>In each project folder, run:<br><code>git init</code><br><code>git add .</code><br><code>git commit -m "initial commit"</code><br><code>git branch -M main</code><br><code>git remote add origin https://github.com/username/repo-name.git</code><br><code>git push -u origin main</code><br>The <code>-u</code> flag sets the default — future pushes only need <code>git push</code>.</p></div></div>
</div>
<!-- /SECTION -->

<!-- SECTION id="gh-repos" icon="📁" color="purple" title="Two-Repo Strategy" num="3" -->
<div class="def-box" style="background:linear-gradient(135deg,#f5f3ff,#ede9fe);border-left-color:var(--c-purple);">
  <div class="def-lbl" style="color:var(--c-purple)">Why Two Separate Repos</div>
  <p>One repo is <strong>private</strong> — your full working backup including all personal content. One repo is <strong>public</strong> — a curated showcase with only the project structure and sample files. They are separate folders on your machine, not branches of the same repo.</p>
</div>
<div class="g2" style="margin-top:12px">
  <div class="p-card p-efcy">
    <h4>Private Repo</h4>
    <span class="p-tag" style="background:#dbeafe;color:var(--c-blue)">Full project · all files</span>
    <p>Contains everything — your real module files, the generated HTML, build tools, and templates. Updated daily. Only you can see it. Used for device sync.</p>
  </div>
  <div class="p-card p-eff">
    <h4>Public Repo</h4>
    <span class="p-tag" style="background:#dcfce7;color:var(--c-green)">Showcase · sample files only</span>
    <p>Contains build tools, templates, sample modules, and README. No personal content. Updated occasionally when something showcase-worthy changes. Anyone can see it.</p>
  </div>
</div>
<div class="tip-box" style="margin-top:12px">💡 <strong>The .gitignore is your safety net:</strong> The public repo's <code>.gitignore</code> blocks the entire <code>modules/</code> folder except files named <code>sample-*.md</code>. Even if you accidentally run <code>git add .</code> in the public folder, your real modules will never be committed.</div>
<div class="warn-box" style="margin-top:10px">⚠️ <strong>You are the bridge between repos.</strong> Shared files like <code>build.py</code> and <code>template.html</code> are not automatically synced between the two. When you update one, manually copy it to the other folder and commit both separately.</div>
<!-- /SECTION -->

<!-- SECTION id="gh-daily" icon="🔄" color="gold" title="Daily Workflow" num="4" -->
<p style="font-size:.87rem;color:#555;margin-bottom:13px;">The private repo is updated every work session. The public repo only when something showcase-relevant changes. Both use the same three commands.</p>
<div class="def-box" style="background:linear-gradient(135deg,#fef9ec,#fef3c7);border-left-color:var(--c-gold-s);">
  <div class="def-lbl" style="color:var(--c-gold-s)">The Three Commands — Every Session</div>
  <p><code>git add .</code> — stages all changed files for the next commit<br><code>git commit -m "brief description"</code> — saves a snapshot with a message<br><code>git push</code> — sends the snapshot to GitHub</p>
</div>
<div class="g2" style="margin-top:12px">
  <div class="card-g cg-lead">
    <h4 class="clr-go">📝 Good commit messages</h4>
    <ul>
      <li><code>add web-l3 css fundamentals</code></li>
      <li><code>fix sidebar scroll on mobile</code></li>
      <li><code>update flashcards in py-l2</code></li>
      <li><code>rebuild after template change</code></li>
    </ul>
    <p style="font-size:.8rem;color:#555;margin-top:8px;">Short, specific, present tense. Tells you what changed without opening the files.</p>
  </div>
  <div class="card-g cg-near">
    <h4 class="clr-go">⏰ When to commit</h4>
    <p>Commit after each meaningful unit of work — adding a module, fixing a bug, updating a section. Do not wait until the end of the week. Frequent commits = finer-grained history = easier recovery if something goes wrong.</p>
  </div>
</div>
<!-- /SECTION -->

<!-- SECTION id="gh-sync" icon="📱" color="slate" title="Syncing Across Devices" num="5" -->
<p style="font-size:.87rem;color:#555;margin-bottom:13px;">Before starting work on any device, pull the latest changes. After finishing, push. That is the entire sync routine.</p>
<div class="steps">
  <div class="step"><div class="step-num">1</div><div class="step-body"><h5>Start of session — pull first</h5><p><code>cd path\to\project</code><br><code>git pull</code><br>This fetches and applies the latest commits from GitHub. Your files are now current. Then work as normal.</p></div></div>
  <div class="step"><div class="step-num">2</div><div class="step-body"><h5>End of session — push</h5><p><code>git add .</code><br><code>git commit -m "description"</code><br><code>git push</code><br>GitHub now holds your latest work, ready to pull on any other device.</p></div></div>
</div>
<div class="warn-box" style="margin-top:12px">⚠️ <strong>If you forget to pull first:</strong> You will get a rejection error when you try to push — Git detects that the remote has changes your local copy does not have. Fix it with:<br><code>git pull --rebase</code><br><code>git push</code><br>This pulls the remote changes and replays your local commits on top, then pushes the combined result.</div>
<div class="info-box" style="margin-top:10px">ℹ️ <strong>First time on a new device:</strong> Clone the repo instead of initialising a new one:<br><code>git clone https://github.com/username/repo-name.git</code><br>This creates a local copy with the remote already configured — no need to run <code>git remote add origin</code> again.</div>
<!-- /SECTION -->


<!-- MINDMAP -->

<svg viewBox="0 0 1000 500" xmlns="http://www.w3.org/2000/svg" aria-label="Guide 2 mindmap — GitHub Setup and Device Syncing">
  <path d="M408 245 C370 228,332 168,296 118" fill="none" stroke="#4a80cc" stroke-width="4" stroke-linecap="round"/>
  <path d="M408 252 C372 262,334 300,296 322" fill="none" stroke="#2d7a5f" stroke-width="4" stroke-linecap="round"/>
  <path d="M408 260 C374 278,336 388,298 432" fill="none" stroke="#5a3a8a" stroke-width="4" stroke-linecap="round"/>
  <path d="M572 245 C608 226,640 164,666 114" fill="none" stroke="#b45309" stroke-width="4" stroke-linecap="round"/>
  <path d="M572 260 C606 278,640 386,666 430" fill="none" stroke="#3a5068" stroke-width="4" stroke-linecap="round"/>
  <path d="M288 112 C246 104,200 96,154 90"  fill="none" stroke="#4a80cc" stroke-width="2" stroke-linecap="round"/>
  <path d="M288 118 C246 118,200 118,154 118" fill="none" stroke="#4a80cc" stroke-width="2" stroke-linecap="round"/>
  <path d="M288 316 C246 308,200 300,154 294" fill="none" stroke="#2d7a5f" stroke-width="2" stroke-linecap="round"/>
  <path d="M288 322 C246 322,200 322,154 322" fill="none" stroke="#2d7a5f" stroke-width="2" stroke-linecap="round"/>
  <path d="M836 246 C858 234,876 218,886 204" fill="none" stroke="#b45309" stroke-width="2" stroke-linecap="round"/>
  <path d="M836 254 C858 248,876 244,886 242" fill="none" stroke="#b45309" stroke-width="2" stroke-linecap="round"/>
  <rect x="406" y="226" width="168" height="52" rx="8" fill="#7a7a8e"/>
  <text x="490" y="248" text-anchor="middle" fill="white" font-family="Arial,sans-serif" font-size="12" font-weight="600">GitHub Setup</text>
  <text x="490" y="266" text-anchor="middle" fill="white" font-family="Arial,sans-serif" font-size="12" font-weight="600">&amp; Device Syncing</text>
  <g class="mm-node" onclick="goSec('gh-what','sample-git')" onmouseenter="showTip('Git &amp; GitHub Concepts','Git = local version control. GitHub = cloud storage &amp; sync. Commit = snapshot. Push/Pull = sync.')" onmouseleave="hideTip()">
    <rect x="74" y="102" width="216" height="30" rx="5" fill="rgba(74,128,204,.09)"/>
    <text x="284" y="122" text-anchor="end" fill="#4a80cc" font-family="Arial,sans-serif" font-size="12.5" font-weight="700">Git &amp; GitHub Concepts</text>
  </g>
  <g class="mm-node" onclick="goSec('gh-what','sample-git')" onmouseenter="showTip('Git &amp; GitHub Concepts','Git runs locally. GitHub is the remote. .gitignore hides files from Git entirely.')" onmouseleave="hideTip()"><text x="150" y="93"  text-anchor="end" fill="#4a80cc" font-family="Arial,sans-serif" font-size="11">Repo · commit · push · pull</text></g>
  <g class="mm-node" onclick="goSec('gh-what','sample-git')" onmouseenter="showTip('Git &amp; GitHub Concepts','.gitignore blocks files permanently — even git add . cannot commit them.')" onmouseleave="hideTip()"><text x="150" y="122" text-anchor="end" fill="#4a80cc" font-family="Arial,sans-serif" font-size="11">.gitignore safety net</text></g>
  <g class="mm-node" onclick="goSec('gh-setup','sample-git')" onmouseenter="showTip('One-Time Setup','Install Git. Set identity. Create repos on GitHub. git init + remote add + push -u origin main.')" onmouseleave="hideTip()">
    <rect x="68" y="306" width="222" height="30" rx="5" fill="rgba(45,122,95,.09)"/>
    <text x="284" y="326" text-anchor="end" fill="#2d7a5f" font-family="Arial,sans-serif" font-size="12.5" font-weight="700">One-Time Setup</text>
  </g>
  <g class="mm-node" onclick="goSec('gh-setup','sample-git')" onmouseenter="showTip('One-Time Setup','git config --global user.name and user.email. Run on every machine you use.')" onmouseleave="hideTip()"><text x="150" y="297" text-anchor="end" fill="#2d7a5f" font-family="Arial,sans-serif" font-size="11">Install · configure identity</text></g>
  <g class="mm-node" onclick="goSec('gh-setup','sample-git')" onmouseenter="showTip('One-Time Setup','git init → add → commit → remote add origin → push -u origin main.')" onmouseleave="hideTip()"><text x="150" y="326" text-anchor="end" fill="#2d7a5f" font-family="Arial,sans-serif" font-size="11">init → commit → push -u</text></g>
  <g class="mm-node" onclick="goSec('gh-repos','sample-git')" onmouseenter="showTip('Two-Repo Strategy','Private = full project, daily sync. Public = showcase only, occasional update. You copy shared files between them.')" onmouseleave="hideTip()">
    <rect x="88" y="420" width="210" height="24" rx="4" fill="rgba(90,58,138,.09)"/>
    <text x="292" y="437" text-anchor="end" fill="#5a3a8a" font-family="Arial,sans-serif" font-size="12.5" font-weight="700">Two-Repo Strategy</text>
  </g>
  <g class="mm-node" onclick="goSec('gh-daily','sample-git')" onmouseenter="showTip('Daily Workflow','git add . → git commit -m &quot;message&quot; → git push. Every session, private repo.')" onmouseleave="hideTip()">
    <rect x="664" y="100" width="188" height="30" rx="4" fill="rgba(180,83,9,.09)"/>
    <text x="668" y="120" text-anchor="start" fill="#b45309" font-family="Arial,sans-serif" font-size="12.5" font-weight="700">Daily Workflow</text>
  </g>
  <g class="mm-node" onclick="goSec('gh-daily','sample-git')" onmouseenter="showTip('Daily Workflow','add → commit → push. Commit after each meaningful unit of work.')" onmouseleave="hideTip()"><text x="890" y="104" text-anchor="start" fill="#b45309" font-family="Arial,sans-serif" font-size="11">add · commit · push</text></g>
  <g class="mm-node" onclick="goSec('gh-daily','sample-git')" onmouseenter="showTip('Daily Workflow','Good commit messages: short, specific, present tense.')" onmouseleave="hideTip()"><text x="890" y="130" text-anchor="start" fill="#b45309" font-family="Arial,sans-serif" font-size="11">Commit messages</text></g>
  <g class="mm-node" onclick="goSec('gh-sync','sample-git')" onmouseenter="showTip('Syncing Across Devices','Pull before starting. Push after finishing. Forgot to pull? git pull --rebase then git push.')" onmouseleave="hideTip()">
    <rect x="664" y="418" width="188" height="24" rx="4" fill="rgba(58,80,104,.09)"/>
    <text x="668" y="435" text-anchor="start" fill="#3a5068" font-family="Arial,sans-serif" font-size="12.5" font-weight="700">Syncing Across Devices</text>
  </g>
</svg>


<!-- FLASHCARDS -->

<div class="fc-sec">
  <div class="fc-hd">🐙 Git & GitHub Essentials</div>
  <div class="fc-grid">
    <div class="flip-card" onclick="this.classList.toggle('flipped')"><div class="flip-in"><div class="fc-f"><div class="fc-lbl">Distinction</div><div class="fc-q">What is the difference between Git and GitHub?</div><div class="fc-tip">Tap to reveal ↗</div></div><div class="fc-b"><div class="fc-a"><strong>Git</strong> is version control software that runs locally on your machine — it tracks file changes and maintains history.<br><br><strong>GitHub</strong> is a cloud platform that stores Git repositories remotely — it provides backup, sharing, and the sync point between multiple devices.</div></div></div></div>
    <div class="flip-card" onclick="this.classList.toggle('flipped')"><div class="flip-in"><div class="fc-f"><div class="fc-lbl">Concept</div><div class="fc-q">What does .gitignore do, and why is it the safety net for the public repo?</div><div class="fc-tip">Tap to reveal ↗</div></div><div class="fc-b"><div class="fc-a"><code>.gitignore</code> lists files and folders that Git will <strong>never track</strong>. Even <code>git add .</code> cannot commit them.<br><br>In the public repo, it blocks the entire <code>modules/</code> folder except <code>sample-*.md</code> files — ensuring real personal content can never accidentally be pushed.</div></div></div></div>
    <div class="flip-card" onclick="this.classList.toggle('flipped')"><div class="flip-in"><div class="fc-f"><div class="fc-lbl">Apply</div><div class="fc-q">What are the three commands for every daily work session, and in what order?</div><div class="fc-tip">Tap to reveal ↗</div></div><div class="fc-b"><div class="fc-a"><strong>1.</strong> <code>git add .</code> — stage all changes<br><strong>2.</strong> <code>git commit -m "message"</code> — save a snapshot<br><strong>3.</strong> <code>git push</code> — send to GitHub<br><br>Run these at the end of every work session in the private repo.</div></div></div></div>
    <div class="flip-card" onclick="this.classList.toggle('flipped')"><div class="flip-in"><div class="fc-f"><div class="fc-lbl">Key Rule</div><div class="fc-q">You forgot to pull before working on Device B. Now git push is rejected. What do you do?</div><div class="fc-tip">Tap to reveal ↗</div></div><div class="fc-b"><div class="fc-a">Run:<br><code>git pull --rebase</code><br><code>git push</code><br><br><code>--rebase</code> fetches the remote changes and replays your local commits on top of them, then push sends the combined result. Works cleanly as long as you have not edited the same file on two devices simultaneously.</div></div></div></div>
  </div>
</div>
