# Remotion Basics ⚛️🎬

[Remotion](https://www.remotion.dev/) is a framework that allows you to write videos programmatically using **React, HTML, CSS, and SVG**. Instead of writing complex vector animation math (like in Manim) or using video editing software (like Premiere or After Effects), you write standard web components, style them with Tailwind, and animate them using frame-based timeline code.

Remotion is the absolute best tool for **System Design animations** because building mockups of web browsers, dashboard cards, API requests, database tables, and JSON payloads is infinitely easier using CSS/HTML than coordinates in Python.

---

## 🚀 Setup & Execution

To create a new Remotion project in this folder, use `npx`:

```bash
# Initialize a new Remotion project inside learning/remotion-basics/
npx -y create-video@latest ./
```

### Key CLI Commands
Once inside your Remotion project directory:
*   `npm run dev` / `npm start`: Launches the local browser-based preview player (usually at `localhost:3000`). It has an interactive timeline, hot reloading, and visual debugging.
*   `npm run build`: Compiles and renders your React components into a final `.mp4` file.

```bash
# Render a specific composition to MP4
npx remotion render src/index.ts MyComposition out/video.mp4
```

---

## ⚙️ Core Concepts

Remotion uses a few key primitives to translate React into video:

### 1. The Composition (`src/Root.tsx`)
A Composition registers your React component as a renderable video track, defining its duration, resolution, and frame rate.
```tsx
import { Composition } from 'remotion';
import { MainScene } from './MainScene';

export const Root: React.FC = () => {
  return (
    <Composition
      id="SystemDesignExplainer"
      component={MainScene}
      durationInFrames={150} // 5 seconds at 30 fps
      fps={30}
      width={1920}
      height={1080}
    />
  );
};
```

### 2. The Timeline Hooks (`src/MainScene.tsx`)
In Remotion, there are no state changes over time. Instead, the video is rendered frame-by-frame. You use hooks to find out exactly which frame is currently rendering.
*   `useCurrentFrame()`: Returns the current frame index (from `0` to `durationInFrames - 1`).
*   `useVideoConfig()`: Returns video metadata (width, height, fps, duration).

### 3. Interpolation (`interpolate`)
Interpolation is how you animate properties. It maps a frame number to a CSS property (like opacity, scale, or position).
```tsx
import { useCurrentFrame, interpolate } from 'remotion';

export const MainScene = () => {
  const frame = useCurrentFrame();
  
  // Fade in opacity from 0 to 1 between frame 10 and frame 30
  const opacity = interpolate(frame, [10, 30], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  
  // Slide in from Y: 100 to Y: 0
  const translateY = interpolate(frame, [10, 35], [100, 0], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  return (
    <div style={{ 
      display: 'flex', 
      justifyContent: 'center', 
      alignItems: 'center', 
      height: '100%', 
      backgroundColor: '#0d1117' 
    }}>
      <h1 style={{ 
        color: '#58a6ff', 
        opacity,
        transform: `translateY(${translateY}px)`,
        fontFamily: 'system-ui'
      }}>
        API Load Balancer
      </h1>
    </div>
  );
};
```

---

## 💡 Best Practices for System Design Videos in Remotion
*   **Leverage Tailwind:** Style your nodes, load balancers, database icons, and clusters using Tailwind. It keeps layout designs clean and modern.
*   **Animate packet flows with SVGs:** Use SVG paths and `strokeDashoffset` to animate data packets traveling down network pipes.
*   **Use the `<Spring>` Component:** For spring-based animations (like UI cards scaling up organically on-screen), use Remotion's built-in `spring()` helper instead of linear interpolation. It looks much more premium and realistic.

---

## 📚 Useful Resources
*   [Remotion Official Documentation](https://www.remotion.dev/docs/)
*   [Spring Animations Guide](https://www.remotion.dev/docs/spring)
*   [Remotion Github Repository](https://github.com/remotion-dev/remotion)
