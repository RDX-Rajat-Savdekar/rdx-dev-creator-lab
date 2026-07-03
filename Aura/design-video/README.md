# Aura — system design video (10–12 min)

> **Status:** **ch 0–9 shipped** (VO mux draft) · [`output/aura_design_video_2160p60_vo.mp4`](output/aura_design_video_2160p60_vo.mp4)  
> **Target:** 10–12 min · **VO:** Rajat (phone + ffmpeg mux)  
> **Visuals:** **Manim** (2D pipelines, code) + **Unity viz** (3D spatial) + Swift snippets + demo B-roll  
> **Process playbook (all projects):** [`../../docs/video-production/README.md`](../../docs/video-production/README.md)  
> **Learning:** [`LEARNING.md`](LEARNING.md) + `# LEARN:` in code · **Journal:** [`../journal.md`](../journal.md)  
> **VO / timestamps:** [`vo/VO-WORKFLOW.md`](vo/VO-WORKFLOW.md) · [`vo/AUDIO-WORKFLOW.md`](vo/AUDIO-WORKFLOW.md)  
> **Ch 6+ standards:** [`MANIM-STANDARDS.md`](MANIM-STANDARDS.md) · [`AGENTS.md`](AGENTS.md) · [`PROCESS-REVIEW.md`](PROCESS-REVIEW.md)

---

## Process (best practice for this repo)

Follow this order — same spirit as 3b1b (visuals test the explanation) + Sebastian (build toolkit incrementally).

### Phase 0 — Story lock (1 session, no Manim)

Write **`HACKATHON-STORY.md`** (honesty doc):

- 24 h, LA Tech Week / USC ISI, 3-person team (you = all code; teammates presented).
- **Explored / failed / cut:** cloud ASR, custom training, `ViewAttachmentEntity` per-frame layout, (optional) spatial wiring not in HEAD.
- **Worked:** on-device dual pipeline, segmentation, texture bake, locale hot-swap, 2nd place.
- Tie every failure to a **rejected alternative** in `architecture[]`.

Do not render until this reads like a true postmortem, not a victory lap.

### Phase 1 — Script before pixels (1–2 sessions)

1. **Beat sheet** — chapter timestamps (below).
2. **Three-column script** per chapter:

   | Narration (you speak) | On-screen text (short) | Visual (Manim / Unity / code / b-roll) |

3. Read aloud; cut until ~**1,400–1,700 words** (~10–12 min at ~140 wpm).
4. Mark **code snippet** beats: which file, which lines, what animates.

### Phase 2 — Code snippet files (ground truth)

Copy **minimal** Swift excerpts into `code_snippets/` (not whole files):

- One concept per file, ≤15 lines when possible.
- Header comment: source path in Aura-Vision-Pro repo + line range.
- Snippets are **evidence** on screen; narration explains *why*.

### Phase 3 — Manim toolkit (incremental, reusable)

Build in **`aura_manim/`** as chapters need them:

| Module | Purpose | Status |
|--------|---------|--------|
| `theme.py` | Colors, fonts (match 60s) | ✅ |
| `typography.py` | `body_text`, `caption_line`, `subtext` (ch 6+) | ✅ |
| `components/layout.py` | `fit_center`, `flow_lr`, `labeled_card` (ch 6+) | ✅ |
| `review.py` | `plop()` layout review | ✅ |
| `icons.py` + `assets/icons/*.svg` | `load_icon()` — bell, clock, **vision-pro**, … | ✅ |
| `components/labels.py` | Bottom-third `on_screen_label()` | ✅ |
| `components/split_layout.py` | Visual top + Swift code bottom | ✅ ch 3+ |
| `components/workflow.py` | Staged pipeline diagram | ✅ |
| `components/team.py` | Hackathon roster · grid · merge lane (ch 0) | ✅ |
| `components/device.py` | Device boundary + Vision Pro (ch 1+) | ✅ |
| `components/locale_picker.py` | Recognition Language panel (ch 1 act 5) | ✅ |
| `broll.py` | Embed `Aura/clips/D*.mp4` in Manim | ✅ |
| `code_panel.py` | Swift `Code` + line highlight | ✅ |
| `rejected.py` | Ghost path + strikethrough + chips | ✅ |
| `components/pipeline.py` | Full dual-pipeline (ch 3+) | ✅ |
| `components/pipeline_stub.py` | Simplified pipeline (ch 2 only) | ✅ |
| `components/segmentation.py` | Ch 4 captions (frozen) | ✅ |
| `components/texture_bake.py` | Ch 5 HUD bake (frozen) | ✅ |
| `tools/extract_act_frames.py` | partial_movie → PNG layout QA | ✅ |
| `tools/adjust_waits.py` | Bulk `scene.wait()` per chapter | ✅ |

