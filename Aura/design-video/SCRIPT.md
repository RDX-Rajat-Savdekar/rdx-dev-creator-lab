# Aura — system design video script

> **Target:** 10–12 min · **VO:** Rajat · **Pace:** ~140 wpm  
> **Status:** ch 0–2 draft · ch 3–9 TBD  
> **Companion:** [`SCENE-PLAN.md`](SCENE-PLAN.md) (timestamps + tool per beat) · [`HACKATHON-STORY.md`](HACKATHON-STORY.md)

---

## How to read this doc

Three columns per chapter:

| Narration | On-screen text | Visual |
|-----------|----------------|--------|

- **Narration** — what you speak (trim on read-aloud)
- **On-screen text** — short labels only (not paragraphs)
- **Visual** — `Manim` · `Unity` · `B-roll` · `Swift` · combo tags

Word counts are targets; adjust after recording.

---

## Chapter 0 — Problem + hackathon frame

**Time:** `0:00` → `1:05` · **~150 words** · **YouTube:** *The problem*

| Narration | On-screen text | Visual |
|-----------|----------------|--------|
| If you're deaf or hard of hearing, a noisy room isn't just loud — you miss *what was said* and *what happened around you*. Speech and environmental sounds both carry context. | `Situational audio gap` | **Manim** — simple room: speech bubbles + sound icons fade out / question marks |
| That's the problem we chased at a hackathon in October 2025 — LA Tech Week at USC ISI. Twenty-four hours. Three-person team. | `24h hackathon · Oct 2025` | **Manim** — clock + team icons (1 coder, 2 presenters) |
| I wrote all of the code — audio, dual machine-learning pipelines, captions, and the spatial HUD prototype. My teammates edited the README and presented the demo on camera. | `All code: Rajat` | **Manim** — git commit icon → single author lane |
| It was also our **first time building on Vision Pro**. Before the real app, we shipped a tiny POC: a sphere that turned **red** when you said "red", and **grew** when you spoke louder — just to prove deploy, mic, speech, and spatial rendering worked. | `Day 0: sphere POC` | **Manim** or **Unity** — sphere: color word → color, RMS → scale (3–5 s) |
| This video is the system design story: what we tried, what we cut, and what actually shipped. Hackathon prototype — not a production app. | `System design · prototype` | **B-roll** — 2 s flash: `D1` live captions → cut to title hold |
| Aura runs on Apple Vision Pro: live speech transcription plus environmental sound classification — entirely on-device. | `Aura · visionOS · on-device` | **Manim** — Vision Pro silhouette + two pipeline stubs (detail in ch 1–3) |

**VO checkpoint:** Should feel like a problem statement, not a resume opener.

---

## Chapter 1 — On-device only

**Time:** `1:05` → `2:35` · **~210 words** · **YouTube:** *On-device only*

| Narration | On-screen text | Visual |
|-----------|----------------|--------|
| First architectural decision: **everything stays on the device**. No cloud speech API, no uploading audio for analysis. | `Decision 1: on-device only` | **Manim** — device boundary box (headset icon inside) |
| The temptation in a hackathon is to cheat — send audio to a network recognizer when on-device struggles. That's faster to demo and often more accurate. | `Temptation: cloud ASR` | **Manim** — ghost arrow leaves device to cloud; label "network fallback" |
| We rejected that. If audio leaves the Vision Pro, you lose the privacy story — and latency becomes whatever the network feels like. For accessibility, unpredictable delay is as bad as wrong text. | `Rejected: privacy + latency` | **Manim** — cloud path **strikethrough** + fade (`rejected.py`); keep on-device path bright |
| So we committed to Apple's on-device Speech framework — `SFSpeechRecognizer` — with no network fallback path in the code. | `SFSpeechRecognizer` | **Swift** — `code_snippets/on_device_speech.swift` highlight: requiresOnDeviceRecognition / local-only config |
| Trade-off we accepted: speech models are **per locale**. Users need the language pack installed. That's a product constraint, not a bug — we surface it in the UI when a locale isn't available. | `Trade-off: locale models` | **Manim** — small inset: 7 locale flags (picker preview); no download animation yet |
| Zero external dependencies in the repo — no CocoaPods, no SPM packages. What you see is Swift, Apple frameworks, and about fifteen hundred lines of app code. | `0 external deps · ~1,475 LOC` | **Manim** — fact card (metrics from fact record) |

**VO checkpoint:** Name the rejection explicitly: "We rejected cloud fallback because…"

**Honesty:** Do not imply custom models — that's chapter 2.

---

## Chapter 2 — Build vs train

**Time:** `2:35` → `4:05` · **~210 words** · **YouTube:** *Build vs train*

