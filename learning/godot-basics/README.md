# Godot Engine Basics 🎮🤖

[Godot](https://godotengine.org/) is a free, open-source, and lightweight 2D and 3D game engine. While designed for game development, it has become a favorite tool of developer-creators (like Sebastian Lague) to build **real-time interactive algorithmic simulations** (e.g., pathfinding visualizers, sorting animations, boids flight patterns, network routing simulations, or custom physics-based UI elements).

---

## 🚀 Why Godot Instead of Unity?

1.  **Zero bloat:** Godot is a single 100MB executable that runs instantly without requiring an installer or project manager hub.
2.  **GDScript (Python-like):** The scripting language used in Godot is syntax-compatible with Python. If you write Python for Manim, you can write GDScript in Godot immediately.
3.  **Real-Time Interactivity:** Unlike Manim, which renders static MP4s, Godot compiled projects are **interactive programs**. You can drag-and-drop nodes, click sliders to change parameters in real-time, and record the visual simulation live or export it as a playable web app for your portfolio.
4.  **Custom Drawing API:** Godot has an explicit programmatic drawing interface. You can override the `_draw()` function to draw vectors, points, circles, grids, and connection paths on the fly. It is essentially **real-time interactive Manim**.

---

## ⚙️ GDScript Basics

GDScript is clean and indentation-based. Here is a basic script attached to a custom Node2D that programmatically draws a simple system architecture (two server nodes and a network packet):

```gdscript
extends Node2D

# 1. Declare state variables
var node_a_pos = Vector2(200, 300)
var node_b_pos = Vector2(600, 300)
var packet_progress = 0.0 # From 0.0 to 1.0

# 2. Main frame update (runs every frame)
func _process(delta):
    # Advance the network packet progress over time
    packet_progress += delta * 0.5
    if packet_progress > 1.0:
        packet_progress = 0.0
        
    # Queue the node for redrawing (calls _draw())
    queue_redraw()

# 3. Custom Programmatic Drawing (Interactive Manim)
func _draw():
    # Draw network pipe (line connecting server nodes)
    draw_line(node_a_pos, node_b_pos, Color.DARK_SLATE_GRAY, 4.0)
    
    # Draw Server Node A
    draw_circle(node_a_pos, 40.0, Color.SLATE_BLUE)
    
    # Draw Server Node B
    draw_circle(node_b_pos, 40.0, Color.ROYAL_BLUE)
    
    # Calculate packet position and draw it
    var packet_pos = node_a_pos.lerp(node_b_pos, packet_progress)
    draw_circle(packet_pos, 10.0, Color.GREEN_YELLOW)
```

---

## 💡 How to Create Simulations in Godot
*   **Use Control Nodes for UI:** Godot has an advanced, responsive UI system. You can build panels, buttons, graphs, and input boxes to let viewers tweak algorithm properties (like speed, scale, array sizes).
*   **The Custom `_draw()` Loop:** To build visual animations of nodes, cells, or paths, attach a script to a `Node2D` and implement the `_draw()` function. Use functions like `draw_circle()`, `draw_rect()`, and `draw_string()`.
*   **Web Export:** Godot supports exporting projects directly to HTML5/WebAssembly. You can easily host your interactive simulation in a standard Web page or inside an MDX portfolio article.

---

## 📚 Useful Resources
*   [Godot Official Documentation](https://docs.godotengine.org/en/stable/)
*   [GDScript Reference Guide](https://docs.godotengine.org/en/stable/tutorials/scripting/gdscript/gdscript_basics.html)
*   [Godot Custom 2D Drawing Guide](https://docs.godotengine.org/en/stable/tutorials/2d/custom_drawing_in_2d.html)
