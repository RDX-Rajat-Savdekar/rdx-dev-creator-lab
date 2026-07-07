# React Three Fiber Learning Plan 🌐🎨

This workspace playground is for learning **React Three Fiber (Three.js)** to build interactive WebGL 3D system architecture explainers.

---

## 🗺️ The 5-Stage Learning Roadmap

### Stage 1: 3D Scene Graph, Lighting, & Material Meshes 💡
*   **Goal:** Learn how `<Canvas>` initializes the Three.js viewport, place standard geometries (`<boxGeometry>`, `<cylinderGeometry>`), apply realistic materials (`<meshStandardMaterial>` with roughness/metalness), and set up lighting (ambient, directional, point lights).
*   **Mini Project:** **Glowing Server Rack.** A metallic server container box with glowing status LED indicators.

### Stage 2: Animation Frame Loop & Interactive Events 🕹️
*   **Goal:** Master the `useFrame()` hook to run custom animation loops, and capture pointer events (`onPointerOver`, `onPointerOut`, `onClick`) to alter state.
*   **Mini Project:** **Interactive Load Balancer.** A spinning node that changes color on hover and scales up dynamically on click.

### Stage 3: Groups, Arrays, & Circular Layouts 📐
*   **Goal:** Group multiple nodes using `<group>` to coordinate positions, and use trigonometry to lay out meshes programmatically (e.g. databases in a ring).
*   **Mini Project:** **Sharded Database Ring.** Five database cylinders arranged in a 3D ring with rotating replica status nodes.

### Stage 4: Orbit Camera Controls & Target Focus 🎥
*   **Goal:** Integrate `@react-three/drei`'s `<OrbitControls>` for interactive pan/zoom, and write camera interpolation scripts to focus on clicked nodes.
*   **Mini Project:** **Kubernetes Pod Explorer.** A grid of microservice cubes where clicking a cube smooth-focuses the camera on it.

### Stage 5: 3D Particle Streams (Networking Cables) ⚡
*   **Goal:** Render moving 3D particle systems to visualize data flow between server nodes.
*   **Mini Project:** **WebGL Request Traffic Flow.** Glowing packets flying along 3D wires connecting an Ingress gateway to the Server Rack and Database Ring.
