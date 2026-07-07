# Remotion Stage 8: Advanced Transitions & Dynamic Scene Sequences 🎥🎬

Welcome to Stage 8! In this stage, we cover **transitioning smoothly between distinct scenes**. When explaining complex system designs or DSA algorithms, you rarely present a single static grid. Instead, you walk the viewer through a series of steps (e.g., Scene 1 $\rightarrow$ Problem state, Scene 2 $\rightarrow$ Architectural solution, Scene 3 $\rightarrow$ Operational recovery).

Instead of hacking opacity keyframes or offset transitions, we use the official **`@remotion/transitions`** package.

---

## 🗺️ What You Are Learning

### 1. The Transition Series Layout
`@remotion/transitions` provides `<TransitionSeries>`, which is a wrapper that manages a sequence of scenes and transitions.
- A `<TransitionSeries.Sequence>` acts like a standard `<Sequence>` but dynamically scales its timings if transition durations overlap.
- A `<TransitionSeries.Transition>` animates the visual boundary between the preceding and succeeding sequences.
- During a transition, **both scenes render simultaneously** in the DOM. Remotion handles overlapping them frame-by-frame using CSS transitions/transforms behind the scenes.

---

### 2. Standard Transition Types
Remotion offers several pre-built transition types:
- **`slide`**: Slides the new scene in from a direction (left, right, top, bottom).
- **`wipe`**: Unrolls the new scene using a linear or circular mask.
- **`fade`**: Cross-fades the opacity between scenes.
- **`flip`**: Performs a 3D rotation flip of the screen canvas.

Example:
```tsx
import { TransitionSeries } from "@remotion/transitions";
import { slide } from "@remotion/transitions/slide";

<TransitionSeries>
  <TransitionSeries.Sequence durationInFrames={60}>
    <SceneOne />
  </TransitionSeries.Sequence>
  <TransitionSeries.Transition
    durationInFrames={15}
    transitionCode={slide({ direction: "left" })}
  />
  <TransitionSeries.Sequence durationInFrames={60}>
    <SceneTwo />
  </TransitionSeries.Sequence>
</TransitionSeries>
```

---

## 🛠️ Files to Explore

1. **[MonolithToMicroservices.tsx](file:///Users/rajatsavdekar/Documents/GitHub/rdx-dev-creator-lab/learning/remotion-basics/hello-world-project/src/Stage8_Transitions/MonolithToMicroservices.tsx)**
   * *What it does:* A 3-scene architecture explainer detailing a monolith database overloading and getting broken down into microservices, complete with clean slide and circular wipe transitions.
