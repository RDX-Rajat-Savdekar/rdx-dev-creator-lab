# New project setup

How to add a **new portfolio video** to this repo (resume project #N).

---

## 1. Register the project

1. Create `docs/video-production/projects/<slug>.md` (copy structure from [aura-design-video.md](projects/aura-design-video.md)).  
2. Add a row to [README.md](../README.md) project table.  
3. Create `{ProjectFolder}/journal.md` using [JOURNAL-TEMPLATE.md](../JOURNAL-TEMPLATE.md).

---

## 2. Choose a pipeline tier

| Tier | When | Minimum structure |
|------|------|-------------------|
| **A — Clip deck** | 5–10 standalone clips (Celestia-style) | `sceneN.py`, `notes/`, optional `build_sceneN.py` |
| **B — Short hybrid** | 30–90s, text + footage (Aura 60s) | Manim scenes + `build_*.py` + ffmpeg |
| **C — Long explainer + VO** | Multi-chapter, narrated (Aura design) | act files, `vo/`, `tools/`, mux pipeline |

Don't force tier C unless you need chapter VO sync.

---

## 3. Tier C checklist (full pipeline)

Copy patterns from `Aura/design-video/`:

```
MyProject/
├── journal.md
├── README.md
├── HACKATHON-STORY.md or STORY.md
├── SCRIPT.md · SCENE-PLAN.md
├── vo/_TEMPLATE.md · vo/scene0.md …
├── my_manim/scenes/sceneN_actM.py
├── my_manim/theme.py · typography.py · components/
├── tools/          ← copy Aura/design-video/tools/; adjust paths in scripts
├── output/
└── .venv/          ← whisper + pillow
```

Update tool `REPO` / `DESIGN` paths at top of each script, or refactor to `--project-root` (future).

---

## 4. Story lock before pixels

- Facts / `never_claim` list  
- Rejected alternatives (what you did **not** do)  
- Evidence paths (demo clips, repo URLs)

---

## 5. Manim conventions

- Layout scene before motion scene (if using act pattern)  
- Default `scene.wait(5.5)` before terminal fade  
- Document project-specific standards in `{project}/MANIM-STANDARDS.md` when ch count grows

---

## 6. VO (if narrated)

1. `build_teleprompter.py` from `vo/sceneN.md`  
2. Record → `audio_record_<slug>/`  
3. `process_vo_audio.py` → `processed/`  
4. `mux_chapter_vo.py --banner` → `build_full_film.py`  

See [02-VO-RECORDING-AND-SYNC.md](../02-VO-RECORDING-AND-SYNC.md).

---

## 7. Ship

- [ ] Final MP4 in `{project}/output/`  
- [ ] Journal entry dated + artifacts table  
- [ ] Update resume / README links when published

---

## Example slugs

| Resume project | Suggested folder | Tier |
|----------------|------------------|------|
| Company X architecture | `CompanyX/design-video/` | C |
| ML paper walkthrough | `paper-explainer/` | A or C |
| Hackathon demo 60s | `{name}/manim/` | B |
