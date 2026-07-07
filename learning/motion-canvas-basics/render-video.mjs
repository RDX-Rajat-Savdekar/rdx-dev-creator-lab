import { execSync } from 'child_process';
import path from 'path';
import fs from 'fs';

console.log('\n🎬 --- Motion Canvas CLI Frame Compiler Utility ---');
console.log('mental model: Motion Canvas compiles to MP4 in the browser editor using the @motion-canvas/ffmpeg plugin.');
console.log('This script serves as a manual fallback to compile raw PNG frames into high-fidelity MP4 videos.\n');

// 1. Verify FFmpeg installation
try {
  const version = execSync('ffmpeg -version').toString().split('\n')[0];
  console.log(`✅ System check: ${version}`);
} catch (e) {
  console.error('❌ Error: FFmpeg CLI was not found on the local system path.');
  console.log('Please ensure FFmpeg is installed and added to your environment variables.');
  process.exit(1);
}

// 2. Locate output frames directory
const outputPath = path.resolve('output');
if (!fs.existsSync(outputPath)) {
  console.log(`⚠️  Warning: The "output/" directory does not exist at: ${outputPath}`);
  console.log('Please run the browser editor (npm start) and execute a render pass first.');
  process.exit(0);
}

// Read subdirectories to find compiled image sequences
const dirs = fs.readdirSync(outputPath).filter(f => fs.statSync(path.join(outputPath, f)).isDirectory());
if (dirs.length === 0) {
  console.log('⚠️  No compiled scene folders found inside "output/".');
  process.exit(0);
}

console.log(`\nFound scene output folders: ${dirs.map(d => `"${d}"`).join(', ')}`);

// Compile each directory
for (const dir of dirs) {
  const scenePath = path.join(outputPath, dir);
  const frames = fs.readdirSync(scenePath).filter(f => f.endsWith('.png'));
  if (frames.length === 0) {
    console.log(`Skipping "${dir}": No PNG files found inside.`);
    continue;
  }

  // Extract sorting template (usually named %06d.png or project-####.png)
  const sampleFrame = frames[0];
  let pattern = '%06d.png'; // default
  
  // Detect standard Motion Canvas pattern (e.g. project-000001.png or 000001.png)
  if (sampleFrame.startsWith('project-')) {
    pattern = 'project-%06d.png';
  } else if (/^\d+\.png$/.test(sampleFrame)) {
    const digitCount = sampleFrame.split('.')[0].length;
    pattern = `%0${digitCount}d.png`;
  }

  const outputVideo = path.join(outputPath, `${dir}.mp4`);
  const inputPattern = path.join(scenePath, pattern);

  console.log(`\nCompiling "${dir}" frames into video...`);
  console.log(`Input: ${inputPattern}`);
  console.log(`Output: ${outputVideo}`);

  // FFmpeg command to compile 60fps high-quality H264 MP4
  const command = `ffmpeg -y -framerate 60 -i "${inputPattern}" -c:v libx264 -pix_fmt yuv420p -crf 18 "${outputVideo}"`;
  
  try {
    execSync(command, { stdio: 'inherit' });
    console.log(`🎉 Success! Video saved to: ${outputVideo}`);
  } catch (err) {
    console.error(`❌ Error compiling video for "${dir}":`, err.message);
  }
}
