# VO workflow — design video

> **Goal:** One `vo/sceneN.md` per chapter, filled **after** final per-act Manim renders, so VO recording matches what’s actually on screen.

> **Full pipeline (all projects):** [`../../docs/video-production/README.md`](../../docs/video-production/README.md)

**Companion files:**

| File | Role |
|------|------|
| [`SCRIPT.md`](../SCRIPT.md) | Chapter-level narration ideas (may lag visuals) |
| [`SCENE-PLAN.md`](../SCENE-PLAN.md) | Target timestamps + tool per beat |
| `aura_manim/scenes/sceneN_actM.py` | Ground truth — PLAY CHECKLIST + on-screen labels |
| `output/sceneN_chapter*_2160p60.mp4` | Concat preview for read-aloud |
| [`tools/prompter.html`](../tools/prompter.html) | Teleprompter (import narration from `sceneN.md`) |
| [`AUDIO-WORKFLOW.md`](AUDIO-WORKFLOW.md) | Phone VO cleanup → alignment → Resolve |
| [`AUDIO-ALIGNMENT.md`](AUDIO-ALIGNMENT.md) | Per-act Δ vs 4K video (auto-generated) |

---

## Per-chapter checklist (copy for every scene)

```
[ ] vo/sceneN.md — PLAY CHECKLIST + VO seed (before code, ch 6+)
[ ] All acts rendered: manim -qk --frame_rate 60 scenes/sceneN_actM.py SceneNActM
[ ] Layout QA: extract_act_frames.py → checklist in MANIM-STANDARDS.md
[ ] Concat: output/sceneN_chapterN_2160p60.mp4 (absolute paths in concat.txt)
[ ] Run build_act_timestamps.py --chapter N → paste timeline table
[ ] Read aloud over concat MP4 — adjust_waits.py --add|--set → re-render acts
[ ] Update SCRIPT.md chapter table if narration locked
[ ] Record VO → phone clips in audio_record_aura/ → mux via playbook (see AUDIO-WORKFLOW.md)
```

---

## Timestamp source of truth

**Use rendered MP4 duration**, not SCENE-PLAN targets. Plans drift when holds change (e.g. act 1’s 7.2 s VO hold).

From repo root:

```bash
python Aura/design-video/vo/build_act_timestamps.py --chapter 0
```

Or manually:

```bash
ffprobe -v error -show_entries format=duration -of csv=p=0 \
  Aura/design-video/aura_manim/media/videos/scene0_act1/2160p60/Scene0Act1.mp4
```

Concat acts (absolute paths in list file):

```bash
# See output/scene0_concat.txt — paths must be absolute if list lives outside aura_manim
ffmpeg -y -f concat -safe 0 -i Aura/design-video/output/scene0_concat.txt -c copy \
  Aura/design-video/output/scene0_chapter0_2160p60.mp4
```

---

## `vo/sceneN.md` sections

1. **Header** — chapter title, YouTube chapter name, render file, total duration, VO pace target  
2. **Act timeline** — act #, start, end, duration, on-screen label, source `.py`  
3. **Act descriptions** — what the viewer sees (for editors + future you)  
4. **VO draft** — speakable text timed to acts; word count + estimated seconds  
5. **Trim notes** — gaps vs SCENE-PLAN; which `self.wait()` to cut  
6. **Status** — draft / read-aloud / recorded  

Copy structure from [`_TEMPLATE.md`](_TEMPLATE.md). First completed example: [`scene0.md`](scene0.md).

---

## Manim ↔ VO iteration loop

```
Edit sceneN_actM.py  →  re-render that act only (-qk)
                    →  re-concat sceneN_chapter*_2160p60.mp4
                    →  update vo/sceneN.md timestamps (build_act_timestamps.py)
                    →  read-aloud again
```

**Bulk pacing:** `python Aura/design-video/tools/adjust_waits.py --chapter N --show|--add 2.0`

**Layout QA (ch 6+):** `python Aura/design-video/tools/extract_act_frames.py --scene sceneN_actM`

Fast layout/motion iteration: `SceneNFull` at `-ql`.  
**Do not** record VO until `-qk` per-act concat is approved.

---

## Chapter index (fill as you go)

