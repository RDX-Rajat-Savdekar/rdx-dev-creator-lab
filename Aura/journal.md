# Aura — video production journal

> **Purpose:** Record how each video was made — process, mistakes, final decisions — so future sessions (and agents) don’t re-learn the same lessons.
>
> **Scope:** **Aura** portfolio videos only. Generic process for all resume projects: [`docs/video-production/`](../docs/video-production/README.md)
>
> **Reusable process (all projects):** [`docs/video-production/`](../docs/video-production/README.md)  
> **Related:** `project-sources/projects/aura-visionos/COMPLETENESS.md` · `60s-beat-sheet.md` · `project-sources/VIDEO-PRODUCTION-LEARNING.md`

---

## How to use this journal

After each video ship (or major draft):

1. Add a dated entry under **Entries** (copy the template at the bottom).
2. Log **what we tried**, **what went wrong**, **what we shipped**.
3. Point to **files** (scripts, outputs, licenses) — not just chat memory.
4. Update `COMPLETENESS.md` checklist row + session log when applicable.
5. If the process changed materially, update [`docs/video-production/`](../docs/video-production/README.md) — not only this journal.

---

## Entries

### 2026-07-03 — Design video · Chapters 0–9 complete + VO mux pipeline (shipped)

**Deliverable:** Full system design video with Rajat VO, chapter banners, no Resolve  
**Status:** ✅ Draft complete — `aura_design_video_2160p60_vo.mp4`  
**Final file:** [`design-video/output/aura_design_video_2160p60_vo.mp4`](design-video/output/aura_design_video_2160p60_vo.mp4) (**553.5 s** · ~9.2 min)  
**Playbook:** [`docs/video-production/`](../docs/video-production/README.md) · Aura entry [`projects/aura-design-video.md`](../docs/video-production/projects/aura-design-video.md)

#### Goal

10-chapter Manim explainer (ch 0–9): hackathon story, on-device architecture, segmentation, HUD, scale, outro — with **phone-recorded VO** synced to 4K acts without manual NLE.

#### What we shipped

| Chapter | YouTube chapter | Acts | VO export |
|---------|-----------------|------|-----------|
| 0 | The problem | 6 | `scene0_chapter0_2160p60_vo.mp4` |
| 1 | On-device only | 5 | `scene1_chapter1_2160p60_vo.mp4` |
| 2 | Build vs train | 6 | `scene2_chapter2_2160p60_vo.mp4` |
| 3 | One tap, dual pipeline | 6 | `scene3_chapter3_2160p60_vo.mp4` |
| 4 | Segmentation | 4 | `scene4_chapter4_2160p60_vo.mp4` |
| 5 | Texture HUD vs 90 Hz | 4 | `scene5_chapter5_2160p60_vo.mp4` |
| 6 | MainActor bridge | 3 | `scene6_chapter6_2160p60_vo.mp4` |
| 7 | Iron Man HUD | 6 | `scene7_chapter7_2160p60_vo.mp4` |
| 8 | Scale | 3 | `scene8_chapter8_2160p60_vo.mp4` |
| 9 | Outro | 3 | `scene9_chapter9_2160p60_vo.mp4` |

Ch 6–9 built last: `scale.py`, `outro.py`, learnings in `LEARNING.md` / `PROCESS-REVIEW.md`. Video ends at ch 9 (no ch 10).

#### Final pipeline (locked — use playbook for details)

```
MANIM (act-by-act)
  vo/sceneN.md PLAY CHECKLIST → sceneN_actM.py → -ql layout QA → -qk 4K acts
  → ffmpeg concat → sceneN_chapterN_2160p60.mp4

VO RECORD (phone)
  build_teleprompter.py → serve.py + prompter.html (Record tab + synced act video)
  → audio_record_aura/{chapter}{act}.m4a  (46 clips)

AUDIO CLEAN + TRANSCRIBE
  process_vo_audio.py  (silence trim, loudnorm, 1s pad)
  → --transcribe (Whisper in design-video/.venv) → vo_clips.json

FINAL MUX (no Resolve)
  mux_chapter_vo.py --all --banner
    · vo_video_fit: strip FadeOut tail, HOLD last visible frame to WAV length
    · chapter_banners: 2s title card per chapter
  → build_full_film.py → aura_design_video_2160p60_vo.mp4
```

