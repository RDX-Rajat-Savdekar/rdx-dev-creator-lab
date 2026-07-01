# Aura — video production journal

> **Purpose:** Record how each video was made — process, mistakes, final decisions — so future sessions (and agents) don’t re-learn the same lessons.
>
> **Scope:** Portfolio videos for **Aura** living under `Aura/`. One section per deliverable.
>
> **Related:** `project-sources/projects/aura-visionos/COMPLETENESS.md` · `60s-beat-sheet.md` · `project-sources/VIDEO-PRODUCTION-LEARNING.md`

---

## How to use this journal

After each video ship (or major draft):

1. Add a dated entry under **Entries** (copy the template at the bottom).
2. Log **what we tried**, **what went wrong**, **what we shipped**.
3. Point to **files** (scripts, outputs, licenses) — not just chat memory.
4. Update `COMPLETENESS.md` checklist row + session log.

---

## Entries

### 2026-07-01 — 60s recruiter clip (`aura-60s-with-music.mp4`)

**Deliverable:** 60s demo for recruiters (LinkedIn / README hook)  
**Status:** Draft ready for YouTube upload (not yet live)  
**Final file:** [`output/aura-60s-with-music.mp4`](output/aura-60s-with-music.mp4)  
**Muted assembly (no music):** [`output/aura-60s-rough-assembly.mp4`](output/aura-60s-rough-assembly.mp4)

#### Goal

Prove Aura works in under 65s: on-device captions, sound classification, EN→JA locale switch, one fact-backed outcome — without re-recording on Vision Pro.

#### Constraints we had

| Constraint | Impact |
|------------|--------|
| No Vision Pro available | Re-cut existing YouTube demo only |
| Teammates presented full demo (Namratha + Fardeen on camera) | Skip intro pitch; mute all source audio; Rajat story via Manim text only |
| Hackathon prototype (`facts/aura.json`) | No custom ML / latency / production-scale claims |
| Solo code, 3-person team | Credit teammates in full demo link; 60s is screen + Rajat-authored overlays |

#### Process we followed (final pipeline)

```
1. Audit (COMPLETENESS.md + fact record)
2. Beat sheet (60s-beat-sheet.md) — Option A: text + footage, no VO
3. Source: AURA-Vision-pro-app_Media_HbW9F2zjmLQ_001_720p.mp4
4. Transcript with timestamps → ffmpeg clips D1–D6 in clips/
5. Manim text (aura_cards.py): full-screen cards + transparent lower-thirds
6. build_60s.py: trim → overlay → concat → rough assembly (~56 s, muted)
7. Music: Pixabay track → add_music.py → aura-60s-with-music.mp4
8. (Pending) YouTube upload + description + license certificate if Content ID claims
```

**Automation entry points:**

```bash
# Full rebuild (Manim + assembly)
.venv/bin/python Aura/manim/build_60s.py
.venv/bin/python Aura/manim/build_60s.py --skip-render   # ffmpeg only

# Music only
.venv/bin/python Aura/manim/add_music.py \
  --music Aura/music/leberch-documentary-517370.mp3 \
  --volume 0.10
```

#### Timeline / assembly (final)

| Order | Duration | Content | Source |
|-------|----------|---------|--------|
| Hook card | 3 s | "Can't hear the room?" | Manim `HookCard` |
| Problem card | 4 s | zero cloud · on-device | Manim `ProblemCard` |
| Product | 3 s | D1 trim + "Aura · visionOS" | Clip + `ProductLowerThird` |
| Speech | 10 s | D1+D2 + transcription label | Clips + `SpeechLowerThird` |
| Sound | 12 s | D3+D4+D5 montage | Clips + `SoundLowerThird` |
| Pipeline card | 4 s | Speech + SoundAnalysis | Manim `PipelineCard` |
| Locale | 10 s | D6 trim + JA switch | Clip + `LocaleLowerThird` |
| Proof card | 6 s | 2nd place · 24 h · solo code | Manim `ProofCard` |
| CTA card | 6 s | GitHub URL | Manim `CTACard` |
| **Total** | **~56 s** | | |

