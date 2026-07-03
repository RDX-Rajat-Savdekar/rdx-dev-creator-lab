# Chapter 4 — Segmentation

> **YouTube chapter:** *Segmentation*  
> **Render:** [`output/scene4_chapter4_2160p60.mp4`](../output/scene4_chapter4_2160p60.mp4)  
> **Total duration:** `0:36.2` (36.2 s measured) · **SCENE-PLAN target:** `5:55` → `7:25` (~90 s)  
> **VO status:** draft (read-aloud pending) · **Measured:** 36.2 s — **add ~54 s wait** after read-aloud or trim SCRIPT  
> **Preview:** `manim -ql scenes/scene4_full.py Scene4Full`

**Source acts:** `aura_manim/scenes/scene4_act{1…4}.py`  
**Script seed:** [`SCRIPT.md`](../SCRIPT.md) Chapter 4 (TBD)  
**Prev chapter:** [`scene3.md`](scene3.md) — one tap, dual pipeline (concat ✅)

---

## Act timeline (2160p60 · 2026-07-03)

| Act | Start | End | Dur | On-screen label | Manim file |
|-----|-------|-----|-----|-----------------|------------|
| 1 | 0:00.0 | 0:07.5 | 7.5s | Wall of text | `scene4_act1.py` |
| 2 | 0:07.5 | 0:17.2 | 9.7s | Pause gap: 1.1 s | `scene4_act2.py` |
| 3 | 0:17.2 | 0:26.4 | 9.2s | Sentence splitter | `scene4_act3.py` |
| 4 | 0:26.4 | 0:36.2 | 9.9s | Readable captions | `scene4_act4.py` |

**Concat:** [`output/scene4_concat.txt`](../output/scene4_concat.txt)

---

## Story arc

Apple Speech gives us a raw `formattedString` — one long blob with no pauses, no sentence boundaries, unreadable on screen during live conversation. We fix it with a **two-layer split**:

1. **Temporal layer** — pause gaps ≥ **1.1 s** start a new utterance (breath between speakers or thoughts).
2. **Grammatical layer** — abbreviation-aware sentence splitting keeps `"Dr."` and `"e.g."` intact while breaking real sentence boundaries.

The payoff is **readable caption chunks** instead of a wall of text. **D2** b-roll proves the flow with a second speaker.

---

## Locked decisions (2026-07-03)

| Question | Decision |
|----------|----------|
| Act count | **4 acts** — problem → temporal → grammatical → before/after + proof |
| Layout acts 2–3 | **`components/split_layout.py`** — visual top, Swift bottom |
| Text spacing | `disable_ligatures=True`, explicit line breaks in cards, no crush-scale on wall |
| Before/after flow | Wall **LEFT** → arrow **L→R** → readable chunks **RIGHT** |
| Proof B-roll | **D2** second speaker @ 3 s |

---

## Act map

| Act | SCENE-PLAN beat | Target | On-screen label | File |
|-----|-----------------|--------|-----------------|------|
| 1 | formattedString problem | ~15 s | Wall of text | `scene4_act1.py` |
| 2 | Pause threshold | ~15 s | Pause gap: 1.1 s | `scene4_act2.py` |
| 3 | Sentence splitter | ~15 s | Sentence splitter | `scene4_act3.py` |
| 4 | Before/after + D2 | ~15 s | Readable captions | `scene4_act4.py` |

---

## Act 1 — Wall of text

**VO seed:** *Speech recognition returns a formatted string — one continuous dump. No pauses, no sentences, no structure. During a live conversation it becomes an unreadable wall of text on screen.*

**What the animation shows:** Full-width dense paragraph inside a red-bordered panel tagged `formattedString → UI`. This is the **before** state — everything at once.

```
PLAY CHECKLIST — Scene4Act1
  1      Fade in wall_of_text() — multi-line sample, readable font
  2      Tag above panel: formattedString → UI (warn stroke)
  3      Bottom label: Wall of text
  4      Hold ~5.5 s
```

**Component:** `components/segmentation.py` → `wall_of_text(compact=False)`

---

