# DSA Toolkit

A reusable Manim toolkit for data-structure / algorithm animations, plus the scenes
that use it.

| File | What it is |
|---|---|
| `manim_utils.py` | The library: `Base_DSA_Scene` (3-zone code/anim/log layout), `LinkedListNode` & `LinkedList` smart Mobjects, and helpers (`highlight_line`, `update_log_text`, `create_scrambled_title`). |
| `scenes.py` | "Intro to Linked Lists" video + layout/FX test scenes. Imports `manim_utils`. |
| `title_card_scene.py` | Scrambled-title card scenes (`LinkedTitle`, `PathTitle`). |
| `code_snippets/` | Python source rendered on-screen inside the animations. |

## Run (from this folder)

```bash
uv run manim -pqh scenes.py IntroToLinkedListScene   # full 1080p
uv run manim -pql scenes.py TestFXScene              # quick preview
```

`scenes.py` references `./code_snippets/…`, so run from inside `dsa_toolkit/`.