| Narration | On-screen text | Visual |
|-----------|----------------|--------|
| Second decision: **we did not train any machine-learning model**. I need to say that clearly because the demo looks like "ML magic." | `Decision 2: build vs train` | **Manim** — fork: left "Train custom" / right "Integrate Apple ML" |
| The left path — collect data, label sounds, train, export Core ML, debug — is a multi-week project. We had twenty-four hours. | `Train: weeks` | **Manim** — left path dims; timeline bar "weeks" vs "hours" |
| Apple had recently shipped strong on-device models: Speech for transcription, SoundAnalysis for environmental classes — hundreds of built-in labels. Good enough to prove the *product* idea. | `Apple Speech + SoundAnalysis` | **Manim** — two Apple ML boxes; arrow to "Your pipeline" box |
| My job wasn't training. It was **integration engineering**: one microphone tap feeding two consumers, realtime discipline, caption segmentation, UI that doesn't choke at ninety hertz. | `Our work: pipeline + UI` | **Manim** — zoom into pipeline stub (preview of ch 3); labels: tap · queue · UI |
| If we'd spent the hackathon training, we'd have a model slide and no working app. We traded ML research for a working accessibility prototype — and placed second. | `2nd place · working demo` | **B-roll** — 3 s montage: `D4` siren label + `D5` clap (sound classes work) |
| Honest scope: I integrated Apple's models. The engineering story is everything *around* them. | `Integrated, not trained` | **Manim** — bold on-screen honesty card 2 s hold |

**VO checkpoint:** Say "I did not train any model" once, clearly.

---

## Chapter 7 — UI evolution: directional pins → Iron Man HUD

**Time:** `9:55` → `11:25` · **~245 words** · **YouTube:** *Iron Man HUD*

| Narration | On-screen text | Visual |
|-----------|----------------|--------|
| Early in the hackathon we tried something that *sounds* right for spatial computing: **pin each sound to the direction it came from** — a marker in the world where the audio seems to originate. | `Tried: world-locked pins` | **Unity** or **Manim** — rays from head to pins around room |
| Two problems ended that experiment. First: Vision Pro gives you **direction from the mic**, not an **exact coordinate** to anchor a marker. The pin is guesswork — it drifts and feels wrong. | `No exact world coords` | **Manim** — pin with `?` / wobble; label "azimuth ≠ position" |
| Second — and this mattered for accessibility — an urgent sound **behind you** might never enter your field of view. A **baby crying** pinned outside your gaze is a **missed alert**, not a helpful cue. | `Off-screen = hazard` | **Manim** — baby-cry icon behind user, outside FOV cone, red X |
| So we pivoted to an **Iron Man–style HUD**: captions and sound labels on a **panel that stays in view** — head-relative, not world-hunted. That's what the demo shows in the 2D window. | `Iron Man HUD` | **B-roll** — `D1`/`D3` caption panel · **Manim** HUD frame overlay |
| We still compute azimuth in the audio path for analysis, but we **don't ship directional markers** in the UI. | `Azimuth: computed, not shown` | **Manim** — small pipeline inset; UI branch grayed |
| Separately, we built a **spatial HUD prototype** — texture-baked SwiftUI in RealityKit — designed and demoed on video. Honest caveat: the committed repo HEAD doesn't wire `ImmersiveView` into the app entry point; the spatial demo ran from a build that's not in current HEAD. | `Spatial: demoed · HEAD caveat` | **Unity** — `SpatialCaptionRoom.unity` slow orbit · optional **Swift** `immersive_caveat` |
| Unity clips in this section are **explainers only** — Aura ships in Swift on visionOS. | `Viz only · Swift app` | **Manim** — honesty card 2 s |

**VO checkpoint:** Name both rejection reasons before celebrating the HUD.

---

## Chapters 3–6, 8–9 (placeholder headers)

| Ch | Time | Title | Status |
|----|------|-------|--------|
| 3 | 4:05–5:55 | One tap, dual pipeline | outline in SCENE-PLAN |
| 4 | 5:55–7:25 | Segmentation | outline in SCENE-PLAN |
| 5 | 7:25–8:55 | Texture HUD vs 90 Hz | outline in SCENE-PLAN |
| 6 | 8:55–9:55 | MainActor bridge | outline in SCENE-PLAN |
| 7 | 9:55–11:25 | UI evolution: directional → Iron Man HUD | ✅ draft |
| 8 | 11:25–12:15 | Scale | outline in SCENE-PLAN |
| 9 | 12:15–12:45 | Outro | outline in SCENE-PLAN |

Draft ch 3–9 narration after toolkit v0 + read-aloud of ch 0–2.

---

## YouTube description — chapter timestamps (full target)

Copy when video is final; times will shift after VO.

```
0:00 The problem (+ sphere POC)
1:05 On-device only
2:35 Build vs train
4:05 One tap, dual pipeline
5:55 Segmentation
7:25 Texture HUD vs 90 Hz
8:55 MainActor bridge
9:55 Iron Man HUD (directional → panel)
11:25 Scale
12:15 Outro
```

*Runtime ~12:45 after ch 0 + ch 7 additions — trim on read-aloud or tighten ch 8–9 in edit.*

---

## Read-aloud notes (ch 0–2)

| Check | |
|-------|---|
| Total words ch 0–2 | ~570 → ~4:05 at 140 wpm (ch 0 longer — trim on read) |
| Sphere POC | ch 0 once — pipeline shakedown, not the product |
| Directional pins → HUD | ch 7 — both rejection reasons |
| "I did not train" | ch 2 only (once) |
| Teammates | ch 0 once — presenters, not coders |
| Prototype disclaimer | ch 0 |
| Cloud rejection | ch 1 with reason |
| Custom ML rejection | ch 2 with reason |