## Act 2 — Pause threshold

**VO seed:** *First layer: temporal segmentation. When the speaker pauses longer than 1.1 seconds, we treat that as a new utterance — a breath between thoughts or between speakers.*

**What the animation shows:** Top pane — timeline of speech token blocks with **‖** markers and `>1.1s` labels on wide gaps. Bottom pane — `pause_threshold.swift` with highlighted threshold constant.

```
PLAY CHECKLIST — Scene4Act2
  1      split_layout: utterance_timeline() in visual pane
  2      Header: Pause gaps → new utterance (accent)
  3      Note below: temporal layer · 1.1 s threshold
  4      Code pane: pause_threshold.swift fades in
  5      Highlight threshold line in Swift
  6      Bottom label: Pause gap: 1.1 s
```

**Snippet:** `code_snippets/pause_threshold.swift`  
**Component:** `utterance_timeline(pause_s=1.1)`

---

## Act 3 — Sentence splitter

**VO seed:** *Second layer: grammatical splitting. Abbreviations like Dr. and e.g. stay intact — we only break on real sentence boundaries. One utterance in, clean sentence chips out.*

**What the animation shows:** Top pane — **Grammatical layer** card with input line `"Dr. Smith arrived e.g. before noon."` on the **left**, arrow **right**, two output chips on the **right** (`Dr. Smith arrived` / `e.g. before noon.`) — **no overlap**. Bottom pane — `sentence_split.swift`.

```
PLAY CHECKLIST — Scene4Act3
  1      split_layout: sentence_split_preview() in visual pane
  2      Input utterance in single card (left)
  3      Horizontal arrow right to two stacked output chips (right)
  4      Code pane: sentence_split.swift + highlight abbreviation comment
  5      Bottom label: Sentence splitter
```

**Snippet:** `code_snippets/sentence_split.swift`  
**Component:** `sentence_split_preview()`

---

## Act 4 — Readable captions + D2

**VO seed:** *Before: one blob. After: utterance-to-sentence chunks you can actually read while someone is talking. The two-layer split fixed readability — and it holds up with multiple speakers.*

**What the animation shows:** Side-by-side comparison — **LEFT** compact wall (`formattedString → UI`, short 3-line sample, readable size) → **arrow L→R** → **RIGHT** three green-bordered caption cards (`utterance → sentences`). Then fade to **D2** second-speaker b-roll.

```
PLAY CHECKLIST — Scene4Act4
  1      before_after_segmentation() fades in
  2      LEFT: compact wall (3 lines, not tiny scaled text)
  3      Arrow points LEFT → RIGHT (wall to chunks)
  4      RIGHT: three readable caption cards with proper word spacing
  5      Bottom label: Readable captions
  6      Fade out compare → D2_SECOND_SPEAKER b-roll (3 s)
```

**B-roll:** `broll.D2_SECOND_SPEAKER`  
**Component:** `before_after_segmentation()`, `readable_caption_chunks()`

---

## Toolkit

| Module | Role |
|--------|------|
| `components/segmentation.py` | Wall, timeline, split preview, before/after |
| `components/split_layout.py` | Acts 2–3 visual + Swift panes |
| `code_snippets/pause_threshold.swift` | 1.1 s gap constant |
| `code_snippets/sentence_split.swift` | Abbreviation-aware split |
| `broll.D2_SECOND_SPEAKER` | Multi-speaker proof |

---

## Transcript / test notes

- **Act 1:** Narrate the *problem* — don't read the wall verbatim; point at density.
- **Act 2:** Call out **1.1 s** explicitly; gesture at gap markers on timeline.
- **Act 3:** Read input once, then each output chip — proves Dr./e.g. preservation.
- **Act 4:** Say "before / after" while arrow is visible; let D2 play with minimal VO overlay.
- **Spacing QA:** Caption cards use explicit `\n` breaks; wall compact mode avoids sub-10pt text.

---

## Status

- [x] Code + layout fixes (overlap, arrow direction, spacing)
- [x] `-qk` per act → concat → measured timestamps
- [ ] VO draft + read-aloud
