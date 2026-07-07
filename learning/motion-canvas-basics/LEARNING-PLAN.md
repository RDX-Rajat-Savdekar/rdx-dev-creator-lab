# Motion Canvas Learning Roadmap 🧪📊

This document lays out the conceptual shift and learning path for mastering **Motion Canvas** to build fluid algorithm visualizers (DSA) and system design diagrams.

---

## 🧠 Mental Model Shift: Remotion vs. Motion Canvas

When transitioning from Remotion to Motion Canvas, you must shift from a **declarative, stateless frame-ticking model** to an **imperative, stateful generator-thread model**.

| Dimension | Remotion 📹 | Motion Canvas 🎨 |
| :--- | :--- | :--- |
| **Execution Paradigm** | **Stateless Declarative React:** Re-renders component function on every frame. | **Stateful Imperative Generator:** Runs once as a generator `function*` mutating node state. |
| **Animation Trigger** | Frame interpolation: `interpolate(frame, [0, 30], [0, 1])` driven by `useCurrentFrame()`. | Yielding generator commands: `yield* node.opacity(1, 1)` (animate opacity to 1 over 1 second). |
| **Timeline Control** | Calculated frame offsets: `<Sequence from={30}>` or mathematical frame arithmetic. | Sequential instructions: `yield* delay(1);` or staggered loops inside the generator. |
| **Parallel vs. Sequential** | Parallel by default (everything is evaluated at frame $N$); sequence containers isolate time. | Sequential by default. Run parallel updates explicitly using `yield* all(...)` or `any(...)`. |
| **Coordinate Origin** | Top-left `(0, 0)` based on standard HTML/CSS DOM box layouts. | Screen center `(0, 0)` based on mathematical cartesian space. |
| **State Retention** | No persistent instance state between frames. Rederived from props/current frame. | Stateful: nodes maintain coordinates and properties that you modify over time. |

---

## 📐 Vector Space & Coordinate Systems

In Motion Canvas, everything is drawn on an HTML5 2D Canvas. This changes how you position and layout components:

1. **The Origin is Centered:** 
   - A screen of size `1920x1080` has its center at `(0, 0)`.
   - Top-left is `(-960, -540)`.
   - Bottom-right is `(960, 540)`.
   - Positive $X$ coordinates move **right**.
   - Positive $Y$ coordinates move **down**.
2. **Signals as Mutators:**
   - Visual properties (e.g. position, scale, opacity, size) are wrapped in **Signals**.
   - Read a property value: `const posX = node.position.x();`
   - Set/animate a property value: `yield* node.position.x(200, 1.5);` (moves $X$ to 200 over 1.5s).
3. **Hierarchy and Alignment:**
   - Nested nodes inherit their parent's coordinate systems.
   - You can group nodes inside a `<Layout>` container to use automatic layout engines (CSS Flexbox models like `gap`, `direction`, `alignItems`).

---

## 🗺️ The Path to Mastery

### 🏁 Stage 1: Vector Shapes, Coordinate Spaces, & Generator Timelines [COMPLETED]
*   **Goal:** Master standard 2D vector elements (`Rect`, `Circle`, `Line`), coordinate translations, basic easing, and sequential/parallel generator execution.
*   **Key Concepts:** `makeScene2D()`, `createRef()`, `yield*`, `all()`, `to()`, easing functions.
*   **Mini Project:** *The Network Packet Router.* Animated a visual node at the center of the canvas drawing dynamic circular scanner paths, spawning child nodes connected by lines, and routing a glowing packet along those lines using coordinate translations.

---

### 🏁 Stage 2: Signals, References, & CSS Flexbox Layouts [ACTIVE]
*   **Goal:** Create dynamic component structures that automatically adapt their positions when contents change, driving background tasks concurrently.
*   **Key Concepts:** `createSignal()`, `createRefMap()`, CSS Flexbox in Canvas (`Layout` component, `gap`, `direction`, `alignItems`), component composition, concurrent background threads with `spawn()`.
*   **Mini Project:** *Adaptive Database Server Stack.* Render a dynamic vertical stack of server node blocks. Use `spawn()` to run independent background heartbeat pulse animations on each database block. Triggering a layout scale-up on one database node should smoothly push adjacent servers down.

---

### 🏁 Stage 3: SVG Curved Paths & Network Flow Storytelling
*   **Goal:** Write network pipelines with curved connections and custom flows.
*   **Key Concepts:** `Path` shapes, bezier curves with `<Spline />`, SVG path data, line drawing progress (`line.end()`), staggered execution loops, flow particles moving along curves.
*   **Mini Project:** *Kafka Message Queue Broker.* Draw a publisher node transmitting packets along dynamic curved paths to a central broker (rendered as a partitioned horizontal message queue). Stagger multiple consumers pulling packets off the partitions in real-time.

---

### 🏁 Stage 4: Custom Nodes & Algorithmic Tree Traversal (DSA Visuals)
*   **Goal:** Learn to separate visual presentation from logic by writing self-drawing custom components and algorithmic visualizer controllers.
*   **Key Concepts:** Extending `Node` class, `@signal` properties decoration, JSX element factories, runtime algorithmic state mapping, syntax-highlighted code transitions with the `<Code />` component.
*   **Mini Project:** *Binary Search Tree Traversal Visualizer.* Scaffold a custom `TreeNode` node component with circles and connecting parent-child pointers. Write a generator that executes an In-Order traversal, highlighting nodes, and filling an array tracker at the bottom of the screen while a visual `<Code />` block traces execution line-by-line.

---

### 🏁 Stage 5: Audio Narration & Video Export Automation
*   **Goal:** Mux voiceovers with custom timings and render the project into high-fidelity MP4 videos programmatically.
*   **Key Concepts:** Audio alignment, generator synchronization markers (`useAudio()`, custom timing sync), CLI render parameters, `@motion-canvas/ffmpeg` exports.
*   **Mini Project:** *Microservices Saga Orchestration explainer.* Render a 1-minute high-fidelity system design animation illustrating database transaction rollbacks, synchronized perfectly to an audio voiceover.
