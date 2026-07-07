# Interactive Web Explainers Basics 🌐✨

To build interactive portfolio articles like Gemini’s in-app widgets or advanced technical blogs, you want to combine written words (Markdown) with live, reactive widgets. This guide compiles the setup, basic syntax, and resources for the elite developer-creator web stack: **MDX, React Three Fiber, Spline, Sandpack, Framer Motion, and GSAP**.

---

## 1. MDX (Markdown + JSX)
MDX allows you to write standard Markdown text but import and render custom React/JSX components directly inside your content.

### Basic MDX File Example (`article.mdx`)
```mdx
import { SortingVisualizer } from './components/SortingVisualizer';

# Explaining Merge Sort

Merge sort is a divide-and-conquer algorithm. It splits the array in half, recursively sorts each half, and merges them.

Here is a live simulation. Try clicking **"Step"** to watch the indices swap:

<SortingVisualizer initialArray={[4, 2, 7, 1]} />

Notice how the search space shrinks systematically...
```

---

## 2. Three.js & React Three Fiber (R3F)
React Three Fiber is a React renderer for Three.js. It lets you write browser-based 3D animations and interactive network nodes declaratively.

### Installation
```bash
npm install three @types/three @react-three/fiber @react-three/drei
```

### Simple 3D Cube Canvas Component
```tsx
import React, { useRef } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { Mesh } from 'three';

const SpinningCube = () => {
  const meshRef = useRef<Mesh>(null);

  // Rotate the cube on every frame loop
  useFrame((state, delta) => {
    if (meshRef.current) {
      meshRef.current.rotation.x += delta;
      meshRef.current.rotation.y += delta;
    }
  });

  return (
    <mesh ref={meshRef}>
      <boxGeometry args={[2, 2, 2]} />
      <meshStandardMaterial color="#58a6ff" />
    </mesh>
  );
};

export const App = () => (
  <div style={{ width: '100vw', height: '100vh', backgroundColor: '#0d1117' }}>
    <Canvas>
      <ambientLight intensity={0.5} />
      <directionalLight position={[10, 10, 5]} intensity={1} />
      <SpinningCube />
    </Canvas>
  </div>
);
```

---

## 3. Spline (Visual 3D & React Integration)
[Spline](https://spline.design/) is a visual 3D design editor. You can design server layouts, databases, and microprocessors visually, set up triggers (hover, click, orbit) inside their GUI, and embed the scene directly in your React page.

### Installation
```bash
npm install @splinetool/react-spline
```

### React Embedding Example
```tsx
import Spline from '@splinetool/react-spline';

export default function SystemDesignScene() {
  return (
    <div style={{ width: '100%', height: '500px' }}>
      {/* Paste the Spline scene URL generated in the export panel */}
      <Spline scene="https://prod.spline.design/your-scene-id/scene.splinecode" />
    </div>
  );
}
```

---

## 4. Sandpack (Inline Runnable Code Playgrounds)
[Sandpack](https://sandpack.codesandbox.io/) by CodeSandbox is a React component that lets you render live code editors and run previews inside your articles.

### Installation
```bash
npm install @codesandbox/sandpack-react
```

### React Embedding Example
```tsx
import { Sandpack } from "@codesandbox/sandpack-react";

export const InteractiveCode = () => (
  <Sandpack
    template="react"
    theme="dark"
    files={{
      "/App.js": `export default function App() {
  return <h1>Edit me live in the article!</h1>
}`
    }}
  />
);
```

---

## 5. Framer Motion & GSAP (Scroll-Driven Animating)
Scroll-driven animations (**Scrollytelling**) are animations that lock their progression to the user's scrollbar. As the user reads, network lines light up or server blocks fade in.

### Framer Motion: Simple Hover and Transition
```tsx
import { motion } from 'framer-motion';

export const LoadBalancerNode = () => (
  <motion.div
    whileHover={{ scale: 1.1, backgroundColor: '#58a6ff' }}
    initial={{ opacity: 0, y: 50 }}
    animate={{ opacity: 1, y: 0 }}
    transition={{ duration: 0.5 }}
    style={{ padding: '20px', borderRadius: '8px', border: '1px solid gray' }}
  >
    Load Balancer Node
  </motion.div>
);
```

### GSAP: ScrollTrigger Scrollytelling Setup
```javascript
import gsap from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';

gsap.registerPlugin(ScrollTrigger);

// Animate a database line to fill on scroll
gsap.to(".network-path", {
  strokeDashoffset: 0,
  scrollTrigger: {
    trigger: ".explainer-section",
    start: "top center", // Animation starts when top of trigger hits center of screen
    end: "bottom center",
    scrub: true, // Ties animation timeline directly to scroll speed
  }
});
```

---

## 📚 Useful Resources
*   [MDX Official Docs](https://mdxjs.com/)
*   [React Three Fiber Documentation](https://r3f.docs.pmnd.rs/getting-started/introduction)
*   [Spline Design Home](https://spline.design/)
*   [Sandpack by CodeSandbox Docs](https://sandpack.codesandbox.io/docs)
*   [GSAP ScrollTrigger Docs](https://gsap.com/docs/v3/Plugins/ScrollTrigger/)
*   [Framer Motion Docs](https://www.framer.com/motion/)
