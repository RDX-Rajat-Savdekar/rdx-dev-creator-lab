import React from "react";
import {
  AbsoluteFill,
  Html5Audio,
  interpolate,
  spring,
  useCurrentFrame,
  useVideoConfig,
  staticFile,
} from "remotion";

export const TechExplainer: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();

  // ===================================================
  // TIMELINE MARKERS & TRIGGER SYNC
  // ===================================================
  // 1. Frame 45: First request (Cache Miss flow starts)
  // 2. Frame 90: CDN Edge checks Origin
  // 3. Frame 130: Origin returns data to CDN
  // 4. Frame 170: CDN returns data to Client & saves Cache
  // 5. Frame 220: Second request (Cache Hit flow starts)
  // 6. Frame 250: CDN returns data directly to Client

  // Request 1 Progress (Client -> CDN)
  const req1Progress = interpolate(frame, [45, 75], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  // Edge to Origin Request Progress (CDN -> Origin)
  const edgeToOriginProgress = interpolate(frame, [90, 120], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  // Origin response back to CDN (Origin -> CDN)
  const originToEdgeProgress = interpolate(frame, [130, 160], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  // CDN response back to Client (CDN -> Client)
  const edgeToClientProgress = interpolate(frame, [170, 200], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  // Request 2 Progress (Client -> CDN second request)
  const req2Progress = interpolate(frame, [220, 245], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  // Instant CDN response on Cache Hit (CDN -> Client)
  const hitToClientProgress = interpolate(frame, [250, 275], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  // ===================================================
  // DYNAMIC COMPONENT TRANSFORMS
  // ===================================================

  // CDN State (changes to show if it is empty, lookup, or cached)
  let cdnState = "EMPTY";
  let cdnBorderColor = "border-slate-800";
  let cdnTextColor = "text-slate-400";
  let cdnGlow = "shadow-none";

  if (frame >= 75 && frame < 170) {
    cdnState = "CACHE MISS";
    cdnBorderColor = "border-amber-500/80";
    cdnTextColor = "text-amber-400";
    cdnGlow = "shadow-[0_0_20px_rgba(245,158,11,0.15)]";
  } else if (frame >= 170 && frame < 246) {
    cdnState = "CACHED (OK)";
    cdnBorderColor = "border-indigo-500/80";
    cdnTextColor = "text-indigo-400";
    cdnGlow = "shadow-[0_0_20px_rgba(99,102,241,0.15)]";
  } else if (frame >= 246) {
    cdnState = "CACHE HIT! (FAST)";
    cdnBorderColor = "border-emerald-500/80";
    cdnTextColor = "text-emerald-400";
    cdnGlow = "shadow-[0_0_20px_rgba(16,185,129,0.25)]";
  }

  // Springs for popup labels
  const label1Spring = spring({ frame: frame - 45, fps, config: { damping: 12 } });
  const label2Spring = spring({ frame: frame - 90, fps, config: { damping: 12 } });
  const label3Spring = spring({ frame: frame - 220, fps, config: { damping: 12 } });

  return (
    <AbsoluteFill className="bg-slate-950 flex flex-col items-center justify-between py-10 font-sans text-white overflow-hidden">

      {/* Play the background music track */}
      {/* Remotion <Html5Audio> handles blending and volume scaling automatically */}
      <Html5Audio src={staticFile("solarflex-hype-background-music-558271.mp3")} volume={0.5} />

      {/* Grid pattern */}
      <div className="absolute inset-0 bg-[linear-gradient(to_right,rgba(255,255,255,0.01)_1px,transparent_1px),linear-gradient(to_bottom,rgba(255,255,255,0.01)_1px,transparent_1px)] bg-[size:40px_40px] pointer-events-none" />

      {/* Header */}
      <div className="z-10 text-center">
        <span className="px-3 py-1 text-xs font-semibold tracking-wider text-purple-400 uppercase bg-purple-950/50 border border-purple-800/40 rounded-full">
          Stage 4: Audio & Timeline Sync
        </span>
        <h1 className="mt-3 text-4xl font-extrabold tracking-tight bg-gradient-to-r from-white via-indigo-200 to-indigo-400 bg-clip-text text-transparent">
          How CDN Caching Works
        </h1>
        <p className="mt-2 text-sm text-slate-400">
          Syncing complex multi-step visualizations to a background audio track
        </p>
      </div>

      {/* Network Canvas */}
      <div className="relative w-[1000px] h-[450px]">
        {/* Connection Cables */}
        <svg className="absolute inset-0 w-full h-full pointer-events-none overflow-visible">
          {/* Client -> CDN */}
          <line x1={150} y1={220} x2={500} y2={220} stroke="#1e293b" strokeWidth={3} />
          {/* CDN -> Origin */}
          <line x1={500} y1={220} x2={850} y2={220} stroke="#1e293b" strokeWidth={3} />
        </svg>

        {/* ===================================================
            PACKET FLOW TRIGGERS
            =================================================== */}
        {/* Packet 1: Client -> CDN (Request 1) */}
        {frame >= 45 && frame <= 75 && (
          <div
            style={{
              position: "absolute",
              left: interpolate(req1Progress, [0, 1], [150, 500]),
              top: 220 - 8,
            }}
            className="w-4 h-4 bg-sky-400 rounded-full shadow-[0_0_10px_#38bdf8] z-30"
          />
        )}

        {/* Packet 2: CDN -> Origin (Cache Miss forward) */}
        {frame >= 90 && frame <= 120 && (
          <div
            style={{
              position: "absolute",
              left: interpolate(edgeToOriginProgress, [0, 1], [500, 850]),
              top: 220 - 8,
            }}
            className="w-4 h-4 bg-amber-400 rounded-full shadow-[0_0_10px_#fbbf24] z-30"
          />
        )}

        {/* Packet 3: Origin -> CDN (Database Response) */}
        {frame >= 130 && frame <= 160 && (
          <div
            style={{
              position: "absolute",
              left: interpolate(originToEdgeProgress, [0, 1], [850, 500]),
              top: 220 - 8,
            }}
            className="w-4 h-4 bg-purple-400 rounded-full shadow-[0_0_10px_#c084fc] z-30"
          />
        )}

        {/* Packet 4: CDN -> Client (Response Client 1) */}
        {frame >= 170 && frame <= 200 && (
          <div
            style={{
              position: "absolute",
              left: interpolate(edgeToClientProgress, [0, 1], [500, 150]),
              top: 220 - 8,
            }}
            className="w-4 h-4 bg-indigo-400 rounded-full shadow-[0_0_10px_#818cf8] z-30"
          />
        )}

        {/* Packet 5: Client -> CDN (Request 2) */}
        {frame >= 220 && frame <= 245 && (
          <div
            style={{
              position: "absolute",
              left: interpolate(req2Progress, [0, 1], [150, 500]),
              top: 220 - 8,
            }}
            className="w-4 h-4 bg-sky-400 rounded-full shadow-[0_0_10px_#38bdf8] z-30"
          />
        )}

        {/* Packet 6: CDN -> Client (Instant Cache Hit response) */}
        {frame >= 250 && frame <= 275 && (
          <div
            style={{
              position: "absolute",
              left: interpolate(hitToClientProgress, [0, 1], [500, 150]),
              top: 220 - 8,
            }}
            className="w-4 h-4 bg-emerald-400 rounded-full shadow-[0_0_10px_#34d399] z-30"
          />
        )}

        {/* ===================================================
            SERVER CARDS
            =================================================== */}
        {/* Client */}
        <div style={{ position: "absolute", left: 50, top: 160 }} className="w-40 h-30 bg-slate-900 border border-slate-800 rounded-2xl p-4 flex flex-col items-center justify-center gap-2 shadow-xl z-20">
          <div className="text-2xl">💻</div>
          <span className="font-bold text-xs">CLIENT</span>
          <span className="font-mono text-[9px] text-slate-500">USER-IP: 89.2.14.9</span>
        </div>

        {/* CDN Cache Node */}
        <div
          style={{ position: "absolute", left: 420, top: 150 }}
          className={`w-44 h-36 bg-slate-900 border rounded-3xl p-4 flex flex-col justify-between shadow-2xl z-20 ${cdnBorderColor} ${cdnGlow}`}
        >
          <div className="flex justify-between items-center">
            <span className="font-bold text-[9px] text-slate-400 uppercase">CDN EDGE</span>
            <div className={`px-2 py-0.5 rounded text-[8px] font-bold font-mono border ${cdnTextColor}`}>
              {cdnState}
            </div>
          </div>
          <div className="flex flex-col items-center gap-1.5">
            <div className="text-3xl">⚡</div>
            <span className="font-bold text-[10px] text-slate-200">EDGE-SERVER-01</span>
          </div>
          <div className="text-center">
            <span className="font-mono text-[9px] text-slate-500">104.16.24.5</span>
          </div>
        </div>

        {/* Origin Database */}
        <div style={{ position: "absolute", left: 800, top: 160 }} className="w-40 h-30 bg-slate-900 border border-slate-800 rounded-2xl p-4 flex flex-col items-center justify-center gap-2 shadow-xl z-20">
          <div className="text-2xl">🗄️</div>
          <span className="font-bold text-xs">ORIGIN SERVER</span>
          <span className="font-mono text-[9px] text-slate-500">DB-IP: 10.0.1.20</span>
        </div>

        {/* ===================================================
            NARRATIVE STAGE OVERLAYS (EXPLAINERS)
            =================================================== */}
        {frame >= 45 && frame < 90 && (
          <div
            style={{
              position: "absolute",
              left: 200,
              top: 320,
              transform: `scale(${label1Spring})`,
            }}
            className="w-[600px] text-center bg-slate-900/90 border border-sky-800/40 rounded-xl p-3 shadow-xl backdrop-blur-md"
          >
            <span className="text-xs text-sky-400 font-bold">STEP 1: INITIAL REQUEST</span>
            <p className="text-xs text-slate-300 mt-1">
              Client requests <code>/assets/profile.jpg</code>. The request hits the nearest CDN Edge server first.
            </p>
          </div>
        )}

        {frame >= 90 && frame < 170 && (
          <div
            style={{
              position: "absolute",
              left: 200,
              top: 320,
              transform: `scale(${label2Spring})`,
            }}
            className="w-[600px] text-center bg-slate-900/90 border border-amber-800/40 rounded-xl p-3 shadow-xl backdrop-blur-md"
          >
            <span className="text-xs text-amber-400 font-bold">STEP 2: CACHE MISS & FORWARD</span>
            <p className="text-xs text-slate-300 mt-1">
              CDN Edge doesn't have the file cached. It forwards the request to the Origin Database to fetch the data.
            </p>
          </div>
        )}

        {frame >= 220 && (
          <div
            style={{
              position: "absolute",
              left: 200,
              top: 320,
              transform: `scale(${label3Spring})`,
            }}
            className="w-[600px] text-center bg-slate-900/90 border border-emerald-800/40 rounded-xl p-3 shadow-xl backdrop-blur-md"
          >
            <span className="text-xs text-emerald-400 font-bold">STEP 3: SECOND REQUEST & CACHE HIT</span>
            <p className="text-xs text-slate-300 mt-1">
              The next client requests the same file. The CDN returns it instantly from its local memory, completely bypassing the origin!
            </p>
          </div>
        )}
      </div>

      {/* Telemetry panel */}
      <div className="z-10 w-[800px] bg-slate-900/60 border border-slate-800 rounded-2xl p-5 backdrop-blur-md shadow-xl font-mono text-xs text-slate-300 flex flex-col gap-3">
        <div className="flex justify-between border-b border-slate-800/60 pb-2 text-[10px] text-slate-500">
          <span>TIMELINE AUDIO & LOGISTICS MATRIX</span>
          <span>Global Frame: {frame} / {durationInFrames}</span>
        </div>
        <div className="grid grid-cols-4 gap-4 text-center text-[10px]">
          <div className="flex flex-col gap-1 border-r border-slate-800/60">
            <span className="text-slate-500">AUDIO VOLUME</span>
            <span className="text-indigo-400 font-bold">8.0%</span>
          </div>
          <div className="flex flex-col gap-1 border-r border-slate-800/60">
            <span className="text-slate-500">REQ 1 LATENCY</span>
            <span className="text-amber-400 font-bold">{frame >= 45 && frame < 200 ? "150ms (SLOW)" : "IDLE"}</span>
          </div>
          <div className="flex flex-col gap-1 border-r border-slate-800/60">
            <span className="text-slate-500">REQ 2 LATENCY</span>
            <span className="text-emerald-400 font-bold">{frame >= 220 ? "10ms (FAST)" : "WAITING"}</span>
          </div>
          <div className="flex flex-col gap-1">
            <span className="text-slate-500">CDN MEMORY</span>
            <span className="text-indigo-400 font-bold">{frame >= 170 ? "1.2 MB (LOADED)" : "0.0 KB (EMPTY)"}</span>
          </div>
        </div>
      </div>
    </AbsoluteFill>
  );
};
