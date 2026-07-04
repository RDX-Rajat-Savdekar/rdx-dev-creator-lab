import React from "react";
import {
  AbsoluteFill,
  interpolate,
  spring,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";

export const BounceIn: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // ==========================================
  // SPRING CONFIGURATION 1: STIFF & BOUNCY
  // ==========================================
  // Stiffness is high (180), so the pull is strong.
  // Damping is low (12), so there is little resistance, causing oscillation.
  const bouncySpring = spring({
    frame: frame - 10, // Start animation at frame 10
    fps,
    config: {
      stiffness: 180,
      damping: 12,
      mass: 5,
    },
  });

  // ==========================================
  // SPRING CONFIGURATION 2: SMOOTH & DAMPED
  // ==========================================
  // Stiffness is moderate (100).
  // Damping is high (26) relative to stiffness, creating a smooth "criticially damped" settle without overshoot.
  const smoothSpring = spring({
    frame: frame - 20, // Start animation at frame 20
    fps,
    config: {
      stiffness: 100,
      damping: 26,
      mass: 10,
    },
  });

  // Map the 0-1 spring progress to CSS properties:
  // - Scale: start at 0 (invisible), spring up to 1 (full size)
  // - Translate Y: pop up from 100px below to original position (0px)
  const bouncyScale = bouncySpring; //可以直接用 spring value 作为 scale
  const bouncyTranslateY = interpolate(bouncySpring, [0, 1], [150, 0]);

  const smoothScale = smoothSpring;
  const smoothTranslateY = interpolate(smoothSpring, [0, 1], [150, 0]);

  return (
    <AbsoluteFill className="bg-slate-950 flex flex-col items-center justify-between py-12 font-sans text-white overflow-hidden">
      {/* Background decoration */}
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,rgba(99,102,241,0.06),transparent_75%)] pointer-events-none" />

      {/* Header */}
      <div className="z-10 text-center">
        <span className="px-3 py-1 text-xs font-semibold tracking-wider text-indigo-400 uppercase bg-indigo-950/50 border border-indigo-800/40 rounded-full">
          Stage 2: Lab Exercise 1
        </span>
        <h1 className="mt-3 text-4xl font-extrabold tracking-tight bg-gradient-to-r from-white via-indigo-200 to-indigo-400 bg-clip-text text-transparent">
          Spring-Based Physics Motion
        </h1>
        <p className="mt-2 text-sm text-slate-400">
          Comparing different stiffness and damping configurations side-by-side
        </p>
      </div>

      {/* Cards Area */}
      <div className="z-10 flex gap-12 w-[900px] justify-center items-center h-[350px]">
        {/* Card 1: Bouncy Spring */}
        <div
          style={{
            transform: `translateY(${bouncyTranslateY}px) scale(${bouncyScale})`,
            opacity: bouncySpring,
          }}
          className="w-80 bg-slate-900/80 border border-pink-500/30 rounded-2xl p-6 shadow-[0_10px_30px_rgba(244,63,94,0.15)] backdrop-blur-md flex flex-col gap-4"
        >
          <div className="flex justify-between items-center">
            <span className="text-xs font-bold text-pink-400 tracking-wider uppercase">Config A: Bouncy</span>
            <span className="text-[10px] text-slate-500 font-mono">Start: f10</span>
          </div>
          <div className="w-12 h-12 rounded-xl bg-pink-500/10 border border-pink-400/20 flex items-center justify-center text-2xl">
            🍒
          </div>
          <div>
            <h3 className="font-bold text-lg text-white">Stiff & Osculating</h3>
            <p className="text-xs text-slate-400 mt-1 leading-relaxed">
              Low friction relative to tension makes the box overshoot the mark and spring back repeatedly.
            </p>
          </div>
          <div className="border-t border-slate-800/60 pt-3 font-mono text-[10px] text-slate-400 flex flex-col gap-1">
            <div className="flex justify-between"><span>stiffness</span><span className="text-pink-400">180</span></div>
            <div className="flex justify-between"><span>damping</span><span className="text-pink-400">12</span></div>
            <div className="flex justify-between"><span>mass</span><span className="text-pink-400">0.8</span></div>
          </div>
        </div>

        {/* Card 2: Smooth Spring */}
        <div
          style={{
            transform: `translateY(${smoothTranslateY}px) scale(${smoothScale})`,
            opacity: smoothSpring,
          }}
          className="w-80 bg-slate-900/80 border border-emerald-500/30 rounded-2xl p-6 shadow-[0_10px_30px_rgba(16,185,129,0.15)] backdrop-blur-md flex flex-col gap-4"
        >
          <div className="flex justify-between items-center">
            <span className="text-xs font-bold text-emerald-400 tracking-wider uppercase">Config B: Damped</span>
            <span className="text-[10px] text-slate-500 font-mono">Start: f20</span>
          </div>
          <div className="w-12 h-12 rounded-xl bg-emerald-500/10 border border-emerald-400/20 flex items-center justify-center text-2xl">
            🟢
          </div>
          <div>
            <h3 className="font-bold text-lg text-white">Smooth & Settled</h3>
            <p className="text-xs text-slate-400 mt-1 leading-relaxed">
              Higher friction absorbs kinetic energy rapidly, causing the card to slide into place with zero overshoot.
            </p>
          </div>
          <div className="border-t border-slate-800/60 pt-3 font-mono text-[10px] text-slate-400 flex flex-col gap-1">
            <div className="flex justify-between"><span>stiffness</span><span className="text-emerald-400">100</span></div>
            <div className="flex justify-between"><span>damping</span><span className="text-emerald-400">26</span></div>
            <div className="flex justify-between"><span>mass</span><span className="text-emerald-400">1.2</span></div>
          </div>
        </div>
      </div>

      {/* Telemetry Footer */}
      <div className="z-10 w-[800px] bg-slate-900/60 border border-slate-800 rounded-2xl p-5 backdrop-blur-md shadow-xl font-mono text-xs text-slate-300 flex flex-col gap-3">
        <div className="flex justify-between border-b border-slate-800/60 pb-2 text-[10px] text-slate-500">
          <span>SPRING SIMULATION DATA</span>
          <span>Frame: {frame}</span>
        </div>
        <div className="grid grid-cols-2 gap-6">
          <div className="flex flex-col gap-1.5">
            <div className="flex justify-between">
              <span className="text-slate-500 text-[10px]">A: BOUNCY VALUE</span>
              <span className="text-pink-400 font-bold">{bouncySpring.toFixed(3)}</span>
            </div>
            <div className="h-2 bg-slate-950 rounded-full overflow-hidden border border-slate-800 relative">
              <div
                className="h-full bg-pink-500"
                style={{ width: `${Math.min(Math.max(bouncySpring * 100, 0), 100)}%` }}
              />
            </div>
          </div>
          <div className="flex flex-col gap-1.5">
            <div className="flex justify-between">
              <span className="text-slate-500 text-[10px]">B: DAMPED VALUE</span>
              <span className="text-emerald-400 font-bold">{smoothSpring.toFixed(3)}</span>
            </div>
            <div className="h-2 bg-slate-950 rounded-full overflow-hidden border border-slate-800 relative">
              <div
                className="h-full bg-emerald-500"
                style={{ width: `${Math.min(Math.max(smoothSpring * 100, 0), 100)}%` }}
              />
            </div>
          </div>
        </div>
      </div>
    </AbsoluteFill>
  );
};