| Ch | VO file | Concat output | Acts | Status |
|----|---------|---------------|------|--------|
| 0 | [`scene0.md`](scene0.md) | `output/scene0_chapter0_2160p60.mp4` | 6 | draft VO |
| 1 | [`scene1.md`](scene1.md) | `output/scene1_chapter1_2160p60.mp4` | 5 | draft VO · extend waits |
| 2 | [`scene2.md`](scene2.md) | `output/scene2_chapter2_2160p60.mp4` | 6 | draft VO · extend waits |
| 3 | [`scene3.md`](scene3.md) | `output/scene3_chapter3_2160p60.mp4` | 6 | draft VO · extend waits |
| 4 | [`scene4.md`](scene4.md) | `output/scene4_chapter4_2160p60.mp4` | 4 | draft VO · extend waits |
| 5 | [`scene5.md`](scene5.md) | `output/scene5_chapter5_2160p60.mp4` | 4 | draft VO · extend waits |
| 6 | [`scene6.md`](scene6.md) | `output/scene6_chapter6_2160p60.mp4` | 3 | draft VO · extend waits |
| 7 | [`scene7.md`](scene7.md) | `output/scene7_chapter7_2160p60.mp4` | 6 | draft VO · extend waits |
| 8 | [`scene8.md`](scene8.md) | `output/scene8_chapter8_2160p60.mp4` | 3 | draft VO · extend waits |
| 9 | [`scene9.md`](scene9.md) | `output/scene9_chapter9_2160p60.mp4` | 3 | draft VO · **final chapter** |

---

## VO pace

- **Target:** ~140 wpm (same as `SCRIPT.md`)
- **Formula:** `seconds ≈ word_count / 140 × 60`
- Act 1 often has long `self.wait()` for VO — trim waits in code after read-aloud, not by rushing speech

---

## Full teleprompter script

Generated from all `vo/sceneN.md` files (VO draft quotes + VO seeds):

```bash
python Aura/design-video/tools/build_teleprompter.py
# → vo/TELEPROMPTER.md   (readable, per-act)
# → vo/teleprompter.txt  (plain text for phone apps)
# → vo/teleprompter.json (prompter API)
```

**Prompter UI:** `python Aura/design-video/tools/serve.py` → http://127.0.0.1:8765/prompter.html

---

## Extending holds for VO (two paths)

`scene.wait(N)` in Manim **freezes the current frame** for N seconds — usually at the end of an act, while the diagram + label stay on screen.

### Path A — ffmpeg freeze (recommended for read-aloud)

**No Manim re-render.** Appends cloned last-frame holds via ffmpeg `tpad`:

```bash
python Aura/design-video/tools/extend_act_holds.py --init          # template vo/hold_extensions.json
python Aura/design-video/tools/extend_act_holds.py --show          # base + extra + total per act
# Edit vo/hold_extensions.json — keys "chapter:act", values = EXTRA seconds after Manim clip
python Aura/design-video/tools/extend_act_holds.py --apply --concat  # → SceneNActM_vo.mp4 + chapter _vo concat
```

Example: Manim act is 7.7s, you need 10s hold → set `"1:1": 2.3`.

Outputs: `aura_manim/media/videos/sceneN_actM/2160p60/SceneNActM_vo.mp4`  
Concat: `output/sceneN_chapterN_2160p60_vo.mp4`

### Prompter + video sync (phone recording)

```bash
python Aura/design-video/tools/serve.py
# Mac:  http://127.0.0.1:8765/prompter.html
# Phone (same Wi‑Fi): http://<mac-ip>:8765/prompter.html  ← printed on startup
```

1. Open **Record** tab on phone  
2. Filter to one **chapter**  
3. **Per act** video (480p) — loads each act clip as you advance  
4. Tap **▶ Video** / **↺ Restart**, read script, record audio in Samsung Voice Recorder  
5. Optional: **Full chapter** mode seeks within one long MP4 at each act boundary  

Quality **4K + holds** uses `SceneNActM_vo.mp4` after `extend_act_holds.py --apply`.

### Path B — edit Manim source (final lock)

Bulk-edit `scene.wait()` in act files, then re-render 4K:

```bash
python Aura/design-video/tools/adjust_waits.py --chapter 4 --show
python Aura/design-video/tools/adjust_waits.py --chapter 4 --add 2.0
# re-render acts + concat
```

Use Path B when holds are **final** and you want source-of-truth in Manim. Use Path A while iterating VO pacing.
