# Aura design video — full teleprompter script

> **Generated from** `vo/scene0.md` … `vo/scene9.md` · **Pace:** ~140 wpm
> **Acts:** 46 · **Words:** ~1110 · **Est. VO:** ~475.6s (7.9 min)

Read over chapter concat MP4s in `output/`. Extend holds with `tools/extend_act_holds.py` (no Manim re-render).

---

## Chapter 0 — The problem

*Problem + hackathon + sphere POC*

### Act 1 — Noisy room · situational audio gap
**On screen:** Situational audio gap

> If you're deaf or hard of hearing, a noisy room isn't just loud — you miss what was said and what happened around you. Speech and environmental sounds both carry context.

*31 words · ~13.3s @ 140 wpm · source: draft*

### Act 2 — Hackathon frame
**On screen:** 24h hackathon · Oct 2025

> That's the problem we chased at a twenty-four-hour hackathon in October twenty twenty-five — LA Tech Week at USC ISI. Three-person team.

*22 words · ~9.4s @ 140 wpm · source: draft*

### Act 3 — Shared codebase
**On screen:** Team-built · shared code

> Everyone contributed to the shared codebase. I led development; teammates owned README, design, and the on-camera demo. One repo — four merges.

*22 words · ~9.4s @ 140 wpm · source: draft*

### Act 4 — Sphere POC
**On screen:** Day 0: sphere POC

> It was also our first build on Vision Pro. Before Aura, we shipped a tiny proof of concept: say “red,” the sphere turns red; speak louder, it grows. That proved deploy, microphone, speech, and spatial rendering — before we built the real app.

*43 words · ~18.4s @ 140 wpm · source: draft*

### Act 5 — Prototype disclaimer + live demo
**On screen:** System design · prototype (+ D1 B-roll)

> This video is the system design story — what we tried, what we cut, and what actually shipped. Hackathon prototype — not a production app.

*25 words · ~10.7s @ 140 wpm · source: draft*

### Act 6 — Aura teaser
**On screen:** Aura · visionOS · on-device

> Aura runs on Apple Vision Pro: live speech transcription plus environmental sound classification — entirely on-device.

*16 words · ~6.9s @ 140 wpm · source: draft*

## Chapter 1 — On-device only

*On-device only*

### Act 1 — Device boundary
**On screen:** Decision 1: on-device only

> First decision: everything stays on the device. No cloud speech API — no uploading audio.

*15 words · ~6.4s @ 140 wpm · source: draft*

### Act 2 — Cloud temptation
**On screen:** Temptation: cloud ASR

> The hackathon temptation is to cheat — send audio to a network recognizer when on-device struggles. Faster to demo, often more accurate.

*22 words · ~9.4s @ 140 wpm · source: draft*

### Act 3 — Rejection
**On screen:** Rejected: privacy + latency

> We rejected that. Audio leaving Vision Pro kills privacy — latency becomes whatever the network feels like. For accessibility, unpredictable delay is as bad as wrong text.

*27 words · ~11.6s @ 140 wpm · source: draft*

### Act 4 — Swift evidence
**On screen:** SFSpeechRecognizer

> So we committed to Apple's on-device Speech framework — SFSpeechRecognizer — with no network fallback in the code.

*18 words · ~7.7s @ 140 wpm · source: draft*

### Act 5 — Locale + metrics
**On screen:** 0 external deps · ~1,475 LOC

> Trade-off: speech models are per locale — users need the language pack installed. Product constraint, not a bug. Zero external dependencies — Swift, Apple frameworks, about fifteen hundred lines.

*29 words · ~12.4s @ 140 wpm · source: draft*

## Chapter 2 — Build vs train

*Build vs train*

### Act 1 — Fork: train vs integrate
**On screen:** Decision 2: build vs train

> Second decision: we did not train any machine-learning model. I need to say that clearly because the demo looks like "ML magic."

*22 words · ~9.4s @ 140 wpm · source: seed*

### Act 2 — Apple ML inbox reveal
**On screen:** Apple Speech + SoundAnalysis

> Apple had recently shipped strong on-device models: Speech for transcription, SoundAnalysis for environmental classes — hundreds of built-in labels. Good enough to prove the product idea.

*26 words · ~11.1s @ 140 wpm · source: seed*

### Act 3 — Train path impractical
**On screen:** Train: weeks

> The left path — collect data, label sounds, train, export Core ML, debug — is a multi-week project. We had twenty-four hours.

*22 words · ~9.4s @ 140 wpm · source: seed*

### Act 4 — Our pipeline work
**On screen:** Our work: pipeline + UI