**One-command refresh after re-recording VO:**

```bash
Aura/design-video/.venv/bin/python Aura/design-video/tools/process_vo_audio.py --skip-process --transcribe
Aura/design-video/.venv/bin/python Aura/design-video/tools/mux_chapter_vo.py --all --banner
Aura/design-video/.venv/bin/python Aura/design-video/tools/build_full_film.py
```

#### Journey / mistakes (this sprint)

| Phase | What happened | Fix |
|-------|---------------|-----|
| VO alignment | Compared full WAV length; ~2s pad skew; suggested Resolve | Whisper `speech_end`; automated ffmpeg mux |
| Black while speaking | `tpad` extended **last frame after FadeOut** (= black) | `vo_video_fit.py` — content end before fade; freeze last pane |
| Blank tail after b-roll | Acts with `play_broll` + trailing `scene.wait` | Parser holds last b-roll frame, strips blank wait |
| Resolve unknown | User can't use NLE | `mux_chapter_vo.py` + `build_full_film.py` |
| Chapter boundaries | Viewer needs context between chapters | `chapter_banners.py` — 2s card from `vo/sceneN.md` YouTube title |
| ch2 inbox audio | User unsure if Core ML beat was recorded / mislabeled | Transcript verified: `22.m4a` = act2 inbox, `23.m4a` = act3 train path ✅ |
| Stale docs | `inbox.py` said "act 3" | Fixed to act 2; journal + playbook |

#### Tools added this sprint

| Tool | Role |
|------|------|
| `process_vo_audio.py` | Clean phone VO + optional Whisper |
| `sync_vo_alignment.py` | hold_extensions / wait suggestions from transcripts |
| `mux_chapter_vo.py` | Per-act VO mux + optional banner |
| `vo_video_fit.py` | Hold-frame logic (strip black tails) |
| `chapter_banners.py` | 2s chapter title cards |
| `build_full_film.py` | Concat all `_vo` chapters |
| `build_teleprompter.py` | TELEPROMPTER.md + JSON |
| `serve.py` + `prompter.html` | LAN teleprompter + Record tab |
| `extend_act_holds.py` | Optional ffmpeg hold extension (pre-mux path) |

#### Artifacts

| Path | Role |
|------|------|
| `docs/video-production/` | **Repo-wide portfolio playbook** |
| `playbook/` | Redirect → docs/video-production |
| `vo/vo_clips.json` | 46 clips · durations · transcripts |
| `media/audio/processed/chN_actM.wav` | Cleaned VO |
| `media/banners/chN_2160p60.mp4` | Chapter intros |
| `output/aura_design_video_2160p60_vo.mp4` | **Ship candidate** |

#### Still TODO (optional)

- [ ] YouTube upload + chapter timestamps in description
- [ ] Spot-check acts flagged in `vo/AUDIO-ALIGNMENT.md` (e.g. ch3 act6 short speech)
- [ ] Re-render acts with `adjust_waits.py` if hold-frame freeze feels too static in places
- [ ] Background music pass (not in scope yet — video is VO-only)

#### Lessons

1. **Never extend video without checking what's on the last frame** — FadeOut makes black.
2. **Whisper is for speech bounds**, not just captions — enables automated sync.
3. **Playbook + journal** — agents start at `playbook/README.md`, not chat history.
4. **Per-act VO files** + ffmpeg mux beats per-sentence Resolve alignment for this format.

---

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

**Deliverable:** System design video — Chapter 0 (`0:00–1:05`)  
**Status:** Acts **1–6** draft ✅ · **2160p60 concat** ✅ · VO draft in [`vo/scene0.md`](design-video/vo/scene0.md)  
**Concat:** [`design-video/output/scene0_chapter0_2160p60.mp4`](design-video/output/scene0_chapter0_2160p60.mp4) (~1:14 measured — trim waits after read-aloud)  
**Supersedes:** monolith `scene0_problem_REFERENCE.py` + one-shot `scene0_problem-preview.mp4`

