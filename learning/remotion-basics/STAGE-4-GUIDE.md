# Remotion Stage 4: Audio & Timeline Syncing 🎧⏱️

Welcome to the final stage of your Remotion journey! In Stage 4, we learn how to sync visual animations with audio files and narration tracks. This is critical for making videos that feel professional and highly coordinated.

---

## 🗺️ What You Are Learning

### 1. The `<Audio>` Component
Remotion provides an `<Audio>` component to play sound files (`.mp3`, `.wav`, etc.) in your compositions:
* It supports playing a track inline while previewing in the browser.
* During rendering (`remotion render`), the audio will be mixed into the final video file.
* You can import audio tracks from your assets folder or refer to local paths.

#### Basic Usage:
```tsx
import { Audio } from "remotion";
import musicTrack from "./assets/music.mp3";

export const MyComposition = () => {
  return (
    <AbsoluteFill>
      <Audio src={musicTrack} volume={0.5} />
    </AbsoluteFill>
  );
};
```

---

### 2. Time Offsetting & Delaying Audio
You can specify *when* an audio track starts playing using the `startFrom` prop, or offset its playback using `volume` or nested `<Sequence>` elements:
* **`startFrom={30}`**: The audio will start playing from its own 30th frame (skipping the first second).
* **Using `<Sequence from={60}>`**: The audio will only begin playing once the video reaches frame 60.

---

### 3. Visual Cues & Narration Syncing (Timeline Markers)
When syncing animations to a voiceover, it's best practice to structure your components based on **timeline frame indices**.
Instead of using complex relative spring timing, we map keyframes to absolute video frames:
- **Frame `30`**: Speaker says *"First, we check the cache..."* $\rightarrow$ Animate cache lookup line.
- **Frame `110`**: Speaker says *"If it is a cache hit..."* $\rightarrow$ Highlight Cache card green.
- **Frame `180`**: Speaker says *"Otherwise, we fetch from DB..."* $\rightarrow$ Animate database retrieval line.

By using simple conditional logic or mapping `frame` inside `interpolate()`, you can orchestrate multi-step educational systems design explainers.

---

## 🛠️ Files to Explore

1. **[TechExplainer.tsx](file:///Users/rajatsavdekar/Documents/GitHub/rdx-dev-creator-lab/learning/remotion-basics/hello-world-project/src/Stage4_Audio/TechExplainer.tsx)**
   * *What it does:* Combines a premium dark-themed system design visualization explaining "How CDN Caching Works". 
   * Syncs multiple animation triggers (client request, cache lookup, cache miss, server fetch) with timeline markers.
   * Plays a background music track (`solarflex-hype-background-music-558271.mp3`) with adjusted volume.
