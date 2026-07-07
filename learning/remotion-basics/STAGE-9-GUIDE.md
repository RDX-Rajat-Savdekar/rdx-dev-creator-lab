# Remotion Stage 9: Interactive Algorithms & The Remotion Player 🕹️🧮

Welcome to Stage 9! In this stage, we focus on **embedding compositions inside standard web pages** and **creating user-driven interactions** (like sorting step-by-step algorithms).

---

## 🗺️ What You Are Learning

### 1. The `@remotion/player` Component
Instead of rendering static video files, you can embed a Remotion canvas directly in any standard React application:
```tsx
import { Player } from "@remotion/player";
import { MyComposition } from "./MyComposition";

<Player
  component={MyComposition}
  durationInFrames={180}
  fps={30}
  compositionWidth={1920}
  compositionHeight={1080}
  style={{ width: 640, height: 360 }}
  controls // Shows play/pause/timeline scrub controls in the browser
/>
```
This is ideal for dynamic web products (e.g. customized video generators, educational sandboxes, or algorithm playgrounds).

---

### 2. Live React State & Interactive Canvas
Remotion's Dev Studio runs inside a standard browser tab. **Because it is just a live React app, UI inputs, buttons, and click handlers work perfectly in the preview window!**
- You can use standard React `useState` hooks to track user variables (like custom array values or current sort indices).
- Clicking a button on the screen updates the state, instantly triggering a react re-render of the canvas.
- This allows you to step through data structure algorithms (like Bubble Sort) step-by-step, letting viewers see how indices swap values live!

---

## 🛠️ Files to Explore

1. **[SortingVisualizer.tsx](file:///Users/rajatsavdekar/Documents/GitHub/rdx-dev-creator-lab/learning/remotion-basics/hello-world-project/src/Stage9_Player/SortingVisualizer.tsx)**
   * *What it does:* A Bubble Sort visualizer showing data bars. Features interactive UI buttons (Play, Pause, Step Next, Randomize) that update state, allowing you to step through swaps directly in the browser preview!
