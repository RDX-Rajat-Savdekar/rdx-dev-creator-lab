import React from "react";
import { AbsoluteFill, useCurrentFrame } from "remotion";
import { SkiaCanvas } from "@remotion/skia";
import { Circle, Group } from "@shopify/react-native-skia";
import { z } from "zod";
import { zColor } from "@remotion/zod-types";
import { Activity, Server } from "lucide-react";

// ===================================================
// ZOD SCHEMA DEFINITION FOR SKIA PROPERTIES
// ===================================================
export const skiaLoadBalancerSchema = z.object({
  particleCount: z.number().min(20).max(200).step(10).default(120).describe("Total number of active flowing requests"),
  particleColor: zColor().default("#38bdf8").describe("Color of the data packet particles"),
  loadBalancerColor: zColor().default("#6366f1").describe("Highlight color of the routing load balancer"),
});

type SkiaProps = z.infer<typeof skiaLoadBalancerSchema>;

// Server target configurations
const SERVERS = [
  { id: 0, x: 100, label: "SERVER-A" },
  { id: 1, x: 250, label: "SERVER-B" },
  { id: 2, x: 400, label: "SERVER-C" },
];

export const SkiaLoadBalancer: React.FC<SkiaProps> = ({
  particleCount,
  particleColor,
  loadBalancerColor,
}) => {
  const frame = useCurrentFrame();

  // Create particle definitions based on index
  const particles = Array.from({ length: particleCount }, (_, idx) => {
    // Staggered launch start frame
    const startFrame = idx * 6;
    
    // Choose destination server in round-robin sequence
    const targetIdx = idx % SERVERS.length;
    const targetX = SERVERS[targetIdx].x;

    return {
      id: idx,
      startFrame,
      targetX,
      color: targetIdx === 0 ? "#ef4444" : targetIdx === 1 ? particleColor : "#10b981",
    };
  });

  const duration = 45; // Traveling duration per packet (45 frames)

  return (
    <AbsoluteFill className="bg-slate-950 flex flex-col items-center justify-between py-6 font-mono text-white overflow-hidden">
      {/* Background Matrix */}
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,rgba(99,102,241,0.02),transparent_70%)] pointer-events-none" />

      {/* Header */}
      <div className="z-10 text-center">
        <span className="px-3 py-1 text-xs font-semibold tracking-wider text-indigo-400 uppercase bg-indigo-950/50 border border-indigo-800/40 rounded-full">
          Stage 10: Canvas Skia (WebGL-Engine)
        </span>
        <h1 className="mt-2 text-4xl font-extrabold tracking-tight bg-gradient-to-r from-white via-indigo-200 to-indigo-400 bg-clip-text text-transparent">
          High-Performance Skia Packet Routing
        </h1>
        <p className="mt-1 text-xs text-slate-400">
          Hardware-accelerated Skia rendering engine driving {particleCount} request packet streams
        </p>
      </div>

      {/* Dynamic Graphic Container */}
      <div className="z-10 relative w-[500px] h-[400px]">
        {/* Layer 1: SVG static background pipes */}
        <svg
          width="500"
          height="400"
          className="absolute inset-0 z-0 pointer-events-none"
        >
          {/* Main vertical trunk pipeline */}
          <line x1="250" y1="110" x2="250" y2="200" stroke="#1e293b" strokeWidth="6" strokeLinecap="round" />
          
          {/* Horizontal branching pipeline */}
          <line x1="100" y1="200" x2="400" y2="200" stroke="#1e293b" strokeWidth="6" strokeLinecap="round" />
          
          {/* Destination server drops */}
          <line x1="100" y1="200" x2="100" y2="330" stroke="#1e293b" strokeWidth="6" strokeLinecap="round" />
          <line x1="250" y1="200" x2="250" y2="330" stroke="#1e293b" strokeWidth="6" strokeLinecap="round" />
          <line x1="400" y1="200" x2="400" y2="330" stroke="#1e293b" strokeWidth="6" strokeLinecap="round" />
        </svg>

        <SkiaCanvas 
          width={500} 
          height={400} 
          className="absolute inset-0 z-10 pointer-events-none"
        >
          <Group>
              {particles.map((p) => {
                // Only draw if the packet is currently active on the timeline
                if (frame < p.startFrame || frame > p.startFrame + duration) {
                  return null;
                }

                // Calculate transition index from 0 to 1
                const t = (frame - p.startFrame) / duration;
                
                let px = 250;
                let py = 110;

                // Coordinate routing path math:
                // 1. Downward segment into distribution junction
                if (t <= 0.3) {
                  const segT = t / 0.3;
                  py = 110 + segT * (200 - 110);
                } 
                // 2. Horizontal branch segment
                else if (t <= 0.7) {
                  const segT = (t - 0.3) / 0.4;
                  py = 200;
                  px = 250 + segT * (p.targetX - 250);
                } 
                // 3. Final drop segment into server node
                else {
                  const segT = (t - 0.7) / 0.3;
                  px = p.targetX;
                  py = 200 + segT * (330 - 200);
                }

                return (
                  <Circle 
                    key={p.id} 
                    cx={px} 
                    cy={py} 
                    r={5}
                    color={p.color}
                  />
                );
              })}
            </Group>
        </SkiaCanvas>

        {/* Layer 3: Interactive HTML Nodes placed absolutely on top */}
        
        {/* Load Balancer Server Block */}
        <div 
          style={{ 
            borderColor: loadBalancerColor,
            boxShadow: `0 0 15px ${loadBalancerColor}22` 
          }}
          className="absolute top-[30px] left-[175px] w-[150px] h-[80px] bg-slate-900 border rounded-2xl flex flex-col items-center justify-center gap-1 z-20"
        >
          <Activity className="w-5 h-5" style={{ color: loadBalancerColor }} />
          <span className="text-[10px] font-black uppercase text-slate-300">LOAD BALANCER</span>
          <span className="text-[7px] text-slate-500 font-mono">ROUND ROBIN ROUTING</span>
        </div>

        {/* Destination Servers Row */}
        {SERVERS.map((srv) => (
          <div
            key={srv.id}
            style={{ left: `${srv.x - 70}px` }}
            className="absolute bottom-[20px] w-[140px] h-[75px] bg-slate-900 border border-slate-800 rounded-2xl flex flex-col items-center justify-center gap-1 z-20"
          >
            <Server className="w-5 h-5 text-slate-400" />
            <span className="text-[10px] font-black uppercase text-slate-300">{srv.label}</span>
            <span className="text-[7px] text-slate-600 font-mono">Status: ACTIVE</span>
          </div>
        ))}
      </div>

      {/* Telemetry panel */}
      <div className="z-10 w-[800px] bg-slate-900/60 border border-slate-800 rounded-2xl p-5 backdrop-blur-md shadow-xl font-mono text-[10px] text-slate-300 flex flex-col gap-3">
        <div className="flex justify-between border-b border-slate-800/60 pb-2 text-slate-500">
          <span>SKIA WEBGL TELEMETRY MATRIX</span>
          <span>Frame: {frame}</span>
        </div>
        <div className="grid grid-cols-4 gap-4 text-center">
          <div className="flex flex-col gap-1 border-r border-slate-800/60">
            <span className="text-slate-500">PARTICLE SCALE</span>
            <span className="text-indigo-400 font-bold">{particleCount}</span>
          </div>
          <div className="flex flex-col gap-1 border-r border-slate-800/60">
            <span className="text-slate-500">ACTIVE ON SCREEN</span>
            <span className="text-indigo-400 font-bold">
              {particles.filter(p => frame >= p.startFrame && frame <= p.startFrame + duration).length}
            </span>
          </div>
          <div className="flex flex-col gap-1 border-r border-slate-800/60">
            <span className="text-slate-500">CANVAS DPI</span>
            <span className="text-indigo-400 font-bold">1.0 (STANDARD)</span>
          </div>
          <div className="flex flex-col gap-1">
            <span className="text-slate-500">RENDER PATH</span>
            <span className="text-emerald-400 font-bold">SKIA.CPU_GPU</span>
          </div>
        </div>
      </div>
    </AbsoluteFill>
  );
};
