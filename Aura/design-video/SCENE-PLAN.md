# Aura design video — scene plan (timestamps + tools)

> **Target runtime:** ~12:00 (may run ~12:45 with ch 0 POC + ch 7 HUD story — trim in edit)  
> **VO pace:** ~140 wpm · **Total word budget:** ~1,540–1,680  
> **Script:** [`SCRIPT.md`](SCRIPT.md) · **Story:** [`HACKATHON-STORY.md`](HACKATHON-STORY.md)

---

## Master timeline

| Ch | Start | End | Dur | Title | Words (target) | Script |
|----|-------|-----|-----|-------|----------------|--------|
| 0 | 0:00 | 1:05 | 1:05 | Problem + hackathon + sphere POC | ~150 | ✅ draft |
| 1 | 1:05 | 2:35 | 1:30 | On-device only | ~210 | ✅ draft |
| 2 | 2:35 | 4:05 | 1:30 | Build vs train | ~210 | ✅ draft |
| 3 | 4:05 | 5:55 | 1:50 | One tap, dual pipeline | ~257 | outline |
| 4 | 5:55 | 7:25 | 1:30 | Segmentation | ~210 | outline |
| 5 | 7:25 | 8:55 | 1:30 | Texture HUD vs 90 Hz | ~210 | outline |
| 6 | 8:55 | 9:55 | 1:00 | MainActor bridge | ~140 | outline |
| 7 | 9:55 | 11:25 | 1:30 | Directional pins → Iron Man HUD | ~245 | ✅ draft |
| 8 | 11:25 | 12:15 | 0:50 | Scale | ~117 | outline |
| 9 | 12:15 | 12:45 | 0:30 | Outro | ~70 | outline |
| | | | **~12:45** | | **~1,819** | |

*Ch 9 may extend to 12:00 if outro + links need air — steal 30 s from ch 8 in edit.*

---

## Tool legend

| Tag | Meaning |
|-----|---------|
| **M** | Manim animation (primary) |
| **U** | Unity viz recording |
| **B** | Demo B-roll from hackathon footage |
| **S** | Swift code snippet (Manim `Code` panel or Resolve overlay) |
| **—** | VO + on-screen text only |

**Primary** = drives the chapter visually. **Support** = ≤30% of chapter runtime.

---

## Chapter 0 — Problem + hackathon + sphere POC (`0:00–1:05`)

| Beat | Time | Primary | Support | Asset / scene file | Notes |
|------|------|---------|---------|-------------------|-------|
| Noisy room — missing speech + sounds | 0:00–0:15 | **M** | — | `scenes/scene0_problem.py` | Icons fade → `?` |
| Hackathon frame (24h, Oct 2025) | 0:15–0:25 | **M** | — | same scene | Clock + team roles |
| Solo code / teammates presented | 0:25–0:35 | **M** | — | same scene | Honesty beat |
| **Sphere POC** — first Vision Pro build | 0:35–0:48 | **M** or **U** | — | `SpherePOC` viz | Color word → color; loud → scale |
| Prototype disclaimer + video scope | 0:48–0:55 | **M** | **B** (2s) | `D1` flash | Proof hook |
| Aura one-liner (dual on-device) | 0:55–1:05 | **M** | — | pipeline teaser | Sets up ch 1–3 |

**Render estimate:** 1 Manim clip ~60 s (optional 5 s Unity sphere)  
**Unity:** optional `SpherePOC.unity` for color/scale demo  
**B-roll budget:** ≤5 s total

---

## Chapter 1 — On-device only (`1:05–2:35`)

| Beat | Time | Primary | Support | Asset / scene file | Notes |
|------|------|---------|---------|-------------------|-------|
| Device boundary | 1:05–1:20 | **M** | — | `scenes/scene1_on_device.py` | Headset inside box |
| Cloud temptation | 1:20–1:40 | **M** | — | `rejected.py` ghost path | Arrow to cloud |
| Rejection + reasons | 1:40–2:00 | **M** | — | strikethrough animation | Privacy + latency |
| Swift evidence | 2:00–2:15 | **S** | **M** | `on_device_speech.swift` | Highlight local-only |
| Locale trade-off + metrics | 2:15–2:35 | **M** | — | 7 flags + fact card | No ms claims |

**Render estimate:** 1 Manim ~80 s + snippet overlay in Resolve or baked in Manim  
**Unity:** none  
**B-roll:** none (keep diagram-clean)

---

## Chapter 2 — Build vs train (`2:35–4:05`)

