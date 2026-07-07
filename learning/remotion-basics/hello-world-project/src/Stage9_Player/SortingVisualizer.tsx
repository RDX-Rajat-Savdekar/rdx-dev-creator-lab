import React, { useState, useEffect, useRef, useCallback } from "react";
import { AbsoluteFill, random } from "remotion";
import { Play, Pause, SkipForward, RotateCcw, Shuffle, Sparkles } from "lucide-react";

// ===================================================
// BUBBLE SORT SNAPSHOT STEP BUILDER
// ===================================================
interface SortStep {
  array: number[];
  comparing: [number, number];
  swapping: boolean;
  sorted: boolean;
}

function computeBubbleSortSteps(initialArray: number[]): SortStep[] {
  const steps: SortStep[] = [];
  const arr = [...initialArray];
  
  // Initial state snapshot
  steps.push({
    array: [...arr],
    comparing: [-1, -1],
    swapping: false,
    sorted: false,
  });

  const n = arr.length;
  for (let i = 0; i < n; i++) {
    for (let j = 0; j < n - i - 1; j++) {
      // 1. Snapshot representing Comparison
      steps.push({
        array: [...arr],
        comparing: [j, j + 1],
        swapping: false,
        sorted: false,
      });

      if (arr[j] > arr[j + 1]) {
        // Swap values
        const temp = arr[j];
        arr[j] = arr[j + 1];
        arr[j + 1] = temp;

        // 2. Snapshot representing Swap Event
        steps.push({
          array: [...arr],
          comparing: [j, j + 1],
          swapping: true,
          sorted: false,
        });
      }
    }
  }

  // Final sorted state snapshot
  steps.push({
    array: [...arr],
    comparing: [-1, -1],
    swapping: false,
    sorted: true,
  });

  return steps;
}

const INITIAL_ARRAY = [45, 80, 20, 95, 60, 10, 70, 35, 50, 15, 85, 30];

