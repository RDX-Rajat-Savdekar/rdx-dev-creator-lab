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
// ZOD SCHEMA DEFINITION
// ===================================================
export const systemDashboardSchema = z.object({
  chartLabel: z.string().default("API GATEWAY (US-EAST)").describe("Title of the monitoring graph"),
  chartGlowColor: zColor().default("#06b6d4").describe("Accent glow color of the metric line"),
  alertThreshold: z.number().min(80).max(220).step(5).default(140).describe("Latency value (ms) above which warnings trigger"),
  showGridLines: z.boolean().default(true).describe("Show/hide background telemetry grids"),
});

type DashboardProps = z.infer<typeof systemDashboardSchema>;

// Pre-defined server latency dataset (simulating spikes and recovery)
const LATENCY_DATASET = [
  82, 85, 90, 88, 84, 80, 85, 92, 94, 91, 86, 83, 85, 89, 90, 92, 95, 93, 89, 84,
  82, 85, 91, 98, 102, 105, 101, 95, 90, 87, 85, 88, 93, 110, 118, 125, 121, 115, 108, 98,
  90, 85, 87, 89, 92, 95, 102, 118, 132, 145, 158, 172, 185, 178, 162, 148, 135, 120, 105, 92,
  88, 86, 84, 89, 95, 100, 105, 112, 108, 96, 88, 85, 83, 86, 92, 98, 105, 110, 105, 94,
  89, 87, 85, 88, 93, 100, 108, 115, 111, 98, 90, 86, 85, 90, 96, 104, 112, 125, 138, 155,
  175, 192, 210, 205, 188, 170, 152, 130, 115, 98, 90, 87, 84, 86, 91, 95, 92, 88, 84, 82,
];

