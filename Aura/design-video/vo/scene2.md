# Chapter 2 — Build vs train

> **YouTube chapter:** *Build vs train*  
> **Render:** [`output/scene2_chapter2_2160p60.mp4`](../output/scene2_chapter2_2160p60.mp4)  
> **Total duration:** `0:55.5` (55.5 s measured) · **SCENE-PLAN target:** `2:35` → `4:05` (~90 s)  
> **VO status:** draft (read-aloud pending) · **Measured:** 55.5 s — **add ~35 s wait** after read-aloud or trim SCRIPT  
> **Preview:** `manim -ql scenes/scene2_full.py Scene2Full`

**Source acts:** `aura_manim/scenes/scene2_act{1…6}.py`  
**Script seed:** [`SCRIPT.md`](../SCRIPT.md) Chapter 2  
**Prev chapter:** [`scene1.md`](scene1.md) — on-device only (concat ✅)  
**Toolkit:** `components/workflow.py`, `components/inbox.py`, `broll.py`, `rejected.py`, `components/labels.py`

---

## Act timeline (2160p60 · 2026-07-02)

| Act | Start | End | Dur | On-screen label | Manim file |
|-----|-------|-----|-----|-----------------|------------|
| 1 | 0:00.0 | 0:08.2 | 8.2s | Decision 2: build vs train | `scene2_act1.py` |
| 2 | 0:08.2 | 0:17.5 | 9.3s | Apple Speech + SoundAnalysis | `scene2_act2.py` |
| 3 | 0:17.5 | 0:26.6 | 9.1s | Train: weeks | `scene2_act3.py` |
| 4 | 0:26.6 | 0:35.2 | 8.6s | Our work: pipeline + UI | `scene2_act4.py` |
| 5 | 0:35.2 | 0:47.6 | 12.4s | 2nd place · working demo | `scene2_act5.py` |
| 6 | 0:47.6 | 0:55.5 | 7.9s | Integrated, not trained | `scene2_act6.py` |

**Concat:** [`output/scene2_concat.txt`](../output/scene2_concat.txt)

---

## Story arc (one sentence)

We did **not** train custom models — we integrated Apple's on-device Speech + SoundAnalysis and spent the hackathon on pipeline, segmentation, and UI engineering.

**VO checkpoint:** Say *"I did not train any machine-learning model"* once, clearly (act 1).

**Honesty:** Demo looks like "ML magic" — this chapter names what's Apple vs what's yours.

---

## Locked decisions (2026-07-02)

| Question | Decision |
|----------|----------|
| Act count | **6 acts** — fork → **inbox reveal** → train dim → pipeline preview → B-roll → honesty card |
| Fork geometry | **Vertical split** — left "Train custom model" / right "Integrate Apple ML" (not Y-fork; no device glyph) |
| Train path visual | Left branch **dims + red cross**; **`components/timeline_bar.py`** — weeks vs hours |
| Act 2 — Apple ML beat | **Manim inbox skit** — mail icon + 1 unread → cursor click → message *"Apple released new Core ML models"* → expand to Speech + SoundAnalysis |
| Pipeline preview | Lightweight stub only — full diagram is ch 3 (`pipeline.py` TBD) |
| B-roll | **~6 s** montage: `D4` siren + `D5` clap @ **3 s each** via `broll.py` |
| Unity | **None** — Manim + clips only |

---

## Act map

| Act | SCENE-PLAN beat | Target | On-screen label | File (future) |
|-----|-----------------|--------|-----------------|---------------|
| 1 | Fork: train vs integrate | ~15 s | Decision 2: build vs train | `scene2_act1.py` |
| 2 | Apple ML inbox reveal | ~15 s | Apple Speech + SoundAnalysis | `scene2_act2.py` |
| 3 | Train path impractical | ~15 s | Train: weeks | `scene2_act3.py` |
| 4 | Our pipeline work | ~15 s | Our work: pipeline + UI | `scene2_act4.py` |
| 5 | Outcome + proof | ~15 s | 2nd place · working demo | `scene2_act5.py` |
| 6 | Honesty card | ~15 s | Integrated, not trained | `scene2_act6.py` |

*Targets sum ~90 s — tune `self.wait()` after first `-ql` full scene.*

---

## Act 1 — Decision fork (train vs integrate)

**VO seed:** *Second decision: we did not train any machine-learning model. I need to say that clearly because the demo looks like "ML magic."*

```
PLAY CHECKLIST — Scene2Act1Layout
  STEP   WHAT YOU SHOULD SEE ON SCREEN
  ────   ─────────────────────────────────────────────────────────────────
  1      Vertical split (center): two columns
  2      + Left column: "Train custom model"
  3      + Right column: "Integrate Apple ML" (accent / selected)
  4      + Bottom label: "Decision 2: build vs train"

──────────────────────────────────────────────────────────────────────────────
PLAY CHECKLIST — Scene2Act1 (motion · target ~15 s)

  PLAY   WHAT YOU SHOULD SEE                         NARRATION / MEANING
  ────   ─────────────────────────────────────────   ─────────────────────────────
  1      Fork + two branch labels fade in            Decision 2 framing
  2      Right branch highlights (accent)            Integrate path = our choice
  3      Bottom label fades in                       Decision 2: build vs train
  wait   Hold — fork diagram                          VO: "did not train any model"
  4      (optional) fork fades at start of act 2      Inbox beat follows fork
```

