# Manim Animations

A single [uv](https://docs.astral.sh/uv/) Python project (`manimations`) containing two
independent [Manim](https://www.manim.community/) animation sub-projects.

## Repository layout

```
.
├── pyproject.toml            # uv project root (shared deps: manim >= 0.19)
├── uv.lock
├── .python-version
│
├── dsa_toolkit/              # Reusable DSA / system-design animation toolkit
│   ├── manim_utils.py        #   the library: Base_DSA_Scene, LinkedList, helpers
│   ├── scenes.py             #   "Intro to Linked Lists" + test scenes
│   ├── title_card_scene.py   #   scrambled-title card scenes
│   ├── code_snippets/        #   source shown on-screen inside animations
│   └── manim.cfg
│
└── celestia_presentation/    # CelestiaVR technical-decision presentation (6 scenes)
    ├── scene0.py … scene5.py #   logo, skybox, magnitude filter, coord pipeline,
    │                         #   B-V color/twinkle, constellation graph/octree
    ├── build_scene1.py       #   render + ffmpeg-stitch helper for Scene 1
    ├── data/                 #   JSON fixtures generated/shown by the scenes
    ├── notes/                #   per-scene narration + render-command notes
    └── manim.cfg
```

## How to run

Each sub-project is self-contained. **`cd` into the sub-project folder, then render** —
the scenes use paths relative to their own folder (e.g. `data/sirius_data.json`,
`./code_snippets/`).

```bash
# DSA toolkit
cd dsa_toolkit
uv run manim -pqh scenes.py IntroToLinkedListScene

# Celestia presentation
cd celestia_presentation
uv run manim --renderer=opengl -qh scene3.py S3_Clip1_CelestialGrid
```

`uv run` locates the shared `pyproject.toml`/`.venv` at the repo root automatically, so
you do not need to activate the venv manually.

## Notes
- Render output (`media/`) and `__pycache__/` are git-ignored.
- See `celestia_presentation/notes/*.txt` for the full clip list and high-res render
  commands per scene.
