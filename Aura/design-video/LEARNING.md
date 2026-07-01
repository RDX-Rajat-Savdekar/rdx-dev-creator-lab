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
**Aura use:** `icons.load_icon("bell", color=ACCENT)` from `assets/icons/`.

### -ql / -qm / -qh
Manim quality flags: **low / medium / high** resolution. Always preview `-ql`; final render `-qm` or `-qh`.

### ReplacementTransform
**ReplacementTransform(a, b)** replaces Mobject `a` with `b` in-place on screen — cleaner than fade-out + fade-in when showing the *same object* changing (e.g. sphere gray → red).  
**Practice:** Use when the viewer should track one entity through a change.

### LaggedStart
**LaggedStart** runs a list of animations with a delay (`lag_ratio`) between each start — good for rooms full of icons or pipeline boxes appearing in sequence.  
**See:** `scenes/scene0_act1.py` (bubbles + sound SVGs).

### Indicate
**Indicate(mob)** briefly scales/highlights a Mobject to draw attention without changing layout.  
**Aura use:** Highlight "Rajat" on the solo-author beat (ch 0 ACT 3).

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
| **Swift snippets** | Ground truth on screen (both tools overlay or cut to snippet) |
| **Demo B-roll** | Real visionOS 2D HUD from hackathon footage |

---

## Index (fill as we go)

| Date | Concept | Where introduced |
|------|---------|------------------|
| 2026-07-01 | Scene, Mobject, VGroup, construct | LEARNING.md bootstrap |
| 2026-07-01 | LaggedStart, ReplacementTransform, Indicate | `scenes/scene0_problem_REFERENCE.py` |
| 2026-07-01 | SVGMobject, one-act-per-file workflow | `icons.py` · `scenes/scene0_act1.py` |
| | | |