#### Goal

Animated Manim ch 0 (not 60s text cards): six beats from `SCRIPT.md` / `SCENE-PLAN.md`, learned and reviewed **one act at a time** before final concat.

#### Locked workflow (milestone — still the standard for ch 1+)

```
Plan (vo/sceneN.md PLAY CHECKLISTS) → user edits → generate all acts in one pass

Per act:
  1. sceneN_actM.py — helpers + PLAY CHECKLIST docstring + play_actM(scene, state)
  2. SceneNActMLayout — plop pieces slowly (layout review)
  3. SceneNActM — motion (standalone render; fades at end)
  4. -qk --frame_rate 60 when act approved

Shared builders (components/ + toolkit modules):
  components/team.py, labels.py, device.py, locale_picker.py
  icons.py + assets/icons/*.svg
  rejected.py, code_panel.py, broll.py

Assembly (two modes):
  sceneN_full.py — play_act chain at -ql for fast iteration (state['chain']=True for continuity)
  ffmpeg concat — per-act 2160p60 MP4s with ABSOLUTE paths in concat.txt (see mistakes)
```

**Do not** import whole previous Scene classes — import **`play_actM`** and **builders**.

#### Act status

| Act | File | On-screen label | Status |
|-----|------|-----------------|--------|
| 1 | `scene0_act1.py` | Situational audio gap | ✅ reviewed |
| 2 | `scene0_act2.py` | 24h hackathon · Oct 2025 | ✅ reviewed |
| 3 | `scene0_act3.py` | Team-built · shared code | ✅ draft |
| 4 | `scene0_act4.py` | Day 0: sphere POC | ✅ draft (sphere pulsates 3×) |
| 5 | `scene0_act5.py` | System design · prototype + D1 B-roll | ✅ draft (4 s embedded clip) |
| 6 | `scene0_act6.py` | Aura · visionOS · on-device | ✅ draft |

#### Render commands (from repo root `.venv`)

Preview:

```bash
cd Aura/design-video/aura_manim
../../../.venv/bin/manim -ql scenes/scene0_actN.py Scene0ActNLayout
../../../.venv/bin/manim -ql scenes/scene0_full.py Scene0Full    # whole ch while iterating
```

Final per act + concat:

```bash
../../../.venv/bin/manim -qk --frame_rate 60 scenes/scene0_actN.py Scene0ActN
# concat → design-video/output/scene0_chapter0_2160p60.mp4 (see vo/VO-WORKFLOW.md)
```

#### Files & structure (ch 0)

| Path | Role |
|------|------|
| `design-video/aura_manim/scenes/scene0_act{1…6}.py` | One act per file + `play_actN()` |
| `design-video/aura_manim/scenes/scene0_full.py` | Full chapter via `play_act` chain |
| `design-video/aura_manim/broll.py` | Embed `clips/D*.mp4` via PyAV + `ImageMobject` frames |
| `design-video/aura_manim/components/team.py` | TEAM roster · grid · merge lane |
| `design-video/vo/scene0.md` | Measured timestamps + VO draft |
| `design-video/vo/build_act_timestamps.py` | ffprobe act durations → markdown table |
| `design-video/output/scene0_concat.txt` | ffmpeg list (**absolute paths**) |

#### Mistakes & fixes (ch 0)

| Issue | Fix |
|-------|-----|
| Built all 6 acts in one file | **One act per file** + layout plop before motion |
| Hand-drawn bell/clock icons | **SVG** via `load_icon()` |
| Act 3 “All code: Rajat” too bold | **Team-built · shared code** + merge lane |
| Act 5 Resolve placeholder only | **`broll.py`** bakes D1 in Manim (4 s flash) |
| ffmpeg concat with relative paths in `/tmp` | **Absolute paths** in `output/scene0_concat.txt` |
| `scene0_full` waited until end | Wire **`scene0_full.py` early** for iteration |
| `VideoMobject` not in Manim CE | PyAV frames → `ImageMobject` + updater; use `Group` not `VGroup` for images |

#### Still TODO (ch 0)

