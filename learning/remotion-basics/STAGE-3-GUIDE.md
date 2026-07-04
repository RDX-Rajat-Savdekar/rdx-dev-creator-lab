# Remotion Stage 3: SVG & Network Flows 🎨🔌

Welcome to Stage 3! Here, we dive into **SVG-based path manipulation**. This is the secret sauce behind dynamic lines, self-growing connections, packet routing animations, and custom vector illustrations.

---

## 🗺️ What You Are Learning

### 1. SVG Self-Drawing Lines (`strokeDasharray` and `strokeDashoffset`)
To make a line appear to "draw itself" dynamically, we use a clever CSS/SVG trick:
* **`strokeDasharray`**: Defines the pattern of dashes and gaps used to stroke paths. If set to the exact total length of the path (e.g., `500`), it means the path will have one dash of length `500`, followed by a gap of `500`.
* **`strokeDashoffset`**: Specifies the offset into the dash pattern. 
  - If `strokeDashoffset` is `500` (equal to path length), the gap covers the entire path, making it **invisible**.
  - If `strokeDashoffset` is `0`, the dash covers the entire path, making it **fully visible**.
* By interpolating `strokeDashoffset` from the path's length to `0`, we get a beautiful self-drawing line!

#### Code Pattern:
```tsx
const pathLength = 300;
const drawProgress = spring({ frame, fps });
const strokeDashoffset = interpolate(drawProgress, [0, 1], [pathLength, 0]);

return (
  <path
    d="M 10 10 L 310 10"
    stroke="white"
    strokeWidth={2}
    strokeDasharray={pathLength}
    strokeDashoffset={strokeDashoffset}
  />
);
```

---

### 2. Floating Packets Along Paths
To animate a request packet traveling along a connection line, we map the frame number to the coordinates of the packet:
* For linear horizontal or vertical lines, we can interpolate the absolute `left` or `top` position.
* For arbitrary paths, we can interpolate the offset of the packet circle along the connection vectors.
* By using modulo math (`frame % duration`), we can create a continuous stream of packets.

---

### 3. Animating Complex Vector SVGs (Mangekyou Sharingan)
SVGs are just XML elements. In React and Remotion, we can import an SVG and animate its sub-elements separately:
* **The Iris Background**: Animate its scale using `spring()`.
* **The Tomoe (Propeller) Blades**: Rotate the path using `transform: rotate(...)` driven by frame interpolation, or draw the outline using `strokeDashoffset` before filling it.
* **Pupil (Center)**: Animate the scale and glow opacity in sync.

---

## 🛠️ Files to Explore

1. **[RequestRouter.tsx](file:///Users/rajatsavdekar/Documents/GitHub/rdx-dev-creator-lab/learning/remotion-basics/hello-world-project/src/Stage3_SVG/RequestRouter.tsx)**
   * *What it does:* Animates requests flowing from a client to a load balancer, which then routes requests alternately to Web Server A and Web Server B.
   
2. **[SharinganIntro.tsx](file:///Users/rajatsavdekar/Documents/GitHub/rdx-dev-creator-lab/learning/remotion-basics/hello-world-project/src/Stage3_SVG/SharinganIntro.tsx)**
   * *What it does:* Activates a fully animated Itachi Mangekyou Sharingan. The outer iris pops in, the central tomoe path draws itself using stroke-dash, and then it rotates at high speed with a glowing overlay to lock onto the screen.
