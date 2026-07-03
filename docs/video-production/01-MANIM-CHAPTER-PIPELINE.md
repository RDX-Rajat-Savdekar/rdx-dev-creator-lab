# Manim chapter pipeline

Generic act-by-act workflow for **long portfolio explainers** (multi-chapter, optional VO).  
**Reference implementation:** `Aura/design-video/` (ch 0–9).

---

## Philosophy

- **Visual-first:** Default holds (~5.5s); tune pacing after VO exists.
- **One act = one file:** `sceneN_actM.py` + `play_actM(scene, state)`.
- **Plan in markdown before code:** `vo/sceneN.md` PLAY CHECKLIST — user edits, then code.
- **Two assembly modes:**
  - `SceneNFull` at `-ql` — fast chapter timing
  - ffmpeg concat of 4K acts — final chapter MP4

---

## Recommended file layout

```
{project}/
├── STORY.md or HACKATHON-STORY.md
├── SCRIPT.md · SCENE-PLAN.md
├── vo/sceneN.md              Plan + timeline + VO
├── {manim_pkg}/scenes/sceneN_actM.py
├── {manim_pkg}/scenes/sceneN_full.py
├── {manim_pkg}/components/   Reusable story modules
├── code_snippets/            On-screen code (any language)
├── tools/                    CLI (see 03-TOOLS-REFERENCE.md)
└── output/                   Concats + final MP4s
```

Manim package name varies (`aura_manim/`, scenes at repo root for Celestia, etc.).

---

## Per-act workflow

### 1. Layout gate (`SceneNActMLayout`)

Slow plop of each on-screen piece — fix overlap/clipping **before** motion.

### 2. Motion (`play_actM`)

```python
def play_actM(scene: Scene, state: dict | None = None) -> dict:
    scene.play(FadeIn(label), run_time=0.5)
    scene.wait(5.5)   # VO hold — tune via adjust_waits.py
    scene.play(FadeOut(...), run_time=0.7)  # stripped in VO mux
    return {}
```

Terminal `FadeOut` is OK in Manim — **VO mux holds the frame before fade**, not black.

### 3. Render

```bash
manim -ql scenes/sceneN_actM.py SceneNActMLayout
manim -ql scenes/sceneN_actM.py SceneNActM
manim -qk --frame_rate 60 scenes/sceneN_actM.py SceneNActM
```

Use repo root `.venv` or project-local venv.

### 4. Chapter concat

ffmpeg concat list with **absolute paths** per act MP4.

---

## Project-specific standards

Each mature project may define its own rules file:

| Project | Standards doc |
|---------|----------------|
| Aura design-video ch 6+ | `Aura/design-video/MANIM-STANDARDS.md` |
| DSA toolkit | Conventions in `dsa_toolkit/manim_utils.py` |
| Celestia | OpenGL renderer; see `celestia_presentation/notes/` |

Read the project's `projects/*.md` entry before coding.

---

## Pacing

```bash
python {project}/tools/adjust_waits.py --chapter N --show
python {project}/tools/adjust_waits.py --chapter N --add 2.0
```

Or skip re-render and use VO mux hold-frame sync ([02-VO-RECORDING-AND-SYNC.md](02-VO-RECORDING-AND-SYNC.md)).

---

## B-roll pattern

Embed real demo footage in Manim via frame updaters (PyAV → `ImageMobject`), not `VideoMobject`.  
Acts ending with **b-roll + blank wait** need special mux handling — see `vo_video_fit.py`.

---

## Related

- [07-NEW-PROJECT-SETUP.md](07-NEW-PROJECT-SETUP.md)
- [projects/aura-design-video.md](projects/aura-design-video.md)
