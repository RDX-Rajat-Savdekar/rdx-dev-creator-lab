# CelestiaVR presentation

**Tier A** — Manim clip deck (OpenGL renderer). **No VO pipeline yet.**

---

## Paths

| What | Where |
|------|--------|
| Scenes | `celestia_presentation/scene0.py` … `scene5.py` |
| Narration notes | `celestia_presentation/notes/` |
| Data fixtures | `celestia_presentation/data/` |
| Stitch helper | `celestia_presentation/build_scene1.py` |
| README | `celestia_presentation/README.md` |

---

## Render

```bash
cd celestia_presentation
uv run manim --renderer=opengl -qh scene3.py S3_Clip1_CelestialGrid
uv run manim --renderer=opengl -qh scene5.py -a
```

---

## If adding VO later

Follow [07-NEW-PROJECT-SETUP.md](../07-NEW-PROJECT-SETUP.md) tier C — likely clip-level sync rather than act-per-chapter unless restructured.

---

## Topics

Skybox projection, magnitude filter, RA/Dec pipeline, B-V color, constellation graph / octree.
