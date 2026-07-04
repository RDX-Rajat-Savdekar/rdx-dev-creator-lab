import React from "react";
import {
  AbsoluteFill,
  Sequence,
  spring,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";

// ===================================================
// CHILD COMPONENT: REPRESENTING A SINGLE NODE CARD
// ===================================================
// Notice how this child component is self-contained. 
// It reads useCurrentFrame() and performs a spring animation.
// Because it is mounted inside a <Sequence>, its useCurrentFrame() 
// will start at 0 at the start of that sequence, regardless of when 
// the sequence itself begins in the parent composition timeline!
const DatabaseNodeItem: React.FC<{
  title: string;
  type: string;
  ip: string;
  badgeColor: string;
  icon: string;
}> = ({ title, type, ip, badgeColor, icon }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Simple clean bounce spring
  const entrySpring = spring({
    frame,
    fps,
    config: {
      stiffness: 120,
      damping: 15,
      mass: 0.9,
    },
  });

  // Calculate slide-in from the left (-80px) and scale up
  const scale = entrySpring;
  const translateX = (1 - entrySpring) * -80;
  const opacity = entrySpring;

  return (
    <div
      style={{
        transform: `translateX(${translateX}px) scale(${scale})`,
        opacity,
      }}
      className="w-[500px] bg-slate-900/70 border border-slate-800 rounded-xl p-4 flex items-center justify-between shadow-lg backdrop-blur-sm"
    >
      <div className="flex items-center gap-4">
        <div className="w-12 h-12 bg-slate-950 border border-slate-850 rounded-lg flex items-center justify-center text-xl">
          {icon}
        </div>
        <div className="flex flex-col">
          <span className="font-bold text-slate-100 text-sm">{title}</span>
          <span className="text-[10px] text-slate-500 font-mono mt-0.5">{ip}</span>
        </div>
      </div>
      <span className={`px-2 py-0.5 rounded text-[9px] font-mono font-semibold border ${badgeColor}`}>
        {type}
      </span>
    </div>
  );
};

export const StaggeredList: React.FC = () => {
  const frame = useCurrentFrame();

  return (
    <AbsoluteFill className="bg-slate-950 flex flex-col items-center justify-between py-12 font-sans text-white overflow-hidden">
      {/* Decorative vertical connection line on the left side of the list */}
      <div className="absolute left-[calc(50%-222px)] top-[230px] bottom-[180px] w-[2px] bg-gradient-to-b from-indigo-500/80 via-purple-500/40 to-transparent pointer-events-none" />

      {/* Header */}
      <div className="z-10 text-center">
        <span className="px-3 py-1 text-xs font-semibold tracking-wider text-purple-400 uppercase bg-purple-950/50 border border-purple-800/40 rounded-full">
          Stage 2: Lab Exercise 2
        </span>
        <h1 className="mt-3 text-4xl font-extrabold tracking-tight bg-gradient-to-r from-white via-purple-200 to-purple-400 bg-clip-text text-transparent">
          Staggered List Entries
        </h1>
        <p className="mt-2 text-sm text-slate-400">
          Mounting reusable components at staggered intervals using <code>&lt;Sequence&gt;</code>
        </p>
      </div>

      {/* The List Container */}
      <div className="z-10 flex flex-col gap-4 my-auto">
        
        {/* Node 1: Enters immediately at frame 15 */}
        {/* The "from" attribute shifts the start time of this Sequence. */}
        <Sequence from={15} layout="none">
          <DatabaseNodeItem
            title="Primary Storage (Leader)"
            type="LEADER"
            ip="10.0.0.1"
            badgeColor="bg-emerald-950/40 text-emerald-400 border-emerald-800/30"
            icon="🗄️"
          />
        </Sequence>

        {/* Node 2: Enters at frame 30 (15 frames delay) */}
        <Sequence from={30} layout="none">
          <DatabaseNodeItem
            title="Replica Server Node A"
            type="REPLICA"
            ip="10.0.0.2"
            badgeColor="bg-sky-950/40 text-sky-400 border-sky-800/30"
            icon="💾"
          />
        </Sequence>

        {/* Node 3: Enters at frame 45 (another 15 frames delay) */}
        <Sequence from={45} layout="none">
          <DatabaseNodeItem
            title="Replica Server Node B"
            type="REPLICA"
            ip="10.0.0.3"
            badgeColor="bg-sky-950/40 text-sky-400 border-sky-800/30"
            icon="💾"
          />
        </Sequence>

      </div>

      {/* Telemetry panel */}
      <div className="z-10 w-[800px] bg-slate-900/60 border border-slate-800 rounded-2xl p-5 backdrop-blur-md shadow-xl font-mono text-xs text-slate-300 flex flex-col gap-3">
        <div className="flex justify-between border-b border-slate-800/60 pb-2 text-[10px] text-slate-500">
          <span>SEQUENCE PLAYHEAD TELEMETRY</span>
          <span>Global Frame: {frame}</span>
        </div>
        <div className="grid grid-cols-3 gap-4 text-center text-[10px]">
          <div className="flex flex-col gap-1 border-r border-slate-800/60">
            <span className="text-slate-500">NODE 1 (FROM f15)</span>
            <span className={frame >= 15 ? "text-emerald-400 font-bold" : "text-slate-600"}>
              {frame >= 15 ? `Local Frame: ${frame - 15}` : "WAITING"}
            </span>
          </div>
          <div className="flex flex-col gap-1 border-r border-slate-800/60">
            <span className="text-slate-500">NODE 2 (FROM f30)</span>
            <span className={frame >= 30 ? "text-sky-400 font-bold" : "text-slate-600"}>
              {frame >= 30 ? `Local Frame: ${frame - 30}` : "WAITING"}
            </span>
          </div>
          <div className="flex flex-col gap-1">
            <span className="text-slate-500">NODE 3 (FROM f45)</span>
            <span className={frame >= 45 ? "text-sky-400 font-bold" : "text-slate-600"}>
              {frame >= 45 ? `Local Frame: ${frame - 45}` : "WAITING"}
            </span>
          </div>
        </div>
      </div>
    </AbsoluteFill>
  );
};
