# Aura — hackathon story (honesty doc)

> **Purpose:** Lock the narrative before any Manim/Unity render.  
> **Source:** `project-sources/facts/aura.json` · `project-sources/projects/aura-visionos/aura-visionos.md`  
> **Rule:** Every “failed” path maps to a rejected alternative in `architecture[]`. No victory lap.

---

## Frame

| Field | Truth |
|-------|-------|
| **When** | Oct 2025 — LA Tech Week / USC ISI hackathon (~24 h build window) |
| **Team** | 3 people — Fardeen Khan, Namratha V Patil, Rajat Savdekar |
| **Who coded** | **Rajat only** (git: all Swift commits under RDX-Rajat-Savdekar) |
| **Who presented** | Teammates on camera in full YouTube demo; Rajat built the app |
| **Outcome** | **2nd place** — fully working prototype, zero external dependencies |
| **Platform** | Apple Vision Pro · visionOS · Swift / SwiftUI / RealityKit |
| **Scale** | Hackathon prototype — **not** production, **not** benchmarked |

---

## Problem we chased

Deaf and hard-of-hearing users miss **situational audio**: speech in a noisy room, environmental cues (sirens, clapping, whispers). Aura captures mic audio on Vision Pro and surfaces **live captions** plus **sound-class alerts** — entirely on-device so audio never leaves the headset.