| Beat | Time | Primary | Support | Asset / scene file | Notes |
|------|------|---------|---------|-------------------|-------|
| Fork: train vs integrate | 2:35–2:55 | **M** | — | `scenes/scene2_build_vs_train.py` | Two paths |
| Train path impractical | 2:55–3:15 | **M** | — | weeks vs hours bar | Dim left path |
| Apple ML boxes | 3:15–3:30 | **M** | — | Speech + SoundAnalysis | Not custom |
| Your pipeline work | 3:30–3:45 | **M** | — | preview pipeline | Bridge to ch 3 |
| Outcome + honesty | 3:45–4:05 | **M** | **B** (3s) | `D4`+`D5` | "Integrated, not trained" card |

**Render estimate:** 1 Manim ~85 s  
**Unity:** none  
**B-roll:** ≤5 s

---

## Chapter 3 — One tap, dual pipeline (`4:05–5:55`)

| Beat | Time | Primary | Support | Asset / scene file | Notes |
|------|------|---------|---------|-------------------|-------|
| Single AVAudioEngine tap | 3:50–4:10 | **M** | **S** | `scene3_dual_pipeline.py`, `tap_install.swift` | One mic icon |
| Split: Speech vs SoundAnalysis | 4:10–4:35 | **M** | — | `pipeline.py` | Parallel branches |
| Serial AnalysisQueue | 4:35–5:00 | **M** | **S** | `analysis_queue.swift` | Never block tap |
| Classifier gate 0.6 / 0.25s | 5:00–5:15 | **M** | — | small inset | Anti-flap |
| Locale hot-swap mention | 5:15–5:25 | **M** | **B** | `D6` optional | 7 locales |
| Proof montage | 5:25–5:40 | **B** | **M** | `D1`+`D3` | Dual pipeline works |

**Optional:** ~~Unity azimuth in ch 3~~ → moved to **ch 7** as rejected directional experiment

**Render estimate:** Manim ~100 s · B-roll ~15 s  
**Manim modules needed:** `pipeline.py`, `code_panel.py`, `thread_lane.py` (preview)

---

## Chapter 4 — Segmentation (`5:40–7:10`)

| Beat | Time | Primary | Support | Asset / scene file | Notes |
|------|------|---------|---------|-------------------|-------|
| formattedString failure | 5:40–6:00 | **M** | — | `scene4_segmentation.py` | Wall of text |
| Pause threshold 1.1s | 6:00–6:25 | **M** | **S** | `pause_threshold.swift` | Timeline gaps |
| Sentence splitter | 6:25–6:50 | **M** | **S** | `sentence_split.swift` | Abbreviation-aware |
| Readable captions result | 6:50–7:10 | **M** | **B** | `D2` multi-speaker | Before/after |

**Render estimate:** Manim ~80 s · B-roll ~8 s  
**Unity:** none (2D timeline is Manim strength)

---

## Chapter 5 — Texture HUD vs 90 Hz (`7:10–8:40`)

| Beat | Time | Primary | Support | Asset / scene file | Notes |
|------|------|---------|---------|-------------------|-------|
| 90 Hz loop problem | 7:10–7:30 | **M** | — | `scene5_texture_bake.py` | ViewAttachment rejected |
| Texture bake path | 7:30–7:55 | **M** | **S** | `debounce_texture.swift` | 100 ms debounce |
| Unity: jitter vs baked quad | 7:55–8:20 | **U** | **M** | `BillboardOverheadBug.unity` or bake compare scene | Side-by-side |
| Billboard NaN teaser | 8:20–8:35 | **U** or **M** | — | overhead camera bug | Optional shorten |
| Hold honesty | 8:35–8:40 | **M** | — | text card | 2D HUD shipped in demo |

**Render estimate:** Manim ~50 s · Unity ~25–30 s  
**First Unity build** — start here or ch 7

---

## Chapter 6 — MainActor bridge (`8:40–9:40`)

| Beat | Time | Primary | Support | Asset / scene file | Notes |
|------|------|---------|---------|-------------------|-------|
| ML callback off main thread | 8:40–8:55 | **M** | — | `scene6_mainactor.py`, `thread_lane.py` | Two lanes |
| @Published mutation rule | 8:55–9:15 | **M** | **S** | `mainactor_bridge.swift` | Highlight isolation |
| Why it matters for captions | 9:15–9:40 | **M** | **B** (optional) | `D1` | UI updates live |

**Render estimate:** Manim ~55 s  
**Unity:** none

---

## Chapter 7 — Directional pins → Iron Man HUD (`9:55–11:25`)

| Beat | Time | Primary | Support | Asset / scene file | Notes |
|------|------|---------|---------|-------------------|-------|
| Tried world-locked sound pins | 9:55–10:08 | **U** or **M** | — | `AzimuthRays.unity` | Rays to pins around room |
| Reject: no exact coords | 10:08–10:20 | **M** | — | wobble pin, `azimuth ≠ position` | Hardware limit |
| Reject: off-screen hazard | 10:20–10:32 | **M** | — | baby-cry behind FOV | Accessibility reason |
| Iron Man HUD pivot | 10:32–10:50 | **M** | **B** | `D1`/`D3` | Panel always in view |
| Azimuth computed, not in UI | 10:50–10:58 | **M** | — | pipeline inset grayed | Honesty |
| Spatial prototype + HEAD caveat | 10:58–11:15 | **U** | **M** | `SpatialCaptionRoom.unity` | Demoed not wired |
| Unity viz honesty line | 11:15–11:25 | **M** | — | text card | Swift ships, Unity explains |