export const SortingVisualizer: React.FC = () => {
  // ===================================================
  // INTERACTIVE REACT STATES
  // ===================================================
  const [array, setArray] = useState<number[]>(INITIAL_ARRAY);
  const [steps, setSteps] = useState<SortStep[]>(computeBubbleSortSteps(INITIAL_ARRAY));
  const [currentStep, setCurrentStep] = useState<number>(0);
  const [isPlaying, setIsPlaying] = useState<boolean>(false);
  
  const timerRef = useRef<NodeJS.Timeout | null>(null);

  // Re-calculate sorting steps whenever array changes
  const randomizeArray = () => {
    setIsPlaying(false);
    // Use Remotion random() helper with time-seeded keys to bypass lint warnings
    const randomized = Array.from({ length: 12 }, (_, idx) => 
      Math.floor(random(`rand-${idx}-${Date.now()}`) * 85) + 15
    );
    setArray(randomized);
    setSteps(computeBubbleSortSteps(randomized));
    setCurrentStep(0);
  };

  // Step forward index loop
  const stepForward = useCallback(() => {
    setCurrentStep((prev) => {
      if (prev < steps.length - 1) {
        return prev + 1;
      }
      setIsPlaying(false); // Stop auto-play at final index
      return prev;
    });
  }, [steps.length]);

  const resetSort = () => {
    setIsPlaying(false);
    setCurrentStep(0);
  };

  // Auto-play timer effect
  useEffect(() => {
    if (isPlaying) {
      timerRef.current = setInterval(() => {
        stepForward();
      }, 150); // Speed: 150ms per algorithm step
    } else if (timerRef.current) {
      clearInterval(timerRef.current);
    }

    return () => {
      if (timerRef.current) clearInterval(timerRef.current);
    };
  }, [isPlaying, stepForward]);

  // Current visual state
  const activeStep = steps[currentStep] || steps[0];
  const { array: currentArray, comparing, swapping, sorted } = activeStep;

  return (
    <AbsoluteFill className="bg-slate-950 flex flex-col items-center justify-between py-10 font-mono text-white overflow-hidden">
      {/* Background highlighted grid */}
      <div className="absolute inset-0 bg-[linear-gradient(to_right,rgba(255,255,255,0.01)_1px,transparent_1px),linear-gradient(to_bottom,rgba(255,255,255,0.01)_1px,transparent_1px)] bg-[size:50px_50px] pointer-events-none" />

      {/* Header */}
      <div className="z-10 text-center">
        <span className="px-3 py-1 text-xs font-semibold tracking-wider text-emerald-400 uppercase bg-emerald-950/50 border border-emerald-800/40 rounded-full">
          Stage 9: Interactive Player (Stateful Sandbox)
        </span>
        <h1 className="mt-2 text-4xl font-extrabold tracking-tight bg-gradient-to-r from-white via-emerald-200 to-emerald-400 bg-clip-text text-transparent">
          DSA Algorithm: Bubble Sort
        </h1>
        <p className="mt-1 text-xs text-slate-400">
          Stateful visualizer. Click buttons to randomize arrays and step through execution live!
        </p>
      </div>

      {/* Visualizer Chart Stage */}
      <div className="z-10 relative bg-slate-900/40 border border-slate-900 rounded-3xl w-[1000px] h-[400px] flex items-end justify-center gap-4 px-10 pb-12 shadow-2xl backdrop-blur-md">
        
        {/* Render data bars */}
        {currentArray.map((value, idx) => {
          // Highlight colors:
          // Red for swapping, Amber for comparing, Cyan for idle
          const isComparing = comparing.includes(idx);
          const isSwapping = isComparing && swapping;
          
          let barBg = "bg-cyan-500/80 shadow-[0_0_15px_rgba(6,182,212,0.15)]";
          let barBorder = "border-cyan-400/50";
          if (sorted) {
            barBg = "bg-emerald-500/80 shadow-[0_0_20px_rgba(16,185,129,0.2)]";
            barBorder = "border-emerald-400/60";
          } else if (isSwapping) {
            barBg = "bg-red-500 shadow-[0_0_25px_rgba(239,68,68,0.45)]";
            barBorder = "border-red-400";
          } else if (isComparing) {
            barBg = "bg-amber-500 shadow-[0_0_20px_rgba(245,158,11,0.35)]";
            barBorder = "border-amber-400";
          }

          return (
            <div
              key={idx}
              className="flex flex-col items-center gap-2 w-14"
            >
              {/* Value Indicator Label */}
              <span className={`text-[10px] font-bold ${isComparing ? "text-amber-400 scale-110" : "text-slate-500"}`}>
                {value}
              </span>

              {/* Graphical Bar */}
              <div
                style={{
                  height: `${value * 2.8}px`,
                }}
                className={`w-full rounded-lg border ${barBg} ${barBorder} flex items-end justify-center`}
              >
                {/* Visual bar notch slots */}
                <div className="w-[70%] h-0.5 bg-white/20 mb-2 rounded" />
              </div>

              {/* Index indicator */}
              <span className="text-[9px] text-slate-600 font-bold">
                i:{idx}
              </span>
            </div>
          );
        })}
      </div>

      {/* Control Buttons HUD Panel */}
      <div className="z-10 bg-slate-900 border border-slate-800/80 px-8 py-4 rounded-2xl flex items-center gap-10 shadow-xl w-[900px] justify-between">
        
        {/* Telemetry info left */}
        <div className="flex flex-col gap-1 w-44">
          <span className="text-[10px] text-slate-500 uppercase tracking-widest">ALGORITHM PROGRESS</span>
          <span className="text-sm font-bold text-slate-200">
            Step {currentStep} / {steps.length - 1}
          </span>
          <span className="text-[8px] text-slate-600">Array Size: {array.length}</span>
        </div>

        {/* Buttons Controls */}
        <div className="flex items-center gap-4">
          {/* Randomize button */}
          <button
            onClick={randomizeArray}
            className="p-3 bg-slate-800 hover:bg-slate-700 active:bg-slate-600 border border-slate-700/60 rounded-xl hover:scale-105 active:scale-95 text-slate-300"
            title="Randomize Array"
          >
            <Shuffle className="w-5 h-5" />
          </button>

          {/* Reset button */}
          <button
            onClick={resetSort}
            className="p-3 bg-slate-800 hover:bg-slate-700 active:bg-slate-600 border border-slate-700/60 rounded-xl hover:scale-105 active:scale-95 text-slate-300"
            title="Reset Sorting"
          >
            <RotateCcw className="w-5 h-5" />
          </button>

          {/* Play / Pause Toggle */}
          <button
            onClick={() => setIsPlaying(!isPlaying)}
            style={{
              backgroundColor: isPlaying ? "#ef4444" : "#10b981",
              borderColor: isPlaying ? "#f87171" : "#34d399",
            }}
            className="p-4 rounded-2xl border text-slate-950 font-extrabold hover:scale-105 active:scale-95 flex items-center justify-center"
          >
            {isPlaying ? (
              <Pause className="w-6 h-6 text-white" />
            ) : (
              <Play className="w-6 h-6 text-slate-950 fill-current" />
            )}
          </button>

          {/* Step Forward next button */}
          <button
            disabled={isPlaying || currentStep >= steps.length - 1}
            onClick={stepForward}
            className="p-3 bg-slate-800 hover:bg-slate-700 active:bg-slate-600 border border-slate-700/60 rounded-xl hover:scale-105 active:scale-95 text-slate-300 disabled:opacity-30 disabled:scale-100 disabled:pointer-events-none"
            title="Step Next Swap"
          >
            <SkipForward className="w-5 h-5" />
          </button>
        </div>

        {/* Telemetry info right */}
        <div className="flex flex-col gap-1 text-right w-44">
          <span className="text-[10px] text-slate-500 uppercase tracking-widest">STATUS</span>
          <span className="text-xs font-black flex items-center justify-end gap-1 text-emerald-400 uppercase">
            {sorted ? (
              <>
                <Sparkles className="w-3.5 h-3.5" /> SORT COMPLETE
              </>
            ) : isPlaying ? (
              <span className="text-yellow-400 animate-pulse">AUTO SORTING...</span>
            ) : (
              <span className="text-slate-400">READY TO STEP</span>
            )}
          </span>
        </div>

      </div>
    </AbsoluteFill>
  );
};
