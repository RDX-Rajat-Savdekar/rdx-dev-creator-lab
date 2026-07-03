# Repo layout — portfolio videos

Where video work lives in **`Manim-DSA-SD-Concepts`**.  
This repo is a **uv monorepo**: shared `.venv` at root; some projects add local venvs.

---

## Top level

```
Manim-DSA-SD-Concepts/
├── docs/video-production/     ← Generic playbook (START HERE for agents)
├── pyproject.toml · .venv/    Shared Manim / uv
│
├── dsa_toolkit/               DSA / system-design animation library
├── celestia_presentation/     CelestiaVR technical deck (OpenGL)
│
└── Aura/                      Aura Vision Pro portfolio videos
    ├── journal.md             Aura production history
    ├── design-video/          Long explainer + VO toolchain
    ├── manim/                 60s recruiter clip
    ├── clips/ · music/
    └── playbook/              → redirects to docs/video-production/
```

---

## By project type

| Project | Manim code | VO / output | Notes |
|---------|------------|-------------|-------|
| **Aura design-video** | `Aura/design-video/aura_manim/` | `design-video/output/`, `vo/` | Full pipeline |
| **Aura 60s** | `Aura/manim/` | `Aura/output/` | Manim cards + ffmpeg + music |
| **Celestia** | `celestia_presentation/scene*.py` | `media/` per scene | Clip-per-file; `notes/` |
| **DSA toolkit** | `dsa_toolkit/scenes.py` | `dsa_toolkit/media/` | Library + samples |

---

## Generic patterns (long explainers)

When a project follows the chapter+act pattern:

```
{project}/
├── vo/sceneN.md
├── {manim}/scenes/sceneN_actM.py
├── tools/                    (optional — copy from Aura/design-video/tools)
├── output/
└── journal.md
```

See [07-NEW-PROJECT-SETUP.md](07-NEW-PROJECT-SETUP.md).

---

## Venvs

| Path | Used for |
|------|----------|
| `{repo}/.venv` | Manim CLI (most projects) |
| `Aura/design-video/.venv` | Whisper, Pillow (VO pipeline) |

---

## External sources

App source, facts, and raw demo footage often live under `project-sources/` (outside or alongside this repo). Link from each project's `projects/*.md` entry.