**Source clip in/out (from YouTube transcript):**

| Clip | Timecode |
|------|----------|
| D1 live EN | 01:06 → 01:20 |
| D2 second speaker | 01:20 → 01:23 |
| D3 whisper | 01:23 → 01:30 |
| D4 siren / emergency vehicle | 01:30 → 01:46 |
| D5 clapping | 01:48 → 02:02 |
| D6 Japanese | 02:03 → 02:26 |

Skipped: `00:00–01:00` teammate intro.

#### Mistakes & dead ends

| Mistake / wrong turn | Why it hurt | Fix we landed on |
|----------------------|-------------|------------------|
| Assumed re-record on Vision Pro | Device not available | Re-cut local copy of YouTube upload |
| Beat sheet with empty SRC timestamps | Blocked editing | User pasted full transcript with timestamps → ffmpeg clips |
| Plan: manual text in iMovie/Resolve | Hard to keep typography consistent | **Manim** for all text (`aura_cards.py`) — 3b1b-style programmatic titles |
| **NCS music** (NoCopyrightSounds) | Too punchy / EDM-compressed for text-heavy accessibility clip | **Pixabay documentary ambient** (solo piano) |
| Leaving teammate VO on a "solo portfolio" cut | Misleading authorship on LinkedIn | **Mute** source audio entirely |
| Considering spatial HUD as hero footage | `ImmersiveView` unwired in repo HEAD | Lead with **2D caption HUD** from demo (honest) |
| `uv run manim` in sandbox | `av` build failed; slow | Use **`.venv/bin/manim`** (existing Manim 0.20.1) |
| Music too loud on first audition (NCS) | Competes with on-screen text | `--volume 0.10` for Pixabay; NCS would need `0.06–0.07` |