export const SystemDashboard: React.FC<DashboardProps> = ({
  chartLabel,
  chartGlowColor,
  alertThreshold,
  showGridLines,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Graph Canvas Dimensions
  const canvasWidth = 1200;
  const canvasHeight = 450;
  const padding = 50;

  // 1. Calculate how many points are currently visible based on timeline progress
  // We scan the data across the first 140 frames of the composition.
  const revealedCount = Math.floor(
    interpolate(frame, [10, 140], [1, LATENCY_DATASET.length], {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
    })
  );

  // Slice the dataset to reveal only the current coordinates
  const visibleData = LATENCY_DATASET.slice(0, revealedCount);
  const currentVal = visibleData[visibleData.length - 1] || 80;

  // Dynamic Telemetry Calculations based on visible subset
  const maxValSoFar = visibleData.length > 0 ? Math.max(...visibleData) : 80;
  const minValSoFar = visibleData.length > 0 ? Math.min(...visibleData) : 80;
  const avgValSoFar =
    visibleData.length > 0
      ? Math.round(visibleData.reduce((a, b) => a + b, 0) / visibleData.length)
      : 80;

  // Alert State: If current latency exceeds user parameter trigger threshold
  const isTriggered = currentVal > alertThreshold;
  const warningOpacity = interpolate(isTriggered ? Math.sin(frame * 0.4) : 0, [-1, 1], [0.1, 0.45]);
  const activeColor = isTriggered ? "#ef4444" : chartGlowColor;

  // Max value in dataset for mapping range (highest coordinate height)
  const maxRange = 240; 

  // ===================================================
  // COORDINATE MAPPING FUNCTIONS
  // ===================================================
  const getX = (index: number) => {
    return padding + (index / (LATENCY_DATASET.length - 1)) * (canvasWidth - 2 * padding);
  };

  const getY = (value: number) => {
    // Math logic: higher values yield lower Y pixels (SVG 0,0 is top-left)
    return canvasHeight - padding - (value / maxRange) * (canvasHeight - 2 * padding);
  };

  // ===================================================
  // PATH STRING BUILDERS
  // ===================================================
  
  // 1. Line Path: "M x0 y0 L x1 y1 ..."
  let linePath = "";
  visibleData.forEach((val, idx) => {
    const prefix = idx === 0 ? "M" : "L";
    linePath += ` ${prefix} ${getX(idx).toFixed(1)} ${getY(val).toFixed(1)}`;
  });

  // 2. Closed Area Path (creates gradient fill beneath the line)
  let areaPath = "";
  if (visibleData.length > 0) {
    const startX = getX(0).toFixed(1);
    const bottomY = (canvasHeight - padding).toFixed(1);
    const lastX = getX(visibleData.length - 1).toFixed(1);

    areaPath = `M ${startX} ${bottomY} L ${startX} ${getY(visibleData[0]).toFixed(1)} ${linePath.substring(linePath.indexOf("L"))} L ${lastX} ${bottomY} Z`;
  }

  // Latest coordinates for the tracking scan indicator
  const currentX = getX(visibleData.length - 1);
  const currentY = getY(currentVal);

  // Springs for warning banners
  const warningSpring = spring({
    frame: isTriggered ? frame - LATENCY_DATASET.findIndex((v) => v > alertThreshold) : 0,
    fps,
    config: { stiffness: 100 },
  });

  return (
    <AbsoluteFill className="bg-slate-950 flex flex-col items-center justify-between py-10 font-mono text-white overflow-hidden">
      {/* Background Alert Overlay */}
      {isTriggered && (
        <div 
          style={{ opacity: warningOpacity }}
          className="absolute inset-0 bg-red-950/60 pointer-events-none z-0"
        />
      )}

      {/* Grid Matrix Background */}
      <div className="absolute inset-0 bg-[linear-gradient(to_right,rgba(255,255,255,0.015)_1px,transparent_1px),linear-gradient(to_bottom,rgba(255,255,255,0.015)_1px,transparent_1px)] bg-[size:50px_50px] pointer-events-none" />

      {/* Dashboard Header */}
      <div className="z-10 w-[1200px] flex justify-between items-end border-b border-slate-800 pb-4">
        <div>
          <div className="flex items-center gap-2">
            <span className={`w-3 h-3 rounded-full ${isTriggered ? "bg-red-500 animate-pulse" : "bg-emerald-500"}`} />
            <span className="text-xs text-slate-500 font-bold uppercase tracking-widest">SYSTEM MONITOR</span>
          </div>
          <h1 className="mt-1 text-3xl font-black text-slate-100 tracking-tight">
            {chartLabel}
          </h1>
        </div>
        <div className="text-right">
          <span className="text-xs text-slate-500 block">SYSTEM STATUS</span>
          <span className={`text-sm font-bold ${isTriggered ? "text-red-400" : "text-emerald-400"}`}>
            {isTriggered ? "WARNING: LATENCY CRITICAL" : "OPERATIONAL / OPTIMIZED"}
          </span>
        </div>
      </div>

      {/* Main Metric Cards Panel */}
      <div className="z-10 w-[1200px] grid grid-cols-4 gap-6">
        {/* Card 1: Live Value */}
        <div className={`bg-slate-900/60 border ${isTriggered ? "border-red-900/40" : "border-slate-800/60"} p-5 rounded-2xl backdrop-blur-md`}>
          <span className="text-xs text-slate-500 block">LIVE LATENCY</span>
          <div className="mt-2 flex items-baseline gap-1">
            <span className={`text-4xl font-extrabold ${isTriggered ? "text-red-400" : "text-slate-100"}`}>
              {currentVal}
            </span>
            <span className="text-xs text-slate-500">ms</span>
          </div>
        </div>

        {/* Card 2: Peak */}
        <div className="bg-slate-900/60 border border-slate-800/60 p-5 rounded-2xl backdrop-blur-md">
          <span className="text-xs text-slate-500 block">PEAK METRIC</span>
          <div className="mt-2 flex items-baseline gap-1">
            <span className="text-4xl font-extrabold text-slate-100">
              {maxValSoFar}
            </span>
            <span className="text-xs text-slate-500">ms</span>
          </div>
        </div>

        {/* Card 3: Minimum */}
        <div className="bg-slate-900/60 border border-slate-800/60 p-5 rounded-2xl backdrop-blur-md">
          <span className="text-xs text-slate-500 block">MINIMUM METRIC</span>
          <div className="mt-2 flex items-baseline gap-1">
            <span className="text-4xl font-extrabold text-slate-100">
              {minValSoFar}
            </span>
            <span className="text-xs text-slate-500">ms</span>
          </div>
        </div>

        {/* Card 4: Average */}
        <div className="bg-slate-900/60 border border-slate-800/60 p-5 rounded-2xl backdrop-blur-md">
          <span className="text-xs text-slate-500 block">AVERAGE</span>
          <div className="mt-2 flex items-baseline gap-1">
            <span className="text-4xl font-extrabold text-slate-100">
              {avgValSoFar}
            </span>
            <span className="text-xs text-slate-500">ms</span>
          </div>
        </div>
      </div>

      {/* Dynamic Graph Chart Stage */}
      <div className="z-10 relative bg-slate-950/40 border border-slate-900/80 rounded-2xl w-[1200px] h-[450px] overflow-hidden flex items-center justify-center shadow-inner">
        <svg
          width={canvasWidth}
          height={canvasHeight}
          viewBox={`0 0 ${canvasWidth} ${canvasHeight}`}
          className="overflow-visible"
        >
          <defs>
            {/* Area fill gradient definition */}
            <linearGradient id="chart-glow-grad" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stopColor={activeColor} stopOpacity={0.25} />
              <stop offset="100%" stopColor={activeColor} stopOpacity={0.0} />
            </linearGradient>
          </defs>

          {/* Guidelines Grid */}
          {showGridLines && (
            <g opacity="0.15">
              {/* Horizontal thresholds */}
              <line x1={padding} y1={getY(80)} x2={canvasWidth - padding} y2={getY(80)} stroke="#fff" strokeWidth="1" strokeDasharray="4 4" />
              <line x1={padding} y1={getY(140)} x2={canvasWidth - padding} y2={getY(140)} stroke="#fff" strokeWidth="1" strokeDasharray="4 4" />
              <line x1={padding} y1={getY(200)} x2={canvasWidth - padding} y2={getY(200)} stroke="#fff" strokeWidth="1" strokeDasharray="4 4" />
            </g>
          )}

          {/* Trigger Alert threshold boundary marker */}
          <g>
            <line
              x1={padding}
              y1={getY(alertThreshold)}
              x2={canvasWidth - padding}
              y2={getY(alertThreshold)}
              stroke="#f43f5e"
              strokeWidth="1.5"
              strokeDasharray="6 3"
              opacity="0.35"
            />
            <text
              x={canvasWidth - padding + 5}
              y={getY(alertThreshold) + 4}
              fill="#f43f5e"
              fontSize="9"
              opacity="0.6"
            >
              LIMIT: {alertThreshold}ms
            </text>
          </g>

          {/* 1. Draw Area Fill Under the Graph Line */}
          {areaPath && (
            <path
              d={areaPath}
              fill="url(#chart-glow-grad)"
            />
          )}

          {/* 2. Draw the main data line */}
          {linePath && (
            <path
              d={linePath}
              fill="none"
              stroke={activeColor}
              strokeWidth="3.5"
              strokeLinecap="round"
              strokeLinejoin="round"
              style={{
                filter: `drop-shadow(0 0 6px ${activeColor})`
              }}
            />
          )}

          {/* 3. The Scanning Laser Head & indicator dot */}
          {visibleData.length > 0 && (
            <g>
              {/* Vertical alignment line */}
              <line
                x1={currentX}
                y1={padding}
                x2={currentX}
                y2={canvasHeight - padding}
                stroke={activeColor}
                strokeWidth="1.5"
                opacity="0.4"
                strokeDasharray="2 2"
              />

              {/* Outer pulsing ring */}
              <circle
                cx={currentX}
                cy={currentY}
                r="9"
                fill="none"
                stroke={activeColor}
                strokeWidth="1.5"
                opacity={0.4 + Math.sin(frame * 0.25) * 0.3}
              />

              {/* Inner solid tracking core */}
              <circle
                cx={currentX}
                cy={currentY}
                r="4.5"
                fill={activeColor}
                style={{
                  filter: `drop-shadow(0 0 4px ${activeColor})`
                }}
              />
            </g>
          )}
        </svg>

        {/* Warning Indicator overlay banner */}
        {isTriggered && (
          <div 
            style={{
              position: "absolute",
              top: 20,
              right: 20,
              opacity: warningSpring,
              transform: `scale(${warningSpring})`,
            }}
            className="px-4 py-2 border border-red-500 bg-red-950/80 text-red-400 font-extrabold text-[10px] rounded-lg shadow-xl animate-pulse"
          >
            CRITICAL LATENCY DETECTED
          </div>
        )}
      </div>

      {/* Telemetry Footer Metadata */}
      <div className="z-10 w-[1200px] flex justify-between text-[10px] text-slate-600 border-t border-slate-900 pt-4">
        <span>SAMPLING FREQ: 30HZ</span>
        <span>BUFFER: {visibleData.length} SECS</span>
        <span>METRIC PATH: US-EAST.API-GW.PROD</span>
      </div>
    </AbsoluteFill>
  );
};