`code_snippets/` — minimal Swift excerpts (one concept per file).

### Phase 4 — One chapter at a time (ch 6+ uses MANIM-STANDARDS)

```
1. Draft PLAY CHECKLISTS + VO seed in vo/sceneN.md (before code)
2. sceneN_act*.py — compose typography + layout; copy _TEMPLATE_act.py
3. -ql SceneNActMLayout → extract_act_frames.py → vision QA checklist
4. -ql SceneNActM → SceneNFull for timing
5. User review — story / pacing (not pixel QA)
6. -qk --frame_rate 60 per act → ffmpeg concat
7. Read-aloud → adjust_waits.py → re-render → build_act_timestamps.py
```

**Ch 0–5:** frozen renders; do not refactor. See [`PROCESS-REVIEW.md`](PROCESS-REVIEW.md).

**Manim path:** `${workspaceFolder}/.venv/bin/manim` from `aura_manim/`.

### Phase 5 — Voice + assembly

1. Draft VO in **`vo/sceneN.md`** (measured act timestamps, not SCENE-PLAN guesses).
2. Read aloud over concat MP4; trim **`self.wait()`** in act files.
3. Record VO (per-act punch-ins OK — align to `vo/sceneN.md` start times).
4. Resolve: Manim concat + VO + optional Unity viz + music bed.
5. Music: Pixabay documentary @ **`0.05–0.07`** under VO (`Aura/manim/add_music.py`).

---

## Manim code comments (learning convention)

Use this header on every scene file:

```python
"""
Scene 3 — Dual pipeline (architecture[0] + hard_parts[1])
Story beat: One AVAudioEngine tap feeds Speech and SoundAnalysis; analysis queue must not block tap.
VO anchor: "The tap runs at realtime — classification moves to a serial queue."
Code snippet: code_snippets/analysis_queue.swift
"""
```

Inside `construct()`:

```python
# ACT 1 — Show single tap (concrete before abstract)
# ACT 2 — Split to Speech vs SoundAnalysis (parallel VGroups)
# ACT 3 — Highlight serial queue on SoundAnalysis branch (code_panel sync)
# HOLD — pause for VO line about blocking
```

**Rule:** Comments explain **story beats and Manim intent**, not full API docs.  
**Learning:** On first use of a new Manim/Unity idea, add `# LEARN: <term> — see LEARNING.md` and append a short entry to [`LEARNING.md`](LEARNING.md).

---

## Manim + Unity — hybrid (revised)

Sebastian uses Unity **as an animation tool** after the fact — not only when the product is Unity. We do the same for Aura **where 3D/spatial is easier than Manim**.

### Honesty line (say once in VO or on-screen)

> *“These Unity clips are explainer visualizations — Aura ships in Swift on visionOS.”*

Never imply the portfolio app runs on Unity.

### When to use which (Aura design video)

| Use **Manim** | Use **Unity viz** | Use **demo B-roll / snippet** |
|---------------|-------------------|--------------------------------|
| On-device vs cloud boundary | Spatial caption panel in 3D space | Real 2D HUD from hackathon |
| Dual pipeline / serial queue | Sound **azimuth ray** from user head | `MicrophoneMonitor.swift` tap |
| Thread lanes (MainActor) | **Billboard** panel + camera overhead NaN bug | MainActor Swift snippet |
| Segmentation timeline (1.1s gaps) | Optional: panel filling with lines over time | Pause threshold code |
| Texture bake vs 90 Hz (diagram) | **Side-by-side:** Update() UI jitter vs static baked quad | `ImmersiveView` debounce code |
| Rejected path (ghosted cloud) | — | — |
| Scale: today vs product arch | — | — |

**Rule of thumb:** If the idea lives on a **flat diagram** → Manim. If the idea needs **camera, depth, or orientation in space** → Unity viz. If it needs **proof** → Swift snippet or real footage.

