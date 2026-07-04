# Manim CE Basics 🐍🎥

[Manim Community Edition](https://www.manim.community/) is a programmatic vector animation engine written in Python. Originally created by Grant Sanderson (3Blue1Brown) for his math videos, Manim is excellent for explaining abstract mathematical topics, data structures (DSA), graphs, and vector diagrams.

This playground is for testing basic positioning, alignment, grouping, custom animations, and layout flows.

---

## 🚀 Setup & Execution

Since the project uses [uv](https://docs.astral.sh/uv/) for Python dependency management, Manim is already pre-configured in the shared virtual environment at the repository root.

### Render Commands
To run a render, run `uv run manim` inside the terminal. Helpful CLI flags:
*   `-ql`: Low quality (480p, 15fps). **Use this for 95% of your development/preview loops.**
*   `-qh`: High quality (1080p, 60fps). Good for final review.
*   `-qk`: 4K quality (2160p, 60fps). Use this only for final YouTube/portfolio outputs.
*   `-p`: Play/open the video file automatically after rendering is complete.

```bash
# Render a basic scene in low quality and preview it
uv run manim -pql scenes.py HelloWorldScene
```

---

## 📝 Hello World Template

Here is a clean, modern template implementing best-practice layout alignment rules:

```python
from manim import *

class HelloWorldScene(Scene):
    def construct(self):
        # 1. Create components (Using standard text wrappers)
        title = Text("Binary Search Tree", font="Outfit", font_size=36)
        description = Text("Dividing search space in half at each step", font="Outfit", font_size=20, color=GRAY)
        
        # 2. Group and arrange (Layout FIRST)
        header_group = VGroup(title, description).arrange(DOWN, buff=0.3)
        
        # 3. Position (Center in the frame LAST)
        header_group.move_to(ORIGIN)
        
        # 4. Play animations
        self.play(Write(title))
        self.play(FadeIn(description, shift=UP * 0.2))
        self.wait(2)
        
        # 5. Clean exit
        self.play(FadeOut(header_group))
```

---

## ⚠️ Enforced Best Practices (From Post-Mortem Reviews)

Avoid typical layout traps by adhering to these guidelines:

### 1. The Layout Pipeline
*   **The Problem:** Anchoring an object at `ORIGIN` and growing right using `next_to(..., RIGHT)` will eventually cause elements to clip the right edge of the screen.
*   **The Fix:** Construct all elements first, group them inside a `VGroup`, arrange them using `.arrange(RIGHT)`, and finally center the whole group:
    ```python
    main_layout = VGroup(node_a, node_b, node_c).arrange(RIGHT, buff=0.5)
    main_layout.move_to(ORIGIN) # Centers the layout in the video frame
    ```

### 2. Typography Constraints
*   **The Problem:** Direct calls to `Text("very long text...", width=4.2)` or running `.scale(0.88)` on groups containing `Text` elements will compress letter spacing, causing word glitches (e.g. `gettranscription`).
*   **The Fix:** Never scale a group containing readable `Text`. Instead, set the font size explicitly, wrap text lines manually, or size the surrounding graphic plates to fit the text.

### 3. Arrows and Connections
*   **The Problem:** Drawing an arrow between Node A and Node B *before* calling `.arrange()` on the parent group causes the arrow to point to where the nodes *used* to be.
*   **The Fix:** Position your nodes first, then construct and animate the arrows:
    ```python
    nodes = VGroup(node_a, node_b).arrange(RIGHT, buff=2)
    nodes.move_to(ORIGIN)
    
    arrow = Arrow(node_a.get_right(), node_b.get_left(), buff=0.1)
    self.play(Create(arrow))
    ```

---

## 📚 Useful Resources
*   [Manim CE Documentation](https://docs.manim.community/en/stable/)
*   [Manim Coordinate System Guide](https://docs.manim.community/en/stable/tutorials/building_blocks.html#positioning-mobjects)
*   [Interactive Manim Sandbox (Binder)](https://docs.manim.community/en/stable/tutorials/quickstart.html#interactive-jupyter-notebook)
