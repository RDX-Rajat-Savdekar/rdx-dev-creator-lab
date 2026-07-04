import React from "react";
import {
  AbsoluteFill,
  interpolate,
  spring,
  useCurrentFrame,
  useVideoConfig,
  Easing,
} from "remotion";
import { z } from "zod";
import { zColor } from "@remotion/zod-types";

// ===================================================
// ZOD SCHEMA DEFINITION FOR UNITY-STYLE PROPERTIES
// ===================================================
export const sharinganSchema = z.object({
  eyeballGlowColor: zColor().default("rgba(239, 68, 68, 0.45)").describe("Color of the outer glow around the eye"),
  irisScaleFactor: z.number().min(0.4).max(1.3).step(0.05).default(0.8).describe("Base scaling factor of the red iris"),
  pupilRadius: z.number().min(8).max(30).step(1).default(14).describe("Radius of the black center pupil circle"),
  rotations: z.number().min(1).max(6).step(1).default(4).describe("Number of full spins during activation"),
  veinsOpacity: z.number().min(0).max(1).step(0.05).default(0.35).describe("Opacity of the bloodshot corner veins"),
  enableJitter: z.boolean().default(true).describe("Enables rapid eye twitch scanning tremors"),
});

// Infer props type from Zod schema
type SharinganProps = z.infer<typeof sharinganSchema>;

