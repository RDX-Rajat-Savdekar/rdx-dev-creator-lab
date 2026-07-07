# Remotion Stage 6: Programmatic Video Automation 🤖⚙️

Welcome to Stage 6! In this stage, we transition from previewing in the browser to **automating video renders from data files**. This is the core engine behind SaaS personalized video generators (like Spotify Wrapped or custom onboarding greetings).

---

## 🗺️ What You Are Learning

### 1. The Rendering Pipeline
To compile a React composition into an `.mp4` video, Remotion does the following behind the scenes:
1. **Bundles the Code**: Compiles your React/TypeScript code using Webpack into a single static web bundle.
2. **Spawns headless Chrome**: Opens the bundled page inside Puppeteer (headless Chrome).
3. **Captures Frames**: Seeks through the composition frame-by-frame and screenshots each canvas as a PNG frame.
4. **Stitches Video**: Feeds these PNG frames (along with audio tracks) to FFmpeg to stitch them into a final high-performance `.mp4` container.

---

### 2. Rendering Programmatically in Node.js
Instead of running `npx remotion render` manually in the console, you can invoke Remotion's API inside a standard Node script:
* **`bundle()`**: Compiles the code entry point.
* **`selectComposition()`**: Fetches properties of the registered composition.
* **`renderMedia()`**: Initiates frame rendering and FFmpeg encoding.

This allows you to loop over database records, pass custom props to each render call, and output custom customized video files automatically!

---

## 🛠️ Files to Explore

1. **[PersonalizedCard.tsx](file:///Users/rajatsavdekar/Documents/GitHub/rdx-dev-creator-lab/learning/remotion-basics/hello-world-project/src/Stage6_Automation/PersonalizedCard.tsx)**
   * *What it does:* A personalized profile card displaying stats like contributions, favorite languages, and total lines coded. Exposes a Zod schema so props can be dynamically injected.
2. **[render-video.mjs](file:///Users/rajatsavdekar/Documents/GitHub/rdx-dev-creator-lab/learning/remotion-basics/hello-world-project/render-video.mjs)**
   * *What it does:* A Node rendering script. It loops over a dataset, launches Puppeteer, injects personalized props, and renders custom MP4 outputs automatically.
