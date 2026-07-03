# Learning log — Manim + Unity (as we build Aura design video)

> **Convention:** Whenever we introduce a **new concept or good practice** in code, add a short entry here and a `# LEARN:` comment at first use in source.
>
> Keep entries **5–10 lines** — enough to recall later, not a tutorial.

---

## Manim

### Scene
A **Scene** is one Manim “episode” — a class subclassing `Scene` with a `construct()` method where all animations run. One exported video clip usually = one Scene class.  
**Practice:** One story beat per Scene; don’t cram a whole chapter into one file while learning.

### Mobject
**Mobject** = “Mathematical object” — anything drawable (Text, Rectangle, Arrow, VGroup). Everything on screen is a Mobject.  
**Practice:** Build complex visuals from small Mobjects grouped in `VGroup`.

### VGroup
A **VGroup** groups Mobjects so you can move/fade/animate them together. Like a `<div>` for diagram pieces.  
**See:** `dsa_toolkit/manim_utils.py` → `LinkedListNode(VGroup)`.

### construct()
The **only** method Manim calls to play your scene. Put animations in order here via `self.play(...)`.  
**Practice:** Split with `# ACT 1`, `# ACT 2` comments matching VO beats.

### self.play() / self.wait()
`self.play(FadeIn(x))` runs an animation; `self.wait(2)` holds the frame for VO.  
**Practice:** `wait()` duration ≈ your spoken line length when syncing to VO later.

### FadeIn, Create, Transform
Common **animations**. `Create` draws shapes; `FadeIn` opacity; `Transform(a, b)` morphs shape a → b.  
**3b1b rule:** Prefer `Transform` to show *same idea, refined* (naive → final architecture).

### Code (Manim mobject)
Manim **`Code`** displays syntax-highlighted source from a file or string — use for Swift snippets on screen.  
**Aura use:** Load from `code_snippets/*.swift` via `Code(...)`.

**Practice:** One act per file while learning (`scene0_act1.py`, then act2…); join in `scene0_full.py` last.

### SVGMobject
**SVGMobject** loads a `.svg` file as a drawable — use for icons instead of hand-drawing with `Line`/`Arc`.  
**Aura use:** `icons.load_icon("bell", color=ACCENT)` for **stroke** icons · `load_filled_icon("cursor", ...)` for **filled** glyphs.  
**Rule:** If an asset exists as SVG (mail, cursor, cloud…), don't hand-draw polygons — add to `assets/icons/`.

### -ql / -qm / -qh
Manim quality flags: **low / medium / high** resolution. Always preview `-ql`; final render `-qm` or `-qh`.

### ReplacementTransform
**ReplacementTransform(a, b)** replaces Mobject `a` with `b` in-place on screen — cleaner than fade-out + fade-in when showing the *same object* changing (e.g. sphere gray → red).  
**Practice:** Use when the viewer should track one entity through a change.

### LaggedStart
**LaggedStart** runs a list of animations with a delay (`lag_ratio`) between each start — good for rooms full of icons or pipeline boxes appearing in sequence.  
**See:** `scenes/scene0_act1.py` (bubbles + sound SVGs).

### play_actN + sceneN_full
Each act file exports **`play_actM(scene, state)`** — motion without a Scene class. **`sceneN_full.py`** calls them in order; pass **`state['chain']=True`** when acts share on-screen Mobjects (e.g. ch 1 device diagram acts 1→3).  
**Practice:** Standalone `SceneNActM` calls `play_actM(self)` with empty state (fade in/out per act). Full scene skips fades between chained acts.

### there_and_back
**Rate function** for `self.play(mob.animate.scale(1.2), rate_func=there_and_back)` — one pulse up and down.  
**See:** `scene0_act4.py` — sphere pulsates 3× on “louder” cue.

### Group vs VGroup
**`ImageMobject`** (video frames, PNG) cannot live in **`VGroup`** — use **`Group`**. VMobjects only in VGroup.  
**See:** `broll.py` — `Group(border, image)`.

### B-roll in Manim (PyAV)
Manim CE has no **`VideoMobject`**. Decode MP4 with **PyAV** (`av`), convert frames to **`ImageMobject`**, advance with an **updater** during `self.wait()`.  
**See:** `broll.py` · `scene0_act5.py` (D1 live captions, 4 s).  
**Alt:** ffmpeg concat in Resolve only — slower iteration for full-chapter preview.

### rejected path (ghost + strikethrough)
Architecture “we cut this” visuals: **`DashedLine`** ghost arrow, **`strikethrough_line(mob)`** with `Create`, dim with `.set_opacity()`, reason **chips**.  
**See:** `rejected.py` · `scene1_act2.py` / `scene1_act3.py`. No external Manim plugin.

