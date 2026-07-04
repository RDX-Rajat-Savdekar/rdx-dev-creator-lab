import React from "react";
import {
  AbsoluteFill,
  interpolate,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";

export const Transformations: React.FC = () => {
  const frame = useCurrentFrame();
  const { durationInFrames } = useVideoConfig();

  // 1. Slide X: Slide from -300px to 300px between frame 0 and 60. Stay at 300px from 60 to 90.
  const translateX = interpolate(
    frame,
    [0, 60],
    [-300, 300],
    { extrapolateRight: "clamp" }
  );

  // 2. Scale: Scale up from 1.0 to 1.5 between frame 15 and 45. Scale back down to 1.0 between frame 45 and 75.
  const scale = interpolate(
    frame,
    [15, 45, 75],
    [1, 1.5, 1],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
  );

  // 3. Rotation: Full 360 rotation from frame 0 to 90.
  const rotation = interpolate(
    frame,
    [0, durationInFrames],
    [0, 360],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
  );

  return (
    <AbsoluteFill className="bg-slate-950 flex flex-col items-center justify-between py-12 font-sans text-white overflow-hidden">
      {/* Decorative grid background */}
      <div className="absolute inset-0 bg-[linear-gradient(to_right,rgba(255,255,255,0.05)_1px,transparent_1px),linear-gradient(to_bottom,rgba(255,255,255,0.05)_1px,transparent_1px)] bg-[size:40px_40px] pointer-events-none" />
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,rgba(99,102,241,0.08),transparent_80%)] pointer-events-none" />

      {/* Header */}
      <div className="z-10 text-center">
        <span className="px-3 py-1 text-xs font-semibold tracking-wider text-indigo-400 uppercase bg-indigo-950/50 border border-indigo-800/40 rounded-full">
          Stage 1: Lab Exercise 2
        </span>
        <h1 className="mt-3 text-4xl font-extrabold tracking-tight bg-gradient-to-r from-white via-indigo-200 to-indigo-400 bg-clip-text text-transparent">
          Multi-Property Transformations
        </h1>
        <p className="mt-2 text-sm text-slate-400">
          Combining Translation, Scaling, and Rotation Interpolations
        </p>
      </div>

      {/* The Animation Area */}
      <div className="relative w-full h-[300px] flex items-center justify-center border-y border-slate-900 bg-slate-950/40">
        {/* Horizontal movement track indicator */}
        <div className="absolute w-[600px] h-[2px] bg-slate-800 border-dashed border-t border-slate-700/50 flex justify-between px-2 text-[10px] text-slate-600">
          <span>Start (-300px)</span>
          <span>Center (0px)</span>
          <span>End (300px)</span>
        </div>

        {/* The Animated Box */}
        <div
          style={{
            transform: `translateX(${translateX}px) scale(${scale}) rotate(${rotation}deg)`,
          }}
          className="w-24 h-24 bg-gradient-to-br from-indigo-500 via-purple-500 to-pink-500 rounded-2xl flex items-center justify-center shadow-[0_0_40px_rgba(139,92,246,0.4)] border border-purple-400/30"
        >
          <div className="text-2xl font-black text-white select-none">3D</div>
        </div>
      </div>

      {/* Telemetry Panel */}
      <div className="z-10 w-[800px] bg-slate-900/60 border border-slate-800 rounded-2xl p-6 backdrop-blur-md shadow-xl font-mono text-xs text-slate-300 flex flex-col gap-4">
        <div className="flex justify-between border-b border-slate-800/60 pb-2 text-[10px] text-slate-500">
          <span>TRANSFORMATION COMPONENT</span>
          <span className="text-indigo-400">transform: translateX(Xpx) scale(S) rotate(Rdeg)</span>
        </div>

        <div className="grid grid-cols-4 gap-4 text-center">
          <div className="flex flex-col gap-1 border-r border-slate-800/60">
            <span className="text-slate-500 text-[10px]">FRAME</span>
            <span className="text-base font-semibold text-white">
              {frame} <span className="text-[10px] text-slate-500">/ {durationInFrames}</span>
            </span>
          </div>

          <div className="flex flex-col gap-1 border-r border-slate-800/60">
            <span className="text-slate-500 text-[10px]">TRANSLATE X</span>
            <span className="text-base font-semibold text-sky-400">
              {translateX.toFixed(1)}px
            </span>
            <div className="w-16 h-1 bg-slate-950 mx-auto rounded-full overflow-hidden mt-1">
              <div 
                className="h-full bg-sky-500" 
                style={{ width: `${((translateX + 300) / 600) * 100}%` }}
              />
            </div>
          </div>

          <div className="flex flex-col gap-1 border-r border-slate-800/60">
            <span className="text-slate-500 text-[10px]">SCALE</span>
            <span className="text-base font-semibold text-purple-400">
              {scale.toFixed(2)}x
            </span>
            <div className="w-16 h-1 bg-slate-950 mx-auto rounded-full overflow-hidden mt-1">
              <div 
                className="h-full bg-purple-500" 
                style={{ width: `${((scale - 1) / 0.5) * 100}%` }}
              />
            </div>
          </div>

          <div className="flex flex-col gap-1">
            <span className="text-slate-500 text-[10px]">ROTATION</span>
            <span className="text-base font-semibold text-pink-400">
              {rotation.toFixed(0)}°
            </span>
            <div className="w-16 h-1 bg-slate-950 mx-auto rounded-full overflow-hidden mt-1">
              <div 
                className="h-full bg-pink-500" 
                style={{ width: `${(rotation / 360) * 100}%` }}
              />
            </div>
          </div>
        </div>
      </div>
    </AbsoluteFill>
  );
};
