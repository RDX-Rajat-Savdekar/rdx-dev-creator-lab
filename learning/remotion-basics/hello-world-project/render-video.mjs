import { bundle } from "@remotion/bundler";
import { renderMedia, selectComposition } from "@remotion/renderer";
import path from "path";
import fs from "fs";

async function renderPersonalizedCard() {
  console.log("🚀 Starting Stage 6 programatic render automation...");

  // 1. Point to the entry file (webpack entry)
  const entryPoint = path.resolve("src/index.ts");
  console.log(`📦 Bundling project entry point: ${entryPoint}`);

  const bundleLocation = await bundle({
    entryPoint,
    // Optional webpack custom configurations can go here
  });
  console.log(`✅ Bundle created successfully at: ${bundleLocation}`);

  // 2. Define custom user stats to inject as input props (like reading from a DB)
  const inputProps = {
    userName: "Rajat Savdekar",
    contributions: 2450,
    linesWritten: 128450,
    favLang: "TypeScript",
    favoriteHexColor: "#06b6d4", // Cyan accent highlight
  };

  const compositionId = "stage6-personalized-card";
  console.log(`🔍 Selecting composition: ${compositionId}`);

  // 3. Select the composition details from the bundle
  const composition = await selectComposition({
    serveUrl: bundleLocation,
    id: compositionId,
    inputProps,
  });

  // Ensure output folder exists
  const outputDir = path.resolve("out");
  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir);
  }

  const outputLocation = path.join(outputDir, "personalized_video.mp4");
  console.log(`🎥 Rendering frames and compiling audio into: ${outputLocation}...`);

  // 4. Trigger rendering to final MP4
  await renderMedia({
    serveUrl: bundleLocation,
    composition,
    outputLocation,
    inputProps,
    codec: "h264",
    onProgress: ({ progress }) => {
      const percentage = Math.round(progress * 100);
      console.log(`⏳ Render progress: ${percentage}%`);
    },
  });

  console.log(`\n🎉 Done! Video compiled successfully to:`);
  console.log(`👉 ${outputLocation}`);
}

renderPersonalizedCard().catch((err) => {
  console.error("❌ Render failed with error:", err);
  process.exit(1);
});