**Design video hook:** Show the gap (can't hear → miss context) → show what we shipped in 24 h to close part of that gap.

---

## Day zero — Vision Pro pipeline POC (sphere)

Before Aura looked like a captioning app, we built a **throwaway proof-of-concept** — on purpose.

| | |
|---|---|
| **What it was** | A basic visionOS app: a **sphere** in space. Say a **color word** (“red”, “blue”, …) → sphere **changes color**. **Loudness (RMS)** → sphere **scales** up or down. |
| **Why we built it** | First time using **Apple Vision Pro** as a dev target. We wanted a **minimal end-to-end pipeline** — mic → on-device speech/sound → RealityKit entity — before betting the hackathon on a full HUD. |
| **What it validated** | Xcode + visionOS deploy, audio session, speech recognition hookup, spatial rendering loop — **without** debugging captions, segmentation, and UI at the same time. |
| **What it was not** | The product. Discarded once the real pipeline was stable. No need to show in demo reel unless useful as a 3 s “day zero” beat. |
| **Video beat** | Ch 0 (teaser) or early Ch 2 — **Manim** or **Unity** sphere: color word → color, volume → scale. Label: `Pipeline POC · hour 0`. |

**Lesson for the video:** Good hackathon hygiene — **de-risk the platform first**, then stack features.

---

## What we explored and rejected

Use these as **ghosted paths** in Manim — each ties to `architecture[]`.

### 1. Cloud speech fallback

| | |
|---|---|
| **Temptation** | Network ASR when on-device struggles; “just call an API.” |
| **Why we cut it** | Audio leaves the device; latency becomes variable; privacy story dies. |
| **Fact ref** | `architecture[0]` — strict on-device ASR, no cloud fallback |
| **Evidence** | `MicrophoneMonitor.swift` — on-device `SFSpeechRecognizer`, no network path |
| **Video beat** | Ch 1 — device boundary diagram; cloud path fades/strikethrough |

### 2. Train custom ML models

| | |
|---|---|
| **Temptation** | Fine-tune sound/speech models for hackathon wow-factor. |
| **Why we cut it** | 24 h budget; Apple had **just shipped** strong on-device Speech + SoundAnalysis. Training = data + MLOps we didn't have. |
| **Fact ref** | `architecture[1]` — reuse Apple's Core ML models |
| **Honesty** | **We did not train any model.** Integration + pipeline is the engineering story. |
| **Video beat** | Ch 2 — two boxes: “Train custom” (crossed out) vs “Apple on-device + your pipeline” |

### 3. Raw `formattedString` for captions

| | |
|---|---|
| **Temptation** | Pipe `bestTranscription.formattedString` straight to UI — fastest path. |
| **Why it failed UX** | No sentence boundaries, no timing structure, unreadable wall of text. |
| **Fact ref** | `architecture[3]` — two-layer segmentation |
| **What worked** | 1.1 s pause-gap utterances + abbreviation-aware sentence splitter |
| **Video beat** | Ch 4 — timeline with gaps → sentence chunks |

### 4. ViewAttachmentEntity / per-frame layout in spatial HUD

| | |
|---|---|
| **Temptation** | Native RealityKit text attachment — “the Apple way.” |
| **Why we cut it** | Re-layout every frame couples UI cost to the ~90 Hz render loop. |
| **Fact ref** | `architecture[2]` — texture-baked SwiftUI + 100 ms debounce |
| **Video beat** | Ch 5 — Manim 90 Hz loop diagram + Unity side-by-side jitter vs baked quad |

### 5. Spatial immersive HUD in committed repo (caveat)

| | |
|---|---|
| **Truth** | `ImmersiveView.swift` exists (343 LOC): texture bake, billboard math, debounce. **Demo footage shows spatial UI.** |
| **Caveat** | **Committed HEAD does not wire `ImmersiveView` into `AuraApp`** — no `ImmersiveSpace` in entry point. Spatial demo ran from a build/branch not reflected in current HEAD. |
| **Claim safely** | “Designed, implemented, and demoed” — disclose wiring gap if asked. |
| **Video beat** | Ch 7 — Unity viz for spatial explainer + honesty line; optional 2D demo B-roll only |

### 6. Directional markers in world space (early hackathon — rejected)

| | |
|---|---|
| **What we tried** | In the **first hours**, we tested **pinning sounds to the direction they came from** — spatial markers anchored where audio seemed to originate (using stereo/azimuth from the mic). |
| **Issue 1 — no ground truth for position** | Vision Pro has **no sensor that gives you an exact world coordinate** to place a marker. You get **direction hints** from audio, not a reliable “put the icon *there*” pose. Pinning felt **guessy** and drift-prone. |
| **Issue 2 — safety / UX hazard** | An alert **outside the user’s field of view** is dangerous. Example: **baby crying** pinned behind you — you might **never look that way** and miss something urgent. World-locked pins optimize for “where is sound?” not “did the user *see* the alert?” |
| **What we chose instead** | **Iron Man–style HUD** — captions and sound labels in a **fixed, head-relative panel** always in view (2D window + spatial prototype). Information comes to the user; user doesn’t hunt the room. |
| **Code truth** | Azimuth/RMS still computed in DSP (`MicrophoneMonitor`) for analysis; **not shown as directional UI** in shipped demo. |
| **Video beat** | **Ch 7** — Manim or Unity: world pins (crossed out) → HUD panel (highlight). Short VO on both rejection reasons. Optional Unity `AzimuthRays.unity` as “what we tried,” then strikethrough. |

---

## What worked (ship the story on these)

### Dual pipeline off one tap

One `AVAudioEngine` tap feeds **Speech ASR** and **SoundAnalysis**. Classification runs on serial `com.aura.AnalysisQueue` so analysis **never blocks** the realtime tap. RMS/azimuth in-callback.

→ Ch 3 · `hard_parts[1]` · B3 bullet territory

### Build vs train

Reused Apple on-device models; engineering focus = wiring, segmentation, concurrency, UI.

→ Ch 2 · `architecture[1]`

### Two-layer transcript segmentation

Temporal utterances (1.1 s pause threshold) + grammatical sentence splitter (abbreviation-aware).

→ Ch 4 · `architecture[3]`

### Classifier hysteresis + throttle

0.6 confidence gate, 0.25 s throttle — stops label flapping on environmental sounds.

→ Mention in Ch 3 or 4 (short beat)

### Locale hot-swap (7 picker languages)

Switch EN ↔ JA (and others in picker) without restarting the engine — demo confirms EN + JA live.

→ Ch 3 tag or Ch 7 B-roll (`D6_japanese-locale.mp4`)

### Texture-baked spatial HUD

SwiftUI rendered off-screen → cached texture → RealityKit quad; 100 ms debounce decouples signal from render.

→ Ch 5 · `architecture[2]` · B2 bullet

### MainActor bridge

Background ML delegate callbacks → `@MainActor` for `@Published` UI mutation.

→ Ch 6 · `hard_parts[0]`

### 2D SwiftUI HUD — Iron Man style (demo truth)

`ContentView` — head-relative panel: captions + sound labels **always in view**. Deliberate pivot away from world-locked directional pins (see rejected #6).

→ B-roll throughout (`Aura/clips/D1–D6`) · Ch 7 narrative

### Sphere pipeline POC (day zero)

Mic → speech/color word → sphere color; RMS → sphere size. Platform shakedown before feature work.

→ Ch 0 teaser · optional Manim/Unity viz

---

## Timeline (narrative order for video)

```
Hour 0–2   Sphere POC — visionOS deploy, mic, speech, spatial loop (first time on device)
Hour 2–4   Directional pin experiment → rejected (no exact coords, FOV safety)
Hour 4–6   Pivot: Iron Man HUD + on-device stack choice (no cloud)
Hour 6–12  AVAudioEngine tap + dual ML wiring + queue discipline
Hour 12–16 Segmentation + 2D HUD + classifier gating
Hour 16–20 ImmersiveView / texture bake (parallel if time)
Hour 20–24 Locale polish + demo prep + teammates present
```

*Approximate — adjust if you remember specific ordering.*

---

## Demo evidence map (reuse from 60s clips)

| Clip | Shows | Use in design video |
|------|-------|---------------------|
| `D1` | Live EN transcription | Ch 0 problem payoff / Ch 3 pipeline proof |
| `D2` | Second speaker | Ch 4 segmentation context |
| `D3` | Whisper + label | Ch 3 sound branch |
| `D4` | Siren → emergency vehicle | Ch 3 classifier |
| `D5` | Clapping | Ch 3 sound classes |
| `D6` | Japanese locale switch | Ch 3 or 7 locale hot-swap |

Full source: `Aura/AURA-Vision-pro-app_Media_HbW9F2zjmLQ_001_720p.mp4`

---

## Never claim (design video)

From `facts/aura.json` → `never_claim`:

- Custom / trained ML models
- Latency %, CPU %, speedup numbers (no benchmark artifact)
- Production scale or real-user metrics
- Spatial HUD as “in repo HEAD” without wiring caveat
- Directional **world-locked markers** as shipped UI (we tried; chose Iron Man HUD instead)
- Sphere POC as “the product” — it was day-zero pipeline only

---

## Interview-grade one-liners (for VO)

| Question | Answer seed |
|----------|-------------|
| Why on-device only? | Privacy + deterministic latency; cost = pre-installed locale models. |
| Did you train ML? | No — integrated Apple's models; my work is pipeline, segmentation, integration. |
| Why texture bake? | Rich SwiftUI layout without paying layout cost every frame at 90 Hz. |
| Why not pin sounds in 3D space? | No exact world coords from hardware; alerts off-screen (e.g. baby crying) are a safety hazard — HUD keeps alerts in view. |
| Why a sphere POC first? | First Vision Pro build — validate deploy + audio + spatial loop before the real app. |
| Hardest bug? | Realtime tap discipline **or** NaN quaternions when camera overhead **or** MainActor bridging — pick one story per chapter. |

---

## Open questions (fill when you remember)

- [ ] Exact hour you pivoted away from cloud ASR (if ever tried)
- [ ] Which build/branch had `ImmersiveSpace` wired for demo
- [ ] Beyond EN+JA, which of the 5 other picker locales were tested live

---

## Sign-off

When this doc feels like a **postmortem** (failures named, scope honest), proceed to `SCRIPT.md` + `SCENE-PLAN.md`. Do not render Manim/Unity until VO for ch 0–2 reads naturally aloud.