**Render estimate:** Manim ~45 s · Unity ~35 s · B-roll ~10 s  
**Key narrative chapter** — sphere POC was ch 0; HUD *product* choice is here

---

## Chapter 8 — Scale (`10:40–11:30`)

| Beat | Time | Primary | Support | Asset / scene file | Notes |
|------|------|---------|---------|-------------------|-------|
| Prototype limits today | 10:40–11:00 | **M** | — | `scene8_scale.py` | Single user, no benchmarks |
| Product would change | 11:00–11:20 | **M** | — | two-column arch | Locale CDN, observability |
| Never claim list | 11:20–11:30 | **M** | — | red stamp | No latency % |

**Render estimate:** Manim ~50 s  
**Unity:** none

---

## Chapter 9 — Outro (`11:30–12:00`)

| Beat | Time | Primary | Support | Asset / scene file | Notes |
|------|------|---------|---------|-------------------|-------|
| Recap one line | 11:30–11:40 | **M** | — | `scene9_outro.py` | On-device dual pipeline |
| Links | 11:40–11:55 | **M** | — | repo · 60s · full demo | Match description |
| End card | 11:55–12:00 | **M** | — | 2nd place · Oct 2025 | |

**Render estimate:** Manim ~25 s

---

## Production summary

### Manim scenes to build (in order)

| Priority | File | Chapter | Est. clip |
|----------|------|---------|-----------|
| 1 | `scene0_problem.py` | 0 | 65 s |
| 2 | `scene1_on_device.py` | 1 | 90 s |
| 3 | `scene2_build_vs_train.py` | 2 | 90 s |
| 4 | `scene3_dual_pipeline.py` | 3 | 100 s |
| 5 | `scene4_segmentation.py` | 4 | 90 s |
| 6 | `scene5_texture_bake.py` | 5 | 50 s |
| 7 | `scene6_mainactor.py` | 6 | 60 s |
| 8 | `scene8_scale.py` | 8 | 50 s |
| 9 | `scene9_outro.py` | 9 | 25 s |

**Toolkit before scene 1:** `theme.py`, `code_panel.py` · add `rejected.py` before scene 1 · `pipeline.py` before scene 3

### Unity scenes to build

| Priority | Scene | Chapter | Est. clip | When |
|----------|-------|---------|-----------|------|
| 1 | `SpatialCaptionRoom.unity` | 7 | 20 s | After Manim ch 2–3 |
| 2 | `AzimuthRays.unity` (rejected pins) | 7 | 10 s | Same session — strikethrough in edit |
| 3 | `BillboardOverheadBug.unity` or bake compare | 5 | 25 s | Same session |
| 4 | `SpherePOC.unity` (optional) | 0 | 5 s | Only if Manim sphere is hard |

### B-roll allocation (total ~45–60 s across video)

| Clip | Chapters | Max use |
|------|----------|---------|
| `D1` | 0, 3, 6 | 15 s |
| `D2` | 4 | 8 s |
| `D3` | 3 | 5 s |
| `D4`, `D5` | 2, 3 | 8 s |
| `D6` | 3, 7 | 10 s |

Path: `Aura/clips/D*.mp4`

---

## Resolve assembly order (per chapter)

```
[Manim ch N] → [Unity beats if any] → [Swift snippet inserts] → [B-roll inserts] → VO track
```

Music bed: documentary track @ 0.05–0.07 under VO (same as 60s).

---

## Decision log

| Date | Decision | Rationale |
|------|----------|-----------|
| 2026-07-01 | Unity for ch 5 + 7, not ch 0–2 | Flat diagrams first; learn Manim toolkit |
| 2026-07-01 | Azimuth Unity in ch 7 not ch 3 | Directional pins = rejected experiment + HUD pivot |
| 2026-07-01 | Sphere POC in ch 0 | First Vision Pro pipeline shakedown |
| 2026-07-01 | B-roll sparse in ch 1 | Keep architecture diagram readable |
| 2026-07-01 | ch 0–2 script before Manim render | 3b1b rule |

---

## Next actions

1. **Read aloud** `SCRIPT.md` ch 0–2 — trim to time
2. **Build** `aura_manim/theme.py` + `code_panel.py` + `rejected.py`
3. **Implement** `scene0_problem.py` first Manim scene
4. **Draft** `SCRIPT.md` ch 3 after scene 0–2 VO lock