### code_panel (Swift snippets)
**`code_panel.swift_panel(filename)`** loads `design-video/code_snippets/*.swift` via Manim **`Code`**. **`highlight_lines(panel, (4, 5))`** + **`play_highlight()`** for evidence beats.  
**Practice:** Snippet file = ground truth; ≤15 lines; header comment with source path in Aura-Vision-Pro repo.

### plop (layout review)
**`review.plop(scene, mob, name)`** — fade one piece in, tag top-left, hold. Build cumulative layout before motion.  
**See:** `SceneNActMLayout` in every act file.

### typography (readable secondary text)
**`MUTED` (#98989d) at 15–16pt on `#0a0a0f` is too faint for copy viewers must read.** Use **`typography.subtext()` / `caption()` / `chip_label()`** instead — color **`SUBTEXT`** (`#c5ced8`), min **18pt**.  
**`MUTED` stays for:** strokes, dividers, plop tags, arrow lines — not sentences on screen.  
**See:** `typography.py` · `theme.SUBTEXT` · `theme.SUBTEXT_SIZE`.

---

## Unity (visualization-only for Aura)

### Viz scene vs shipped app
Our Unity project is **explainer-only** — it does not ship as Aura. Label clips honestly: *“Visualization — not the Swift app.”*  
**Sebastian pattern:** Post-hoc scenes to clarify ideas; screen-record for the video.

### GameObject
Basic entity in a Unity scene (mesh, light, camera, empty parent).  
**Viz use:** Empty parent = “caption panel root” you move in 3D.

### MonoBehaviour + Update()
**MonoBehaviour** scripts attach to GameObjects. `Update()` runs every frame (~90 Hz on Quest / varies on editor).  
**Aura parallel:** Why texture-**bake** beats updating UI layout every frame (ch 5).

### Camera.main
The scene camera — what you screen-record. For spatial HUD viz, orbit slowly rather than jerky motion.

### Shapes / LineRenderer / UI Canvas
**Sebastian** often uses lightweight draw tools. For Aura viz: quads for caption panels, `LineRenderer` for sound-direction rays, World Space Canvas for fake SwiftUI texture.

### Screen capture
Export Unity clips via **Recorder** package or OBS — same role as Manim MP4 outputs in Resolve timeline.

---

## Cross-tool workflow

| Tool | Best for Aura chapters |
|------|-------------------------|
| **Manim** | Pipelines, threads, rejected paths, code panels, scale diagram |
| **Unity viz** | Spatial HUD in 3D, billboard/orbit bug, azimuth rays, immersive mock |
| **Swift snippets** | Ground truth on screen (`code_snippets/` + `code_panel.py`) |
| **Demo B-roll** | In Manim (`broll.py`) or Resolve — D1–D6 in `Aura/clips/` |
| **ffmpeg** | Per-act 2160p60 concat (`output/sceneN_concat.txt`, absolute paths) |
| **VO docs** | `vo/sceneN.md` — measured timestamps + draft narration |

### Standard chapter pipeline (2026-07-02)

```
1. vo/sceneN.md — PLAY CHECKLISTS (plan) → user edits → code gen
2. sceneN_actM.py — Layout plop → motion → play_actM
3. sceneN_full.py — -ql iteration
4. -qk per act → ffmpeg concat → vo/sceneN.md timestamps + read-aloud
5. Record VO → Resolve (optional music bed)
```

Log decisions in [`../journal.md`](../journal.md).

---

## Index (fill as we go)

| Date | Concept | Where introduced |
|------|---------|------------------|
| 2026-07-01 | Scene, Mobject, VGroup, construct | LEARNING.md bootstrap |
| 2026-07-01 | LaggedStart, ReplacementTransform, Indicate | `scenes/scene0_act*.py` |
| 2026-07-01 | SVGMobject, one-act-per-file workflow | `icons.py` · `scenes/scene0_act1.py` |
| 2026-07-02 | play_actN, sceneN_full, state chain | `scene0_full.py` · `scene1_full.py` |
| 2026-07-02 | B-roll via PyAV + ImageMobject, Group | `broll.py` · `scene0_act5.py` |
| 2026-07-02 | there_and_back pulse | `scene0_act4.py` |
| 2026-07-02 | rejected path, code_panel | `rejected.py` · `code_panel.py` · ch 1 |
| 2026-07-02 | typography SUBTEXT vs MUTED | `typography.py` · `theme.py` |
