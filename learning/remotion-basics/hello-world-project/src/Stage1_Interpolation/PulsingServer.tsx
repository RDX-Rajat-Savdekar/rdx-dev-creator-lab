import React from "react";
import {
  AbsoluteFill,
  interpolate,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";

export const PulsingServer: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();

  // Pulse timing: complete one heartbeat every 1.5 seconds
  const pulseDurationSeconds = 0.5;
  const pulseFrames = pulseDurationSeconds * fps;
  const pulseRadian = (frame / pulseFrames) * 2 * Math.PI;

  // Math.sin oscillates between -1 and 1. 
  // Let's shift it to oscillate between 0 and 1:
  const sinValue = Math.sin(pulseRadian);
  const normalizedPulse = (sinValue + 1) / 2;

  // Let's interpolate this normalized pulse to drive style attributes:
  // 1. Glow opacity: from 0.3 (dim state) to 1.0 (peak pulse state)
  const glowOpacity = interpolate(normalizedPulse, [0, 1], [0.25, 0.95]);

  // 2. Glow shadow spread radius: from 10px to 45px
  const shadowSpread = interpolate(normalizedPulse, [0, 1], [15, 55]);

  // 3. Heartbeat scale: slightly scale up the server box on heartbeat peak (from 1.0 to 1.04)
  const scale = interpolate(normalizedPulse, [0, 1], [1, 1.04]);

  // Blinking lights: blink small LEDs on the server console using frame math
  const blinkActive1 = Math.floor(frame / 6) % 2 === 0;
  const blinkActive2 = Math.floor(frame / 15) % 2 === 0;
  const blinkActive3 = Math.floor(frame / 9) % 3 !== 0;

  return (
    <AbsoluteFill className="bg-slate-950 flex flex-col items-center justify-between py-10 font-sans text-white overflow-hidden">
      {/* Network circuit background */}
      <div className="absolute inset-0 bg-[linear-gradient(to_right,rgba(16,185,129,0.03)_1px,transparent_1px),linear-gradient(to_bottom,rgba(16,185,129,0.03)_1px,transparent_1px)] bg-[size:30px_30px] pointer-events-none" />
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,rgba(16,185,129,0.05),transparent_70%)] pointer-events-none" />

      {/* Header */}
      <div className="z-10 text-center">
        <span className="px-3 py-1 text-xs font-semibold tracking-wider text-emerald-400 uppercase bg-emerald-950/50 border border-emerald-800/40 rounded-full">
          Stage 1: Mini Project 1
        </span>
        <h1 className="mt-3 text-4xl font-extrabold tracking-tight bg-gradient-to-r from-white via-emerald-200 to-emerald-400 bg-clip-text text-transparent">
          The Pulsing Server Node
        </h1>
        <p className="mt-2 text-sm text-slate-400">
          Simulating server heartbeat & health using continuous trigonometric interpolation
        </p>
      </div>

      {/* Main Server Scene */}
      <div className="relative flex items-center justify-center w-full h-[360px]">
        {/* Connection cables behind the server */}
        <div className="absolute w-[2px] h-[360px] bg-slate-900 border-dashed border-r border-slate-800/50" />
        <div className="absolute h-[2px] w-[500px] bg-slate-900 border-dashed border-b border-slate-800/50" />

        {/* Server Box */}
        <div
          style={{
            transform: `scale(${scale})`,
            boxShadow: `0 0 ${shadowSpread}px rgba(16, 185, 129, ${glowOpacity})`,
            borderColor: `rgba(16, 185, 129, ${glowOpacity})`,
          }}
          className="z-10 w-[420px] bg-slate-900/90 rounded-2xl border p-6 flex flex-col gap-5 shadow-2xl"
        >
          {/* Server Top Panel */}
          <div className="flex justify-between items-center border-b border-slate-800 pb-3">
            <div className="flex items-center gap-2">
              <div className="w-3 h-3 bg-emerald-500 rounded-full shadow-[0_0_8px_#10b981]" />
              <span className="font-bold text-sm tracking-wide text-slate-200">DB-NODE-PRIMARY</span>
            </div>
            <span className="text-[10px] bg-slate-850 px-2 py-0.5 rounded text-emerald-400 border border-emerald-500/20 font-mono">
              STATUS: HEALTHY
            </span>
          </div>

          {/* Server Body & Storage Bays */}
          <div className="flex flex-col gap-3">
            {/* Bay 1 */}
            <div className="h-10 bg-slate-950/60 rounded border border-slate-800/50 px-3 flex items-center justify-between">
              <div className="flex items-center gap-2.5">
                <div className="w-5 h-2.5 bg-slate-800 rounded-sm relative overflow-hidden">
                  <div className="absolute left-0 top-0 bottom-0 bg-emerald-500" style={{ width: '85%' }} />
                </div>
                <span className="text-[10px] text-slate-400 font-mono">BAY 01 [SSD]</span>
              </div>
              <div className="flex gap-1.5">
                <div className={`w-1.5 h-1.5 rounded-full ${blinkActive1 ? "bg-emerald-400 shadow-[0_0_4px_#34d399]" : "bg-emerald-950"}`} />
                <div className="w-1.5 h-1.5 rounded-full bg-slate-800" />
              </div>
            </div>

            {/* Bay 2 */}
            <div className="h-10 bg-slate-950/60 rounded border border-slate-800/50 px-3 flex items-center justify-between">
              <div className="flex items-center gap-2.5">
                <div className="w-5 h-2.5 bg-slate-800 rounded-sm relative overflow-hidden">
                  <div className="absolute left-0 top-0 bottom-0 bg-emerald-500" style={{ width: '42%' }} />
                </div>
                <span className="text-[10px] text-slate-400 font-mono">BAY 02 [SSD]</span>
              </div>
              <div className="flex gap-1.5">
                <div className={`w-1.5 h-1.5 rounded-full ${blinkActive2 ? "bg-emerald-400 shadow-[0_0_4px_#34d399]" : "bg-emerald-950"}`} />
                <div className={`w-1.5 h-1.5 rounded-full ${blinkActive3 ? "bg-amber-400 shadow-[0_0_4px_#fbbf24]" : "bg-amber-950"}`} />
              </div>
            </div>
          </div>

          {/* Console Output Screen */}
          <div className="bg-slate-950 rounded-lg p-3 font-mono text-[10px] text-emerald-400/90 h-[72px] border border-slate-850 flex flex-col gap-1 overflow-hidden select-none">
            <div className="flex justify-between">
              <span>$ monitoring-agent --check</span>
              <span className="text-slate-600">t={frame}f</span>
            </div>
            <div className="text-slate-400">&gt; ping response: 0.12ms (OK)</div>
            <div className="text-emerald-500/60">&gt; heartbeat frequency: {pulseDurationSeconds}s ({(fps / pulseFrames).toFixed(2)}Hz)</div>
          </div>
        </div>
      </div>

      {/* Telemetry Panel */}
      <div className="z-10 w-[800px] bg-slate-900/60 border border-slate-800 rounded-2xl p-6 backdrop-blur-md shadow-xl font-mono text-xs text-slate-300 flex flex-col gap-4">
        <div className="flex justify-between border-b border-slate-800/60 pb-2 text-[10px] text-slate-500">
          <span>MATHEMATICAL PULSE MODEL</span>
          <span className="text-emerald-400">f(t) = (sin( (t / {pulseFrames}) * 2π ) + 1) / 2</span>
        </div>

        <div className="grid grid-cols-4 gap-4 text-center">
          <div className="flex flex-col gap-1 border-r border-slate-800/60">
            <span className="text-slate-500 text-[10px]">CURRENT FRAME</span>
            <span className="text-base font-semibold text-white">
              {frame} <span className="text-[10px] text-slate-500">/ {durationInFrames}</span>
            </span>
          </div>

          <div className="flex flex-col gap-1 border-r border-slate-800/60">
            <span className="text-slate-500 text-[10px]">RADIAN ANGLE</span>
            <span className="text-base font-semibold text-sky-400">
              {pulseRadian.toFixed(2)} rad
            </span>
          </div>

          <div className="flex flex-col gap-1 border-r border-slate-800/60">
            <span className="text-slate-500 text-[10px]">PULSE RATIO</span>
            <span className="text-base font-semibold text-emerald-400">
              {(normalizedPulse * 100).toFixed(1)}%
            </span>
            <div className="w-16 h-1 bg-slate-950 mx-auto rounded-full overflow-hidden mt-1">
              <div
                className="h-full bg-emerald-500"
                style={{ width: `${normalizedPulse * 100}%` }}
              />
            </div>
          </div>

          <div className="flex flex-col gap-1">
            <span className="text-slate-500 text-[10px]">GLOW RADIUS</span>
            <span className="text-base font-semibold text-teal-400" >
              {shadowSpread.toFixed(1)}px
            </span>
          </div>
        </div>
      </div>
    </AbsoluteFill>
  );
};
