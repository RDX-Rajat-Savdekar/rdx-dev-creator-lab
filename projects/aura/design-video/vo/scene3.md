# Chapter 3 — One tap, dual pipeline

> **YouTube chapter:** *One tap, dual pipeline*  
> **Render:** [`output/scene3_chapter3_2160p60.mp4`](../output/scene3_chapter3_2160p60.mp4)  
> **Total duration:** `0:56.8` (56.8 s measured) · **SCENE-PLAN target:** `4:05` → `5:55` (~110 s)  
> **VO status:** draft (read-aloud pending) · **Measured:** 56.8 s — **add ~53 s wait** after read-aloud or trim SCRIPT  
> **Preview:** `manim -ql scenes/scene3_full.py Scene3Full`

**Source acts:** `aura_manim/scenes/scene3_act{1…6}.py`  
**Script seed:** [`SCRIPT.md`](../SCRIPT.md) Chapter 3 (TBD)  
**Prev chapter:** [`scene2.md`](scene2.md) — build vs train (concat ✅)

---

## Act timeline (2160p60 · 2026-07-02)

| Act | Start | End | Dur | On-screen label | Manim file |
|-----|-------|-----|-----|-----------------|------------|
| 1 | 0:00.0 | 0:09.1 | 9.1s | One AVAudioEngine tap | `scene3_act1.py` |
| 2 | 0:09.1 | 0:17.7 | 8.6s | Speech + SoundAnalysis | `scene3_act2.py` |
| 3 | 0:17.7 | 0:27.4 | 9.7s | Never block the tap | `scene3_act3.py` |
| 4 | 0:27.4 | 0:35.4 | 8.0s | Anti-flap: 0.6 · 0.25 s | `scene3_act4.py` |
| 5 | 0:35.4 | 0:45.0 | 9.7s | 7 locales · hot-swap | `scene3_act5.py` |
| 6 | 0:45.0 | 0:56.8 | 11.7s | Dual pipeline · live | `scene3_act6.py` |

**Concat:** [`output/scene3_concat.txt`](../output/scene3_concat.txt)

---

## Story arc

One `AVAudioEngine` tap feeds **Speech** and **SoundAnalysis** in parallel. Analysis runs on a **serial queue** so the realtime callback never blocks. Classifier **gating** stops label flapping; **locale hot-swap** works live. B-roll proves both caption and whisper paths.

---

## Locked decisions (2026-07-02)

| Question | Decision |
|----------|----------|
| Act count | **6 acts** — tap → dual pipeline → AnalysisQueue → classifier gate → locale → proof montage |
| Pipeline diagram | Reuse **`components/workflow.py`** via `components/pipeline.py` |
| Queue visual | **`components/thread_lane.py`** — tap lane vs `com.aura.AnalysisQueue` |
| Classifier | **`components/classifier_gate.py`** — ≥ 0.6 confidence · 0.25 s throttle |
| Locale | **`locale_hotswap_panel()`** — Japanese selected + **D6** 2.5 s flash |
| Proof B-roll | **D1** (live captions) + **D3** (whisper) @ 3 s each |
| Unity | **None** — azimuth experiment moved to ch 7 |

---

## Act map

| Act | SCENE-PLAN beat | Target | On-screen label | File |
|-----|-----------------|--------|-----------------|------|
| 1 | Single AVAudioEngine tap | ~15 s | One AVAudioEngine tap | `scene3_act1.py` |
| 2 | Speech + SoundAnalysis split | ~15 s | Speech + SoundAnalysis | `scene3_act2.py` |
| 3 | Serial AnalysisQueue | ~15 s | Never block the tap | `scene3_act3.py` |
| 4 | Classifier gate | ~15 s | Anti-flap: 0.6 · 0.25 s | `scene3_act4.py` |
| 5 | Locale hot-swap | ~15 s | 7 locales · hot-swap | `scene3_act5.py` |
| 6 | Proof montage | ~15 s | Dual pipeline · live | `scene3_act6.py` |

---

## Act 1 — Single tap

**VO seed:** *One microphone tap on the AVAudioEngine input node — every buffer flows through a single installTap callback.*

```
PLAY CHECKLIST — Scene3Act1
  1      Mic icon (accent ring) + tap_install.swift panel
  2      Highlight installTap + processAudioBuffer lines
  3      Bottom label: One AVAudioEngine tap
```

**Snippet:** `code_snippets/tap_install.swift`

---

## Act 2 — Dual pipeline

**VO seed:** *That one tap fans out to Apple's Speech framework for transcription and SoundAnalysis for environmental classes — parallel on-device consumers.*

```
PLAY CHECKLIST — Scene3Act2
  1      Full workflow diagram (Capture → ML → Buffer → Present)
  2      Stages fade in L→R; fork/merge edges draw
  3      Bottom label: Speech + SoundAnalysis
```

**Component:** `components/pipeline.py` → `dual_pipeline_group()`

---

## Act 3 — AnalysisQueue

**VO seed:** *Heavy work never runs inside the tap. We dispatch to a serial queue — com.aura.AnalysisQueue — so analysis can't stall realtime audio.*

```
PLAY CHECKLIST — Scene3Act3
  1      Thread lane diagram (tap ticks → async arrow → serial jobs)
  2      Indicate tap lane; fade in analysis_queue.swift
  3      Highlight DispatchQueue label + async block
  4      Bottom label: Never block the tap
```

**Snippet:** `code_snippets/analysis_queue.swift`

---

## Act 4 — Classifier gate

**VO seed:** *Environmental sounds flap labels. We gate on 0.6 confidence and throttle updates to 0.25 seconds.*

```
PLAY CHECKLIST — Scene3Act4
  1      Anti-flap card: confidence ≥ 0.6 · 0.25 s throttle
  2      Flaky labels dimmed; stable label kept
  3      Bottom label: Anti-flap: 0.6 · 0.25 s
```

---

## Act 5 — Locale hot-swap

**VO seed:** *Seven recognition languages in the picker — switch without restarting the engine. Demo flashes Japanese locale live.*

```
PLAY CHECKLIST — Scene3Act5
  1      Locale panel (Japanese selected) + chip "7 locales · no engine restart"
  2      Fade to D6_japanese-locale.mp4 (~2.5 s)
  3      Bottom label: 7 locales · hot-swap
```

---

## Act 6 — Proof montage

**VO seed:** *Live English captions and whisper detection — both pipelines working in the same session.*

```
PLAY CHECKLIST — Scene3Act6
  1      D1 live captions (3 s) → D3 whisper detected (3 s)
  2      Bottom label: Dual pipeline · live
```

---

## New toolkit (ch 3)

| Module | Role |
|--------|------|
| `components/split_layout.py` | Two-pane visual + code layout (scale-to-fit) |
| `components/pipeline.py` | Full dual-pipeline diagram (wraps `workflow.py`) |
| `components/thread_lane.py` | Tap vs AnalysisQueue lanes |
| `components/classifier_gate.py` | 0.6 / 0.25 s anti-flap card |
| `locale_picker.locale_hotswap_*` | Compact JA-selected picker for ch 3 |
| `broll.py` | + `D3_WHISPER`, `D6_JAPANESE` |

---

## Status

- [x] Code + `-ql` full preview
- [x] `-qk` per act → concat → measured timestamps
- [ ] VO draft + read-aloud
- [ ] Extend `SCRIPT.md` ch 3 narration table
