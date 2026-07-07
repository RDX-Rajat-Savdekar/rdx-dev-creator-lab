import React from "react";
import {
  AbsoluteFill,
  interpolate,
  spring,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import { TransitionSeries, linearTiming } from "@remotion/transitions";
import { slide } from "@remotion/transitions/slide";
import { fade } from "@remotion/transitions/fade";
import {
  Server,
  Cpu,
  Users,
  ShoppingBag,
  CreditCard,
  Activity,
  CheckCircle,
  TrendingDown,
} from "lucide-react";

// ===================================================
// SCENE 1: MONOLITH DATABASE OVERLOAD
// ===================================================
const SceneMonolith: React.FC = () => {
  const frame = useCurrentFrame();

  // Pulse effect representing server load stress
  const pulse = interpolate(Math.sin(frame * 0.25), [-1, 1], [0.95, 1.15]);
  const serverGlow = isNaN(pulse) ? 0.95 : pulse;

  // Staggered request arrows flying towards the monolith
  const packet1 = interpolate(frame % 30, [0, 30], [0, 1]);
  const packet2 = interpolate((frame + 10) % 30, [0, 30], [0, 1]);

  return (
    <AbsoluteFill className="bg-slate-950 flex flex-col items-center justify-center font-mono text-white p-10">
      <div className="absolute top-10 text-center">
        <span className="px-3 py-1 text-xs font-semibold tracking-wider text-red-500 uppercase bg-red-950/50 border border-red-800/40 rounded-full">
          Scene 1: The Bottleneck
        </span>
        <h2 className="text-3xl font-extrabold tracking-tight mt-2 text-slate-100">
          Legacy Monolith Server Overload
        </h2>
      </div>

      <div className="flex items-center gap-20 mt-10">
        {/* User Clients Node */}
        <div className="flex flex-col items-center gap-3 bg-slate-900/60 border border-slate-800 p-6 rounded-2xl w-44">
          <Users className="w-10 h-10 text-slate-400" />
          <span className="text-xs font-bold text-slate-300">
            10,000 Concurrent Users
          </span>
        </div>

        {/* Requests flying pipeline */}
        <div className="relative w-48 h-6 flex items-center justify-center">
          <div className="w-full h-1 bg-red-900/30 rounded" />
          {/* Packet 1 */}
          <div
            style={{ left: `${packet1 * 100}%` }}
            className="absolute w-3 h-3 rounded-full bg-red-500 shadow-[0_0_10px_#ef4444]"
          />
          {/* Packet 2 */}
          <div
            style={{ left: `${packet2 * 100}%` }}
            className="absolute w-3 h-3 rounded-full bg-red-500 shadow-[0_0_10px_#ef4444]"
          />
        </div>

        {/* Monolith Server */}
        <div
          style={{
            transform: `scale(${serverGlow})`,
            boxShadow: `0 0 40px rgba(239, 68, 68, ${interpolate(Math.sin(frame * 0.2), [-1, 1], [0.1, 0.4])})`,
          }}
          className="flex flex-col items-center justify-center gap-4 bg-slate-900/80 border-2 border-red-500/80 p-8 rounded-3xl w-56 relative overflow-hidden"
        >
          {/* Glowing alarm badge */}
          <div className="absolute top-3 right-3 flex h-3 w-3">
            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-red-400 opacity-75"></span>
            <span className="relative inline-flex rounded-full h-3 w-3 bg-red-500"></span>
          </div>

          <Server className="w-16 h-16 text-red-400" />
          <span className="text-sm font-black text-red-400">
            MONOLITHIC Core
          </span>

          <div className="flex items-center gap-1.5 bg-red-950/60 border border-red-800/40 px-3 py-1 rounded-lg text-[10px] text-red-400 font-extrabold animate-pulse">
            <Cpu className="w-3.5 h-3.5" /> CPU LOAD: 99%
          </div>
        </div>
      </div>
    </AbsoluteFill>
  );
};

// ===================================================
// SCENE 2: MICROSERVICES MIGRATION (API GATEWAY)
// ===================================================
const SceneMicroservices: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Load entry animation spring for nodes
  const entrySpring = spring({ frame, fps, config: { damping: 13 } });
  const scaleNode = interpolate(entrySpring, [0, 1], [0.5, 1]);

  // Request flow offsets
  const packetY1 = interpolate(frame % 25, [0, 25], [-10, -50]);
  const packetY2 = interpolate(frame % 25, [0, 25], [10, 50]);

  return (
    <AbsoluteFill className="bg-slate-950 flex flex-col items-center justify-center font-mono text-white p-10">
      <div className="absolute top-10 text-center">
        <span className="px-3 py-1 text-xs font-semibold tracking-wider text-indigo-400 uppercase bg-indigo-950/50 border border-indigo-800/40 rounded-full">
          Scene 2: Architecture Upgrade
        </span>
        <h2 className="text-3xl font-extrabold tracking-tight mt-2 text-slate-100">
          Decoupled Microservice Architecture
        </h2>
      </div>

      <div
        style={{ transform: `scale(${scaleNode})` }}
        className="flex items-center justify-center gap-12 mt-16 w-full max-w-4xl"
      >
        {/* API Gateway Entry */}
        <div className="flex flex-col items-center gap-4 bg-slate-900 border border-indigo-500/50 p-6 rounded-2xl w-48 relative shadow-[0_0_20px_rgba(99,102,241,0.1)]">
          <Activity className="w-10 h-10 text-indigo-400" />
          <span className="text-xs font-bold text-slate-200">API GATEWAY</span>
          <span className="text-[9px] text-slate-500">
            Rate Limiting & Routing
          </span>
        </div>

        {/* Dynamic connection paths */}
        <div className="relative w-20 h-40 flex flex-col justify-between py-5">
          <div className="absolute top-[50%] left-0 w-full h-0.5 bg-slate-800" />

          {/* Glowing packets */}
          <div
            style={{
              transform: `translate3d(${interpolate(frame % 25, [0, 25], [0, 80])}px, ${packetY1}px, 0px)`,
            }}
            className="absolute w-2 h-2 rounded-full bg-indigo-400 shadow-[0_0_8px_#818cf8]"
          />
          <div
            style={{
              transform: `translate3d(${interpolate((frame + 12) % 25, [0, 25], [0, 80])}px, ${packetY2}px, 0px)`,
            }}
            className="absolute w-2 h-2 rounded-full bg-emerald-400 shadow-[0_0_8px_#34d399]"
          />
        </div>

        {/* Microservices Column */}
        <div className="flex flex-col gap-4">
          {/* Service 1 */}
          <div className="flex items-center gap-4 bg-slate-900/60 border border-slate-800 p-4 rounded-xl w-60">
            <Users className="w-6 h-6 text-indigo-400" />
            <div className="flex flex-col">
              <span className="text-xs font-black text-slate-200">
                USER SERVICE
              </span>
              <span className="text-[8px] text-slate-500">
                Node-Scale: 4 replicas
              </span>
            </div>
          </div>

          {/* Service 2 */}
          <div className="flex items-center gap-4 bg-slate-900/60 border border-slate-800 p-4 rounded-xl w-60">
            <ShoppingBag className="w-6 h-6 text-indigo-400" />
            <div className="flex flex-col">
              <span className="text-xs font-black text-slate-200">
                ORDER SERVICE
              </span>
              <span className="text-[8px] text-slate-500">
                Node-Scale: 6 replicas
              </span>
            </div>
          </div>

          {/* Service 3 */}
          <div className="flex items-center gap-4 bg-slate-900/60 border border-slate-800 p-4 rounded-xl w-60">
            <CreditCard className="w-6 h-6 text-indigo-400" />
            <div className="flex flex-col">
              <span className="text-xs font-black text-slate-200">
                PAYMENT SERVICE
              </span>
              <span className="text-[8px] text-slate-500">
                Node-Scale: 2 replicas
              </span>
            </div>
          </div>
        </div>
      </div>
    </AbsoluteFill>
  );
};