### Sebastian pattern (adapted for Aura)

1. **Build** Swift app (done — hackathon).
2. **Script** decides which beats need 3D clarity.
3. **Unity viz scenes** — small, disposable scenes (`unity_viz/`) — record 1080p clips.
4. **Manim scenes** — pipelines + code panels.
5. **Resolve** — interleave Manim + Unity + snippets + VO (same as his DaVinci assembly).

You’re learning both tools — **alternate by chapter**, not “learn both at once in one scene.”

### Unity viz scope (keep small)

| Unity scene | Chapter | ~Duration |
|-------------|---------|-----------|
| `SpatialCaptionRoom.unity` | 7 | Floating panel + slow orbit |
| `BillboardOverheadBug.unity` | 5 or 7 | Bad `lookAt` vs stable billboard |
| `AzimuthRays.unity` | 3 (optional) | Mic center, rays to sound direction |

Start with **one** Unity scene when you reach ch 5 or 7 — after Manim toolkit works.

### Portfolio-wide (unchanged)

| Project | Manim | Unity viz | Engine capture |
|---------|-------|-----------|----------------|
| **CelestiaVR** | Math / coords | Optional | **Yes** — shipped Unity app |
| **Aura** | Pipelines, code | **Yes** — spatial explainer | visionOS demo clips |
| **MockPad** | CRDT diagrams | Rare | Browser capture |
| **DevStack** | Service topology | Optional 3D fly-through | Docker/dashboard |

---

## Unity vs Manim — when to use which (summary)

**Previous “no Unity for Aura”** meant: don’t replace Swift/RealityKit truth with a fake Unity *product*.  
**Revised:** Unity is welcome as a **visualization authoring tool** for spatial beats — with the honesty label above.

## Chapter progress

| Ch | Manim acts | Concat | VO doc | Status |
|----|------------|--------|--------|--------|
| 0 | `scene0_act{1…6}.py` + `scene0_full.py` | `output/scene0_chapter0_2160p60.mp4` | [`vo/scene0.md`](vo/scene0.md) | draft VO · trim waits |
| 1 | `scene1_act{1…5}.py` + `scene1_full.py` | `output/scene1_chapter1_2160p60.mp4` | [`vo/scene1.md`](vo/scene1.md) | draft VO · extend waits (~43 s → ~90 s) |
| 2 | `scene2_act{1…6}.py` + `scene2_full.py` | `output/scene2_chapter2_2160p60.mp4` | [`vo/scene2.md`](vo/scene2.md) | draft VO · extend waits (~55 s → ~90 s) |
| 3 | `scene3_act{1…6}.py` + `scene3_full.py` | `output/scene3_chapter3_2160p60.mp4` | [`vo/scene3.md`](vo/scene3.md) | draft VO · extend waits (~57 s → ~110 s) |
| 4 | `scene4_act{1…4}.py` + `scene4_full.py` | `output/scene4_chapter4_2160p60.mp4` | [`vo/scene4.md`](vo/scene4.md) | draft VO · extend waits (~36 s → ~90 s) |
| 5 | `scene5_act{1…4}.py` + `scene5_full.py` | `output/scene5_chapter5_2160p60.mp4` | [`vo/scene5.md`](vo/scene5.md) | draft VO · extend waits (~34 s → ~90 s) |

## Chapter outline (~11 min)

| Ch | Time | Title | Honesty / narrative | Code snippet | **Manim** | **Unity viz** |
|----|------|-------|---------------------|--------------|-----------|---------------|
| 0 | 0:00–1:05 | Problem + hackathon + sphere POC | First Vision Pro build | — | Noisy room + **sphere POC** | — |
| 1 | 1:05–2:35 | On-device only | Cloud temptation failed | `on_device_speech.swift` | Device boundary; reject cloud | — |
| 2 | 2:35–4:05 | Build vs train | No time to train | — | Apple ML vs your pipeline | — |
| 3 | 4:05–5:55 | One tap, dual pipeline | Serial queue | `analysis_queue.swift` | Split + queue lanes | — |
| 4 | 5:55–7:25 | Segmentation | raw `formattedString` failed | `pause_threshold.swift` | Timeline gaps → sentences | — |
| 5 | 7:25–8:55 | Texture HUD vs 90 Hz | ViewAttachment failed | `debounce_texture.swift` | 90 Hz vs bake diagram | Jitter vs baked quad |
| 6 | 8:55–9:55 | MainActor bridge | Callback → UI | `mainactor_bridge.swift` | Thread lanes | — |
| 7 | 9:55–11:25 | **Directional → Iron Man HUD** | Pins rejected; HUD shipped | optional | FOV hazard diagram | **AzimuthRays** + **SpatialCaptionRoom** |
| 8 | 11:25–12:15 | Scale | Prototype → product | — | Today vs product arch | — |
| 9 | 12:15–12:45 | Outro | Links | — | Title card | — |

