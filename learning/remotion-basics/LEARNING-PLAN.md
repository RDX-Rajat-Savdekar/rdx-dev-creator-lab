# Remotion Learning Roadmap 🧪📈

This plan takes you step-by-step from writing your first static React elements to building high-fidelity animated system design diagrams. 

---

## 🗺️ The Path to Mastery

### 🏁 Stage 1: Hello World & Interpolation (Visual Math)
*   **Goal:** Understand how frames, frame rate (`fps`), and duration drive visual updates. Master mapping a frame number to style attributes.
*   **Key Concepts:** `useCurrentFrame()`, `useVideoConfig()`, and `interpolate()`.
*   **Lab Exercises:**
    1.  **Fade In/Out:** Animate `opacity` from `0` to `1`, then back to `0`.
    2.  **Transformations:** Animate a box sliding from left to right, scaling up, and rotating.
*   **🛠️ Mini Project 1:** *The Pulsing Server.* Draw a server box and make its border or glow pulse like a heartbeat (using sine/cosine math mapped to frames).

---

### 🟢 Stage 2: Springs & Absolute Positioning
*   **Goal:** Create natural, physics-based motion instead of linear transitions. Learn how to stagger layout entries.
*   **Key Concepts:** `spring()`, `<AbsoluteFill>`, and `<Sequence>`.
*   **Lab Exercises:**
    1.  **Bounce-In:** Use spring configurations (`damping`, `mass`, `stiffness`) to pop a card onto the screen with a natural bounce.
    2.  **Staggered List:** Arrange a list of three nodes and animate them entering one-by-one with a 15-frame delay.
*   **🛠️ Mini Project 2:** *Database Node Cluster.* Animate a Master Database database node popping up, followed by three replica database nodes branching off from it sequentially.

---

### 🔵 Stage 3: SVG & Network Flows
*   **Goal:** Animate lines, connection pipes, and data packet flows.
*   **Key Concepts:** SVG `<path>`, `strokeDasharray`, `strokeDashoffset`, and position interpolation along coordinates.
*   **Lab Exercises:**
    1.  **Self-Drawing Line:** Make a connection arrow draw itself from Node A to Node B.
    2.  **Floating Packet:** Animate a small circle (data packet) traveling along an SVG line path.
*   **🛠️ Mini Project 3:** *Load Balancer & Request Router.* Animate requests (packets) flying from a "Client" box to a "Load Balancer" box, which then distributes them alternately to "Web Server A" and "Web Server B".

---

### 🟣 Stage 4: Audio & Timeline Sync
*   **Goal:** Sync your animations cleanly to voiceover tracks.
*   **Key Concepts:** `<Audio>` component, visual delays, and managing timeline markers.
*   **Lab Exercises:**
    1.  **VO Triggers:** Fade in labels at the exact moment a voiceover speaks a specific keyword.
*   **🛠️ Mini Project 4:** *A Complete 60s Tech Explainer.* Create a 60-second video explaining a simple system concept (e.g., *"How a Cache works"* or *"What is CDN"*), complete with your own voiceover and animated UI indicators.

---

## 🚀 How to Begin Stage 1
Once your IDE paths are resolved, go to `src/HelloWorld.tsx` and delete the contents of the file. We will write a clean, minimal file together to practice **Stage 1 (Interpolation)**.
