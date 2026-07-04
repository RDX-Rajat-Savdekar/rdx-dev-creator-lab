# Celestia Presentation

Manim animation deck explaining the technical decisions behind the CelestiaVR
stargazing project. Each `sceneN.py` holds the clips for one scene.

> Portfolio pipeline docs: [`../docs/video-production/projects/celestia-presentation.md`](../docs/video-production/projects/celestia-presentation.md)

| Scene | File | Topic |
|---|---|---|
| 0 | `scene0.py` | Celestia logo / title |
| 1 | `scene1.py` | The skybox problem (cube vs. sphere projection) |
| 2 | `scene2.py` | Magnitude filtering (data overload → optimized sky) |
| 3 | `scene3.py` | RA/Dec → Cartesian coordinate pipeline ("Great Migration") |
| 4 | `scene4.py` | B-V color index + twinkle |
| 5 | `scene5.py` | Constellations as graphs (adjacency list, 3D, octree) |

- `data/` — JSON shown on-screen. `scene3.py`/`scene5.py` regenerate these at render time
  (paths are `data/…`, relative to this folder).
- `notes/` — narration + per-clip high-res render commands (`Scene1.txt`, `scene3.txt`,
  `manim_presentation.txt`).
- `build_scene1.py` — renders all Scene 1 clips and stitches them with ffmpeg.

## Run (from this folder)

```bash
uv run manim --renderer=opengl -qh scene3.py S3_Clip1_CelestialGrid
uv run manim --renderer=opengl -qh scene5.py -a        # all clips in a scene
```