**Locked:** **vertical split** fork — two columns, left train / right integrate. No Y-fork; no Vision Pro reuse from ch 1.

---

## Act 2 — Inbox reveal (Apple shipped new models)

**VO seed:** *Apple had recently shipped strong on-device models: Speech for transcription, SoundAnalysis for environmental classes — hundreds of built-in labels. Good enough to prove the product idea.*

**Concept:** Quick Manim skit — you're mid-hackathon, one unread mail arrives, you click it, the subject line is the punchline. Then the message **expands** into the two frameworks we actually integrated.

```
PLAY CHECKLIST — Scene2Act2Layout
  STEP   WHAT YOU SHOULD SEE ON SCREEN
  ────   ─────────────────────────────────────────────────────────────────
  1      Mail/inbox icon (dock-style or menu-bar glyph) — badge "1"
  2      + Mouse cursor (simple arrow pointer)
  3      + Collapsed message row (preview): "Apple released new Core ML models"
  4      + Expanded card (hidden in layout plop): Speech + SoundAnalysis chips
  5      + Bottom label: "Apple Speech + SoundAnalysis"

──────────────────────────────────────────────────────────────────────────────
PLAY CHECKLIST — Scene2Act2 (motion · target ~15 s)

  PLAY   WHAT YOU SHOULD SEE                         NARRATION / MEANING
  ────   ─────────────────────────────────────────   ─────────────────────────────
  0      (if chained) fork from act 1 fades out      Decision beat → inbox skit
  1      Inbox fades in with unread badge "1"        Something landed during hackathon
  2      Cursor moves to inbox · click (Indicate)    You check mail
  3      Message slides open — subject line holds    "Apple released new Core ML models"
  4      Card expands: Speech · SoundAnalysis        The actual on-device APIs we used
         + subtitle: "hundreds of built-in labels"
  5      Bottom label fades in                       Apple Speech + SoundAnalysis
  wait   Hold — expanded card                        VO: good enough for product proof
  6      Fade out                                    → act 3
```

**Locked:** all **Manim-native** — no real macOS capture. Build in **`components/inbox.py`**:
- `inbox_icon()` — SVG `mail.svg` + red badge dot + `"1"`
- `mail_message(subject, body_lines)` — glass card, macOS-adjacent typography
- `cursor_pointer()` — small filled triangle + stem, or simple `Arrow` tip
- `play_inbox_reveal(scene, subject=...)` — cursor path + click pulse + `Transform` collapsed → expanded

**Expanded payload (after click):**
- **Speech** — transcription (`mic` or `audio-wave` icon)
- **SoundAnalysis** — env classes (`audio-wave` or new `sound-analysis.svg`)
- Optional chip: *hundreds of built-in labels*

**Tone:** one beat of levity between the fork seriousness and the train-path rejection — keep message **one line**, cursor click **< 1 s**, don't over-cartoon.

---

## Act 3 — Train path impractical

**VO seed:** *The left path — collect data, label sounds, train, export Core ML, debug — is a multi-week project. We had twenty-four hours.*

```
PLAY CHECKLIST — Scene2Act3Layout
  STEP   WHAT YOU SHOULD SEE ON SCREEN
  ────   ─────────────────────────────────────────────────────────────────
  1      Fork — left branch bright
  2      + Timeline bar: "weeks" (long) vs "hours" (short, accent)
  3      + Left branch dims; optional red cross on train steps
  4      + Bottom label: "Train: weeks"

──────────────────────────────────────────────────────────────────────────────
PLAY CHECKLIST — Scene2Act3 (motion · target ~15 s)

  PLAY   WHAT YOU SHOULD SEE                         NARRATION / MEANING
  ────   ─────────────────────────────────────────   ─────────────────────────────
  1      Fork fades in                               Same decision, after inbox beat
  2      Timeline bar grows: weeks >> hours            24h constraint
  3      Left branch fades / cross                     Train path rejected
  4      Bottom label fades in                         Train: weeks
  wait   Hold — dim left, hours bar visible            VO: multi-week vs 24h
  5      Fade out                                    → act 4
```

**Locked:** **`components/timeline_bar.py`** — reusable weeks vs hours bar.

---

## Act 4 — Pipeline + UI (preview ch 3)

**VO seed:** *My job wasn't training. It was integration engineering: one microphone tap feeding two consumers, realtime discipline, caption segmentation, UI that doesn't choke at ninety hertz.*