> My job wasn't training. It was integration engineering: one microphone tap feeding two consumers, realtime discipline, caption segmentation, UI that doesn't choke at ninety hertz.

*25 words · ~10.7s @ 140 wpm · source: seed*

### Act 5 — Outcome + proof
**On screen:** 2nd place · working demo

> If we'd spent the hackathon training, we'd have a model slide and no working app. We traded ML research for a working accessibility prototype — and placed second.

*28 words · ~12.0s @ 140 wpm · source: seed*

### Act 6 — Honesty card
**On screen:** Integrated, not trained

> Honest scope: I integrated Apple's models. The engineering story is everything around them.

*13 words · ~5.6s @ 140 wpm · source: seed*

## Chapter 3 — One tap, dual pipeline

*One tap, dual pipeline*

### Act 1 — Single AVAudioEngine tap
**On screen:** One AVAudioEngine tap

> One microphone tap on the AVAudioEngine input node — every buffer flows through a single installTap callback.

*17 words · ~7.3s @ 140 wpm · source: seed*

### Act 2 — Speech + SoundAnalysis split
**On screen:** Speech + SoundAnalysis

> That one tap fans out to Apple's Speech framework for transcription and SoundAnalysis for environmental classes — parallel on-device consumers.

*20 words · ~8.6s @ 140 wpm · source: seed*

### Act 3 — Serial AnalysisQueue
**On screen:** Never block the tap

> Heavy work never runs inside the tap. We dispatch to a serial queue — com.aura.AnalysisQueue — so analysis can't stall realtime audio.

*22 words · ~9.4s @ 140 wpm · source: seed*

### Act 4 — Classifier gate
**On screen:** Anti-flap: 0.6 · 0.25 s

> Environmental sounds flap labels. We gate on 0.6 confidence and throttle updates to 0.25 seconds.

*15 words · ~6.4s @ 140 wpm · source: seed*

### Act 5 — Locale hot-swap
**On screen:** 7 locales · hot-swap

> Seven recognition languages in the picker — switch without restarting the engine. Demo flashes Japanese locale live.

*17 words · ~7.3s @ 140 wpm · source: seed*

### Act 6 — Proof montage
**On screen:** Dual pipeline · live

> Live English captions and whisper detection — both pipelines working in the same session.

*14 words · ~6.0s @ 140 wpm · source: seed*

## Chapter 4 — Segmentation

*Segmentation*

### Act 1 — formattedString problem
**On screen:** Wall of text

> Speech recognition returns a formatted string — one continuous dump. No pauses, no sentences, no structure. During a live conversation it becomes an unreadable wall of text on screen.

*29 words · ~12.4s @ 140 wpm · source: seed*

### Act 2 — Pause threshold
**On screen:** Pause gap: 1.1 s

> First layer: temporal segmentation. When the speaker pauses longer than 1.1 seconds, we treat that as a new utterance — a breath between thoughts or between speakers.

*27 words · ~11.6s @ 140 wpm · source: seed*

### Act 3 — Sentence splitter
**On screen:** Sentence splitter

> Second layer: grammatical splitting. Abbreviations like Dr. and e.g. stay intact — we only break on real sentence boundaries. One utterance in, clean sentence chips out.

*26 words · ~11.1s @ 140 wpm · source: seed*

### Act 4 — Before/after + D2
**On screen:** Readable captions

> Before: one blob. After: utterance-to-sentence chunks you can actually read while someone is talking. The two-layer split fixed readability — and it holds up with multiple speakers.

*27 words · ~11.6s @ 140 wpm · source: seed*

## Chapter 5 — Texture HUD vs 90 Hz

*Texture HUD vs 90 Hz*

### Act 1 — 90 Hz ViewAttachment
**On screen:** 90 Hz · layout every frame

> RealityKit runs at 90 Hz. Hooking captions via ViewAttachment means SwiftUI re-layout on every frame — layout cost tied directly to the render loop. We marked this path rejected.

*29 words · ~12.4s @ 140 wpm · source: seed*

### Act 2 — Texture bake pipeline
**On screen:** Texture bake · 100 ms

> Off-screen bake: render captions in SwiftUI, snapshot to a texture, composite on a lightweight RK quad in the scene. Debounce rebakes to 100 milliseconds so partial transcripts don't thrash the GPU.

*31 words · ~13.3s @ 140 wpm · source: seed*

### Act 3 — Jitter vs baked
**On screen:** Jitter vs baked quad

> Same caption content — different render path. Per-frame layout jitters the HUD; the baked texture stays pinned. Watch the left panel wobble while the right stays stable.

*27 words · ~11.6s @ 140 wpm · source: seed*

### Act 4 — Honesty card
**On screen:** 2D HUD shipped in demo