// ===================================================
// SCENE 3: FINAL OPERATIONAL TELEMETRY
// ===================================================
const SceneTelemetry: React.FC = () => {
  return (
    <AbsoluteFill className="bg-slate-950 flex flex-col items-center justify-center font-mono text-white p-10">
      <div className="absolute top-10 text-center">
        <span className="px-3 py-1 text-xs font-semibold tracking-wider text-emerald-400 uppercase bg-emerald-950/50 border border-emerald-800/40 rounded-full">
          Scene 3: Healthy Baseline
        </span>
        <h2 className="text-3xl font-extrabold tracking-tight mt-2 text-slate-100">
          System Recovery Telemetry
        </h2>
      </div>

      <div className="flex flex-col gap-6 items-center mt-12 w-full max-w-2xl">
        {/* Success Alert Banner */}
        <div className="flex items-center gap-3 bg-emerald-950/40 border border-emerald-500/30 p-4 rounded-2xl w-full">
          <CheckCircle className="w-8 h-8 text-emerald-400" />
          <div>
            <span className="text-xs font-black text-emerald-400 uppercase block">
              Migration Success
            </span>
            <span className="text-[10px] text-slate-400">
              Latency spikes mitigated, distributed queues processing cleanly
            </span>
          </div>
        </div>

        {/* Telemetry charts */}
        <div className="grid grid-cols-2 gap-6 w-full">
          {/* Latency reduction metric */}
          <div className="bg-slate-900/60 border border-slate-800/60 p-5 rounded-2xl flex flex-col justify-between">
            <span className="text-[10px] text-slate-500 block">
              AVERAGE LATENCY
            </span>
            <div className="mt-3 flex items-center gap-4">
              <span className="text-4xl font-extrabold text-slate-100">
                35ms
              </span>
              <div className="flex items-center gap-1 bg-emerald-950 text-emerald-400 px-2 py-0.5 rounded text-[9px] font-bold">
                <TrendingDown className="w-3.5 h-3.5" /> -85%
              </div>
            </div>
          </div>

          {/* Request Success Rate */}
          <div className="bg-slate-900/60 border border-slate-800/60 p-5 rounded-2xl flex flex-col justify-between">
            <span className="text-[10px] text-slate-500 block">
              HTTP 200 OK RATE
            </span>
            <div className="mt-3 flex items-center gap-4">
              <span className="text-4xl font-extrabold text-slate-100">
                99.99%
              </span>
              <span className="text-[9px] text-emerald-500 font-bold">
                OPTIMIZED
              </span>
            </div>
          </div>
        </div>
      </div>
    </AbsoluteFill>
  );
};

// ===================================================
// ROOT EXPLAINER: SEQUENCE TIMELINE & TRANSITIONS
// ===================================================
export const MonolithToMicroservices: React.FC = () => {
  return (
    <TransitionSeries>
      {/* 1. Scene Monolith: Active for 65 frames */}
      <TransitionSeries.Sequence durationInFrames={65}>
        <SceneMonolith />
      </TransitionSeries.Sequence>
      {/* Slide left transition: 15 frames */}
      <TransitionSeries.Transition
        presentation={slide({ direction: "from-left" })}
        timing={linearTiming({ durationInFrames: 15 })}
      />
      {/* 2. Scene Microservices: Active for 65 frames */}
      <TransitionSeries.Sequence durationInFrames={65}>
        <SceneMicroservices />
      </TransitionSeries.Sequence>
      {/* Cross-fade transition: 15 frames */}
      <TransitionSeries.Transition
        presentation={fade()}
        timing={linearTiming({ durationInFrames: 15 })}
      />
      {/* 3. Scene Telemetry: Active for 50 frames */}
      <TransitionSeries.Sequence durationInFrames={50}>
        <SceneTelemetry />
      </TransitionSeries.Sequence>
    </TransitionSeries>
  );
};