Adjust after VO read — timestamps are targets.

---

## Scale section (chapter 8) — script seeds

**Breaks today:** single-user prototype; locale model storage; thermal/battery (qualitative); MainActor churn; no benchmarks; spatial not in HEAD.

**Would change for a real product:** locale pack downloads; opt-in encrypted cloud tier (revisit decision 1); OTA model pinning; 2D-first ship path; observability without raw audio upload.

**Do not claim:** ms latency, CPU %, millions of users.

---

## Code snippets to extract (from Aura-Vision-Pro)

| File (repo) | Concept | Scene |
|-------------|---------|-------|
| `MicrophoneMonitor.swift` | AVAudioEngine tap install | 3 |
| `MicrophoneMonitor.swift` | Serial `AnalysisQueue` / analyze dispatch | 3 |
| `MicrophoneMonitor.swift` | On-device Speech, no network | 1 |
| `MicrophoneMonitor.swift` | Pause threshold 1.1 s | 4 |
| `ContentView.swift` | Sentence splitter | 4 |
| `ImmersiveView.swift` | Texture debounce 100 ms | 5 |
| `MicrophoneMonitor.swift` | MainActor isolation / `@Published` | 6 |
| `ContentView.swift` | Locale list (7) | 3 or 7 |

*Pull exact lines when scripting — fact record cites measured thresholds.*

---

## Folder plan (create as you go)

```
Aura/design-video/
  README.md              ← this file · process + progress
  LEARNING.md            ← Manim/Unity concepts index
  HACKATHON-STORY.md
  SCRIPT.md              ← ch 0–2 ✅ · ch 3–9 TBD
  SCENE-PLAN.md
  vo/
    VO-WORKFLOW.md       ← repeatable VO + concat SOP
    _TEMPLATE.md         ← copy per chapter
    scene0.md, scene1.md
    build_act_timestamps.py
  code_snippets/         ← Swift evidence files
  tools/                 ← serve.py · prompter
  aura_manim/
    theme.py, icons.py, review.py
    broll.py, code_panel.py, rejected.py
    components/          ← labels, team, device, locale_picker
    scenes/
      scene0_act{1…6}.py, scene0_full.py
      scene1_act{1…5}.py, scene1_full.py
    assets/icons/        ← SVGs incl. vision-pro.svg
  output/                ← concat MP4s + sceneN_concat.txt
  unity_viz/             ← (ch 5 / 7)
```

Reuse repo **`.venv/bin/manim`**. Renders: `aura_manim/media/` (gitignored).

### Script workspace (read / edit script + scene plan)

Side-by-side **SCRIPT.md** and **SCENE-PLAN.md** with chapter jump and save:

```bash
python Aura/design-video/tools/serve.py
# → http://127.0.0.1:8765/
# prompter  → http://127.0.0.1:8765/prompter.html
```

See [`TOOL_IDEAS.md`](TOOL_IDEAS.md) for other tooling ideas.

---

## Differences from 60s workflow

| 60s | Design video |
|-----|----------------|
| Text cards | **Animated** diagrams + code |
| No VO | **Your VO** + short on-screen labels |
| Montage | **Chapters** + one idea per scene |
| 56 s | 10–12 min |
| `aura_cards.py` | `design-video/aura_manim/` + `scenes/` |

---

## Next deliverable

1. ~~Ch 0 acts + concat~~ ✅ · ~~VO doc~~ ✅ · read-aloud + trim waits  
2. **Ch 1 layout review** (`Scene1ActNLayout`) → `-qk` → concat → VO draft in `vo/scene1.md`  
3. **`vo/scene2.md`** plan → ch 2 code (build vs train)  
4. **`pipeline.py`** before ch 3  
5. **`SCRIPT.md` ch 3** after ch 0–1 VO lock
