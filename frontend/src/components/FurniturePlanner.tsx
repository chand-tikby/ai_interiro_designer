import React, { useState, useMemo, useCallback, useEffect } from 'react';
import type { Structured2DGeometry } from '../types/floorplan';
import {
  FURNITURE_CATALOG,
  CATEGORY_META,
  getAISuggestionsForRoom,
} from '../types/furniture';
import type {
  FurnitureSpec,
  PlacedFurniture,
  FurnitureCategory,
} from '../types/furniture';
import { FloorplanViewer3D } from './FloorplanViewer3D';
import {
  Trash2,
  RotateCcw,
  RotateCw,
  Sparkles,
  MousePointer2,
  Package,
  CheckCircle2,
  X,
  Copy,
} from 'lucide-react';

interface Props {
  geometry: Structured2DGeometry;
}

const CATEGORY_COLORS: Record<FurnitureCategory, string> = {
  living:   'bg-indigo-600 hover:bg-indigo-500 border-indigo-400',
  bedroom:  'bg-purple-600 hover:bg-purple-500 border-purple-400',
  dining:   'bg-amber-600 hover:bg-amber-500 border-amber-400',
  kitchen:  'bg-orange-600 hover:bg-orange-500 border-orange-400',
  bathroom: 'bg-sky-600 hover:bg-sky-500 border-sky-400',
  storage:  'bg-slate-600 hover:bg-slate-500 border-slate-400',
  lighting: 'bg-yellow-600 hover:bg-yellow-500 border-yellow-400',
  outdoor:  'bg-green-600 hover:bg-green-500 border-green-400',
};

// CAT_BADGE reserved for future badge styling

