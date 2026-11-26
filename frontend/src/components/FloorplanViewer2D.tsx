import React, { useState, useMemo } from 'react';
import type { Structured2DGeometry, RoomGeometry, DoorSymbol } from '../types/floorplan';
import {
  ZoomIn,
  ZoomOut,
  RotateCcw,
  Eye,
  EyeOff,
  Layers,
  Sparkles,
  Hand
} from 'lucide-react';

interface Props {
  geometry: Structured2DGeometry;
}

const ROOM_PALETTE = [
  { fill: 'rgba(99, 102, 241, 0.08)', stroke: '#6366f1' },
  { fill: 'rgba(56, 189, 248, 0.08)', stroke: '#0284c7' },
  { fill: 'rgba(16, 185, 129, 0.08)', stroke: '#059669' },
  { fill: 'rgba(245, 158, 11, 0.08)', stroke: '#d97706' },
  { fill: 'rgba(168, 85, 247, 0.08)', stroke: '#9333ea' },
  { fill: 'rgba(100, 116, 139, 0.08)', stroke: '#475569' },
];

function getRoomStyle(index: number) {
  return ROOM_PALETTE[Math.abs(index) % ROOM_PALETTE.length];
}

export const FloorplanViewer2D: React.FC<Props> = ({ geometry }) => {
  const [zoom, setZoom] = useState(1);
  const [panOffset, setPanOffset] = useState<{ x: number; y: number }>({ x: 0, y: 0 });
  const [isPanning, setIsPanning] = useState<boolean>(false);
  const [dragStart, setDragStart] = useState<{ x: number; y: number }>({ x: 0, y: 0 });
  const [dragMode, setDragMode] = useState<boolean>(false);
  const [selectedRoom, setSelectedRoom] = useState<RoomGeometry | null>(null);
  const [hoveredRoom, setHoveredRoom] = useState<RoomGeometry | null>(null);
  const [mousePos, setMousePos] = useState<{ x: number; y: number } | null>(null);
  const [overlayOpacity, setOverlayOpacity] = useState<number>(0.75);
  const [showOverlay, setShowOverlay] = useState<boolean>(true);
  const [layers, setLayers] = useState({
    rooms: true,
    walls: true,
    columns: true,
    doors: true,
    windows: true,
    stairs: true,
    dimensions: true,
    labels: true,
  });

  const {
    metadata,
    rooms = [],
    walls = [],
    doors = [],
    windows = [],
    columns = [],
    stairs = [],
    dimensions_callouts = [],
    pergola_slots = [],
    overlay_image_url = '/sample-floorplan.jpg',
  } = geometry;

  const width = metadata?.page_dimensions?.width || 819;
  const height = metadata?.page_dimensions?.height || 1024;

  // Complete architectural doors: explicit + synthesized room doors for all rooms
  const allDoors = useMemo<DoorSymbol[]>(() => {
    const list: DoorSymbol[] = [...doors];
    if (!rooms || rooms.length === 0) return list;

    rooms.forEach((r) => {
      let minX = Infinity, maxX = -Infinity, minY = Infinity, maxY = -Infinity;
      if (r.boundary && r.boundary.length > 0) {
        r.boundary.forEach((p) => {
          if (p.x < minX) minX = p.x;
          if (p.x > maxX) maxX = p.x;
          if (p.y < minY) minY = p.y;
          if (p.y > maxY) maxY = p.y;
        });
      } else if (r.label_position) {
        minX = r.label_position.x - 25;
        maxX = r.label_position.x + 25;
        minY = r.label_position.y - 20;
        maxY = r.label_position.y + 20;
      }

      const hasDoor = list.some(
        (d) =>
          d.position.x >= minX - 10 &&
          d.position.x <= maxX + 10 &&
          d.position.y >= minY - 10 &&
          d.position.y <= maxY + 10
      );

      if (!hasDoor) {
        const edges = [
          { x: (minX + maxX) / 2, y: maxY },
          { x: (minX + maxX) / 2, y: minY },
          { x: maxX, y: (minY + maxY) / 2 },
          { x: minX, y: (minY + maxY) / 2 },
        ];
        const best = edges.reduce((prev, curr) => {
          const dPrev = Math.hypot(prev.x - width / 2, prev.y - height / 2);
          const dCurr = Math.hypot(curr.x - width / 2, curr.y - height / 2);
          return dCurr < dPrev ? curr : prev;
        });
        const isBath = r.name.toLowerCase().includes('bath');
        list.push({
          id: `door-room-${r.id}`,
          label: isBath ? 'D2' : 'D',
          position: best,
          width: isBath ? 20 : 25,
          swing: 'inward_right',
        });
      }
    });
    return list;
  }, [doors, rooms, width, height]);

  const toggleLayer = (layer: keyof typeof layers) => {
    setLayers((prev) => ({ ...prev, [layer]: !prev[layer] }));
  };

  const handleMouseDown = (e: React.MouseEvent) => {
    if (dragMode || e.button === 1 || e.shiftKey) {
      setIsPanning(true);
      setDragStart({ x: e.clientX - panOffset.x, y: e.clientY - panOffset.y });
    }
  };

  const handleMouseMove = (e: React.MouseEvent) => {
    if (isPanning) {
      setPanOffset({
        x: e.clientX - dragStart.x,
        y: e.clientY - dragStart.y,
      });
    }
  };

  const handleMouseUp = () => {
    setIsPanning(false);
  };

  const handleResetZoomPan = () => {
    setZoom(1);
    setPanOffset({ x: 0, y: 0 });
  };

  return (
    <div className="flex flex-col bg-slate-900 border border-slate-800 rounded-xl overflow-hidden shadow-2xl">
      {/* 2D CAD Toolbar */}
      <div className="flex flex-wrap items-center justify-between px-4 py-3 bg-slate-950/80 border-b border-slate-800 gap-3 z-10">
        <div className="flex items-center gap-2">
          <span className="text-xs font-semibold uppercase tracking-wider text-slate-300 flex items-center gap-1.5">
            <Layers className="w-3.5 h-3.5 text-indigo-400" />
            Architectural 2D CAD Blueprint
          </span>
          <span className="text-xs bg-slate-800 text-indigo-300 font-mono px-2 py-0.5 rounded border border-slate-700">
            Scale: {metadata?.scale || "1:100"}
          </span>
          {metadata?.area_sqft && (
            <span className="text-xs text-slate-400 hidden lg:inline">
              • {metadata.area_sqft}
            </span>
          )}
        </div>

        {/* Blueprint Overlay Opacity Slider */}
        <div className="flex items-center gap-2 bg-slate-900/90 px-3 py-1 rounded-lg border border-slate-800">
          <button
            onClick={() => setShowOverlay((v) => !v)}
            className={`text-xs flex items-center gap-1 font-medium ${showOverlay ? 'text-indigo-400' : 'text-slate-500'
              }`}
            title="Toggle Original Blueprint Drawing Overlay"
          >
            <Sparkles className="w-3.5 h-3.5" />
            <span>Blueprint Overlay</span>
          </button>
          {showOverlay && (
            <>
              <input
                type="range"
                min="0.1"
                max="1.0"
                step="0.05"
                value={overlayOpacity}
                onChange={(e) => setOverlayOpacity(parseFloat(e.target.value))}
                className="w-16 sm:w-24 accent-indigo-500 cursor-pointer h-1.5 bg-slate-700 rounded-lg"
                title="Adjust Original Blueprint Opacity"
              />
              <span className="text-[11px] font-mono text-slate-400 w-8">
                {Math.round(overlayOpacity * 100)}%
              </span>
            </>
          )}
        </div>

        {/* Quick Hide / Show Labels Button */}
        <button
          onClick={() => toggleLayer('labels')}
          className={`text-xs px-3 py-1.5 rounded-lg border flex items-center gap-1.5 font-semibold transition-all shadow-sm ${layers.labels
              ? 'bg-indigo-600/20 border-indigo-500/50 text-indigo-300 hover:bg-indigo-600/30'
              : 'bg-slate-800/80 border-slate-700 text-slate-400 hover:text-slate-200'
            }`}
          title={layers.labels ? 'Hide all room labels in 2D' : 'Show all room labels in 2D'}
        >
          {layers.labels ? (
            <>
              <EyeOff className="w-3.5 h-3.5 text-indigo-400" />
              <span>Hide Labels</span>
            </>
          ) : (
            <>
              <Eye className="w-3.5 h-3.5 text-slate-400" />
              <span>Show Labels</span>
            </>
          )}
        </button>

        {/* Layer Controls */}
        <div className="flex items-center gap-1.5 flex-wrap">
          {(['rooms', 'walls', 'columns', 'doors', 'windows', 'stairs', 'dimensions', 'labels'] as const).map(
            (layer) => (
              <button
                key={layer}
                onClick={() => toggleLayer(layer)}
                className={`text-xs px-2.5 py-1 rounded-md border flex items-center gap-1 transition-all ${layers[layer]
                    ? 'bg-slate-800 border-slate-600 text-slate-200'
                    : 'bg-slate-900/40 border-slate-800 text-slate-500'
                  }`}
              >
                {layers[layer] ? (
                  <Eye className="w-3 h-3 text-indigo-400" />
                ) : (
                  <EyeOff className="w-3 h-3" />
                )}
                <span className="capitalize">{layer}</span>
              </button>
            )
          )}
        </div>

        {/* Navigation & Zoom Controls */}
        <div className="flex items-center gap-1.5">
          {/* Drag / Pan Canvas Toggle */}
          <button
            onClick={() => setDragMode((prev) => !prev)}
            className={`text-xs px-2.5 py-1.5 rounded-lg border flex items-center gap-1.5 font-medium transition-all ${dragMode
                ? 'bg-indigo-600 text-white border-indigo-400 shadow-sm'
                : 'bg-slate-800/80 border-slate-700 text-slate-300 hover:text-white'
              }`}
            title="Drag / Pan Canvas (Click & drag to move blueprint around)"
          >
            <Hand className="w-3.5 h-3.5" />
            <span>Drag</span>
          </button>

          <div className="flex items-center gap-1 bg-slate-800/80 border border-slate-700 rounded-lg p-0.5">
            <button
              onClick={() => setZoom((z) => Math.min(z + 0.2, 2.5))}
              className="p-1.5 text-slate-300 hover:text-white hover:bg-slate-700 rounded"
              title="Zoom In"
            >
              <ZoomIn className="w-4 h-4" />
            </button>
            <span className="text-xs font-mono text-slate-400 px-1 min-w-[45px] text-center">
              {Math.round(zoom * 100)}%
            </span>
            <button
              onClick={() => setZoom((z) => Math.max(z - 0.2, 0.4))}
              className="p-1.5 text-slate-300 hover:text-white hover:bg-slate-700 rounded"
              title="Zoom Out"
            >
              <ZoomOut className="w-4 h-4" />
            </button>
            <button
              onClick={handleResetZoomPan}
              className="p-1.5 text-slate-300 hover:text-white hover:bg-slate-700 rounded"
              title="Reset Zoom & Position"
            >
              <RotateCcw className="w-3.5 h-3.5" />
            </button>
          </div>
        </div>
      </div>

      {/* SVG Canvas Area */}
      <div
        className={`relative overflow-hidden p-4 sm:p-6 bg-[#111622] flex items-center justify-center min-h-[600px] select-none ${dragMode ? (isPanning ? 'cursor-grabbing' : 'cursor-grab') : ''
          }`}
        onMouseDown={handleMouseDown}
        onMouseMove={handleMouseMove}
        onMouseUp={handleMouseUp}
        onMouseLeave={handleMouseUp}
      >
        <div
          className="transition-transform duration-75 origin-center"
          style={{ transform: `translate(${panOffset.x}px, ${panOffset.y}px) scale(${zoom})` }}
        >
          <svg
            width={width}
            height={height}
            viewBox={`0 0 ${width} ${height}`}
            className="bg-white rounded-lg shadow-2xl border border-slate-400 select-none text-slate-900"
          >
            <defs>
              {/* Engineering Grid Pattern */}
              <pattern id="cad-grid" width="20" height="20" patternUnits="userSpaceOnUse">
                <path d="M 20 0 L 0 0 0 20" fill="none" stroke="rgba(0,0,0,0.03)" strokeWidth="0.5" />
              </pattern>
              {/* Courtyard Diamond Lattice Paver Hatch */}
              <pattern id="lattice-pavers" width="16" height="16" patternUnits="userSpaceOnUse">
                <path d="M 0 8 L 8 0 L 16 8 L 8 16 Z" fill="none" stroke="#3b82f6" strokeWidth="0.6" opacity="0.65" />
                <path d="M 8 0 L 8 16 M 0 8 L 16 8" fill="none" stroke="#2563eb" strokeWidth="0.4" opacity="0.35" />
              </pattern>
            </defs>

            {/* Architectural Paper Background */}
            <rect width={width} height={height} fill="#ffffff" />
            <rect width={width} height={height} fill="url(#cad-grid)" />

            {/* 0. ORIGINAL BLUEPRINT OVERLAY (1:1 with uploaded drawing) */}
            {showOverlay && overlay_image_url && (
              <image
                href={overlay_image_url}
                x={0}
                y={0}
                width={width}
                height={height}
                opacity={overlayOpacity}
                preserveAspectRatio="xMidYMid meet"
                className="pointer-events-none transition-opacity duration-150"
              />
            )}

            {/* 1. SHADED PERGOLA SLOTS (if present in geometry) */}
            {pergola_slots.map((slot, idx) => (
              <rect
                key={`pergola-${idx}`}
                x={slot.x}
                y={slot.y}
                width={slot.width}
                height={slot.height}
                fill="rgba(255, 255, 255, 0.9)"
                stroke="#dc2626"
                strokeWidth={1.8}
              />
            ))}

            {/* 3. ROOMS LAYER */}
            {layers.rooms &&
              rooms.map((room, idx) => {
                if (!room.boundary || room.boundary.length === 0) return null;
                const pointsStr = room.boundary.map((p) => `${p.x},${p.y}`).join(' ');
                const isSelected = selectedRoom?.id === room.id;
                const { fill, stroke } = getRoomStyle(idx);

                return (
                  <polygon
                    key={room.id}
                    points={pointsStr}
                    fill={isSelected ? 'rgba(99, 102, 241, 0.28)' : hoveredRoom?.id === room.id ? 'rgba(99, 102, 241, 0.18)' : fill}
                    stroke={isSelected ? '#4f46e5' : hoveredRoom?.id === room.id ? '#6366f1' : stroke}
                    strokeWidth={isSelected ? 2.5 : hoveredRoom?.id === room.id ? 2.0 : 1.2}
                    className="cursor-pointer transition-colors"
                    onClick={() => setSelectedRoom(room)}
                    onMouseEnter={() => setHoveredRoom(room)}
                    onMouseMove={(e) => setMousePos({ x: e.clientX, y: e.clientY })}
                    onMouseLeave={() => {
                      setHoveredRoom(null);
                      setMousePos(null);
                    }}
                  />
                );
              })}

            {/* 4. WALLS LAYER */}
            {layers.walls &&
              walls.map((wall) => {
                const isExterior = wall.type === 'exterior';
                return (
                  <line
                    key={wall.id}
                    x1={wall.start.x}
                    y1={wall.start.y}
                    x2={wall.end.x}
                    y2={wall.end.y}
                    stroke={isExterior ? '#0f172a' : '#334155'}
                    strokeWidth={isExterior ? 3.0 : 1.8}
                    strokeLinecap="round"
                  />
                );
              })}

            {/* 5. STRUCTURAL COLUMNS (Clean Dark Slate Pillars) */}
            {layers.columns &&
              columns.map((col) => (
                <rect
                  key={col.id}
                  x={col.position.x - col.width / 2}
                  y={col.position.y - col.height / 2}
                  width={col.width}
                  height={col.height}
                  fill="#334155"
                  stroke="#0f172a"
                  strokeWidth={1.0}
                  rx={1}
                />
              ))}

            {/* 6. SPIRAL STAIRCASE */}
            {layers.stairs &&
              stairs.map((stair) => {
                if (stair.type === 'spiral') {
                  const radius = stair.radius || 32;
                  const steps = stair.steps || 12;
                  return (
                    <g key={stair.id} transform={`translate(${stair.position.x}, ${stair.position.y})`}>
                      {/* Outer Ring */}
                      <circle r={radius} fill="none" stroke="#22c55e" strokeWidth={2} />
                      <circle r={radius * 0.3} fill="#22c55e" opacity={0.3} stroke="#22c55e" strokeWidth={1.5} />
                      {/* Spiral Treads */}
                      {Array.from({ length: steps }).map((_, i) => {
                        const angle = (i * 2 * Math.PI) / steps;
                        const x1 = Math.cos(angle) * (radius * 0.3);
                        const y1 = Math.sin(angle) * (radius * 0.3);
                        const x2 = Math.cos(angle) * radius;
                        const y2 = Math.sin(angle) * radius;
                        return (
                          <line
                            key={`step-${i}`}
                            x1={x1}
                            y1={y1}
                            x2={x2}
                            y2={y2}
                            stroke="#15803d"
                            strokeWidth={1.2}
                          />
                        );
                      })}
                    </g>
                  );
                }
                return null;
              })}

            {/* 7. DOORS (MD, D, D2) WITH SWING ARCS FOR ALL ROOMS */}
            {layers.doors &&
              allDoors.map((door) => {
                const r = door.width ? door.width * 0.8 : 20;
                return (
                  <g key={door.id}>
                    {/* Door Leaf */}
                    <line
                      x1={door.position.x}
                      y1={door.position.y}
                      x2={door.position.x + r}
                      y2={door.position.y}
                      stroke="#d97706"
                      strokeWidth={2}
                    />
                    {/* Door Swing Arc */}
                    <path
                      d={`M ${door.position.x + r} ${door.position.y} A ${r} ${r} 0 0 1 ${door.position.x} ${door.position.y + r}`}
                      fill="none"
                      stroke="#d97706"
                      strokeWidth={1.2}
                      strokeDasharray="2.5 1.5"
                    />
                    {door.label && (
                      <text
                        x={door.position.x + r / 2}
                        y={door.position.y - 4}
                        fill="#b45309"
                        fontSize="9"
                        fontWeight="bold"
                        textAnchor="middle"
                      >
                        {door.label}
                      </text>
                    )}
                  </g>
                );
              })}

            {/* 8. WINDOWS (W2, W3, Fw, V) - SNAPPED & ALIGNED */}
            {layers.windows &&
              windows.map((win) => {
                const w = win.width || 30;
                let isVertical = false;
                let snappedPos = { ...win.position };
                if (walls && walls.length > 0) {
                  let minDist = Infinity;
                  for (const wl of walls) {
                    const dx = wl.end.x - wl.start.x;
                    const dy = wl.end.y - wl.start.y;
                    const lenSq = dx * dx + dy * dy;
                    if (lenSq < 1) continue;
                    const t = Math.max(0.05, Math.min(0.95, ((win.position.x - wl.start.x) * dx + (win.position.y - wl.start.y) * dy) / lenSq));
                    const px = wl.start.x + t * dx;
                    const py = wl.start.y + t * dy;
                    const dist = Math.hypot(win.position.x - px, win.position.y - py);
                    if (dist < minDist) {
                      minDist = dist;
                      if (dist < 20) {
                        snappedPos = { x: px, y: py };
                        isVertical = Math.abs(dy) > Math.abs(dx);
                      }
                    }
                  }
                }

                return (
                  <g key={win.id}>
                    {isVertical ? (
                      <>
                        <line
                          x1={snappedPos.x - 2}
                          y1={snappedPos.y - w / 2}
                          x2={snappedPos.x - 2}
                          y2={snappedPos.y + w / 2}
                          stroke="#0284c7"
                          strokeWidth={2}
                        />
                        <line
                          x1={snappedPos.x + 2}
                          y1={snappedPos.y - w / 2}
                          x2={snappedPos.x + 2}
                          y2={snappedPos.y + w / 2}
                          stroke="#0284c7"
                          strokeWidth={2}
                        />
                      </>
                    ) : (
                      <>
                        <line
                          x1={snappedPos.x - w / 2}
                          y1={snappedPos.y - 2}
                          x2={snappedPos.x + w / 2}
                          y2={snappedPos.y - 2}
                          stroke="#0284c7"
                          strokeWidth={2}
                        />
                        <line
                          x1={snappedPos.x - w / 2}
                          y1={snappedPos.y + 2}
                          x2={snappedPos.x + w / 2}
                          y2={snappedPos.y + 2}
                          stroke="#0284c7"
                          strokeWidth={2}
                        />
                      </>
                    )}
                    {win.label && (
                      <text
                        x={snappedPos.x}
                        y={snappedPos.y - (isVertical ? w / 2 + 3 : 5)}
                        fill="#0369a1"
                        fontSize="9"
                        fontWeight="bold"
                        textAnchor="middle"
                      >
                        {win.label}
                      </text>
                    )}
                  </g>
                );
              })}

            {/* 9. DIMENSION CALLOUTS (58'-3", 55'-11", 27'-7") */}
            {layers.dimensions &&
              dimensions_callouts.map((dim) => (
                <g key={dim.id} stroke="#c026d3" fill="#c026d3">
                  <line
                    x1={dim.start.x}
                    y1={dim.start.y}
                    x2={dim.end.x}
                    y2={dim.end.y}
                    strokeWidth={1.2}
                  />
                  {/* Extension witness lines */}
                  <circle cx={dim.start.x} cy={dim.start.y} r={2} />
                  <circle cx={dim.end.x} cy={dim.end.y} r={2} />
                  <text
                    x={dim.textPos.x}
                    y={dim.textPos.y}
                    fontSize="11"
                    fontWeight="bold"
                    textAnchor="middle"
                    stroke="none"
                  >
                    {dim.label}
                  </text>
                </g>
              ))}

            {/* 10. ROOM LABELS & DIMENSIONS */}
            {layers.labels &&
              rooms.map((room) => {
                const posX = room.label_position?.x || width / 2;
                const posY = room.label_position?.y || height / 2;
                const textLen = Math.max(room.name.length, (room.dimensions || '').length);
                const badgeWidth = Math.max(80, textLen * 7.5 + 20);
                const isHovered = hoveredRoom?.id === room.id;

                return (
                  <g
                    key={`lbl-${room.id}`}
                    className="cursor-pointer select-none transition-transform"
                    onClick={() => setSelectedRoom(room)}
                    onMouseEnter={() => setHoveredRoom(room)}
                    onMouseMove={(e) => setMousePos({ x: e.clientX, y: e.clientY })}
                    onMouseLeave={() => {
                      setHoveredRoom(null);
                      setMousePos(null);
                    }}
                  >
                    <rect
                      x={posX - badgeWidth / 2}
                      y={posY - (room.dimensions ? 16 : 11)}
                      width={badgeWidth}
                      height={room.dimensions ? 32 : 22}
                      rx={5}
                      fill={isHovered ? 'rgba(15, 23, 42, 0.98)' : 'rgba(255, 255, 255, 0.94)'}
                      stroke={isHovered ? '#6366f1' : 'rgba(0, 0, 0, 0.22)'}
                      strokeWidth={isHovered ? 1.8 : 0.8}
                    />
                    <text
                      x={posX}
                      y={posY - (room.dimensions ? 2 : -4)}
                      textAnchor="middle"
                      fill={isHovered ? '#ffffff' : '#0f172a'}
                      fontSize="10"
                      fontWeight="bold"
                      fontFamily="system-ui"
                    >
                      {room.name}
                    </text>
                    {room.dimensions && (
                      <text
                        x={posX}
                        y={posY + 10}
                        textAnchor="middle"
                        fill={isHovered ? '#a5b4fc' : '#475569'}
                        fontSize="8.5"
                        fontFamily="ui-monospace, monospace"
                      >
                        {room.dimensions}
                      </text>
                    )}
                  </g>
                );
              })}
          </svg>
        </div>
      </div>

      {/* Interactive Floating Hover Tooltip */}
      {hoveredRoom && mousePos && (
        <div
          className="fixed z-50 pointer-events-none px-3.5 py-2 rounded-xl bg-slate-900/95 border border-indigo-500/60 shadow-2xl backdrop-blur text-xs transition-opacity duration-100 flex flex-col gap-0.5"
          style={{ left: mousePos.x + 14, top: mousePos.y + 14 }}
        >
          <div className="font-bold text-white flex items-center gap-1.5 text-sm">
            <span className="w-2 h-2 rounded-full bg-indigo-400 animate-pulse"></span>
            {hoveredRoom.name}
          </div>
          {hoveredRoom.dimensions && (
            <div className="text-xs font-mono text-indigo-300 flex items-center gap-1">
              <span>📐</span>
              <span>{hoveredRoom.dimensions}</span>
            </div>
          )}
          <div className="text-[10px] text-slate-400 mt-0.5">Click to select room</div>
        </div>
      )}

      {/* Selected Room Details Bar */}
      {selectedRoom && (
        <div className="px-5 py-3 bg-slate-950 border-t border-slate-800 flex items-center justify-between text-xs">
          <div className="flex items-center gap-3">
            <span className="font-bold text-white text-sm">{selectedRoom.name}</span>
            <span className="text-indigo-300 font-mono text-xs">
              Dimensions: {selectedRoom.dimensions || 'N/A'}
            </span>
          </div>
          <button
            onClick={() => setSelectedRoom(null)}
            className="text-slate-400 hover:text-white px-2 py-1 rounded bg-slate-800 hover:bg-slate-700"
          >
            Clear Selection
          </button>
        </div>
      )}
    </div>
  );
};
