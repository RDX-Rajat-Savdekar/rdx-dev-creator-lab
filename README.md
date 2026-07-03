# Manim Animations

A single [uv](https://docs.astral.sh/uv/) Python project (`manimations`) for **portfolio / resume explainer videos** — multiple independent Manim sub-projects.

> **New agent?** Start at [`docs/video-production/README.md`](docs/video-production/README.md) — generic pipeline for all projects.

## Repository layout

```
.
├── docs/video-production/    ← Portfolio video playbook (generic)
├── pyproject.toml            # uv project root (shared deps: manim >= 0.19)
├── uv.lock
├── .python-version
│
├── dsa_toolkit/              # Reusable DSA / system-design animation toolkit
├── celestia_presentation/    # CelestiaVR technical-decision presentation
│
└── Aura/                       # Aura Vision Pro portfolio videos
    ├── design-video/           # Long Manim explainer + VO toolchain
    ├── manim/                  # 60s recruiter clip
    ├── journal.md              # Aura production history
    └── clips/ · music/
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