> What we actually shipped in the demo: a 2D HUD overlay — not the full world-space texture path. Honest about the gap between prototype and production.

*26 words · ~11.1s @ 140 wpm · source: seed*

## Chapter 6 — MainActor bridge

*MainActor bridge*

### Act 1 — ML callback off main thread
**On screen:** Background thread · ML result

> Speech and sound delegates fire on background threads — not on MainActor. ML results arrive while the tap keeps running on the audio thread from chapter three.

*27 words · ~11.6s @ 140 wpm · source: seed*

### Act 2 — @Published mutation rule
**On screen:** MainActor · UI updates

> Any @Published property that drives SwiftUI must mutate on MainActor. We wrap caption updates in Task { @MainActor in } so the panel refreshes safely.

*25 words · ~10.7s @ 140 wpm · source: seed*

### Act 3 — Why it matters for captions
**On screen:** Captions update on main

> That's why live captions can refresh on screen while classification keeps streaming — UI work hops to main; the tap never waits.

*22 words · ~9.4s @ 140 wpm · source: seed*

## Chapter 7 — Iron Man HUD

*Directional pins → Iron Man HUD*

### Act 1 — Tried world-locked pins
**On screen:** Tried: world-locked pins

> Early on we tried pinning each sound to the direction it came from — markers in the world where audio seemed to originate.

*23 words · ~9.9s @ 140 wpm · source: seed*

### Act 2 — Reject: no exact coords
**On screen:** azimuth ≠ position

> First problem: Vision Pro gives direction from the mic, not an exact coordinate. The pin is guesswork — it drifts and feels wrong.

*23 words · ~9.9s @ 140 wpm · source: seed*

### Act 3 — Reject: off-screen hazard
**On screen:** Off-screen = hazard

> Second — for accessibility — an urgent sound behind you might never enter your field of view. A baby crying pinned outside your gaze is a missed alert.

*28 words · ~12.0s @ 140 wpm · source: seed*

### Act 4 — Iron Man HUD pivot
**On screen:** Iron Man HUD

> So we pivoted to an Iron Man–style HUD — captions and sound labels on a panel that stays in view. Head-relative, not world-hunted. That's what the demo shows.

*28 words · ~12.0s @ 140 wpm · source: seed*

### Act 5 — Azimuth computed, not shown
**On screen:** Azimuth: computed, not shown

> We still compute azimuth in the audio path for analysis, but we don't ship directional markers in the UI.

*19 words · ~8.1s @ 140 wpm · source: seed*

### Act 6 — Spatial caveat + honesty
**On screen:** Viz only · Swift app

> Separately we built a spatial HUD prototype — texture-baked SwiftUI in RealityKit — demoed on video. Honest caveat: committed HEAD doesn't wire ImmersiveView into the app entry. Unity clips here are explainers only — Aura ships in Swift.

*38 words · ~16.3s @ 140 wpm · source: seed*

## Chapter 8 — Scale

*Scale*

### Act 1 — 0:00.0
**On screen:** Prototype · today

> This was a hackathon prototype — one user, one headset, no benchmarks. We demoed live captions and sound alerts qualitatively; we did not measure thermal, battery, or latency.

*28 words · ~12.0s @ 140 wpm · source: seed*

### Act 2 — 0:08.1
**On screen:** Product · would change

> The same core pipeline could grow into a product — locale bundles on CDN, observability, multi-user fleet metrics. That is a different ops envelope, not what we shipped in twenty-four hours.

*31 words · ~13.3s @ 140 wpm · source: seed*

### Act 3 — 0:16.8
**On screen:** Never claim

> We never claim latency percentages, production user metrics, or benchmark artifacts. The demo is proof of concept — not a performance study.

*22 words · ~9.4s @ 140 wpm · source: seed*

## Chapter 9 — Outro

*Outro*

### Act 1 — 0:00.0
**On screen:** On-device dual pipeline

> One tap — on-device speech and sound analysis — captions and alerts in view. That is the pipeline we built in twenty-four hours.

*23 words · ~9.9s @ 140 wpm · source: seed*

### Act 2 — 0:07.7
**On screen:** Links

> Links are in the description — starting with the GitHub repo at github.com slash RDX-Rajat-Savdekar slash Aura-Vision-Pro. The sixty-second clip and full hackathon demo are there too.

*27 words · ~11.6s @ 140 wpm · source: seed*

### Act 3 — 0:14.8
**On screen:** 2nd place · Oct 2025

> Second place at LA Tech Week — October twenty twenty-five. Thanks for watching.

*13 words · ~5.6s @ 140 wpm · source: seed*