export const FurniturePlanner: React.FC<Props> = ({ geometry }) => {
  const { rooms = [] } = geometry;

  // ── State ───────────────────────────────────────────────────────────────────
  const [activeCategory, setActiveCategory] = useState<FurnitureCategory | 'all' | 'ai'>('ai');
  const [selectedRoomForAI, setSelectedRoomForAI] = useState<string>(rooms[0]?.id || '');
  const [pendingFurniture, setPendingFurniture] = useState<{ spec: FurnitureSpec } | null>(null);
  const [placedFurniture, setPlacedFurniture] = useState<PlacedFurniture[]>([]);
  const [selectedUid, setSelectedUid] = useState<string | null>(null);

  // ── AI Suggestions ──────────────────────────────────────────────────────────
  const aiSuggestions = useMemo(() => {
    const room = rooms.find((r) => r.id === selectedRoomForAI);
    if (!room) return FURNITURE_CATALOG.slice(0, 8);
    return getAISuggestionsForRoom(room.name);
  }, [rooms, selectedRoomForAI]);

  // ── Catalog Items to show ───────────────────────────────────────────────────
  const visibleItems = useMemo(() => {
    if (activeCategory === 'ai') return aiSuggestions;
    if (activeCategory === 'all') return FURNITURE_CATALOG;
    return FURNITURE_CATALOG.filter((f) => f.category === activeCategory);
  }, [activeCategory, aiSuggestions]);

  // ── Handlers ────────────────────────────────────────────────────────────────
  const handleSelectSpec = useCallback((spec: FurnitureSpec) => {
    setPendingFurniture({ spec });
    setSelectedUid(null);
  }, []);

  const handleFurniturePlaced = useCallback((pf: PlacedFurniture) => {
    setPlacedFurniture((prev) => [...prev, pf]);
    // Keep pending so user can drop multiple copies; press Escape or X to cancel
  }, []);

  const handleDelete = useCallback(() => {
    if (!selectedUid) return;
    setPlacedFurniture((prev) => prev.filter((p) => p.uid !== selectedUid));
    setSelectedUid(null);
  }, [selectedUid]);

  const handleRotate = useCallback((delta: number) => {
    if (!selectedUid) return;
    setPlacedFurniture((prev) =>
      prev.map((p) =>
        p.uid === selectedUid ? { ...p, rotationY: p.rotationY + delta } : p
      )
    );
  }, [selectedUid]);

  const handleDuplicate = useCallback(() => {
    if (!selectedUid) return;
    const src = placedFurniture.find((p) => p.uid === selectedUid);
    if (!src) return;
    const newPf: PlacedFurniture = {
      ...src,
      uid: `pf-dup-${Date.now()}`,
      x: src.x + 0.5,
      z: src.z + 0.5,
    };
    setPlacedFurniture((prev) => [...prev, newPf]);
    setSelectedUid(newPf.uid);
  }, [selectedUid, placedFurniture]);

  const handleCancelPlacement = useCallback(() => {
    setPendingFurniture(null);
    setSelectedUid(null);
  }, []);

  useEffect(() => {
    const handler = (e: KeyboardEvent) => {
      if (e.key === 'Escape') {
        handleCancelPlacement();
      }
    };
    window.addEventListener('keydown', handler);
    return () => window.removeEventListener('keydown', handler);
  }, [handleCancelPlacement]);

  const selectedItem = placedFurniture.find((p) => p.uid === selectedUid);
  const selectedSpec = selectedItem
    ? FURNITURE_CATALOG.find((s) => s.id === selectedItem.specId)
    : null;

  const categories: Array<FurnitureCategory | 'all' | 'ai'> = [
    'ai', 'all', 'living', 'bedroom', 'dining', 'kitchen', 'bathroom', 'storage', 'lighting', 'outdoor',
  ];

  return (
    <div className="flex flex-col gap-4">
      {/* ── Header ─────────────────────────────────────────────────────────── */}
      <div className="flex flex-wrap items-center justify-between gap-3 px-1">
        <div className="flex items-center gap-2">
          <Package className="w-5 h-5 text-indigo-400" />
          <span className="text-white font-bold text-base">Furniture Planner</span>
          <span className="text-xs text-slate-400 font-mono">
            {placedFurniture.length} item{placedFurniture.length !== 1 ? 's' : ''} placed
          </span>
        </div>
        {pendingFurniture && (
          <div className="flex items-center gap-2 px-3 py-1.5 bg-indigo-600/20 border border-indigo-500/40 rounded-lg text-indigo-300 text-xs font-semibold animate-pulse">
            <MousePointer2 className="w-3.5 h-3.5" />
            Click on the 3D floor to place: {pendingFurniture.spec.icon} {pendingFurniture.spec.name}
            <button
              onClick={handleCancelPlacement}
              className="ml-1 text-indigo-400 hover:text-white"
            >
              <X className="w-3.5 h-3.5" />
            </button>
          </div>
        )}
      </div>

      {/* ── Main Layout: Sidebar + 3D View ─────────────────────────────────── */}
      <div className="flex gap-4">
        {/* Left Sidebar: Catalog */}
        <div className="w-64 shrink-0 flex flex-col gap-3">

          {/* Category tabs */}
          <div className="flex flex-wrap gap-1">
            {categories.map((cat) => {
              const isAI = cat === 'ai';
              const isAll = cat === 'all';
              const meta = (!isAI && !isAll) ? CATEGORY_META[cat as FurnitureCategory] : null;
              const active = activeCategory === cat;
              return (
                <button
                  key={cat}
                  onClick={() => setActiveCategory(cat)}
                  className={`px-2.5 py-1 rounded-lg text-xs font-semibold transition-all border ${
                    active
                      ? isAI
                        ? 'bg-emerald-600 border-emerald-400 text-white'
                        : isAll
                          ? 'bg-slate-600 border-slate-400 text-white'
                          : `${CATEGORY_COLORS[cat as FurnitureCategory]} text-white`
                      : 'bg-slate-900 border-slate-700 text-slate-400 hover:text-slate-200 hover:border-slate-500'
                  }`}
                >
                  {isAI ? '✨ AI Pick' : isAll ? 'All' : `${meta!.emoji} ${meta!.label}`}
                </button>
              );
            })}
          </div>

          {/* AI Room Selector */}
          {activeCategory === 'ai' && rooms.length > 0 && (
            <div className="flex flex-col gap-1.5">
              <span className="text-xs text-emerald-400 font-semibold flex items-center gap-1.5">
                <Sparkles className="w-3.5 h-3.5" /> AI suggests for room:
              </span>
              <select
                value={selectedRoomForAI}
                onChange={(e) => setSelectedRoomForAI(e.target.value)}
                className="bg-slate-800 border border-slate-700 text-slate-200 text-xs rounded-lg px-2.5 py-1.5 focus:outline-none focus:border-indigo-500 cursor-pointer"
              >
                {rooms.map((r) => (
                  <option key={r.id} value={r.id}>{r.name}</option>
                ))}
              </select>
            </div>
          )}

          {/* Furniture Items */}
          <div className="flex flex-col gap-1.5 max-h-[560px] overflow-y-auto pr-1 scrollbar-thin scrollbar-thumb-slate-700">
            {visibleItems.length === 0 ? (
              <div className="text-slate-500 text-xs text-center py-6">
                No furniture for this room type
              </div>
            ) : (
              visibleItems.map((spec) => {
                const isPending = pendingFurniture?.spec.id === spec.id;
                return (
                  <button
                    key={spec.id}
                    onClick={() => handleSelectSpec(spec)}
                    className={`flex items-center gap-2.5 px-3 py-2.5 rounded-lg border text-left transition-all group ${
                      isPending
                        ? 'bg-indigo-600/20 border-indigo-500/60 ring-1 ring-indigo-400'
                        : 'bg-slate-900 border-slate-800 hover:bg-slate-800 hover:border-slate-600'
                    }`}
                  >
                    <span className="text-xl leading-none shrink-0">{spec.icon}</span>
                    <div className="flex flex-col min-w-0 flex-1">
                      <span className={`text-xs font-semibold truncate ${isPending ? 'text-indigo-300' : 'text-slate-200 group-hover:text-white'}`}>
                        {spec.name}
                      </span>
                      <span className="text-[10px] text-slate-500 font-mono">
                        {spec.width}m × {spec.depth}m × {spec.height}m
                      </span>
                    </div>
                    {isPending && (
                      <CheckCircle2 className="w-4 h-4 text-indigo-400 shrink-0" />
                    )}
                    <span
                      className="shrink-0 text-[9px] font-bold border rounded-full px-1.5 py-0.5"
                      style={{
                        background: `${spec.color}22`,
                        borderColor: `${spec.color}55`,
                        color: spec.color,
                      }}
                    >
                      {CATEGORY_META[spec.category].emoji}
                    </span>
                  </button>
                );
              })
            )}
          </div>

          {/* Selected Furniture Controls */}
          {selectedSpec && selectedItem && (
            <div className="flex flex-col gap-2 p-3 bg-slate-900 border border-indigo-500/30 rounded-xl">
              <div className="flex items-center gap-2">
                <span className="text-lg">{selectedSpec.icon}</span>
                <div>
                  <div className="text-xs font-bold text-white">{selectedSpec.name}</div>
                  <div className="text-[10px] text-slate-400 font-mono">
                    Rot: {((selectedItem.rotationY * 180) / Math.PI).toFixed(0)}°
                  </div>
                </div>
              </div>
              <div className="flex gap-1.5">
                <button
                  onClick={() => handleRotate(-Math.PI / 8)}
                  className="flex-1 flex items-center justify-center gap-1 px-2 py-1.5 bg-slate-800 hover:bg-slate-700 rounded-lg text-slate-300 text-xs font-medium transition-colors"
                  title="Rotate Left 22.5°"
                >
                  <RotateCcw className="w-3.5 h-3.5" /> ↺
                </button>
                <button
                  onClick={() => handleRotate(Math.PI / 8)}
                  className="flex-1 flex items-center justify-center gap-1 px-2 py-1.5 bg-slate-800 hover:bg-slate-700 rounded-lg text-slate-300 text-xs font-medium transition-colors"
                  title="Rotate Right 22.5°"
                >
                  <RotateCw className="w-3.5 h-3.5" /> ↻
                </button>
                <button
                  onClick={handleDuplicate}
                  className="flex items-center justify-center gap-1 px-2 py-1.5 bg-slate-800 hover:bg-slate-700 rounded-lg text-slate-300 text-xs font-medium transition-colors"
                  title="Duplicate"
                >
                  <Copy className="w-3.5 h-3.5" />
                </button>
                <button
                  onClick={handleDelete}
                  className="flex items-center justify-center gap-1 px-2 py-1.5 bg-rose-900/40 hover:bg-rose-800/60 border border-rose-700/40 rounded-lg text-rose-400 text-xs font-medium transition-colors"
                  title="Delete"
                >
                  <Trash2 className="w-3.5 h-3.5" />
                </button>
              </div>
            </div>
          )}

          {/* Placed items list */}
          {placedFurniture.length > 0 && (
            <div className="flex flex-col gap-1 mt-1">
              <div className="text-[11px] text-slate-500 font-semibold uppercase tracking-wider px-1">
                Placed Items
              </div>
              <div className="flex flex-col gap-1 max-h-48 overflow-y-auto">
                {placedFurniture.map((pf) => {
                  const s = FURNITURE_CATALOG.find((x) => x.id === pf.specId);
                  return (
                    <button
                      key={pf.uid}
                      onClick={() => setSelectedUid((prev) => prev === pf.uid ? null : pf.uid)}
                      className={`flex items-center gap-2 px-2.5 py-1.5 rounded-lg border text-left text-xs transition-all ${
                        selectedUid === pf.uid
                          ? 'bg-indigo-600/20 border-indigo-500/50 text-white'
                          : 'bg-slate-900 border-slate-800 text-slate-400 hover:text-slate-200 hover:border-slate-600'
                      }`}
                    >
                      <span>{s?.icon ?? '📦'}</span>
                      <span className="truncate flex-1">{s?.name ?? pf.specId}</span>
                      <button
                        onClick={(e) => {
                          e.stopPropagation();
                          setPlacedFurniture((prev) => prev.filter((x) => x.uid !== pf.uid));
                          if (selectedUid === pf.uid) setSelectedUid(null);
                        }}
                        className="text-slate-600 hover:text-rose-400 transition-colors"
                      >
                        <X className="w-3 h-3" />
                      </button>
                    </button>
                  );
                })}
              </div>
            </div>
          )}
        </div>

        {/* Right: 3D Viewer */}
        <div className="flex-1 min-w-0">
          {/* Instructions banner */}
          <div className={`flex items-center gap-2 px-3 py-2 rounded-t-xl border-x border-t text-xs ${
            pendingFurniture
              ? 'bg-indigo-600/15 border-indigo-500/30 text-indigo-300'
              : 'bg-slate-900/80 border-slate-800 text-slate-400'
          }`}>
            {pendingFurniture ? (
              <>
                <MousePointer2 className="w-3.5 h-3.5 shrink-0 text-indigo-400 animate-pulse" />
                <span>
                  <strong className="text-white">Click anywhere on the 3D floor</strong> to place{' '}
                  <strong className="text-indigo-300">{pendingFurniture.spec.icon} {pendingFurniture.spec.name}</strong>.
                  You can place multiple. Press <kbd className="px-1 py-0.5 bg-slate-800 rounded text-[10px] border border-slate-600">Esc</kbd> or{' '}
                  <span className="text-slate-300">✕</span> to cancel.
                </span>
              </>
            ) : selectedSpec ? (
              <>
                <CheckCircle2 className="w-3.5 h-3.5 shrink-0 text-indigo-400" />
                <span>
                  Selected: <strong className="text-white">{selectedSpec.icon} {selectedSpec.name}</strong> —
                  Use rotate/delete buttons on the left to edit it.
                </span>
              </>
            ) : (
              <>
                <Package className="w-3.5 h-3.5 shrink-0" />
                <span>Select furniture from the catalog → then click on the floor to place it in the 3D model</span>
              </>
            )}
          </div>

          <FloorplanViewer3D
            geometry={geometry}
            placedFurniture={placedFurniture}
            pendingFurniture={pendingFurniture}
            onFurniturePlaced={handleFurniturePlaced}
          />
        </div>
      </div>
    </div>
  );
};
