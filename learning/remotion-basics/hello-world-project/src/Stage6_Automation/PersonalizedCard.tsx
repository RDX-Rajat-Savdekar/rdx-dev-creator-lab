import React from "react";
import {
  AbsoluteFill,
  interpolate,
  spring,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import { z } from "zod";

// ===================================================
// ZOD SCHEMA DEFINITION FOR PERSONALIZED PARAMETERS
// ===================================================
export const personalizedCardSchema = z.object({
  userName: z.string().default("Rajat Savdekar").describe("Developer profile name"),
  contributions: z.number().min(0).max(10000).default(1850).describe("Total annual git contributions"),
  linesWritten: z.number().min(0).max(1000000).default(142000).describe("Total lines of code written"),
  favLang: z.string().default("TypeScript").describe("Primary programming language"),
  favoriteHexColor: z.string().default("#a855f7").describe("Accent highlight theme hex code"),
});

type PersonalizedProps = z.infer<typeof personalizedCardSchema>;

export const PersonalizedCard: React.FC<PersonalizedProps> = ({
  userName,
  contributions,
  linesWritten,
  favLang,
  favoriteHexColor,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // 1. Entry Animation (Spring-driven slide up and scale of the container card)
  const cardSpring = spring({
    frame: frame - 10,
    fps,
    config: { stiffness: 95, damping: 14, mass: 5 },
  });

  const cardY = interpolate(cardSpring, [0, 1], [400, 0]);
  const cardScale = interpolate(cardSpring, [0, 1], [0.8, 1]);
  const cardOpacity = interpolate(cardSpring, [0, 1], [0, 1]);

  // 2. Count-Up Animation for Contributions (frames 40 -> 90)
  const contributionsCount = Math.round(
    interpolate(frame, [40, 90], [0, contributions], {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
      easing: (t) => t * (2 - t), // smooth decelerating ease
    })
  );

  // 3. Count-Up Animation for Lines Written (frames 50 -> 100)
  const linesCount = Math.round(
    interpolate(frame, [50, 100], [0, linesWritten], {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
      easing: (t) => t * (2 - t),
    })
  );

  // 4. Slide-in staggered offsets for stats rows
  const row1Spring = spring({ frame: frame - 40, fps, config: { damping: 12 } });
  const row2Spring = spring({ frame: frame - 50, fps, config: { damping: 12 } });
  const row3Spring = spring({ frame: frame - 60, fps, config: { damping: 12 } });

  return (
    <AbsoluteFill className="bg-slate-950 flex items-center justify-center font-sans overflow-hidden text-white">
      {/* Background abstract glowing auroras */}
      <div
        style={{
          width: 500,
          height: 500,
          background: `radial-gradient(circle, ${favoriteHexColor} 0%, transparent 65%)`,
          opacity: 0.15,
          top: "10%",
          left: "20%",
          filter: "blur(60px)",
        }}
        className="absolute rounded-full pointer-events-none"
      />
      <div
        style={{
          width: 400,
          height: 400,
          background: `radial-gradient(circle, #3b82f6 0%, transparent 65%)`,
          opacity: 0.12,
          bottom: "10%",
          right: "20%",
          filter: "blur(60px)",
        }}
        className="absolute rounded-full pointer-events-none"
      />

      {/* Grid Pattern */}
      <div className="absolute inset-0 bg-[linear-gradient(to_right,rgba(255,255,255,0.01)_1px,transparent_1px),linear-gradient(to_bottom,rgba(255,255,255,0.01)_1px,transparent_1px)] bg-[size:60px_60px] pointer-events-none" />

      {/* Main Stats Card Container */}
      <div
        style={{
          transform: `translateY(${cardY}px) scale(${cardScale})`,
          opacity: cardOpacity,
          border: `1px solid rgba(255, 255, 255, 0.08)`,
          background: "linear-gradient(135deg, rgba(15, 23, 42, 0.6) 0%, rgba(30, 41, 59, 0.4) 100%)",
          boxShadow: `0 25px 50px -12px rgba(0,0,0,0.5), 0 0 40px ${favoriteHexColor}1a`,
        }}
        className="w-[700px] h-[480px] rounded-3xl p-10 flex flex-col justify-between backdrop-blur-xl relative overflow-hidden"
      >
        {/* Top Header Row */}
        <div className="flex justify-between items-center border-b border-white/5 pb-5">
          <div>
            <span
              style={{ color: favoriteHexColor }}
              className="text-[10px] font-black uppercase tracking-[0.25em]"
            >
              2026 Developer Wrapped
            </span>
            <h2 className="text-2xl font-black tracking-tight mt-1 text-slate-100">
              {userName}
            </h2>
          </div>
          {/* Avatar circle containing name initial */}
          <div
            style={{
              background: `linear-gradient(135deg, ${favoriteHexColor}33, ${favoriteHexColor}66)`,
              border: `1px solid ${favoriteHexColor}aa`,
            }}
            className="w-14 h-14 rounded-full flex items-center justify-center font-black text-lg"
          >
            {userName ? userName.charAt(0).toUpperCase() : "?"}
          </div>
        </div>

        {/* Stats Content Rows */}
        <div className="flex flex-col gap-6 my-4">

          {/* Stat Row 1: Contributions */}
          <div
            style={{
              opacity: row1Spring,
              transform: `translateX(${interpolate(row1Spring, [0, 1], [-30, 0])}px)`
            }}
            className="flex justify-between items-center bg-white/2 p-4 rounded-xl border border-white/5"
          >
            <span className="text-xs text-slate-400 font-bold uppercase tracking-wider">Git Contributions</span>
            <span
              style={{ color: favoriteHexColor }}
              className="text-2xl font-black"
            >
              {contributionsCount}
            </span>
          </div>

          {/* Stat Row 2: Lines of Code */}
          <div
            style={{
              opacity: row2Spring,
              transform: `translateX(${interpolate(row2Spring, [0, 1], [-30, 0])}px)`
            }}
            className="flex justify-between items-center bg-white/2 p-4 rounded-xl border border-white/5"
          >
            <span className="text-xs text-slate-400 font-bold uppercase tracking-wider">Lines Written</span>
            <span className="text-2xl font-black text-slate-100">
              {linesCount.toLocaleString()}
            </span>
          </div>

          {/* Stat Row 3: Favorite Language */}
          <div
            style={{
              opacity: row3Spring,
              transform: `translateX(${interpolate(row3Spring, [0, 1], [-30, 0])}px)`
            }}
            className="flex justify-between items-center bg-white/2 p-4 rounded-xl border border-white/5"
          >
            <span className="text-xs text-slate-400 font-bold uppercase tracking-wider">Favorite Weapon</span>
            <div className="flex items-center gap-2">
              <span className="px-2.5 py-1 text-[10px] font-black tracking-wider uppercase bg-white/10 rounded-full text-slate-200">
                CORE
              </span>
              <span
                style={{ color: favoriteHexColor }}
                className="text-2xl font-black"
              >
                {favLang}
              </span>
            </div>
          </div>

        </div>

        {/* Footer details */}
        <div className="flex justify-between items-center border-t border-white/5 pt-4 text-[9px] text-slate-500 font-mono tracking-widest uppercase">
          <span>AUTOMATION MATRIX</span>
          <span>COMP-ID: DWRAP-2026</span>
        </div>
      </div>
    </AbsoluteFill>
  );
};
