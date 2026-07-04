# Chapter 9 — Outro

> **YouTube chapter:** *Outro*  
> **Total duration:** `0:22.0` (22.0 s measured · `-ql`) · **SCENE-PLAN target:** `12:15` → `12:45` (~30 s)  
> **VO status:** draft (read-aloud pending) · **Measured 4K:** 22.0 s — extend waits after read-aloud  
> **Preview:** `manim -ql scenes/scene9_full.py Scene9Full`  
> **layout QA:** pass (2026-07-03)

**Source acts:** `aura_manim/scenes/scene9_act{1…3}.py`  
**Script seed:** [`SCRIPT.md`](../SCRIPT.md) Chapter 9 · [`HACKATHON-STORY.md`](../HACKATHON-STORY.md) outcome + links  
**Prev chapter:** [`scene8.md`](scene8.md) — scale honesty

**Note:** Final chapter — video ends here (~12:45 total). No chapter 10 in SCENE-PLAN.

---

## Story arc

One-line recap of the on-device dual pipeline, links matching the YouTube description, then the hackathon outcome card — **2nd place · Oct 2025**.

---

## Locked decisions (2026-07-03)

| Question | Decision |
|----------|----------|
| Act count | **3 acts** — recap → links → end card |
| Recap visual | Mini `dual_pipeline_group()` from ch 3 (scaled 0.72) |
| Links on screen | [Aura-Vision-Pro](https://github.com/RDX-Rajat-Savdekar/Aura-Vision-Pro) + “All links in the video description” |
| Swift / B-roll | **None** |
| Unity | **None** |

---

## Links (YouTube description)

Copy into the video description — on-screen act 2 shows the repo + this pointer only.

| Label | URL |
|-------|-----|
| **GitHub** | https://github.com/RDX-Rajat-Savdekar/Aura-Vision-Pro |
| **60 s demo clip** | https://www.youtube.com/clip/UgkxpRDpwatHZPRf5Oyjow0mAWBwYbVKn7rI |
| **Full hackathon demo** | https://www.youtube.com/watch?v=HbW9F2zjmLQ |

---

## Act map

| Act | SCENE-PLAN beat | Target | On-screen label | File |
|-----|-----------------|--------|-----------------|------|
| 1 | Recap one line | ~10 s | On-device dual pipeline | `scene9_act1.py` |
| 2 | Links | ~10 s | Links | `scene9_act2.py` |
| 3 | End card | ~10 s | 2nd place · Oct 2025 | `scene9_act3.py` |

---

## Act 1 — Recap

**VO seed:** *One tap — on-device speech and sound analysis — captions and alerts in view. That is the pipeline we built in twenty-four hours.*

**What the animation shows:** Recap line + scaled-down dual pipeline diagram from chapter 3.

```
PLAY CHECKLIST — Scene9Act1
  1      recap_diagram() fades in
  2      One-line recap above mini pipeline
  3      Pipeline stages readable at 0.72 scale
  4      Bottom label: On-device dual pipeline
```

**Component:** `components/outro.py` → `recap_diagram()`

---

## Act 2 — Links

**VO seed:** *Links are in the description — starting with the GitHub repo at github.com slash RDX-Rajat-Savdekar slash Aura-Vision-Pro. The sixty-second clip and full hackathon demo are there too.*

**What the animation shows:** Card with GitHub repo path (accent) + subtext *All links in the video description*.

```
PLAY CHECKLIST — Scene9Act2
  1      links_card() fades in
  2      Title: Links
  3      github.com/RDX-Rajat-Savdekar/Aura-Vision-Pro (accent)
  4      Subtext: All links in the video description
  5      Bottom label: Links
```

**Component:** `components/outro.py` → `links_card()`

---

## Act 3 — End card

**VO seed:** *Second place at LA Tech Week — October twenty twenty-five. Thanks for watching.*

**What the animation shows:** End slate — **2nd place · Oct 2025** with subtitle *Aura · visionOS accessibility prototype*.

```
PLAY CHECKLIST — Scene9Act3
  1      end_card() fades in
  2      Title: 2nd place · Oct 2025
  3      Subtitle in merge-ok green
  4      Bottom label: 2nd place · Oct 2025
  5      Hold for fade to black in edit
```

**Component:** `components/outro.py` → `end_card()`

---

## Concat / 4K

```bash
cd aura_manim
../../../.venv/bin/manim -qk --frame_rate 60 scenes/scene9_act1.py Scene9Act1
../../../.venv/bin/manim -qk --frame_rate 60 scenes/scene9_act2.py Scene9Act2
../../../.venv/bin/manim -qk --frame_rate 60 scenes/scene9_act3.py Scene9Act3
ffmpeg -y -f concat -safe 0 -i output/scene9_concat.txt -c copy output/scene9_chapter9_2160p60.mp4
```

**4K concat:** `output/scene9_chapter9_2160p60.mp4` — **22.0 s**

| Act | Start | End | Dur |
|-----|-------|-----|-----|
| 1 | 0:00.0 | 0:07.7 | 7.7s |
| 2 | 0:07.7 | 0:14.8 | 7.0s |
| 3 | 0:14.8 | 0:22.0 | 7.2s |

---

## Status

- [x] VO doc + PLAY CHECKLISTs
- [x] `-ql` render + layout QA per act (2026-07-03)
- [x] 4K concat (22.0 s) — **final chapter**
- [ ] VO draft + read-aloud
