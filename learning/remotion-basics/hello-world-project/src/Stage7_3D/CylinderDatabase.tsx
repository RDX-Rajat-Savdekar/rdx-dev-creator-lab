import React from "react";
import {
  AbsoluteFill,
  interpolate,
  spring,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import { z } from "zod";
import { zColor } from "@remotion/zod-types";

// ===================================================
// ZOD SCHEMA DEFINITION FOR CSS 3D PROPERTIES
// ===================================================
export const cylinderDatabaseSchema = z.object({
  cylinderGlowColor: zColor().default("#6366f1").describe("Glow and border color of the database panels"),
  rotationSpeed: z.number().min(0.2).max(4).step(0.1).default(1.2).describe("Speed factor of the cylinder spin"),
  panelOpacity: z.number().min(0.1).max(0.9).step(0.05).default(0.4).describe("Opacity of the glassmorphic panels"),
  stackLevels: z.number().min(1).max(4).step(1).default(3).describe("Number of vertical database disk layers"),
});

type CylinderProps = z.infer<typeof cylinderDatabaseSchema>;

// Panel count configuration (12 panels form a complete cylinder)
const PANELS = Array.from({ length: 12 }, (_, i) => i);
const DEG_STEP = 360 / PANELS.length; // 30 degrees
const RADIUS = 150; // translateZ radius in pixels to align 80px panels

export const CylinderDatabase: React.FC<CylinderProps> = ({
  cylinderGlowColor,
  rotationSpeed,
  panelOpacity,
  stackLevels,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // 1. Initial entry scale-up spring
  const entrySpring = spring({
    frame,
    fps,
    config: { stiffness: 70, damping: 14 },
  });

  const baseScale = interpolate(entrySpring, [0, 1], [0.6, 1]);
  const baseOpacity = interpolate(entrySpring, [0, 1], [0, 1]);

  // 2. Camera perspective tilts
  // Slowly swing the camera angle back and forth to show off 3D depth
  const cameraTiltX = interpolate(
    Math.sin(frame * 0.2), // try changing this to 0.2
    [-1, 1],
    [-22, -12] // Tilt angle in degrees
  );

  // 3. Scan Ring Y-coordinate: travels up and down the stack tower
  const scanRingY = interpolate(
    Math.sin(frame * 0.05),
    [-1, 1],
    [-160, 160] // Moves between Y=-160px and Y=160px
  );

  return (
    <AbsoluteFill className="bg-slate-950 flex flex-col items-center justify-between py-8 font-mono text-white overflow-hidden">

      {/* Background stars / dust highlight */}
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,rgba(99,102,241,0.04),transparent_60%)] pointer-events-none" />

      {/* Header */}
      <div className="z-10 text-center">
        <span className="px-3 py-1 text-xs font-semibold tracking-wider text-indigo-400 uppercase bg-indigo-950/50 border border-indigo-800/40 rounded-full">
          Stage 7: CSS 3D Transforms
        </span>
        <h1 className="mt-2 text-4xl font-extrabold tracking-tight bg-gradient-to-r from-white via-indigo-200 to-indigo-400 bg-clip-text text-transparent">
          3D Database Cluster Stack
        </h1>
        <p className="mt-1 text-xs text-slate-400">
          True hardware-accelerated CSS 3D cylinder assembly and perspective camera sweeps
        </p>
      </div>

      {/* 3D Scene Viewport (Camera Rig) */}
      <div
        style={{
          perspective: "1000px", // Standard distance to viewer
          perspectiveOrigin: "50% 40%",
          width: "100%",
          height: "550px",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
        }}
        className="relative overflow-visible"
      >
        {/* World Space Container (moves with camera tilts and spins) */}
        <div
          style={{
            transformStyle: "preserve-3d",
            transform: `rotateY(${cameraTiltX}deg) scale(${baseScale})`,
            opacity: baseOpacity,
          }}
          className="relative w-0 h-0 overflow-visible flex items-center justify-center"
        >

          {/* ===================================================
              GLOWING HORIZONTAL SCANNING RINGS
              =================================================== */}
          <div
            style={{
              width: 380,
              height: 380,
              border: `2px solid ${cylinderGlowColor}`,
              borderRadius: "50%",
              transformStyle: "preserve-3d",
              transform: `translate3d(0px, ${scanRingY}px, 0px) rotateX(90deg)`,
              boxShadow: `0 0 35px ${cylinderGlowColor}, inset 0 0 35px ${cylinderGlowColor}`,
              opacity: 0.8,
            }}
            className="absolute z-10 pointer-events-none"
          />

          {/* ===================================================
              CYLINDER SERVER STACKS
              =================================================== */}
          {Array.from({ length: stackLevels }).map((_, levelIdx) => {
            // Y-offset coordinate for each stacked cylinder block
            // Calculates height offsets based on stack level (e.g. 3 levels stacked)
            const yOffset = (levelIdx - (stackLevels - 1) / 2) * 130;

            // Spin angle: Alternate spin direction for adjacent stack layers
            const isEven = levelIdx % 2 === 0;
            const directionMultiplier = isEven ? 1 : -1;
            const spinAngle = frame * rotationSpeed * directionMultiplier;

            return (
              <g
                key={levelIdx}
                style={{
                  transformStyle: "preserve-3d",
                  transform: `translate3d(0px, ${yOffset}px, 0px) rotateY(${spinAngle}deg)`,
                  position: "absolute",
                }}
              >
                {/* Center Core Column Glow */}
                <div
                  style={{
                    width: 30,
                    height: 100,
                    background: `linear-gradient(to bottom, transparent, ${cylinderGlowColor}, transparent)`,
                    filter: "blur(8px)",
                    transform: "translate3d(-15px, -50px, 0px)",
                    opacity: 0.9,
                  }}
                  className="absolute"
                />

                {/* 12 Outer panels forming the cylinder ring */}
                {PANELS.map((p) => {
                  const panelAngle = p * DEG_STEP;

                  return (
                    <div
                      key={p}
                      style={{
                        position: "absolute",
                        width: 80,
                        height: 95,
                        left: -40,
                        top: -47.5,
                        // Assemble the cylinder mesh panel by panel
                        transform: `rotateY(${panelAngle}deg) translateZ(${RADIUS}px)`,
                        transformStyle: "preserve-3d",
                        background: "linear-gradient(135deg, rgba(30, 41, 59, 0.7) 0%, rgba(15, 23, 42, 0.9) 100%)",
                        border: `1.5px solid ${cylinderGlowColor}33`,
                        borderRadius: "8px",
                        boxShadow: `inset 0 0 10px rgba(255,255,255,0.03), 0 0 15px ${cylinderGlowColor}15`,
                        opacity: panelOpacity,
                        display: "flex",
                        flexDirection: "column",
                        alignItems: "center",
                        justifyContent: "space-between",
                        padding: "8px",
                        backfaceVisibility: "hidden", // Hide back of panels for clarity
                      }}
                      className="backdrop-blur-sm"
                    >
                      {/* Mini indicator LEDs inside each panel */}
                      <div className="w-full flex justify-between">
                        <div className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse" />
                        <div
                          style={{
                            backgroundColor: (frame + p * 4) % 15 < 6 ? cylinderGlowColor : "#475569"
                          }}
                          className="w-1.5 h-1.5 rounded-full"
                        />
                      </div>

                      {/* Stylized server chassis slot mark */}
                      <div className="w-[85%] h-5 border border-slate-800 rounded flex flex-col justify-center gap-0.5 px-1 bg-slate-950/60 opacity-60">
                        <div className="w-[90%] h-0.5 bg-slate-800" />
                        <div className="w-[70%] h-0.5 bg-slate-800" />
                      </div>

                      {/* Small metadata text */}
                      <span className="text-[7px] text-slate-500 font-mono tracking-tighter">
                        NODE-{levelIdx}-{p}
                      </span>
                    </div>
                  );
                })}
              </g>
            );
          })}

        </div>
      </div>

      {/* Telemetry panel */}
      <div className="z-10 w-[800px] bg-slate-900/60 border border-slate-800 rounded-2xl p-5 backdrop-blur-md shadow-xl font-mono text-[10px] text-slate-300 flex flex-col gap-3">
        <div className="flex justify-between border-b border-slate-800/60 pb-2 text-slate-500">
          <span>CSS 3D MATRIX ENGINE</span>
          <span>FPS: 30</span>
        </div>
        <div className="grid grid-cols-4 gap-4 text-center">
          <div className="flex flex-col gap-1 border-r border-slate-800/60">
            <span className="text-slate-500">CAMERA TILT X</span>
            <span className="text-indigo-400 font-bold">{cameraTiltX.toFixed(1)}°</span>
          </div>
          <div className="flex flex-col gap-1 border-r border-slate-800/60">
            <span className="text-slate-500">LASER SWEEP Y</span>
            <span className="text-indigo-400 font-bold">{scanRingY.toFixed(0)}px</span>
          </div>
          <div className="flex flex-col gap-1 border-r border-slate-800/60">
            <span className="text-slate-500">RADIUS CONST</span>
            <span className="text-indigo-400 font-bold">{RADIUS}px</span>
          </div>
          <div className="flex flex-col gap-1">
            <span className="text-slate-500">TOTAL NODES</span>
            <span className="text-indigo-400 font-bold">{stackLevels * 12}</span>
          </div>
        </div>
      </div>
    </AbsoluteFill>
  );
};
