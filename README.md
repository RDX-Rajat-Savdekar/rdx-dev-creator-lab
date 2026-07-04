# rdx-dev-creator-lab 🛠️🎨

Welcome to the **rdx-dev-creator-lab** (formerly `Manim-DSA-SD-Concepts`). This is a central, structured playground and production laboratory for the **Developer-Creator**—an engineer who combines deep systems and algorithmic understanding with high-fidelity, interactive, and programmatic storytelling.

Here, we explore, learn, and build visuals for system designs, data structures, algorithms, and interactive web documents.

> **New to the repo?** Start with the repo-wide video production playbook at [docs/video-production/README.md](file:///Users/rajatsavdekar/Documents/GitHub/Manim-DSA-SD-Concepts/docs/video-production/README.md).

---

## 🏗️ Repository Layout

The repository is split into two clean parts: **Learning Playgrounds** (to explore new tools and master basics) and **Projects** (production-ready showcases and videos).

```
.
├── learning/                       # PART 1: The Tool Playgrounds
│   ├── manim-basics/               # Python-based programmatic math & DSA animations
│   ├── remotion-basics/            # React/HTML/CSS-based video rendering
│   ├── godot-basics/               # Lightweight real-time algorithm simulations
│   ├── web-interactive-basics/     # MDX, Spline, Three.js, Sandpack, and GSAP/Framer Motion
│   └── voice-testing/              # Audio test files and speech analysis
│
├── projects/                       # PART 2: Visual Showcases
│   ├── aura/                       # On-device AI/visionOS design video & assets
│   ├── celestia-presentation/      # CelestiaVR technical decision presentation
│   ├── channel-intro/              # Channel motion graphics and logo intro
│   └── dsa-toolkit/                # Programmatic data structure visualizer toolkit
│
├── docs/                           # Centralized video-production playbooks
├── pyproject.toml                  # Shared uv project root (Manim python dependencies)
└── uv.lock
```

---

## 🛠️ The Developer-Creator Stack

This lab is powered by a curated, elite set of open-source and professional tools designed to bring software engineering concepts to life. 

| Category | Tool | Best Used For | Learning Path |
| :--- | :--- | :--- | :--- |
| **DSA & Math** | **[Manim CE](https://www.manim.community/)** | Programmatic vector animations, math, algorithm traversals, and abstract graphs. | [`learning/manim-basics/`](file:///Users/rajatsavdekar/Documents/GitHub/Manim-DSA-SD-Concepts/learning/manim-basics/README.md) |
| **System UIs** | **[Remotion](https://www.remotion.dev/)** | Programmatic web-based videos. Excellent for UI layouts, database tables, and API payloads. | [`learning/remotion-basics/`](file:///Users/rajatsavdekar/Documents/GitHub/Manim-DSA-SD-Concepts/learning/remotion-basics/README.md) |
| **Interactive** | **[Godot Engine](https://godotengine.org/)** | Light, interactive 2D/3D visualizer apps and pathfinding simulations. GDScript syntax is Python-like. | [`learning/godot-basics/`](file:///Users/rajatsavdekar/Documents/GitHub/Manim-DSA-SD-Concepts/learning/godot-basics/README.md) |
| **3D Web** | **[React Three Fiber](https://r3f.docs.pmnd.rs/)** | 3D browser-based canvas animations and interactive network graphs. | [`learning/web-interactive-basics/`](file:///Users/rajatsavdekar/Documents/GitHub/Manim-DSA-SD-Concepts/learning/web-interactive-basics/README.md) |
| **3D Assets** | **[Spline](https://spline.design/)** | Designing interactive 3D assets visually and exporting them directly as React web components. | [`learning/web-interactive-basics/`](file:///Users/rajatsavdekar/Documents/GitHub/Manim-DSA-SD-Concepts/learning/web-interactive-basics/README.md) |
| **Web Writing** | **[MDX](https://mdxjs.com/)** | Writing standard markdown technical articles that run interactive React components inline. | [`learning/web-interactive-basics/`](file:///Users/rajatsavdekar/Documents/GitHub/Manim-DSA-SD-Concepts/learning/web-interactive-basics/README.md) |
| **Web Playgrounds** | **[Sandpack](https://sandpack.codesandbox.io/)** | Embedding live running code editors inside your articles for interactive reader experimentation. | [`learning/web-interactive-basics/`](file:///Users/rajatsavdekar/Documents/GitHub/Manim-DSA-SD-Concepts/learning/web-interactive-basics/README.md) |
| **Motion** | **[GSAP](https://gsap.com/) & [Framer Motion](https://www.framer.com/motion/)** | Smooth scrollytelling (scroll-driven animations) and UI micro-animations on the web. | [`learning/web-interactive-basics/`](file:///Users/rajatsavdekar/Documents/GitHub/Manim-DSA-SD-Concepts/learning/web-interactive-basics/README.md) |

---

## 💼 Resume Pitch: Framing Your Creator Work for Hiring Managers

Teaching is the highest proof of engineering mastery. When presenting this work to hiring managers, focus on **technical communication, architectural depth, and programmatic automation** rather than video view counts:

1.  **Emphasize System Visualizations:** Present your explainers as visual documentation. Senior/Staff engineers must frequently write RFCs and design sheets that communicate complex architectures to stakeholders.
2.  **Highlight Automation Tooling:** Mention that you built a programmatic pipeline (using Whisper and FFmpeg) to automatically align audio files and generate visual freezes, cutting video-rendering times.
3.  **Resume Bullet Point Examples:**
    *   *Designed and built **rdx-dev-creator-lab**, an open-source visual lab combining Python (Manim), React (Remotion), and Godot to programmatically render algorithm visualizers and system architectures.*
    *   *Authored deep-dive technical explainers for complex projects (e.g., dual-pipeline on-device ML segmentation on visionOS), translating system bottlenecks into high-fidelity animated assets.*
    *   *Built custom audio-video automation tools using Whisper API transcripts and FFmpeg command chains to automate speech-to-video alignment.*

---

## 🚀 Quick Start: Running Projects

Each sub-project in `projects/` is self-contained. `cd` into the project directory to run scripts:

```bash
# Render a DSA Linked List Scene
cd projects/dsa-toolkit
uv run manim -pqh scenes.py IntroToLinkedListScene

# Render the Celestia technical presentation
cd projects/celestia-presentation
uv run manim --renderer=opengl -qh scene3.py S3_Clip1_CelestialGrid
```