```
PLAY CHECKLIST — Scene2Act4Layout
  STEP   WHAT YOU SHOULD SEE ON SCREEN
  ────   ─────────────────────────────────────────────────────────────────
  1      Zoomed pipeline stub (preview of ch 3):
         mic tap → [Speech | SoundAnalysis] → queue → UI
  2      + Chip labels: "tap" · "queue" · "UI @ 90 Hz"
  3      + Bottom label: "Our work: pipeline + UI"

──────────────────────────────────────────────────────────────────────────────
PLAY CHECKLIST — Scene2Act4 (motion · target ~15 s)

  PLAY   WHAT YOU SHOULD SEE                         NARRATION / MEANING
  ────   ─────────────────────────────────────────   ─────────────────────────────
  1      Pipeline stub draws (Create / LaggedStart)  Integration engineering
  2      Chips fade in on key nodes                  tap · queue · UI
  3      Bottom label fades in                       Our work: pipeline + UI
  wait   Hold — stub + chips                         Bridge to chapter 3
  4      Fade out                                    → act 5
```

**Note:** full `pipeline.py` lands in ch 3 — here only a **teaser** (4–5 nodes max).

---

## Act 5 — Outcome + B-roll proof

**VO seed:** *If we'd spent the hackathon training, we'd have a model slide and no working app. We traded ML research for a working accessibility prototype — and placed second.*

```
PLAY CHECKLIST — Scene2Act5Layout
  STEP   WHAT YOU SHOULD SEE ON SCREEN
  ────   ─────────────────────────────────────────────────────────────────
  1      Title card: "2nd place · working demo"
  2      + B-roll slot (~6 s): D4 siren + D5 clap @ 3 s each
  3      + Bottom label: "2nd place · working demo"

──────────────────────────────────────────────────────────────────────────────
PLAY CHECKLIST — Scene2Act5 (motion · target ~15 s)

  PLAY   WHAT YOU SHOULD SEE                         NARRATION / MEANING
  ────   ─────────────────────────────────────────   ─────────────────────────────
  1      Title / card fades in                       Outcome framing
  2      B-roll montage plays (D4 → D5)              Sound classes actually work
  3      Bottom label (if not on card)               2nd place · working demo
  wait   Hold on last B-roll frame or card            VO: traded research for demo
  4      Fade out                                    → act 6
```

**B-roll:** extend `broll.py` with `play_montage(scene, [D4, D5], duration=3.0)` or two sequential flashes.

---

## Act 6 — Honesty card

**VO seed:** *Honest scope: I integrated Apple's models. The engineering story is everything around them.*

```
PLAY CHECKLIST — Scene2Act6Layout
  STEP   WHAT YOU SHOULD SEE ON SCREEN
  ────   ─────────────────────────────────────────────────────────────────
  1      Bold honesty card (center):
         "Integrated, not trained"
  2      + Subtitle: "Engineering = pipeline · segmentation · UI"
  3      + Bottom label: "Integrated, not trained"

──────────────────────────────────────────────────────────────────────────────
PLAY CHECKLIST — Scene2Act6 (motion · target ~15 s)

  PLAY   WHAT YOU SHOULD SEE                         NARRATION / MEANING
  ────   ─────────────────────────────────────────   ─────────────────────────────
  1      Honesty card fades in (accent border)       Scope lock
  2      Subtitle fades in                           What's actually yours
  3      Bottom label fades in                       Integrated, not trained
  wait   Hold ~2 s minimum                           VO checkpoint — land clearly
  4      Fade out                                    End chapter 2
```

**Reuse:** `fact_card()` pattern from `locale_picker.py` with WARN or MERGE_OK accent.

---

## Toolkit gaps (build with acts)

| Module | Purpose |
|--------|---------|
| `components/fork.py` | **Vertical split** two-branch decision diagram (ch 2, maybe ch 7) |
| `components/timeline_bar.py` | weeks vs hours comparison bar ✅ |
| `components/inbox.py` | Mail icon + badge + cursor click + message expand (act 3 skit) |
| `components/pipeline_stub.py` | 5-node teaser; superseded by `pipeline.py` in ch 3 |
| `broll.py` | Add D4+D5 montage helper |
| `assets/icons/mail.svg` | Inbox glyph (stroke, Lucide-style) |
| `assets/icons/sound-analysis.svg` | Optional — SoundAnalysis chip in expanded card |

---

## Your edit checklist

- [x] Act count: **6 acts**
- [x] Fork style: **vertical split**
- [x] Act 3: **inbox click reveal** (Manim skit)
- [x] Timeline bar: **`timeline_bar.py`**
- [ ] B-roll: D4+D5 only, or add D3 whisper beat?
- [ ] Pipeline stub detail level — how many nodes before ch 3 owns it?
- [ ] Inbox copy exact wording — subject line OK as *"Apple released new Core ML models"*?
- [x] Target durations — tune `self.wait()` after read-aloud (all acts `-ql` OK)

**Shipped:** `scene2_act{1…6}.py` · `scene2_full.py` · toolkit below (2026-07-02).
