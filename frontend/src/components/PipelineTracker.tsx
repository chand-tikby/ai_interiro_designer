import React from 'react';
import type { PipelineStage } from '../types/floorplan';
import { 
  Upload, 
  Server, 
  Cpu, 
  FileCode2, 
  Scan, 
  Sparkles, 
  Layers, 
  CheckCircle2, 
  Clock, 
  AlertCircle 
} from 'lucide-react';

interface Props {
  stages: PipelineStage[];
}

const STEP_ICONS = [
  Upload,      // 1. Upload
  Server,      // 2. Node.js
  Cpu,         // 3. FastAPI
  FileCode2,   // 4. PyMuPDF
  Scan,        // 5. OpenCV
  Sparkles,    // 6. Gemini
  Layers,      // 7. 2D Geometry
];

export const PipelineTracker: React.FC<Props> = ({ stages }) => {
  return (
    <div className="bg-slate-900/80 border border-slate-800 rounded-xl p-5 shadow-lg backdrop-blur">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-base font-semibold text-slate-200 flex items-center gap-2">
          <Layers className="w-5 h-5 text-indigo-400" />
          7-Step Architecture Pipeline
        </h3>
        <span className="text-xs text-slate-400 bg-slate-800 px-2.5 py-1 rounded-full border border-slate-700">
          PyMuPDF • OpenCV • Gemini 2.5
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-7 gap-3">
        {stages.map((stage, idx) => {
          const Icon = STEP_ICONS[idx] || Layers;
          const isCompleted = stage.status === 'completed';
          const isInProgress = stage.status === 'in_progress';
          const isFailed = stage.status === 'failed';

          return (
            <div
              key={stage.step}
              className={`flex flex-col p-3 rounded-lg border transition-all ${
                isCompleted
                  ? 'bg-emerald-950/20 border-emerald-500/30 text-emerald-300'
                  : isInProgress
                  ? 'bg-indigo-950/30 border-indigo-500/50 text-indigo-300 animate-pulse'
                  : isFailed
                  ? 'bg-rose-950/20 border-rose-500/30 text-rose-300'
                  : 'bg-slate-800/40 border-slate-800 text-slate-400'
              }`}
            >
              <div className="flex items-center justify-between mb-2">
                <span className="text-xs font-mono font-bold px-1.5 py-0.5 rounded bg-slate-800/80 text-slate-300">
                  #{stage.step}
                </span>
                {isCompleted && <CheckCircle2 className="w-4 h-4 text-emerald-400" />}
                {isInProgress && <Clock className="w-4 h-4 text-indigo-400 animate-spin" />}
                {isFailed && <AlertCircle className="w-4 h-4 text-rose-400" />}
              </div>

              <div className="flex items-center gap-1.5 mb-1">
                <Icon className="w-4 h-4 shrink-0" />
                <span className="text-xs font-medium truncate">{stage.name}</span>
              </div>

              {stage.details && (
                <p className="text-[11px] text-slate-400 mt-auto line-clamp-2 leading-relaxed">
                  {stage.details}
                </p>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
};