// ===================================================
// SHARINGAN BLADE COMPONENT (TOMOE)
// ===================================================
const SharinganBlade: React.FC<{
  delay: number;
  rotation: number;
}> = ({ delay, rotation }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const tomoeDrawLength = 450;
  const drawSpring = spring({
    frame: frame - delay,
    fps,
    config: {
      stiffness: 80,
      damping: 16,
      mass: 0.9,
    },
  });

  const strokeDashoffset = interpolate(drawSpring, [0, 1], [tomoeDrawLength, 0]);
  const fillOpacity = interpolate(drawSpring, [0.7, 1.0], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const scale = interpolate(drawSpring, [0, 1], [0.8, 1.0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  if (frame < delay) {
    return null;
  }

  return (
    <path
      style={{
        fill: "#000",
        fillOpacity,
        stroke: "#000",
        strokeWidth: 4,
        strokeDasharray: tomoeDrawLength,
        strokeDashoffset,
        transformOrigin: "150px 150px",
        transform: `rotate(${rotation}deg) scale(${scale})`,
      }}
      d="M 177.6,10.7 C 135,68.4 155.4,100.7 179.8,118.5 C 190,140 170,150 150,150 C 130,150 110,140 107.9,128.3 C 109.5,97.6 111.5,16.6 177.6,10.7 z"
    />
  );
};

// ===================================================
// SACCADE (RAPID EYE MOVEMENT) COORDINATE LOOKUPS
// ===================================================
const SACCADE_POINTS = [
  { frame: 110, x: 0, y: 0 },
  { frame: 114, x: -35, y: -20 },
  { frame: 118, x: 30, y: 30 },
  { frame: 122, x: -15, y: 40 },
  { frame: 126, x: 40, y: -10 },
  { frame: 130, x: -40, y: -30 },
  { frame: 134, x: 0, y: 35 },
  { frame: 138, x: 35, y: 15 },
  { frame: 142, x: -40, y: -10 },
  { frame: 146, x: 20, y: -35 },
  { frame: 150, x: -10, y: 25 },
  { frame: 154, x: 30, y: 10 },
  { frame: 158, x: -25, y: -20 },
  { frame: 162, x: 15, y: 35 },
  { frame: 166, x: -35, y: 5 },
  { frame: 170, x: 0, y: 0 },
];

export const SharinganIntro: React.FC<SharinganProps> = ({
  eyeballGlowColor,
  irisScaleFactor,
  pupilRadius,
  rotations,
  veinsOpacity,
  enableJitter,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // ===================================================
  // 1. SACCADIC DARTING & JITTER MATH
  // ===================================================
  let dx = 0;
  let dy = 0;

  if (frame >= 110 && frame <= 170) {
    // Find active saccade interval
    for (let i = 0; i < SACCADE_POINTS.length - 1; i++) {
      const p1 = SACCADE_POINTS[i];
      const p2 = SACCADE_POINTS[i + 1];
      if (frame >= p1.frame && frame <= p2.frame) {
        // Interpolate linearly between looking target offsets
        dx = interpolate(frame, [p1.frame, p2.frame], [p1.x, p2.x], {
          extrapolateLeft: "clamp",
          extrapolateRight: "clamp",
        });
        dy = interpolate(frame, [p1.frame, p2.frame], [p1.y, p2.y], {
          extrapolateLeft: "clamp",
          extrapolateRight: "clamp",
        });
        break;
      }
    }

    // Add high-frequency organic micro-jitter (tremors) if enabled
    if (enableJitter) {
      const jitterFreq = 2.4;
      const jitterAmp = 4;
      dx += Math.sin(frame * jitterFreq) * jitterAmp;
      dy += Math.cos(frame * jitterFreq * 1.3) * jitterAmp;
    }
  }

  // ===================================================
  // 2. SHARINGAN ASSEMBLY & ACTIVATION TIMING
  // ===================================================
  
  // Iris scale-up
  const irisSpring = spring({
    frame: frame - 15,
    fps,
    config: { stiffness: 140, damping: 14, mass: 0.9 },
  });
  const irisScale = irisSpring;

  // Activation spin: goes from slow -> fast -> slow
  const spinAngle = interpolate(
    frame,
    [90, 160],
    [0, rotations * 360], // Dynamic spins based on UI props
    {
      easing: Easing.bezier(0.76, 0, 0.24, 1),
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
    }
  );

  // Scale pulse on activation
  const activationSpring = spring({
    frame: frame - 90,
    fps,
    config: { stiffness: 90, damping: 15, mass: 1.1 },
  });
  const activationScale = interpolate(activationSpring, [0, 0.5, 1], [1.0, 1.25, 1.1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  // Red glow flash overlay
  const flashOpacity = interpolate(
    frame,
    [88, 93, 110],
    [0, 0.6, 0],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
  );

  return (
    <AbsoluteFill className="bg-slate-950 flex flex-col items-center justify-between py-6 font-sans text-white overflow-hidden">
      {/* Background radial highlight */}
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,rgba(239,68,68,0.02),transparent_70%)] pointer-events-none" />

      {/* Screen red flash layer */}
      <div 
        style={{ opacity: flashOpacity }}
        className="absolute inset-0 bg-red-700 mix-blend-screen pointer-events-none z-50"
      />

      {/* Header */}
      <div className="z-10 text-center">
        <span className="px-3 py-1 text-xs font-semibold tracking-wider text-red-500 uppercase bg-red-950/50 border border-red-800/40 rounded-full">
          Stage 3: Cinematic Feature (Parametrized)
        </span>
        <h1 className="mt-2 text-4xl font-extrabold tracking-tight bg-gradient-to-r from-white via-red-200 to-red-400 bg-clip-text text-transparent">
          Mangekyou Sharingan Activation
        </h1>
        <p className="mt-1 text-xs text-slate-400">
          Clipped eye socket containing high-speed organic scanning movements
        </p>
      </div>

      {/* The Eye Stage */}
      <div className="relative flex items-center justify-center w-full h-[400px]">
        
        {/* Ambient Eye Shadow Glow */}
        {irisSpring > 0.05 && (
          <div 
            style={{
              width: 330 * activationScale,
              height: 330 * activationScale,
              opacity: irisSpring * 0.4,
              boxShadow: `0 0 80px ${eyeballGlowColor}`, // Dynamic glow color
            }}
            className="absolute rounded-full bg-red-950/20 blur-xl pointer-events-none"
          />
        )}

        {/* Eyeball Canvas */}
        <svg
          width="500"
          height="400"
          viewBox="0 0 500 400"
          className="overflow-visible"
        >
          <defs>
            {/* Eye socket clipping path */}
            <clipPath id="eye-clip">
              <path d="M 20,200 Q 250,30 480,200 Q 250,370 20,200 Z" />
            </clipPath>

            {/* Sclera light gradient (white of the eye with corner shading) */}
            <radialGradient id="sclera-grad" cx="50%" cy="50%" r="50%">
              <stop offset="60%" style={{ stopColor: "#f8fafc", stopOpacity: 1 }} />
              <stop offset="90%" style={{ stopColor: "#e2e8f0", stopOpacity: 1 }} />
              <stop offset="100%" style={{ stopColor: "#94a3b8", stopOpacity: 1 }} />
            </radialGradient>

            {/* Iris red radial gradient */}
            <radialGradient id="iris-grad" cx="50%" cy="50%" r="50%">
              <stop offset="0%" style={{ stopColor: "#660000", stopOpacity: 1 }} />
              <stop offset="65%" style={{ stopColor: "#c30000", stopOpacity: 1 }} />
              <stop offset="100%" style={{ stopColor: "#800000", stopOpacity: 1 }} />
            </radialGradient>
          </defs>

          {/* ===================================================
              CLIPPED EYEBALL INTERNAL CONTENT
              =================================================== */}
          <g clipPath="url(#eye-clip)">
            {/* Sclera background */}
            <path
              d="M 20,200 Q 250,30 480,200 Q 250,370 20,200 Z"
              fill="url(#sclera-grad)"
            />

            {/* Bloodshot eye veins in corners */}
            {irisSpring > 0.1 && (
              <g opacity={veinsOpacity}> {/* Dynamic veins opacity */}
                {/* Left corner veins */}
                <path d="M 25,200 Q 120,170 160,205" stroke="#ef4444" strokeWidth="2" fill="none" />
                <path d="M 25,200 Q 100,225 130,202" stroke="#ef4444" strokeWidth="1.5" fill="none" />
                <path d="M 90,191 Q 120,170 110,195" stroke="#ef4444" strokeWidth="1" fill="none" />

                {/* Right corner veins */}
                <path d="M 475,200 Q 380,170 340,205" stroke="#ef4444" strokeWidth="2" fill="none" />
                <path d="M 475,200 Q 400,225 370,202" stroke="#ef4444" strokeWidth="1.5" fill="none" />
                <path d="M 410,191 Q 380,170 390,195" stroke="#ef4444" strokeWidth="1" fill="none" />
              </g>
            )}

            {/* ===================================================
                THE SHARINGAN IRIS (Clipped, moves around dynamically)
                =================================================== */}
            <g
              transform={`translate(${100 + dx}, ${50 + dy}) scale(${irisScale * activationScale * irisScaleFactor})`}
              style={{
                transformOrigin: "150px 150px",
                opacity: irisSpring,
              }}
            >
              {/* Red Iris Base */}
              <circle
                style={{
                  fill: "url(#iris-grad)",
                  stroke: "#000",
                  strokeWidth: 9,
                }}
                cx="150"
                cy="150"
                r="138"
              />

              {/* Inner black boundary ring */}
              <circle
                style={{
                  fill: "none",
                  stroke: "#000",
                  strokeWidth: 2.5,
                  opacity: 0.65,
                }}
                cx="150"
                cy="150"
                r="88"
              />

              {/* Three Tomoe blades rotating around center */}
              <g style={{ transformOrigin: "150px 150px", transform: `rotate(${spinAngle}deg)` }}>
                <SharinganBlade delay={40} rotation={0} />
                <SharinganBlade delay={55} rotation={120} />
                <SharinganBlade delay={70} rotation={240} />
              </g>

              {/* Center Pupil */}
              <circle cx="150" cy="150" r={pupilRadius} fill="#000" /> {/* Dynamic pupil size */}
            </g>
          </g>

          {/* ===================================================
              EYELIDS & OUTLINES OVERLAY (Outside clip area)
              =================================================== */}
          {/* Upper eyelid contour with shadow effect */}
          <path
            d="M 20,200 Q 250,30 480,200"
            stroke="#020617"
            strokeWidth="10"
            strokeLinecap="round"
            fill="none"
          />
          {/* Lower eyelid outline */}
          <path
            d="M 20,200 Q 250,370 480,200"
            stroke="#0f172a"
            strokeWidth="7"
            strokeLinecap="round"
            fill="none"
          />
        </svg>

      </div>

      {/* Telemetry panel */}
      <div className="z-10 w-[800px] bg-slate-900/60 border border-slate-800 rounded-2xl p-5 backdrop-blur-md shadow-xl font-mono text-xs text-slate-300 flex flex-col gap-3">
        <div className="flex justify-between border-b border-slate-800/60 pb-2 text-[10px] text-slate-500">
          <span>AMATERASU DARTING MATRIX</span>
          <span>Frame: {frame}</span>
        </div>
        <div className="grid grid-cols-4 gap-4 text-center text-[10px]">
          <div className="flex flex-col gap-1 border-r border-slate-800/60">
            <span className="text-slate-500">SACCADE OFFSET X</span>
            <span className={frame >= 110 && frame <= 170 ? "text-red-400 font-bold" : "text-slate-600"}>
              {dx.toFixed(1)}px
            </span>
          </div>
          <div className="flex flex-col gap-1 border-r border-slate-800/60">
            <span className="text-slate-500">SACCADE OFFSET Y</span>
            <span className={frame >= 110 && frame <= 170 ? "text-red-400 font-bold" : "text-slate-600"}>
              {dy.toFixed(1)}px
            </span>
          </div>
          <div className="flex flex-col gap-1 border-r border-slate-800/60">
            <span className="text-slate-500">ROTOR ROTATION</span>
            <span className="text-red-400 font-bold">{spinAngle.toFixed(0)}°</span>
          </div>
          <div className="flex flex-col gap-1">
            <span className="text-slate-500">SACCADIC BEHAVIOR</span>
            <span className={frame >= 110 && frame <= 170 ? "text-yellow-400 font-bold" : "text-slate-600"}>
              {frame >= 110 && frame <= 170 ? "DARTING / JITTER" : "STABLE LOCK"}
            </span>
          </div>
        </div>
      </div>
    </AbsoluteFill>
  );
};
