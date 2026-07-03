# DSA toolkit

**Library + sample scenes** — reusable Manim helpers for DSA / system-design animations.

Not a shipped portfolio video yet; use as **component tier** reference when building explainers.

---

## Paths

| What | Where |
|------|--------|
| Library | `dsa_toolkit/manim_utils.py` |
| Sample scenes | `dsa_toolkit/scenes.py`, `title_card_scene.py` |
| Code on screen | `dsa_toolkit/code_snippets/` |
| Config | `dsa_toolkit/manim.cfg` |

---

## Render

```bash
cd dsa_toolkit
uv run manim -pqh scenes.py IntroToLinkedListScene
```

---

## Patterns to reuse

- `Base_DSA_Scene`, linked-list nodes as `VGroup`  
- Title card scramble scenes  
- Shared layout helpers — precursor to Aura `components/layout.py`

When a DSA video becomes a resume deliverable, add `dsa_toolkit/journal.md` + registry entry.
