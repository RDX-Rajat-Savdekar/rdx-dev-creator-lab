# Aura 60s — Manim text + ffmpeg assembly

Text cards and lower-thirds are **Manim** (3b1b-style programmatic typography). Demo footage comes from `../clips/`.

## Quick run

From repo root:

```bash
.venv/bin/python Aura/manim/build_60s.py
```

Output: **`../output/aura-60s-rough-assembly.mp4`** (~56 s, muted).

Re-run after editing copy in `aura_cards.py`:

```bash
.venv/bin/python Aura/manim/build_60s.py --skip-render   # ffmpeg only
.venv/bin/python Aura/manim/build_60s.py --quality h     # sharper Manim (-qh)
.venv/bin/python Aura/manim/add_music.py --music ../music/bed.mp3   # optional bed
```

See **`../music/README.md`** for what kind of track to download (YouTube Audio Library, etc.).

## What Manim renders

| Scene | Type | Used in timeline |
|-------|------|------------------|
| `HookCard` | Full-screen | Opening hook |
| `ProblemCard` | Full-screen | zero cloud |
| `PipelineCard` | Full-screen | Speech + SoundAnalysis |
| `ProofCard` | Full-screen | 2nd place · 24 h |
| `CTACard` | Full-screen | GitHub URL |
| `ProductLowerThird` | Transparent overlay | On D1 trim |
| `SpeechLowerThird` | Transparent overlay | On D1+D2 |
| `SoundLowerThird` | Transparent overlay | On D3+D4+D5 |
| `LocaleLowerThird` | Transparent overlay | On D6 trim |

Edit strings, colors (`ACCENT`, `AURA_BG`), or `HOLD` durations in `aura_cards.py`.

## Render one card manually

```bash
cd Aura/manim
../../.venv/bin/manim -ql -r 1280,720 --frame_rate 60 aura_cards.py HookCard
../../.venv/bin/manim -ql -r 1280,720 --frame_rate 60 -t aura_cards.py ProductLowerThird
```

## Files

- `aura_cards.py` — all Manim scenes
- `build_60s.py` — render + trim + overlay + concat
- `media/` — Manim render cache (gitignored via root `media/`)
- `../output/build/` — intermediate segments
