# Remotion Stage 10: Canvas Skia & Dynamic Vector Graphics 🎨⚡

Welcome to Stage 10! In this final stage, we explore **high-performance 2D vector drawing** inside Remotion using **Skia** (`@remotion/skia`).

---

## 🗺️ What You Are Learning

### 1. What is Skia?
Skia is the core 2D graphics engine that drives Chrome, Android, Flutter, and Google Docs.
- In normal React, rendering hundreds of individual DOM nodes (e.g. `<circle>` inside SVGs) can cause significant rendering bottlenecks and slow down Webpack bundles.
- Skia renders graphics on a single `<Canvas>` using efficient coordinate drawing scripts.
- Remotion integrates with **React Native Skia**, exposing components like `<Canvas>`, `<Group>`, `<Path>`, and `<Paint>`.

---

### 2. Basic Skia Markup
Instead of standard SVG tags, Skia components are capitalized React wrappers:
```tsx
import { Canvas, Circle, Group, Paint } from "@remotion/skia";

<Canvas width={800} height={600}>
  <Group>
    {/* Inner elements are drawn onto the canvas */}
    <Circle cx={150} cy={150} r={50}>
      <Paint color="#38bdf8" />
    </Circle>
  </Group>
</Canvas>
```
To enable Skia in Remotion, you simply import `enableSkia` in `remotion.config.ts` and wrap your Webpack configuration.

---

## 🛠️ Files to Explore

1. **[SkiaLoadBalancer.tsx](file:///Users/rajatsavdekar/Documents/GitHub/rdx-dev-creator-lab/learning/remotion-basics/hello-world-project/src/Stage10_Skia/SkiaLoadBalancer.tsx)**
   * *What it does:* Uses `@remotion/skia` to render a high-performance **Fluid Dynamic Load Balancer** with 150+ glowing particles traveling down pipe networks in real-time, showcasing how to build intense data flow mockups efficiently.
