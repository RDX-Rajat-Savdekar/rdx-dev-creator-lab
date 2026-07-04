import React from "react";
import {
  AbsoluteFill,
  interpolate,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";

export const FadeInOut: React.FC = () => {
  const frame = useCurrentFrame();
  const { durationInFrames } = useVideoConfig();

  // Interpolate opacity: 
  // 0 to 20 frames: fade in (0 -> 1)
  // 20 to 70 frames: solid (1)
  // 70 to 90 frames: fade out (1 -> 0)
  const opacity = interpolate(
    frame,
    [0, 20, durationInFrames - 20, durationInFrames],
    [0, 1, 1, 0],
    {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
    }
  );

  return (
    <AbsoluteFill className="bg-slate-950 flex flex-col items-center justify-center font-sans text-white">
      {/* Background radial glow */}
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,rgba(56,189,248,0.1),transparent_70%)] pointer-events-none" />

      {/* Main Container */}
      <div className="z-10 w-[700px] flex flex-col items-center gap-8">

        {/* Lab Header */}
        <div className="text-center">
          <span className="px-3 py-1 text-xs font-semibold tracking-wider text-sky-400 uppercase bg-sky-950/50 border border-sky-800/40 rounded-full">
            Stage 1: Lab Exercise 1
          </span>
          <h1 className="mt-3 text-4xl font-extrabold tracking-tight bg-gradient-to-r from-white via-slate-200 to-slate-400 bg-clip-text text-transparent">
            Fade In / Out Interpolation
          </h1>
          <p className="mt-2 text-sm text-slate-400">
            Mapping frames to CSS opacity using <code>interpolate()</code>
          </p>
        </div>

        {/* The Animated Target Element */}
        <div
          style={{ opacity }}
          className="w-80 h-48 bg-gradient-to-br from-sky-500 to-indigo-600 rounded-2xl flex flex-col items-center justify-center shadow-[0_0_50px_rgba(56,189,248,0.3)] border border-sky-400/20"
        >
          <div className="text-4xl">😁 - 😠</div>
          <span className="mt-2 text-lg font-bold tracking-wide">Target Element</span>
          <span className="text-xs text-sky-200 font-mono mt-1">opacity: {opacity.toFixed(2)}</span>
        </div>

        {/* Telemetry Panel */}
        <div className="w-full bg-slate-900/60 border border-slate-800 rounded-2xl p-6 backdrop-blur-md shadow-xl font-mono text-xs text-slate-300 flex flex-col gap-4">
          <div className="flex justify-between border-b border-slate-800/60 pb-2">
            <span className="text-slate-500">CONCEPT</span>
            <span className="text-sky-400 font-semibold">interpolate(frame, [0, 20, 70, 90], [0, 1, 1, 0])</span>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div className="flex flex-col gap-1">
              <span className="text-slate-500">CURRENT FRAME</span>
              <span className="text-lg font-semibold text-white">
                {frame} <span className="text-xs text-slate-500">/ {durationInFrames}</span>
              </span>
            </div>
            <div className="flex flex-col gap-1">
              <span className="text-slate-500">COMPUTED OPACITY</span>
              <span className="text-lg font-semibold text-emerald-400">
                {opacity.toFixed(3)}
              </span>
            </div>
          </div>

          {/* Timeline indicator bar */}
          <div className="w-full flex flex-col gap-1.5 mt-2">
            <div className="flex justify-between text-[10px] text-slate-500">
              <span>Frame 0</span>
              <span>Frame 20 (Full)</span>
              <span>Frame 70 (Fade Start)</span>
              <span>Frame 90</span>
            </div>
            <div className="h-2 w-full bg-slate-950 rounded-full overflow-hidden border border-slate-800 relative">
              {/* Playhead */}
              <div
                className="absolute top-0 bottom-0 w-0.5 bg-sky-400 shadow-[0_0_8px_#38bdf8] z-10"
                style={{ left: `${(frame / durationInFrames) * 100}%` }}
              />
              {/* Opacity level color overlay */}
              <div
                className="h-full bg-gradient-to-r from-sky-500/10 via-sky-500/60 to-sky-500/10"
                style={{ width: `${opacity * 100}%`, opacity }}
              />
            </div>
          </div>
        </div>

      </div>
    </AbsoluteFill>
  );
};