- [ ] Read-aloud VO — trim `self.wait()` per act (target ~1:05 vs ~1:14 today)
- [ ] Update `SCRIPT.md` act 3 line to match team-built visuals
- [ ] Record VO + Resolve assembly

---

### 2026-07-02 — Design video · Standardized pipeline + Chapter 1

**Deliverable:** Repeatable workflow for all chapters; ch 1 first full implementation  
**Status:** Ch 0 concat ✅ · Ch 1 code ✅ (layout review pending) · VO system ✅

#### What we standardized

| Layer | Convention | Where documented |
|-------|------------|------------------|
| **Planning** | PLAY CHECKLIST in `vo/sceneN.md` → user edits → **one-pass code gen** | `vo/scene1.md` (template: `vo/_TEMPLATE.md`) |
| **Acts** | `sceneN_actM.py` + `SceneNActMLayout` + `SceneNActM` + **`play_actM(scene, state)`** | `scenes/scene0_act*.py`, `scene1_act*.py` |
| **Full preview** | `sceneN_full.py` with `ENABLED_ACTS` + `state['chain']=True` for acts that share a diagram | `scene0_full.py`, `scene1_full.py` |
| **VO** | Measured timestamps from **2160p60 renders**, not SCENE-PLAN targets | `vo/sceneN.md`, `build_act_timestamps.py` |
| **Final assembly** | Per-act `-qk` → **ffmpeg concat** (`-c copy`) — faster than re-rendering `SceneNFull` at 4K | `vo/VO-WORKFLOW.md` |
| **B-roll in Manim** | `broll.play_broll()` — PyAV decode, frame updater (not Resolve-only) | `broll.py` · act 5 |
| **Swift on screen** | `code_snippets/*.swift` + `code_panel.swift_panel()` + line highlight | `code_panel.py` · ch 1 act 4 |
| **Rejected paths** | `rejected.py` — ghost `DashedLine`, `strikethrough_line`, reason chips | ch 1 acts 2–3 |
| **Icons** | MIT stroke SVGs in `assets/icons/` — e.g. `vision-pro.svg` | `icons.py` · `components/device.py` |

#### Chapter 1 shipped (code)

| Act | File | Label |
|-----|------|-------|
| 1 | `scene1_act1.py` | Decision 1: on-device only |
| 2 | `scene1_act2.py` | Temptation: cloud ASR |
| 3 | `scene1_act3.py` | Rejected: privacy + latency |
| 4 | `scene1_act4.py` | SFSpeechRecognizer + snippet |
| 5 | `scene1_act5.py` | Locale picker (7 langs) + metrics |

**New toolkit:** `components/device.py`, `components/locale_picker.py`, `rejected.py`, `code_panel.py`, `code_snippets/on_device_speech.swift`

**Ch 1 continuity:** acts 1→3 share device on screen via `state['chain']` in `scene1_full.py`.

#### Render entry points

```bash
cd Aura/design-video/aura_manim
../../../.venv/bin/manim -ql scenes/scene1_actN.py Scene1ActNLayout   # layout
../../../.venv/bin/manim -ql scenes/scene1_full.py Scene1Full         # whole ch
python Aura/design-video/vo/build_act_timestamps.py --chapter 1 --markdown  # after -qk
```

#### Still TODO

- [ ] Ch 1 layout review (`Scene1ActNLayout` plops)
- [ ] Ch 1 `-qk` per act + concat + `vo/scene1.md` VO draft
- [ ] Ch 2 planning (`vo/scene2.md` from `_TEMPLATE.md`)
- [ ] `pipeline.py`, `thread_lane.py` — before ch 3 (not built yet)

#### Lessons

1. **Plan in `vo/sceneN.md` before code** — avoids rework; user edits PLAY CHECKLISTS, then one `go`.
2. **Two assembly paths:** `SceneNFull` for timing iteration; **ffmpeg concat** for final 4K when acts are locked.
3. **SCRIPT.md lags visuals** — `vo/sceneN.md` is VO source of truth after first render.
4. **Journal + LEARNING + vo/** — agents read files, not chat.

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

*Last updated: 2026-07-03 (design video ch 0–9 + VO mux shipped · playbook/ formalized)*
