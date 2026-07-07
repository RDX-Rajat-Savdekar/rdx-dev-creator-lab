# Programmatic Animation Toolkit Map 🗺️🎬

This document maps the complete ecosystem of animation and audio tools configured in this repository. It serves as a persistent coordinate system for sessions, developers, and AI agents.

---

## 📹 Video Rendering Frameworks (The Animators)

### 1. Remotion (React / HTML / CSS / SVG)
*   **Best For:** System design explainers, dashboard telemetry cards, mock web browser layouts, responsive components, and data-driven timelines.
*   **Mental Model:** *Frame-by-Frame Stateless Ticking.* driving CSS and SVGs directly from the active timeline frame index via `interpolate()` and `spring()`.
*   **Path:** `learning/remotion-basics/`

### 2. Motion Canvas (TypeScript / HTML5 Canvas / Vite)
*   **Best For:** Fluid vector diagrams, mathematical illustrations, self-drawing networks, and algorithm sequences (e.g. BST traversal or QuickSort swaps).
*   **Mental Model:** *Imperative Timeline Generators.* Writing animations sequentially using generator functions (`function*` and `yield*` commands) to control layout threads.
*   **Path:** `learning/motion-canvas-basics/` (Next Step)

### 3. Manim (Python / Cairo / OpenGL)
*   **Best For:** High-fidelity mathematical animation, coordinate geometry, linear algebra transformations, and abstract theorem visuals.
*   **Mental Model:** *Object Morphing.* Building math configurations (`Mobjects`) and describing their visual translations in Python classes.
*   **Path:** `learning/manim-basics/`

---

## 🕹️ Interactive Layout & Coordinate Engines

### 1. React Flow (React DOM)
*   **Best For:** Interactive, drag-and-drop system diagrams and node graphs for standard web platforms.
*   **Mental Model:** *Stateful Connected Flowcharts.* Managing custom card shapes with handles that automatically compute connector cables (edges) in React DOM.
*   **Path:** `learning/web-interactive-basics/`

### 2. D3.js (`d3-shape` / `d3-hierarchy` / `d3-scale`)
*   **Best For:** Math mapping and hierarchy calculations.
*   **Mental Model:** *Pure Mathematical Layouts.* Instead of using D3's DOM selection APIs, use it as a calculator to output relative coordinates (for trees, sorting blocks, or force-directed nodes) and render those coordinates inside React SVG/Canvas frames.

---

## 🎮 Game Engines & WebGL 3D

### 1. React Three Fiber (Three.js WebGL)
*   **Best For:** Full WebGL-based 3D modeling, detailed lighting, custom shaders, and camera movement.
*   **Mental Model:** *Declarative WebGL Scene Graphs.* Placing lights, materials, cameras, and meshes inside a React component wrapper.

### 2. Godot Engine (C# / GDScript)
*   **Best For:** Physics-based simulations, lightweight custom visualizations, and complex interactive scenes.
*   **Mental Model:** *Node-Tree Game Loops.* Scripting nodes that execute translations frame-by-frame using game physics engines.
*   **Path:** `learning/godot-basics/`

---

## 🎙️ Voiceover Muxing & Concat Pipelines (The Packagers)

### 1. Whisper Transcription API / Local CLI
*   **Best For:** Mapping recorded narration voiceovers to visual frames automatically.
*   **Mental Model:** *Speech-to-Frame Timestamping.* Whispering transcripts to locate exact frame boundaries (`speech_end` triggers) to automate scene cuts.

### 2. FFmpeg CLI
*   **Best For:** Stitching rendering clips, normalization of vocal assets, padding frame ends, and muxing video with background music.
*   **Mental Model:** *Fast, Headless Multimedia Concatenation.* Programmatically processing media tracks directly from Node/Python backend servers.
