# Tool ideas — Aura video production

> Living list of **small tools** (custom or free online) that speed up scripting → render → publish.  
> Status: **idea** · **trying** · **using** · **skipped**  
> First project: Aura design video (10–12 min). Reuse patterns for CelestiaVR, MockPad, etc.

---

## Custom tools (this repo)

| Tool | Path | Status | Problem it solves |
|------|------|--------|-------------------|
| **Script workspace** | `tools/serve.py` + `tools/index.html` | **using** | SCRIPT + SCENE-PLAN side-by-side, chapter jump, edit + save |
| **VO prompter + pace trainer** | `tools/prompter.html` + `parse_script.py` | **using** | One line at a time, ring timer per statement, scroll teleprompter, .txt export |
| Manim toolkit | `aura_manim/` | idea | Reusable theme, code panels, pipeline diagrams |
| VO word-count script | — | idea | Parse SCRIPT.md narration column → per-chapter word count vs target |
| Chapter timestamp calculator | — | idea | Given VO duration per ch, emit YouTube description timestamps |
| `build_60s.py`-style assembler | design-video | idea | FFmpeg concat Manim + Unity + B-roll per SCENE-PLAN |
| Music bed helper | `../manim/add_music.py` | **using** (60s) | Pixabay documentary mix under VO at fixed volume |

### Script workspace — run

```bash
python Aura/design-video/tools/serve.py
# workspace → http://127.0.0.1:8765/
# prompter  → http://127.0.0.1:8765/prompter.html
```

**Prompter modes:**
- **Pace trainer** — one narration line, ring timer + dot progress, on-screen/visual hints, WPM target (default 140)
- **Teleprompter** — scrolling text for recording; **Export .txt** for phone apps

**Pace keys:** `Space` next · `Shift+Space` prev · `P` auto-advance when timer completes

---

## Free / online tools (by pipeline phase)

### Phase 0 — Story & honesty

| Tool | URL / note | Status | Use for Aura |
|------|------------|--------|--------------|
| Markdown in repo | git | **using** | HACKATHON-STORY.md source of truth |
| Script workspace | local HTML | **using** | Read script + scene plan together |

### Phase 1 — Script & beat sheet

| Tool | URL / note | Status | Use for Aura |
|------|------------|--------|--------------|
| **Teleprompter apps** | Teleprompter Lite, PromptSmart (iOS) | **using** (via export) | Import `aura-teleprompter.txt` from prompter |
| **Read-aloud pace trainer** | `tools/prompter.html` | **using** | Ring timer + one line per beat from SCRIPT.md |
| **Hemingway Editor** | hemingwayapp.com | idea | Trim narration bloat (free web, limited) |
| Google Docs / Notion | — | skipped | Prefer markdown in git + script workspace |

### Phase 2 — Code snippets

| Tool | Status | Use for Aura |
|------|--------|--------------|
| Minimal copy into `code_snippets/` | idea | One concept per file, header with repo path + lines |
| Xcode → export selection | **using** | Ground-truth Swift on screen |

### Phase 3–4 — Manim / Unity visuals

| Tool | URL / note | Status | Use for Aura |
|------|------------|--------|--------------|
| Manim CE | docs.manim.community | **using** | 2D pipelines, code panels |
| `manim -ql` preview | local | **using** | Fast iteration before final render |
| Unity Recorder | Unity package | idea | 1080p Unity viz clips (ch 5, 7) |
| OBS Studio | obsproject.com | idea | Unity/game capture fallback (free) |

### Phase 5 — VO

| Tool | Status | Use for Aura |
|------|--------|--------------|
| Quiet room + phone voice memos | idea | Punch-in friendly |
| Audacity | **using** (optional) | Normalize VO, noise reduction (free) |
| Descript / Adobe Podcast Enhance | idea | AI cleanup if room is noisy (freemium) |

### Phase 6 — Assembly & publish

| Tool | URL / note | Status | Use for Aura |
|------|------------|--------|--------------|
| **DaVinci Resolve** | blackmagicdesign.com | **using** | Manim + Unity + B-roll + VO + chapters |
| FFmpeg | local | **using** (60s) | Clip extract, concat, music mux |
| `add_music.py` | `Aura/manim/` | **using** | Documentary bed under VO |
| YouTube Studio | — | **using** | Chapters from SCRIPT timestamps, Not Made for Kids |
| yt-dlp | — | **using** (60s) | Re-download own demo for re-cut |

### Phase 7 — Learning & docs

| Tool | Status | Use for Aura |
|------|--------|--------------|
| LEARNING.md | **using** | Manim/Unity concept log as we code |
| journal.md | **using** | What worked / failed per render session |

---

## Theories to test (hypotheses)

| Hypothesis | Test | Metric |
|------------|------|--------|
| Side-by-side script + scene plan reduces edit confusion | Script workspace for ch 3 draft | Fewer mismatched timestamps |
| Split mode (edit + preview) catches broken markdown tables before save | Use Split when editing SCRIPT | No broken table renders |
| Chapter jump nav beats Ctrl+F across two files | Navigate ch 7 HUD section | Time to find paired beats |
| VO word-count script keeps runtime under 12 min | Auto-count narration column only | ±10% of SCENE-PLAN target |
| One Manim scene file per chapter matches Resolve timeline | sceneN.py ↔ ch N | Easier re-render on script change |

---

## Backlog — small tools worth building next

1. ~~**`tools/export-teleprompter.md`**~~ → built into prompter **Export .txt**
2. **`tools/wordcount.py`** — read SCRIPT.md, count words in narration cells per chapter, compare to SCENE-PLAN targets, print overrun warnings.
3. **`tools/chapters.txt`** — emit YouTube chapter block from SCENE-PLAN master timeline table.
4. **Optional third pane** in script workspace for HACKATHON-STORY.md (tab or 3-column on wide screens).

---

## Add new entries here

When you find or build something useful:

```markdown
| **Name** | path or URL | status | one-line why |
```

Keep entries honest — **skipped** with reason is as valuable as **using**.
