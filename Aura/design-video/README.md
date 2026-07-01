# Aura — system design video (10–12 min)

> **Status:** planning · **Target:** 10–12 min · **VO:** Rajat  
> **Visuals:** **Manim** (2D pipelines, code) + **Unity viz** (3D spatial) + Swift snippets + demo B-roll  
> **Learning:** new concepts → [`LEARNING.md`](LEARNING.md) + `# LEARN:` in code  
> **Not:** placeholder text cards · **Not:** duplicate of 60s script  
> **Fact record:** `project-sources/facts/aura.json` · **Journal:** `../journal.md`

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

### Phase 3 — Manim toolkit v0 (incremental, reusable)

Start **`aura_manim/`** (shared helpers), not one-off scenes:

| Module | Purpose | Ship in v0 |
|--------|---------|------------|
| `theme.py` | Colors, fonts (match 60s) | ✅ |
| `code_panel.py` | Swift snippet panel + highlight line | ✅ |
| `pipeline.py` | Boxes + arrows (AVAudioEngine → Speech / SoundAnalysis) | ✅ |
| `thread_lane.py` | MainActor vs background queue lanes | ✅ |
| `rejected.py` | “Rejected path” ghosted + strikethrough | ✅ |

Add components **only when scene 2 needs them** — don’t build the whole library upfront.

**Manim libraries:** No drop-in “system design” pack. Use:

- Manim **`Code`** / **`Text`** for snippets ([Manim CE docs](https://docs.manim.community/)).
- This repo’s pattern: `dsa_toolkit/manim_utils.py` (custom Mobjects), `celestia_presentation/scene*.py` (domain scenes).
- Optional later: [`manim-slides`](https://github.com/jeertmans/manim-slides) for presenter mode — not required for YouTube.

### Phase 4 — One scene at a time

For each `scenes/sceneN.py`:

1. Storyboard sketch (paper or bullet list).
2. Implement **one Manim idea** (e.g. dual pipeline split).
3. Preview: `.venv/bin/manim -ql -r 1280,720 --frame_rate 30 scenes/sceneN.py SceneName`
4. Adjust **script** if animation feels wrong (3b1b rule).
5. Log in `../journal.md`.

Render **final** at `-qm` or `-qh` only when VO is locked.

### Phase 5 — Voice + assembly

1. Record VO against **final script** (quiet room; punch-ins OK).
2. DaVinci Resolve: Manim clips + **Unity viz recordings** + VO + demo B-roll.
3. Music: same Pixabay documentary family, **`--volume 0.05–0.07`** under VO (`add_music.py`).
4. Chapters in YouTube description (match beat sheet).

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
  README.md
  LEARNING.md
  HACKATHON-STORY.md     ← Phase 0 ✅
  SCRIPT.md              ← ch 0–2 ✅ · ch 3–9 TBD
  SCENE-PLAN.md          ← timestamps + Manim/Unity/B-roll per beat ✅
  TOOL_IDEAS.md          ← production tool theories + backlog
  tools/                 ← script workspace (HTML + serve.py)
  aura_manim/
  unity_viz/
  output/
```

Reuse root `.venv` Manim; config copy from `../manim/manim.cfg` (1280×720 or 1920×1080 @ 30 fps for YouTube).

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

## Next deliverable (pick one)

1. ~~**`HACKATHON-STORY.md`**~~ ✅  
2. ~~**`SCRIPT.md` ch 0–2**~~ ✅ · **`SCENE-PLAN.md`** ✅  
3. **`aura_manim/theme.py` + `code_panel.py`** — first Manim toolkit slice with `# LEARN:` comments  
4. **`SCRIPT.md` ch 3** — after read-aloud of ch 0–2  
5. **`unity_viz/` README** — when starting ch 5 or 7

Say which number to execute next (one only).
