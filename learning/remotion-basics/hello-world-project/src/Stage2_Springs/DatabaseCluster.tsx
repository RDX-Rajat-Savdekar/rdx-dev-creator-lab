import React from "react";
import {
  AbsoluteFill,
  interpolate,
  spring,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";

// ==========================================
// TYPES & CONSTANTS
// ==========================================
interface ReplicaConfig {
  id: string;
  name: string;
  ip: string;
  targetX: number; // Target offset X from center
  targetY: number; // Target offset Y from center
  icon: string;
}

const REPLICAS: ReplicaConfig[] = [
  { id: "rep-1", name: "Replica North", ip: "10.0.1.10", targetX: 0, targetY: -220, icon: "💾" },
  { id: "rep-2", name: "Replica West", ip: "10.0.1.11", targetX: -260, targetY: 130, icon: "💾" },
  { id: "rep-3", name: "Replica East", ip: "10.0.1.12", targetX: 260, targetY: 130, icon: "💾" },
];

export const DatabaseCluster: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // ===================================================
  // 1. PRIMARY DATABASE SPRING
  // ===================================================
  // Pops into the center at frame 15.
  const primarySpring = spring({
    frame: frame - 15,
    fps,
    config: {
      stiffness: 140,
      damping: 14,
      mass: 0.9,
    },
  });
  const primaryScale = primarySpring;
  const primaryOpacity = primarySpring;

  // ===================================================
  // 2. REPLICA ENTRY & BRANCHING SPRING
  // ===================================================
  // Replicas appear and slide out starting at frame 40.
  const replicaSpring = spring({
    frame: frame - 40,
    fps,
    config: {
      stiffness: 90,
      damping: 18,
      mass: 1.1,
    },
  });

  // Replicas fade in as they slide
  const replicaOpacity = replicaSpring;
  // Scale starts from 0.5 to 1.0
  const replicaScale = interpolate(replicaSpring, [0, 1], [0.5, 1]);

  return (
    <AbsoluteFill className="bg-slate-950 flex flex-col items-center justify-between py-10 font-sans text-white overflow-hidden">
      {/* Dynamic network background grid */}
      <div className="absolute inset-0 bg-[linear-gradient(to_right,rgba(99,102,241,0.03)_1px,transparent_1px),linear-gradient(to_bottom,rgba(99,102,241,0.03)_1px,transparent_1px)] bg-[size:40px_40px] pointer-events-none" />
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,rgba(99,102,241,0.04),transparent_70%)] pointer-events-none" />

      {/* Header */}
      <div className="z-10 text-center">
        <span className="px-3 py-1 text-xs font-semibold tracking-wider text-emerald-400 uppercase bg-emerald-950/50 border border-emerald-800/40 rounded-full">
          Stage 2: Mini Project 2
        </span>
        <h1 className="mt-3 text-4xl font-extrabold tracking-tight bg-gradient-to-r from-white via-indigo-200 to-indigo-400 bg-clip-text text-transparent">
          Database Cluster Architecture
        </h1>
        <p className="mt-2 text-sm text-slate-400">
          Replicating database state dynamically with staggered spring offsets
        </p>
      </div>

      {/* Visual Canvas Area */}
      <div className="relative w-full h-[500px] flex items-center justify-center">
        
        {/* ===================================================
            SVG CONNECTIONS LAYER (Cables connecting servers)
            =================================================== */}
        {/* We place an absolute SVG behind the nodes. By drawing lines 
            from (0,0) center to (x, y) coordinates of the replicas 
            multiplied by replicaSpring, the lines automatically 
            draw themselves outwards in sync with the nodes! */}
        <svg className="absolute w-[800px] h-[500px] pointer-events-none overflow-visible">
          {primarySpring > 0.1 && REPLICAS.map((rep) => {
            // Calculate current line ending coordinates based on slide progress
            const currentX = rep.targetX * replicaSpring;
            const currentY = rep.targetY * replicaSpring;
            
            return (
              <g key={`cable-${rep.id}`}>
                {/* Connection pipe shadow/glow */}
                <line
                  x1={400} // Center of SVG canvas (800 / 2)
                  y1={250} // Center of SVG canvas (500 / 2)
                  x2={400 + currentX}
                  y2={250 + currentY}
                  stroke="rgba(99, 102, 241, 0.25)"
                  strokeWidth={6}
                  strokeLinecap="round"
                  style={{ opacity: replicaOpacity }}
                />
                {/* Core pipe line */}
                <line
                  x1={400}
                  y1={250}
                  x2={400 + currentX}
                  y2={250 + currentY}
                  stroke="rgba(129, 140, 248, 0.8)"
                  strokeWidth={2}
                  strokeLinecap="round"
                  style={{ opacity: replicaOpacity }}
                />
              </g>
            );
          })}
        </svg>

        {/* ===================================================
            PRIMARY DATABASE NODE (Center)
            =================================================== */}
        <div
          style={{
            transform: `scale(${primaryScale})`,
            opacity: primaryOpacity,
          }}
          className="absolute z-20 w-44 h-44 bg-slate-900 border-2 border-indigo-500 rounded-3xl flex flex-col justify-between p-4 shadow-[0_0_40px_rgba(99,102,241,0.35)]"
        >
          <div className="flex justify-between items-start">
            <span className="text-[9px] bg-indigo-950 text-indigo-300 px-1.5 py-0.5 rounded font-bold border border-indigo-500/20">
              PRIMARY
            </span>
            <div className="w-2.5 h-2.5 bg-emerald-400 rounded-full shadow-[0_0_6px_#34d399] animate-pulse" />
          </div>
          <div className="flex flex-col items-center gap-1.5 my-auto">
            <div className="text-3xl">🗄️</div>
            <span className="font-extrabold text-[11px] tracking-wide text-slate-100">PROD-DB-MAIN</span>
          </div>
          <div className="text-center">
            <span className="font-mono text-[9px] text-slate-500">10.0.1.1</span>
          </div>
        </div>

        {/* ===================================================
            REPLICA DATABASE NODES (Branching out)
            =================================================== */}
        {REPLICAS.map((rep) => {
          // Compute current relative translation coordinate driven by the spring
          const currentX = rep.targetX * replicaSpring;
          const currentY = rep.targetY * replicaSpring;

          return (
            <div
              key={rep.id}
              style={{
                transform: `translate(${currentX}px, ${currentY}px) scale(${replicaScale})`,
                opacity: replicaOpacity,
              }}
              className="absolute z-10 w-36 h-36 bg-slate-900/90 border border-slate-800 rounded-2xl flex flex-col justify-between p-3.5 shadow-lg backdrop-blur-sm"
            >
              <div className="flex justify-between items-start">
                <span className="text-[8px] bg-slate-950 text-slate-400 px-1.5 py-0.5 rounded font-semibold border border-slate-800">
                  REPLICA
                </span>
                <div className="w-2 h-2 bg-indigo-400 rounded-full shadow-[0_0_4px_#818cf8]" />
              </div>
              <div className="flex flex-col items-center gap-1 my-auto">
                <div className="text-2xl">{rep.icon}</div>
                <span className="font-bold text-[10px] text-slate-200">{rep.name}</span>
              </div>
              <div className="text-center">
                <span className="font-mono text-[8px] text-slate-500">{rep.ip}</span>
              </div>
            </div>
          );
        })}

      </div>

      {/* Telemetry panel */}
      <div className="z-10 w-[800px] bg-slate-900/60 border border-slate-800 rounded-2xl p-5 backdrop-blur-md shadow-xl font-mono text-xs text-slate-300 flex flex-col gap-3">
        <div className="flex justify-between border-b border-slate-800/60 pb-2 text-[10px] text-slate-500">
          <span>CLUSTER STATE SYNC TELEMETRY</span>
          <span>Frame: {frame}</span>
        </div>
        <div className="grid grid-cols-3 gap-4 text-center text-[10px]">
          <div className="flex flex-col gap-1 border-r border-slate-800/60">
            <span className="text-slate-500">PRIMARY SCALE</span>
            <span className="text-indigo-400 font-bold">
              {(primarySpring * 100).toFixed(1)}%
            </span>
          </div>
          <div className="flex flex-col gap-1 border-r border-slate-800/60">
            <span className="text-slate-500">REPLICA SLIDE PROGRESS</span>
            <span className="text-emerald-400 font-bold">
              {(replicaSpring * 100).toFixed(1)}%
            </span>
          </div>
          <div className="flex flex-col gap-1">
            <span className="text-slate-500">SYSTEM STATE</span>
            <span className={frame < 15 ? "text-slate-600" : frame < 40 ? "text-indigo-400 font-bold" : "text-emerald-400 font-bold"}>
              {frame < 15 ? "INITIALIZING" : frame < 40 ? "PROVISIONING LEADER" : "CLUSTER ACTIVE"}
            </span>
          </div>
        </div>
      </div>
    </AbsoluteFill>
  );
};
