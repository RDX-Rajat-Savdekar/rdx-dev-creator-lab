# The Learning Playgrounds 🧪📖

Welcome to the learning playgrounds directory of the **rdx-dev-creator-lab**. This section of the repository is dedicated to learning the fundamentals of our developer-creator tool stack, writing exploratory scripts, trying out tutorials, and testing new configurations before applying them to our core video showcases.

Each subdirectory inside `learning/` is a self-contained environment for a specific visual or interactive technology.

---

## 🗺️ Playground Roadmap

Choose a playground based on what you are trying to learn or build:

### 1. [Manim Basics](file:///Users/rajatsavdekar/Documents/GitHub/Manim-DSA-SD-Concepts/learning/manim-basics/README.md)
*   **Focus:** Programmatic mathematical and algorithm animations.
*   **Key Concepts:** Object positioning, custom camera settings, value trackers, vectors, and rendering optimization.
*   **Use when:** You need to explain algorithmic steps, graph structures, or formulaic derivations.

### 2. [Remotion Basics](file:///Users/rajatsavdekar/Documents/GitHub/Manim-DSA-SD-Concepts/learning/remotion-basics/README.md)
*   **Focus:** Programmatic React-based video generation.
*   **Key Concepts:** Frame-based timelines, animating CSS elements, styling vector SVGs, and compiling React apps to MP4.
*   **Use when:** You need to show web mockups, network request/response headers, database tables, or interactive web UIs.

### 3. [Godot Basics](file:///Users/rajatsavdekar/Documents/GitHub/Manim-DSA-SD-Concepts/learning/godot-basics/README.md)
*   **Focus:** Lightweight, real-time algorithmic simulations.
*   **Key Concepts:** 2D canvas nodes, physics bodies, camera tracking, and writing state machines in GDScript (Python-like).
*   **Use when:** You want to build interactive simulator tools or visualizers (similar to Sebastian Lague's pathfinding and sorting demos) where readers can interact with the nodes live.

### 4. [Web Interactive Basics](file:///Users/rajatsavdekar/Documents/GitHub/Manim-DSA-SD-Concepts/learning/web-interactive-basics/README.md)
*   **Focus:** Building interactive documents and portfolio articles.
*   **Key Concepts:**
    *   **MDX:** Embedding React/Svelte widgets in markdown text.
    *   **Spline & Three.js:** Building and embedding 3D models in the browser.
    *   **Sandpack:** Live runnable code playgrounds.
    *   **Framer Motion & GSAP:** Scroll-driven animations (Scrollytelling).
*   **Use when:** You are writing interactive system design explainers for your portfolio website.

### 5. [Voice Testing](file:///Users/rajatsavdekar/Documents/GitHub/Manim-DSA-SD-Concepts/learning/voice-testing/)
*   **Focus:** Audio quality, voiceovers, and speech synchronization.
*   **Key Concepts:** Speech-to-text timing thresholds, silence padding, volume normalization, and local Whisper transcript tests.
*   **Use when:** You are testing microphone setups, practicing scripts, or modifying the VO toolchain.

---

## 💡 Best Practices for Learning
1.  **Fail Small, Fail Fast:** Don't write a 10-chapter animation in the learning folder. Write a simple 30-second scene testing *one* specific concept (like aligning text to nodes).
2.  **Document as You Go:** If you run into a weird tool bug (e.g., a Manim rendering error or a Remotion build glitch), add it to that playground's README under a "Troubleshooting" section.
3.  **Graduate to Projects:** Once you feel confident with a playground concept, copy your templates/logic over to the `projects/` directory to create a full showcase.
