import React, { useState } from 'react';
import type { Structured2DGeometry } from '../types/floorplan';
import { Copy, Check, Download, Layers, Home, Grid, DoorClosed } from 'lucide-react';

interface Props {
  geometry: Structured2DGeometry;
}

export const GeometryJsonViewer: React.FC<Props> = ({ geometry }) => {
  const [copied, setCopied] = useState(false);

  const jsonString = JSON.stringify(geometry, null, 2);

  const handleCopy = () => {
    navigator.clipboard.writeText(jsonString);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleDownload = () => {
    const blob = new Blob([jsonString], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `floorplan-geometry-${Date.now()}.json`;
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="flex flex-col gap-4">
      {/* Metrics Summary Grid */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-3 flex items-center gap-3">
          <div className="p-2.5 rounded-lg bg-indigo-500/10 text-indigo-400">
            <Home className="w-5 h-5" />
          </div>
          <div>
            <div className="text-xl font-bold text-slate-100">{geometry.rooms?.length || 0}</div>
            <div className="text-xs text-slate-400">Rooms Identified</div>
          </div>
        </div>

        <div className="bg-slate-900 border border-slate-800 rounded-xl p-3 flex items-center gap-3">
          <div className="p-2.5 rounded-lg bg-emerald-500/10 text-emerald-400">
            <Grid className="w-5 h-5" />
          </div>
          <div>
            <div className="text-xl font-bold text-slate-100">{geometry.walls?.length || 0}</div>
            <div className="text-xs text-slate-400">Wall Segments</div>
          </div>
        </div>

        <div className="bg-slate-900 border border-slate-800 rounded-xl p-3 flex items-center gap-3">
          <div className="p-2.5 rounded-lg bg-amber-500/10 text-amber-400">
            <DoorClosed className="w-5 h-5" />
          </div>
          <div>
            <div className="text-xl font-bold text-slate-100">{geometry.doors?.length || 0}</div>
            <div className="text-xs text-slate-400">Doors Mapped</div>
          </div>
        </div>

        <div className="bg-slate-900 border border-slate-800 rounded-xl p-3 flex items-center gap-3">
          <div className="p-2.5 rounded-lg bg-sky-500/10 text-sky-400">
            <Layers className="w-5 h-5" />
          </div>
          <div>
            <div className="text-xl font-bold text-slate-100">{geometry.windows?.length || 0}</div>
            <div className="text-xs text-slate-400">Windows Mapped</div>
          </div>
        </div>
      </div>

      {/* JSON Code Viewer */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden shadow-xl">
        <div className="flex items-center justify-between px-4 py-2.5 bg-slate-950 border-b border-slate-800">
          <span className="text-xs font-mono text-slate-400">structured_2d_geometry.json</span>
          <div className="flex items-center gap-2">
            <button
              onClick={handleCopy}
              className="text-xs flex items-center gap-1.5 px-2.5 py-1 rounded bg-slate-800 hover:bg-slate-700 text-slate-200 transition-colors"
            >
              {copied ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
              <span>{copied ? 'Copied' : 'Copy JSON'}</span>
            </button>
            <button
              onClick={handleDownload}
              className="text-xs flex items-center gap-1.5 px-2.5 py-1 rounded bg-slate-800 hover:bg-slate-700 text-slate-200 transition-colors"
            >
              <Download className="w-3.5 h-3.5" />
              <span>Download</span>
            </button>
          </div>
        </div>
        <pre className="p-4 text-xs font-mono text-slate-300 overflow-x-auto max-h-[500px] leading-relaxed bg-[#0a0f1d]">
          {jsonString}
        </pre>
      </div>
    </div>
  );
};

