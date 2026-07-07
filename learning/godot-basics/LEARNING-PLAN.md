# Godot Learning Plan: Celestia Interactive 🪐🎮

This playground project introduces **Godot Engine 4** concepts by building an interactive 3D astronomy presentation. You will learn the node-based scene graph, GDScript, user input handling, UI design, signals, and custom GLSL-like shaders.

---

## 🗺️ The 4-Stage Learning Roadmap

### 🏁 Stage 1: The Scene Graph & Orbit Camera 🎥
* **Concept**: Godot organizes everything in **Nodes**. The root of a 3D scene is a `Node3D`. We add `Camera3D` to view it, `DirectionalLight3D` to illuminate it, and `WorldEnvironment` for backgrounds.
* **Goal**: Write an `orbit_camera.gd` script to orbit the center using mouse drag and mouse wheel zoom.
* **Key API**: `_unhandled_input()`, `Vector3`, `transform`, `lerp()`.

### 🏁 Stage 2: Programmatic Generation & Coordinate Pipeline 📐
* **Concept**: Spawns stars programmatically from a script rather than placing them by hand in the editor.
* **Goal**: Create a grid wireframe and write a conversion pipeline that maps Right Ascension (RA) and Declination (Dec) to Cartesian coordinates (X, Y, Z) on a unit sphere.
* **Key API**: `MeshInstance3D`, `ImmediateMesh` (for lines), `BoxMesh`, `Mathf.deg_to_rad()`.

### 🏁 Stage 3: UI Controls & Signals 🎛️
* **Concept**: Godot has a powerful UI system (`Control` nodes). Nodes communicate using **Signals** (event listeners).
* **Goal**: Add a `CanvasLayer` containing a magnitude slider and category buttons. Connect their signals to filter the 3D star cloud.
* **Key API**: `HSlider`, `Button`, `signal`, `connect()`, `visible`.

### 🏁 Stage 4: Custom Shaders & Visual Effects ⚡
* **Concept**: Godot Shader Language (`.gdshader`) is a custom dialect of GLSL. It runs directly on the GPU.
* **Goal**: Map B-V color indices to color temperatures, and write a shader to animate scale/transparency to make the stars twinkle.
* **Key API**: `shader_type spatial`, `VERTEX`, `ALBEDO`, `TIME`, `ShaderMaterial`.
