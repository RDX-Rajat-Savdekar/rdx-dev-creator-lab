# Chapter 1 — On-device only

> **YouTube chapter:** *On-device only*  
> **Render:** [`output/scene1_chapter1_2160p60.mp4`](../output/scene1_chapter1_2160p60.mp4)  
> **Total duration:** `0:42.8` (42.8 s measured) · **SCENE-PLAN target:** `1:05` → `2:35` (~90 s)  
> **VO status:** draft (read-aloud pending) · **Measured:** 42.8 s — **add ~47 s wait** after read-aloud or trim SCRIPT  
> **Pace target:** ~140 wpm (~100 words fits 43 s brisk)

**Source acts:** `aura_manim/scenes/scene1_act{1…5}.py`  
**Script seed:** [`SCRIPT.md`](../SCRIPT.md) Chapter 1  

---

## Locked decisions (shipped 2026-07-02)

| Question | Decision |
|----------|----------|
| Vision Pro glyph | MIT stroke SVG → `assets/icons/vision-pro.svg` via `load_icon()` |
| Acts 1→3 continuity | Device stays on screen; cloud path dies in act 3 |
| Rejection visual | **`reject_cross()`** — red `Cross` on ghost arrow + cloud dims (not strikethrough) |
| Swift snippet | `code_panel.py` + `code_snippets/on_device_speech.swift` |
| Act 5 locales | All 7 picker rows; glass panel; trade-off inset + fact card |

---

## Act timeline (2160p60 · 2026-07-02)

| Act | Start | End | Dur | On-screen label | Manim file |
|-----|-------|-----|-----|-----------------|------------|
| 1 | 0:00.0 | 0:07.7 | 7.7s | Decision 1: on-device only | `scene1_act1.py` |
| 2 | 0:07.7 | 0:16.8 | 9.1s | Temptation: cloud ASR | `scene1_act2.py` |
| 3 | 0:16.8 | 0:26.4 | 9.7s | Rejected: privacy + latency | `scene1_act3.py` |
| 4 | 0:26.4 | 0:33.9 | 7.5s | SFSpeechRecognizer | `scene1_act4.py` |
| 5 | 0:33.9 | 0:42.8 | 8.9s | 0 external deps · ~1,475 LOC | `scene1_act5.py` |

*Refresh:* `python Aura/design-video/vo/build_act_timestamps.py --chapter 1 --markdown`

---

## Act descriptions

### Act 1 — Device boundary (`0:00` → `0:08`)

**What the viewer sees**

- Rounded device boundary box (accent stroke) + Vision Pro SVG inside  
- Bottom label: **Decision 1: on-device only**

**Story beat**

- Decision 1: the trust boundary is the headset — no audio leaves the device.

---

### Act 2 — Cloud temptation (`0:08` → `0:17`)

**What the viewer sees**

- Same device box (chained from act 1)  
- Cloud SVG (right) + horizontal dashed ghost arrow + **network fallback** label  
- Bottom label: **Temptation: cloud ASR**

**Story beat**

- The hackathon cheat path: cloud ASR is faster to demo and often more accurate.

---

### Act 3 — Rejection (`0:17` → `0:26`)

**What the viewer sees**

- Temptation diagram on screen → **red cross** on connector; cloud + arrow dim  
- Chips: **privacy** · **latency**  
- Device box pulses (stays bright)  
- Bottom label: **Rejected: privacy + latency**  
- Cloud path fades out; device fades for act 4

**Story beat**

- Explicit rejection with reasons; on-device path wins.

---

### Act 4 — Swift evidence (`0:26` → `0:34`)

**What the viewer sees**

- Code window: `on_device_speech.swift` (3 lines, no comments)  
- Highlight: `requiresOnDeviceRecognition` + `shouldReportPartialResults`  
- Bottom label: **SFSpeechRecognizer**

**Story beat**

- Code proof — no network fallback in the prototype.

---

### Act 5 — Locale + metrics (`0:34` → `0:43`)

**What the viewer sees**

- visionOS **Recognition Language** glass panel (7 rows, EN-US checked; title + Done inside box)  
- Inset: **Trade-off: locale models**  
- Fact card: **0 external deps · ~1,475 LOC** / Swift · Apple frameworks only  
- Bottom label: **0 external deps · ~1,475 LOC**

**Story beat**

- Honest product constraint (per-locale models) + repo facts.

---

## VO draft (first read-aloud)

Read over [`scene1_chapter1_2160p60.mp4`](../output/scene1_chapter1_2160p60.mp4). Adjust pacing before recording.

### Act 1 (`0:00` → `0:08`) — 7.7 s · ~18 words

> First decision: everything stays on the device. No cloud speech API — no uploading audio.

*Land “on the device” as the boundary box completes (~0:02). Use hold (~0:04–0:08) for breathing or slower delivery.*

---

### Act 2 (`0:08` → `0:17`) — 9.1 s · ~22 words

> The hackathon temptation is to cheat — send audio to a network recognizer when on-device struggles. Faster to demo, often more accurate.

*Hit “network recognizer” as the ghost arrow draws (~0:10). “Temptation: cloud ASR” label ~0:13.*

---

### Act 3 (`0:17` → `0:26`) — 9.7 s · ~28 words

> We rejected that. Audio leaving Vision Pro kills privacy — latency becomes whatever the network feels like. For accessibility, unpredictable delay is as bad as wrong text.

*Sync “rejected” to red cross (~0:18). Name **privacy** / **latency** as chips appear (~0:20).*

---

### Act 4 (`0:26` → `0:34`) — 7.5 s · ~18 words

> So we committed to Apple's on-device Speech framework — SFSpeechRecognizer — with no network fallback in the code.

*Highlight sweep ~0:28. Bottom label ~0:30.*

---

### Act 5 (`0:34` → `0:43`) — 8.9 s · ~32 words

> Trade-off: speech models are per locale — users need the language pack installed. Product constraint, not a bug. Zero external dependencies — Swift, Apple frameworks, about fifteen hundred lines.

*Picker ~0:35 · trade-off note ~0:37 · fact card ~0:38 · bottom label ~0:40.*

---

**Chapter totals:** ~118 words · ~50 s at 140 wpm · **42.8 s clip** → read brisk **or** extend `self.wait()` in each act (~9 s/act average target).

**Plain export for teleprompter:** concatenate blocks above, or `tools/prompter.html`.

---

## Trim notes

| Issue | Suggested fix |
|-------|----------------|
| **43 s vs 90 s SCENE-PLAN** | After read-aloud: add `self.wait()` per act to land ~18 s/act (~90 s total), **or** accept tight chapter and update SCENE-PLAN |
| Act 1 hold | `scene1_act1.py` — currently ~5.5 s wait; bump to ~12 s if VO needs room |
| Act 2 hold | `scene1_act2.py` — `scene.wait(5.5)` → ~10 s |
| Act 3 hold | `scene1_act3.py` — `scene.wait(5.0)` → ~12 s |
| Act 4 hold | `scene1_act4.py` — `scene.wait(4.5)` → ~10 s |
| Act 5 hold | `scene1_act5.py` — `scene.wait(5.5)` → ~12 s |
| SCRIPT.md act 3 row | Still says “strikethrough” — update to “red cross” when narration locks |

---

## Recording notes

- **Punch-ins:** Per act OK — align in Resolve to table above  
- **Music:** Documentary bed @ 0.05–0.07 under VO (post-assembly)  
- **Next:** [`scene2.md`](scene2.md) — build vs train (planning)