#### Final decisions (locked for this video)

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Format | Text overlays + demo footage, **no VO** | Mute-friendly; avoids teammate voices; beginner-friendly |
| Text tool | **Manim CE** full cards + transparent lower-thirds | Reusable, matches repo’s explainer direction; not hand-keyframed in NLE |
| Build | **`build_60s.py` + ffmpeg** | Repeatable one command |
| Footage | Existing hackathon demo only | No device; content already shows EN/JA/sounds |
| Intro | **Cut** teammate pitch | Portfolio hook = product proof, not team presentation |
| Music genre | **Documentary / solo piano ambient** | Sits under text; not gaming montage |
| Music track | **Documentary** by leberch (Nikita Kondrashev), Pixabay ID 517370 | [Track URL](https://pixabay.com/music/solo-piano-documentary-517370/) |
| Music level | `--volume 0.10`, fade in 0.8 s / out 4 s | Readable text remains primary |
| Music file | `music/leberch-documentary-517370.mp3` | |
| License proof | `music/solo-piano-documentary-517370-license.txt` | Content ID registered — keep for YouTube claims |
| Honesty | Prototype, Apple Speech/SoundAnalysis, solo code | Matches `never_claim` in fact record |

#### Music — YouTube description (copy when uploading)

```
Music by Nikita Kondrashev (leberch) from Pixabay
https://pixabay.com/users/leberch-42823964/
https://pixabay.com/music/solo-piano-documentary-517370/
```

If Content ID claim appears: submit Pixabay license certificate (`solo-piano-documentary-517370-license.txt`).

#### Artifacts produced

| Path | Role |
|------|------|
| `clips/D1–D6_*.mp4` | Trimmed demo segments |
| `manim/aura_cards.py` | Manim scenes (text) |
| `manim/build_60s.py` | Assembly pipeline |
| `manim/add_music.py` | Music mix |
| `music/MUSIC-PICKS.md` | Music sift list (NCS deprioritized) |
| `music/leberch-documentary-517370.mp3` | Bed track |
| `music/solo-piano-documentary-517370-license.txt` | Pixabay license |
| `output/aura-60s-rough-assembly.mp4` | Muted master |
| `output/aura-60s-with-music.mp4` | **Ship candidate** |

#### Still TODO before ✅ on checklist

- [ ] Upload to YouTube (unlisted OK for review)
- [ ] Paste description (repo + full demo + music credit)
- [ ] Watch on phone (muted + with captions) — recruiter skim test
- [ ] Add YouTube URL to `facts/aura.json` evidence + README when hub exists
- [ ] Optional: `--volume 0.08` if music still feels strong on phone speakers

#### Lessons for next Aura video (system design / Manim explainer)

1. **Start from fact record `architecture[]`** — one Manim scene per decision + rejected alt.
2. **Don’t use NCS** for explainers with dense text; use documentary/ambient beds.
3. **Manim for diagrams, footage for product truth** — same hybrid as this 60s.
4. **Journal before moving on** — future agent reads this + `COMPLETENESS.md`, not chat.

---

### 2026-07-01 — Design video · Chapter 0 Manim (act-by-act workflow)

**Deliverable:** System design video — Chapter 0 only (`0:00–1:05`)  
**Status:** Acts **1–3** draft ✅ · Acts 4–6 + `scene0_full.py` assembly pending  
**Supersedes:** monolith `scene0_problem_REFERENCE.py` + one-shot `scene0_problem-preview.mp4`

#### Goal

Animated Manim ch 0 (not 60s text cards): six beats from `SCRIPT.md` / `SCENE-PLAN.md`, learned and reviewed **one act at a time** before final concat.

#### Locked workflow (milestone)

```
Per act:
  1. scene0_actN.py — helpers + PLAY CHECKLIST docstring + # PLAY N comments
  2. Scene0ActNLayout — plop pieces slowly (layout review)
  3. Scene0ActN — motion (~10–15 s per act)
  4. -qk --frame_rate 60 when act approved

Shared (when act 2+ reuses visuals):
  components/team.py   — TEAM roster, team_grid (act 2), team_contribution_lane (act 3)
  components/labels.py — on_screen_label()
  icons.py + assets/icons/*.svg — tint at load; diagrams stay Manim shapes

Assembly (last):
  scene0_full.py — concat approved act motions only; no new visuals
```

**Do not** import whole previous Scene classes — import **builders** from `components/`.

#### Act status

| Act | File | Scene classes | On-screen label | Status |
|-----|------|---------------|-----------------|--------|
| 1 | `scenes/scene0_act1.py` | Layout + Motion | Situational audio gap | ✅ reviewed (room rect, SVG icons, columns) |
| 2 | `scenes/scene0_act2.py` | Layout + Motion | 24h hackathon · Oct 2025 | ✅ reviewed (clock SVG, 2×2 team grid) |
| 3 | `scenes/scene0_act3.py` | Layout + Motion | Team-built · shared code | ✅ draft (shared commits lane) |
| 4 | `scene0_act4.py` | — | Day 0: sphere POC | pending |
| 5 | `scene0_act5.py` | — | System design · prototype | pending |
| 6 | `scene0_act6.py` | — | Aura · visionOS · on-device | pending |

#### Render commands (from `Aura/design-video/aura_manim/`)

Preview (while learning):

```bash
../../.venv/bin/manim -ql scenes/scene0_act1.py Scene0Act1Layout
../../.venv/bin/manim -ql scenes/scene0_act1.py Scene0Act1
# … act2, act3 same pattern
```

Final per act (4K · 60 fps):

```bash
../../.venv/bin/manim -qk --frame_rate 60 scenes/scene0_act1.py Scene0Act1
../../.venv/bin/manim -qk --frame_rate 60 scenes/scene0_act2.py Scene0Act2
../../.venv/bin/manim -qk --frame_rate 60 scenes/scene0_act3.py Scene0Act3
```

Manim Sideview: `.vscode/settings.json` → `manim-sideview.defaultManimPath` = `${workspaceFolder}/.venv/bin/manim` (fixes bad `python/bin/manim` path).

#### Files & structure

| Path | Role |
|------|------|
| `design-video/aura_manim/theme.py` | Palette (matches 60s) |
| `design-video/aura_manim/icons.py` | `load_icon()` |
| `design-video/aura_manim/assets/icons/*.svg` | bell, alert, clock, laptop, mic, palette, … |
| `design-video/aura_manim/components/team.py` | Single TEAM roster · act 2 grid · act 3 lane |
| `design-video/aura_manim/components/labels.py` | Bottom-third labels |
| `design-video/aura_manim/review.py` | `plop()` for layout review |
| `design-video/aura_manim/scenes/scene0_act{1,2,3}.py` | One act per file |
| `design-video/aura_manim/scenes/scene0_full.py` | Assembly stub + reuse notes |
| `design-video/aura_manim/scenes/scene0_problem_REFERENCE.py` | Old 6-act monolith — do not render |
| `design-video/LEARNING.md` | Manim concepts + `# LEARN:` index |
| `.gitignore` | `**/media/`, `design-video/output/`, render caches |

#### Mistakes & fixes (ch 0 so far)

| Issue | Fix |
|-------|-----|
| Built all 6 acts in one file | **One act per file** + layout plop before motion |
| Hand-drawn bell/clock icons | **SVG** via `load_icon()` |
| Speech/sound overlap in act 1 | **Columns** — bubble above icon, `next_to` buff |
| Act 2 clock hands looked wrong | **clock.svg** + separate `24h` text |
| Act 2 role cards cramped | Fixed `CARD_W/H`, icon→label buff `0.38` |
| Act 3 “All code: Rajat” too bold | Reframed → **team-built · shared code** + shared commit lane |
| Duplicate team data act 2/3 | **`components/team.py`** single `TEAM` tuple |
| Manim Sideview path error | Workspace `.vscode/settings.json` |
| Committed render MP4s | `.gitignore` for `media/`, outputs |

#### Narrative notes (update SCRIPT when VO recorded)

- Act 3 on-screen text ≠ original SCRIPT solo-code line — VO should say team contributed to codebase.
- Act 2 shows **4** role cards; SCRIPT says “three-person team” — align on read-aloud.
- Honesty unchanged: prototype, no custom ML / latency / production scale.

#### Still TODO (ch 0)

- [ ] Act 4 — sphere POC (`"red"` → color, loud → scale)
- [ ] Act 5 — prototype disclaimer + 2 s black hold for Resolve `clips/D1`
- [ ] Act 6 — Vision Pro silhouette + dual pipeline stub
- [ ] `scene0_full.py` — wire acts 1–6 after each approved
- [ ] Read-aloud VO — trim `self.wait()` per act
- [ ] Optional: act 2→3 `Transform(team_grid(), team_contribution_lane())` for continuity
- [ ] Update `SCRIPT.md` act 3 (+ act 2 team count) to match visuals

---

### 2026-07-01 — Design video ch 0 monolith (superseded)

**Status:** ⚠️ Superseded by act-by-act workflow above  
**Archive:** [`scenes/scene0_problem_REFERENCE.py`](design-video/aura_manim/scenes/scene0_problem_REFERENCE.py) · [`output/scene0_problem-preview.mp4`](design-video/output/scene0_problem-preview.mp4) (65.1 s one-shot)

First pass rendered all six beats in `Scene0Problem` before layout review workflow existed. Keep for reference only.

---

## Entry template (copy for next video)

```markdown
### YYYY-MM-DD — [Video title / deliverable]

**Deliverable:**  
**Status:**  
**Final file:**  

#### Goal


#### Constraints


#### Process (steps)


#### Mistakes & dead ends

| Mistake | Why | Fix |

#### Final decisions

| Decision | Choice | Rationale |

#### Artifacts


#### Still TODO

```

---

*Last updated: 2026-07-01 (ch 0 acts 1–3 · components/ workflow)*
