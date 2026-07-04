import React from "react";
import {
  AbsoluteFill,
  interpolate,
  spring,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";

export const RequestRouter: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // ===================================================
  // 1. SELF-DRAWING CONNECTIONS MATH
  // ===================================================
  // Line lengths:
  // Client (200, 270) -> LB (480, 270) => Length = 280px
  // LB (520, 250) -> Web A (750, 150) => dx=230, dy=-100 => Length = sqrt(230^2 + 100^2) = ~250px
  // LB (520, 290) -> Web B (750, 390) => dx=230, dy=100 => Length = ~250px
  const lineLengthClientToLB = 280;
  const lineLengthLBToWeb = 250;

  // Connection 1 (Client -> LB) draws from frame 15 to 45
  const drawClientToLBSpring = spring({
    frame: frame - 15,
    fps,
    config: { stiffness: 90, damping: 15 },
  });
  const offsetClientToLB = interpolate(drawClientToLBSpring, [0, 1], [lineLengthClientToLB, 0]);

  // Connection 2 (LB -> Web A & B) draws from frame 45 to 75
  const drawLBToWebSpring = spring({
    frame: frame - 45,
    fps,
    config: { stiffness: 90, damping: 15 },
  });
  const offsetLBToWeb = interpolate(drawLBToWebSpring, [0, 1], [lineLengthLBToWeb, 0]);

  // ===================================================
  // 2. DATA PACKET FLOW MATH
  // ===================================================
  // Packets start flowing after the paths are drawn (from frame 75 onwards).
  // We'll create repeating packets using modulo.
  const flowStartFrame = 75;
  const activeFrame = frame - flowStartFrame;

  // Client -> Load Balancer Packets:
  // We send a packet every 40 frames.
  const packet1Progress = activeFrame > 0 ? (activeFrame % 40) / 30 : -1; // travels for 30 frames
  // Load Balancer -> Web Server Packets:
  // These start after the packet reaches the Load Balancer (30 frames offset).
  // Alternate routing: even packets go to Server A, odd packets go to Server B.
  const isPacketEven = Math.floor(activeFrame / 40) % 2 === 0;
  const packet2Progress = activeFrame > 30 ? ((activeFrame - 30) % 40) / 30 : -1;

  // Interpolated coordinates for packets:
  // Packet 1: Client (x: 200, y: 270) -> LB (x: 480, y: 270)
  const packet1X = interpolate(packet1Progress, [0, 1], [200, 480], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  
  // Packet 2: LB (x: 520) -> Web A (x: 750, y: 150) OR Web B (x: 750, y: 390)
  const packet2X = interpolate(packet2Progress, [0, 1], [520, 750], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const packet2Y = interpolate(
    packet2Progress,
    [0, 1],
    [270, isPacketEven ? 150 : 390],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
  );

  return (
    <AbsoluteFill className="bg-slate-950 flex flex-col items-center justify-between py-10 font-sans text-white overflow-hidden">
      {/* Visual canvas grid */}
      <div className="absolute inset-0 bg-[linear-gradient(to_right,rgba(99,102,241,0.02)_1px,transparent_1px),linear-gradient(to_bottom,rgba(99,102,241,0.02)_1px,transparent_1px)] bg-[size:40px_40px] pointer-events-none" />
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,rgba(56,189,248,0.03),transparent_70%)] pointer-events-none" />

      {/* Header */}
      <div className="z-10 text-center">
        <span className="px-3 py-1 text-xs font-semibold tracking-wider text-sky-400 uppercase bg-sky-950/50 border border-sky-800/40 rounded-full">
          Stage 3: Lab Exercise 1 & 2
        </span>
        <h1 className="mt-3 text-4xl font-extrabold tracking-tight bg-gradient-to-r from-white via-sky-200 to-sky-400 bg-clip-text text-transparent">
          Load Balancer & Request Router
        </h1>
        <p className="mt-2 text-sm text-slate-400">
          Animating self-drawing SVG connections and packet coordinate flows
        </p>
      </div>

      {/* Interactive Architecture Canvas */}
      <div className="relative w-[1000px] h-[480px] bg-slate-900/30 rounded-3xl border border-slate-900/80 flex items-center justify-center">
        
        {/* ===================================================
            SVG LINE LAYERS & ARROWS
            =================================================== */}
        <svg className="absolute inset-0 w-full h-full pointer-events-none overflow-visible">
          {/* Defs for arrow heads */}
          <defs>
            <marker id="arrow" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
              <path d="M 0 1 L 10 5 L 0 9 z" fill="#38bdf8" />
            </marker>
          </defs>

          {/* Connection 1: Client -> Load Balancer */}
          <path
            d="M 200,270 L 480,270"
            stroke="#1e293b"
            strokeWidth={4}
            strokeLinecap="round"
          />
          <path
            d="M 200,270 L 480,270"
            stroke="#38bdf8"
            strokeWidth={4}
            strokeLinecap="round"
            strokeDasharray={lineLengthClientToLB}
            strokeDashoffset={offsetClientToLB}
            markerEnd="url(#arrow)"
          />

          {/* Connection 2a: Load Balancer -> Web Server A */}
          <path
            d="M 520,270 L 750,150"
            stroke="#1e293b"
            strokeWidth={4}
            strokeLinecap="round"
          />
          <path
            d="M 520,270 L 750,150"
            stroke="#818cf8"
            strokeWidth={4}
            strokeLinecap="round"
            strokeDasharray={lineLengthLBToWeb}
            strokeDashoffset={offsetLBToWeb}
            markerEnd="url(#arrow)"
          />

          {/* Connection 2b: Load Balancer -> Web Server B */}
          <path
            d="M 520,270 L 750,390"
            stroke="#1e293b"
            strokeWidth={4}
            strokeLinecap="round"
          />
          <path
            d="M 520,270 L 750,390"
            stroke="#818cf8"
            strokeWidth={4}
            strokeLinecap="round"
            strokeDasharray={lineLengthLBToWeb}
            strokeDashoffset={offsetLBToWeb}
            markerEnd="url(#arrow)"
          />
        </svg>

        {/* ===================================================
            ANIMATING PACKET FLOW CIRCLES
            =================================================== */}
        {/* Packet 1 (Client -> LB) */}
        {packet1Progress >= 0 && packet1Progress <= 1 && (
          <div
            style={{
              position: "absolute",
              left: packet1X - 8,
              top: 270 - 8,
            }}
            className="w-4 h-4 bg-sky-400 rounded-full shadow-[0_0_12px_#38bdf8] border border-white/20 z-30"
          />
        )}

        {/* Packet 2 (LB -> Web A or Web B) */}
        {packet2Progress >= 0 && packet2Progress <= 1 && (
          <div
            style={{
              position: "absolute",
              left: packet2X - 8,
              top: packet2Y - 8,
            }}
            className={`w-4 h-4 rounded-full border border-white/20 z-30 shadow-lg ${
              isPacketEven 
                ? "bg-emerald-400 shadow-[0_0_12px_#34d399]" 
                : "bg-purple-400 shadow-[0_0_12px_#c084fc]"
            }`}
          />
        )}

        {/* ===================================================
            SERVER / NODE CARDS
            =================================================== */}
        {/* Client Card */}
        <div style={{ position: "absolute", left: 50, top: 210 }} className="w-36 h-30 bg-slate-900 border border-slate-800 rounded-2xl p-4 flex flex-col items-center justify-center gap-2 shadow-2xl">
          <div className="text-2xl">💻</div>
          <span className="font-bold text-xs">CLIENT</span>
          <span className="font-mono text-[9px] text-slate-500">192.168.1.50</span>
        </div>

        {/* Load Balancer Card */}
        <div style={{ position: "absolute", left: 430, top: 210 }} className="w-36 h-30 bg-slate-900 border border-sky-500/50 rounded-2xl p-4 flex flex-col items-center justify-center gap-2 shadow-[0_0_20px_rgba(56,189,248,0.15)] z-20">
          <div className="text-2xl animate-pulse">🎛️</div>
          <span className="font-bold text-xs text-sky-400">NGINX / LB</span>
          <span className="font-mono text-[9px] text-slate-500">10.0.0.1</span>
        </div>

        {/* Web Server A Card */}
        <div style={{ position: "absolute", left: 780, top: 90 }} className="w-40 h-30 bg-slate-900 border border-slate-800 rounded-2xl p-4 flex flex-col items-center justify-center gap-2 shadow-2xl">
          <div className="flex justify-between items-center w-full px-1">
            <span className="text-emerald-400 font-bold text-[8px] tracking-wider uppercase">WEB-01</span>
            <div className={`w-2 h-2 rounded-full ${packet2Progress >= 0.9 && isPacketEven ? "bg-emerald-400 shadow-[0_0_6px_#34d399]" : "bg-slate-700"}`} />
          </div>
          <div className="text-2xl">⚙️</div>
          <span className="font-bold text-xs">WEB SERVER A</span>
        </div>

        {/* Web Server B Card */}
        <div style={{ position: "absolute", left: 780, top: 330 }} className="w-40 h-30 bg-slate-900 border border-slate-800 rounded-2xl p-4 flex flex-col items-center justify-center gap-2 shadow-2xl">
          <div className="flex justify-between items-center w-full px-1">
            <span className="text-purple-400 font-bold text-[8px] tracking-wider uppercase">WEB-02</span>
            <div className={`w-2 h-2 rounded-full ${packet2Progress >= 0.9 && !isPacketEven ? "bg-purple-400 shadow-[0_0_6px_#c084fc]" : "bg-slate-700"}`} />
          </div>
          <div className="text-2xl">⚙️</div>
          <span className="font-bold text-xs">WEB SERVER B</span>
        </div>

      </div>

      {/* Telemetry panel */}
      <div className="z-10 w-[800px] bg-slate-900/60 border border-slate-800 rounded-2xl p-5 backdrop-blur-md shadow-xl font-mono text-xs text-slate-300 flex flex-col gap-3">
        <div className="flex justify-between border-b border-slate-800/60 pb-2 text-[10px] text-slate-500">
          <span>PACKET ROUTING MATRIX</span>
          <span>Frame: {frame}</span>
        </div>
        <div className="grid grid-cols-4 gap-4 text-center text-[10px]">
          <div className="flex flex-col gap-1 border-r border-slate-800/60">
            <span className="text-slate-500">{"CLIENT -> LB DASH"}</span>
            <span className="text-sky-400 font-bold">{offsetClientToLB.toFixed(0)}px</span>
          </div>
          <div className="flex flex-col gap-1 border-r border-slate-800/60">
            <span className="text-slate-500">{"LB -> WEB DASH"}</span>
            <span className="text-indigo-400 font-bold">{offsetLBToWeb.toFixed(0)}px</span>
          </div>
          <div className="flex flex-col gap-1 border-r border-slate-800/60">
            <span className="text-slate-500">PACKET 1 POS</span>
            <span className="text-sky-400 font-bold">
              {packet1Progress >= 0 && packet1Progress <= 1 ? `x=${packet1X.toFixed(0)}` : "OFFLINE"}
            </span>
          </div>
          <div className="flex flex-col gap-1">
            <span className="text-slate-500">ROUTING TARGET</span>
            <span className={packet2Progress >= 0 && packet2Progress <= 1 ? (isPacketEven ? "text-emerald-400 font-bold" : "text-purple-400 font-bold") : "text-slate-600"}>
              {packet2Progress >= 0 && packet2Progress <= 1 ? (isPacketEven ? "SERVER A" : "SERVER B") : "IDLE"}
            </span>
          </div>
        </div>
      </div>
    </AbsoluteFill>
  );
};
