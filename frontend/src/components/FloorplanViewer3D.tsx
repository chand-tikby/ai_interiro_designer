import React, { useMemo, useState, useRef, useEffect, useCallback } from 'react';
import { Canvas, useThree, useFrame } from '@react-three/fiber';
import { OrbitControls, ContactShadows } from '@react-three/drei';
import * as THREE from 'three';
import type {
  Structured2DGeometry,
  RoomGeometry,
  WallSegment,
  DoorSymbol,
  WindowSymbol,
  StaircaseSymbol,
  Point2D,
} from '../types/floorplan';
import type { PlacedFurniture, FurnitureSpec } from '../types/furniture';
import { FURNITURE_CATALOG } from '../types/furniture';
import {
  Sliders,
  RotateCcw,
  Sun,
  Moon,
  Sparkles,
  Eye,
  Maximize2,
  Compass,
  Palette,
  Home,
  Camera,
  Layers,
  X,
  Search,
  Armchair,
} from 'lucide-react';
import { AIPhotorealisticRoomView } from './AIPhotorealisticRoomView';

interface Props {
  geometry: Structured2DGeometry;
  placedFurniture?: PlacedFurniture[];
  pendingFurniture?: { spec: FurnitureSpec } | null;
  onFurniturePlaced?: (furniture: PlacedFurniture) => void;
  onSelectFurniture?: (uid: string) => void;
  selectedFurnitureUid?: string | null;
}

// ── STYLE DEFINITIONS ─────────────────────────────────────────────────────────
export type InteriorStyle = 'modern' | 'scandinavian' | 'luxury';

interface StyleConfig {
  name: string;
  icon: string;
  description: string;
  wallColor: string;
  woodBaseColor: string;
  woodDarkColor: string;
  sofaColor: string;
  accentMetal: string;
  ambientLightColor: string;
  ambientLightIntensity: number;
}

const STYLE_PALETTES: Record<InteriorStyle, StyleConfig> = {
  modern: {
    name: 'Modern Warmth',
    icon: '✨',
    description: 'Rustic stone fireplace, honey-oak wide planks, warm greige linen modular sofa & sunset glow',
    wallColor: '#f4efe8',
    woodBaseColor: '#c49a6c',
    woodDarkColor: '#362316',
    sofaColor: '#d6cfc7', // Warm greige / oatmeal linen
    accentMetal: '#1c1b1a',
    ambientLightColor: '#fff9ee',
    ambientLightIntensity: 0.75,
  },
  scandinavian: {
    name: 'Nordic Lodge',
    icon: '🌿',
    description: 'Pale riverstone fireplace, light ash timbers, oatmeal bouclé, bright golden hour sunlight',
    wallColor: '#f9f8f6',
    woodBaseColor: '#ded0be',
    woodDarkColor: '#635345',
    sofaColor: '#e4ddd3',
    accentMetal: '#3f3f46',
    ambientLightColor: '#ffffff',
    ambientLightIntensity: 0.8,
  },
  luxury: {
    name: 'Alpine Estate',
    icon: '👑',
    description: 'Stacked quarry ledge stone, rich fumed oak, warm amber glow & deep plush upholstery',
    wallColor: '#ebe4db',
    woodBaseColor: '#a17852',
    woodDarkColor: '#24140a',
    sofaColor: '#c5bcb2',
    accentMetal: '#92400e',
    ambientLightColor: '#fff5e6',
    ambientLightIntensity: 0.7,
  },
};

// ── PROCEDURAL PBR TEXTURE GENERATORS ─────────────────────────────────────────

// 1. Wide-Plank Warm Honey-Oak Hardwood Flooring (Matching Image Exactly)
function createHardwoodFloorTexture(style: InteriorStyle): THREE.CanvasTexture {
  const canvas = document.createElement('canvas');
  canvas.width = 1024;
  canvas.height = 1024;
  const ctx = canvas.getContext('2d')!;

  const rows = 10;
  const cols = 4;
  const rowH = canvas.height / rows;
  const colW = canvas.width / cols;

  const baseTones =
    style === 'scandinavian'
      ? ['#dfd6cb', '#d8cec2', '#e5ddd3', '#cfc4b7']
      : style === 'luxury'
      ? ['#b89977', '#a68765', '#be9f7e', '#967755']
      : ['#c9a882', '#bd9b74', '#d2b18c', '#b39069']; // Rich honey-oak

  for (let r = 0; r < rows; r++) {
    const y = r * rowH;
    const offset = (r % 2) * (colW * 0.5);

    for (let c = -1; c < cols + 1; c++) {
      const x = c * colW + offset;
      const tone = baseTones[(r * 3 + c + 10) % baseTones.length];

      ctx.fillStyle = tone;
      ctx.fillRect(x, y, colW, rowH);

      // Fine wood grain lines
      for (let g = 0; g < 8; g++) {
        const gy = y + Math.random() * rowH;
        ctx.fillStyle = 'rgba(50, 30, 10, 0.035)';
        ctx.fillRect(x, gy, colW, 1.5);
      }

      // Dark bevel groove between planks
      ctx.strokeStyle = 'rgba(40, 25, 12, 0.45)';
      ctx.lineWidth = 2.0;
      ctx.strokeRect(x, y, colW, rowH);
    }
  }

  const texture = new THREE.CanvasTexture(canvas);
  texture.wrapS = THREE.RepeatWrapping;
  texture.wrapT = THREE.RepeatWrapping;
  texture.repeat.set(3, 4);
  return texture;
}

// 2b. Teakwood Deck Planking Texture (for Sitout / Balcony Veranda - Matching Planner 5D Exactly)
function createTeakDeckTexture(): THREE.CanvasTexture {
  const canvas = document.createElement('canvas');
  canvas.width = 1024;
  canvas.height = 1024;
  const ctx = canvas.getContext('2d')!;

  ctx.fillStyle = '#854d0e'; // Warm rich teakwood base
  ctx.fillRect(0, 0, 1024, 1024);

  const plankH = 42;
  for (let y = 0; y < 1024; y += plankH) {
    const toneVar = (Math.random() - 0.5) * 26;
    const r = Math.min(255, Math.max(0, 133 + toneVar));
    const g = Math.min(255, Math.max(0, 77 + toneVar * 0.75));
    const b = Math.min(255, Math.max(0, 14 + toneVar * 0.4));
    ctx.fillStyle = `rgb(${Math.round(r)}, ${Math.round(g)}, ${Math.round(b)})`;
    ctx.fillRect(0, y, 1024, plankH);

    // Fine wood grain lines along plank length
    for (let k = 0; k < 6; k++) {
      ctx.fillStyle = 'rgba(50, 25, 5, 0.09)';
      ctx.fillRect(0, y + Math.random() * plankH, 1024, 1.5);
    }

    // Groove shadow between horizontal deck planks
    ctx.fillStyle = 'rgba(25, 12, 2, 0.7)';
    ctx.fillRect(0, y + plankH - 2.5, 1024, 2.5);
    ctx.fillStyle = 'rgba(255, 230, 170, 0.18)';
    ctx.fillRect(0, y, 1024, 1.0);
  }

  const texture = new THREE.CanvasTexture(canvas);
  texture.wrapS = THREE.RepeatWrapping;
  texture.wrapT = THREE.RepeatWrapping;
  texture.repeat.set(1.5, 8);
  return texture;
}

// 2c. Crisp Ceramic Floor Tile Texture (for Bathrooms and Wet Kitchen)
function createTileFloorTexture(): THREE.CanvasTexture {
  const canvas = document.createElement('canvas');
  canvas.width = 512;
  canvas.height = 512;
  const ctx = canvas.getContext('2d')!;

  ctx.fillStyle = '#f8fafc';
  ctx.fillRect(0, 0, 512, 512);

  const tileSize = 128;
  ctx.strokeStyle = '#cbd5e1';
  ctx.lineWidth = 3;
  for (let x = 0; x <= 512; x += tileSize) {
    ctx.beginPath();
    ctx.moveTo(x, 0);
    ctx.lineTo(x, 512);
    ctx.stroke();
  }
  for (let y = 0; y <= 512; y += tileSize) {
    ctx.beginPath();
    ctx.moveTo(0, y);
    ctx.lineTo(512, y);
    ctx.stroke();
  }

  const texture = new THREE.CanvasTexture(canvas);
  texture.wrapS = THREE.RepeatWrapping;
  texture.wrapT = THREE.RepeatWrapping;
  texture.repeat.set(4, 4);
  return texture;
}

// 2d. Nero Marquina Dark Grey/Black Veined Marble (for Drawing Hall Focal Wall - Matching Planner 5D Reference Exactly)
function createDarkMarbleTexture(): THREE.CanvasTexture {
  const canvas = document.createElement('canvas');
  canvas.width = 1024;
  canvas.height = 1024;
  const ctx = canvas.getContext('2d')!;

  // Deep dark graphite / charcoal base
  ctx.fillStyle = '#22252a';
  ctx.fillRect(0, 0, 1024, 1024);

  // Soft cloudy organic mineral shading
  for (let i = 0; i < 28; i++) {
    const rx = Math.random() * 1024;
    const ry = Math.random() * 1024;
    const rad = 70 + Math.random() * 240;
    const grad = ctx.createRadialGradient(rx, ry, 10, rx, ry, rad);
    grad.addColorStop(0, 'rgba(52, 57, 65, 0.42)');
    grad.addColorStop(1, 'rgba(34, 37, 42, 0)');
    ctx.fillStyle = grad;
    ctx.beginPath();
    ctx.arc(rx, ry, rad, 0, Math.PI * 2);
    ctx.fill();
  }

  // Crisp organic white and silver marble veining
  const drawVein = (startX: number, startY: number, color: string, width: number) => {
    ctx.strokeStyle = color;
    ctx.lineWidth = width;
    ctx.beginPath();
    let cx = startX;
    let cy = startY;
    ctx.moveTo(cx, cy);
    while (cx < 1050 && cy < 1050 && cx > -50 && cy > -50) {
      const stepX = (Math.random() - 0.28) * 52;
      const stepY = (Math.random() + 0.35) * 44;
      cx += stepX;
      cy += stepY;
      ctx.lineTo(cx, cy);
    }
    ctx.stroke();
  };

  for (let v = 0; v < 16; v++) {
    drawVein(Math.random() * 900 - 100, Math.random() * 200 - 100, 'rgba(235, 240, 248, 0.45)', 2.5 + Math.random() * 3);
    drawVein(Math.random() * 900 - 100, Math.random() * 200 - 100, 'rgba(255, 255, 255, 0.8)', 1.0 + Math.random() * 1.5);
    drawVein(Math.random() * 900 - 100, Math.random() * 200 - 100, 'rgba(180, 190, 205, 0.3)', 4 + Math.random() * 4);
  }

  const texture = new THREE.CanvasTexture(canvas);
  texture.wrapS = THREE.RepeatWrapping;
  texture.wrapT = THREE.RepeatWrapping;
  texture.repeat.set(1.5, 1.5);
  return texture;
}

// 3. Woven Sisal / Jute Area Rug Texture
function createRugTexture(): THREE.CanvasTexture {
  const canvas = document.createElement('canvas');
  canvas.width = 512;
  canvas.height = 512;
  const ctx = canvas.getContext('2d')!;

  ctx.fillStyle = '#b8ad9c'; // Earthy neutral jute base
  ctx.fillRect(0, 0, 512, 512);

  const step = 6;
  for (let x = 0; x < 512; x += step) {
    for (let y = 0; y < 512; y += step) {
      ctx.fillStyle = (x + y) % (step * 2) === 0 ? 'rgba(255,255,255,0.09)' : 'rgba(0,0,0,0.09)';
      ctx.fillRect(x, y, step, step);
    }
  }

  const texture = new THREE.CanvasTexture(canvas);
  texture.wrapS = THREE.RepeatWrapping;
  texture.wrapT = THREE.RepeatWrapping;
  texture.repeat.set(8, 8);
  return texture;
}

// 4. Textured Heathered Linen-Bouclé Upholstery (For Sectional Sofa)
function createLinenFabricTexture(baseHex: string): THREE.CanvasTexture {
  const canvas = document.createElement('canvas');
  canvas.width = 512;
  canvas.height = 512;
  const ctx = canvas.getContext('2d')!;

  // Warm textured heathered base
  ctx.fillStyle = baseHex;
  ctx.fillRect(0, 0, 512, 512);

  // Warp & weft slub linen threads
  const step = 4;
  for (let x = 0; x < 512; x += step) {
    for (let y = 0; y < 512; y += step) {
      const isAlt = (x / step + y / step) % 2 === 0;
      ctx.fillStyle = isAlt ? 'rgba(255, 252, 245, 0.14)' : 'rgba(30, 24, 18, 0.12)';
      ctx.fillRect(x, y, step, step);
    }
  }

  // Organic irregular linen slub threads
  for (let i = 0; i < 40; i++) {
    const sy = Math.random() * 512;
    const sx = Math.random() * 400;
    ctx.fillStyle = Math.random() > 0.5 ? 'rgba(255, 255, 255, 0.18)' : 'rgba(40, 30, 20, 0.16)';
    ctx.fillRect(sx, sy, 30 + Math.random() * 60, 2.0);
  }

  const texture = new THREE.CanvasTexture(canvas);
  texture.wrapS = THREE.RepeatWrapping;
  texture.wrapT = THREE.RepeatWrapping;
  texture.repeat.set(4, 4);
  return texture;
}

// 5. Solid Natural Oak Wood Grain (For Split Coffee Table & Side Console)
function createNaturalOakTexture(): THREE.CanvasTexture {
  const canvas = document.createElement('canvas');
  canvas.width = 512;
  canvas.height = 512;
  const ctx = canvas.getContext('2d')!;

  ctx.fillStyle = '#c8a379'; // Honey oak
  ctx.fillRect(0, 0, 512, 512);

  for (let i = 0; i < 24; i++) {
    const y = Math.random() * 512;
    ctx.fillStyle = 'rgba(70, 45, 20, 0.05)';
    ctx.fillRect(0, y, 512, 2 + Math.random() * 3);
  }

  const texture = new THREE.CanvasTexture(canvas);
  texture.wrapS = THREE.RepeatWrapping;
  texture.wrapT = THREE.RepeatWrapping;
  texture.repeat.set(2, 2);
  return texture;
}



// 7. Calacatta Gold / Italian White Marble Texture (Kitchen Waterfall Island & Vanities)
function createCalacattaMarbleTexture(): THREE.CanvasTexture {
  const canvas = document.createElement('canvas');
  canvas.width = 1024;
  canvas.height = 1024;
  const ctx = canvas.getContext('2d')!;

  // Warm milky white marble base
  ctx.fillStyle = '#f8f6f0';
  ctx.fillRect(0, 0, 1024, 1024);

  // Soft subtle grey and warm gold veins
  const drawVein = (startX: number, startY: number, color: string, width: number) => {
    ctx.strokeStyle = color;
    ctx.lineWidth = width;
    ctx.beginPath();
    let cx = startX;
    let cy = startY;
    ctx.moveTo(cx, cy);
    while (cx < 1024 && cy < 1024 && cx > -50 && cy > -50) {
      cx += 20 + Math.random() * 30;
      cy += (Math.random() - 0.45) * 45;
      ctx.lineTo(cx, cy);
    }
    ctx.stroke();
  };

  for (let i = 0; i < 6; i++) {
    drawVein(-20, 150 + i * 160, 'rgba(160, 150, 140, 0.15)', 4 + Math.random() * 4);
    drawVein(-20, 150 + i * 160, 'rgba(120, 115, 110, 0.22)', 1.5);
    drawVein(-20, 160 + i * 160, 'rgba(190, 150, 90, 0.12)', 2.0); // Gold whisper
  }

  const texture = new THREE.CanvasTexture(canvas);
  texture.wrapS = THREE.RepeatWrapping;
  texture.wrapT = THREE.RepeatWrapping;
  texture.repeat.set(1.5, 1.5);
  return texture;
}

// 8. Architectural Wood Ceiling Planks (Matching Instagram Video Demo)
function createWoodCeilingTexture(style: InteriorStyle): THREE.CanvasTexture {
  const canvas = document.createElement('canvas');
  canvas.width = 1024;
  canvas.height = 1024;
  const ctx = canvas.getContext('2d')!;

  const plankCount = 28;
  const plankH = 1024 / plankCount;

  const baseTones =
    style === 'scandinavian'
      ? ['#ded5c6', '#d6ccbc', '#e2d9cb', '#cec4b4']
      : style === 'luxury'
      ? ['#6e5038', '#5c412c', '#75563d', '#503825']
      : ['#b8946f', '#ab8660', '#c29d77', '#a07d57']; // Warm honey-oak

  for (let p = 0; p < plankCount; p++) {
    const y = p * plankH;
    const tone = baseTones[p % baseTones.length];
    ctx.fillStyle = tone;
    ctx.fillRect(0, y, 1024, plankH);

    // Fine wood grain
    for (let g = 0; g < 4; g++) {
      ctx.fillStyle = 'rgba(40, 20, 5, 0.04)';
      ctx.fillRect(0, y + Math.random() * plankH, 1024, 1.2);
    }

    // Groove reveal gap between planks
    ctx.fillStyle = 'rgba(25, 12, 4, 0.55)';
    ctx.fillRect(0, y + plankH - 1.5, 1024, 1.5);
    ctx.fillStyle = 'rgba(255, 255, 255, 0.12)';
    ctx.fillRect(0, y, 1024, 0.8);
  }

  const texture = new THREE.CanvasTexture(canvas);
  texture.wrapS = THREE.RepeatWrapping;
  texture.wrapT = THREE.RepeatWrapping;
  texture.repeat.set(2, 4);
  return texture;
}

export interface SplitWallSegment {
  id: string;
  start: Point2D;
  end: Point2D;
  thickness: number;
  type: 'interior' | 'exterior';
  isHeader?: boolean;
}

// ── EXACT BLUEPRINT WALL DERIVATION WITH OPEN DOORWAYS ───────────────────────
function deriveCleanWallsWithDoorways(
  rooms: RoomGeometry[],
  allDoors: DoorSymbol[],
  scale: number,
  centerX: number,
  centerZ: number,
  fallbackWalls: WallSegment[] = []
): SplitWallSegment[] {
  if (!rooms || rooms.length === 0) {
    return fallbackWalls.map(w => ({
      id: w.id,
      start: w.start,
      end: w.end,
      thickness: w.thickness || 4,
      type: w.type || 'interior'
    }));
  }

  const edgeMap = new Map<string, { start: Point2D; end: Point2D; count: number }>();
  const snap = (v: number) => Math.round(v * 2) / 2;

  rooms.forEach((r: RoomGeometry) => {
    const pts = r.boundary;
    if (!pts || pts.length < 3) return;
    for (let i = 0; i < pts.length; i++) {
      const p1 = pts[i];
      const p2 = pts[(i + 1) % pts.length];

      const x1 = snap(p1.x);
      const y1 = snap(p1.y);
      const x2 = snap(p2.x);
      const y2 = snap(p2.y);

      if (Math.hypot(x2 - x1, y2 - y1) < 4) continue;

      const key =
        x1 < x2 || (x1 === x2 && y1 < y2)
          ? `${x1},${y1}-${x2},${y2}`
          : `${x2},${y2}-${x1},${y1}`;

      const existing = edgeMap.get(key);
      if (existing) {
        existing.count += 1;
      } else {
        edgeMap.set(key, {
          start: { x: p1.x, y: p1.y },
          end: { x: p2.x, y: p2.y },
          count: 1,
        });
      }
    }
  });

  const baseWalls: WallSegment[] = [];
  let idx = 1;
  for (const [, val] of edgeMap.entries()) {
    baseWalls.push({
      id: `clean-wall-${idx++}`,
      start: val.start,
      end: val.end,
      thickness: val.count === 1 ? 6 : 4,
      type: val.count === 1 ? 'exterior' : 'interior',
    });
  }

  // Now split walls where doors create walk-through openings (matching Planner 5D exactly!)
  const splitWalls: SplitWallSegment[] = [];

  baseWalls.forEach((w) => {
    const x1 = (w.start.x - centerX) * scale;
    const z1 = (w.start.y - centerZ) * scale;
    const x2 = (w.end.x - centerX) * scale;
    const z2 = (w.end.y - centerZ) * scale;

    const dx = x2 - x1;
    const dz = z2 - z1;
    const wallLen = Math.hypot(dx, dz);
    if (wallLen < 0.1) return;

    const ux = dx / wallLen;
    const uz = dz / wallLen;

    // Find doors on this wall segment
    const doorsOnWall: { t: number; halfW: number }[] = [];

    allDoors.forEach((d) => {
      const doorX = (d.position.x - centerX) * scale;
      const doorZ = (d.position.y - centerZ) * scale;

      const t = (doorX - x1) * ux + (doorZ - z1) * uz;
      const projX = x1 + t * ux;
      const projZ = z1 + t * uz;
      const perpDist = Math.hypot(doorX - projX, doorZ - projZ);

      const doorW = Math.max((d.width || 36) * scale, 0.9);
      const halfW = doorW / 2;

      if (perpDist < 0.35 && t > halfW + 0.05 && t < wallLen - halfW - 0.05) {
        doorsOnWall.push({ t, halfW });
      }
    });

    if (doorsOnWall.length === 0) {
      splitWalls.push({
        id: w.id,
        start: w.start,
        end: w.end,
        thickness: w.thickness || 4,
        type: w.type || 'interior',
      });
      return;
    }

    doorsOnWall.sort((a, b) => a.t - b.t);

    let currentT = 0;
    doorsOnWall.forEach((door, dIdx) => {
      const cutStart = Math.max(0, door.t - door.halfW);
      const cutEnd = Math.min(wallLen, door.t + door.halfW);

      // Solid wall before opening
      if (cutStart - currentT > 0.06) {
        const segStart: Point2D = {
          x: ((x1 + currentT * ux) / scale) + centerX,
          y: ((z1 + currentT * uz) / scale) + centerZ,
        };
        const segEnd: Point2D = {
          x: ((x1 + cutStart * ux) / scale) + centerX,
          y: ((z1 + cutStart * uz) / scale) + centerZ,
        };
        splitWalls.push({
          id: `${w.id}-seg-${dIdx}-a`,
          start: segStart,
          end: segEnd,
          thickness: w.thickness || 4,
          type: w.type || 'interior',
        });
      }

      // Doorway header above opening (rendered only in Room mode above 2.1m)
      const headStart: Point2D = {
        x: ((x1 + cutStart * ux) / scale) + centerX,
        y: ((z1 + cutStart * uz) / scale) + centerZ,
      };
      const headEnd: Point2D = {
        x: ((x1 + cutEnd * ux) / scale) + centerX,
        y: ((z1 + cutEnd * uz) / scale) + centerZ,
      };
      splitWalls.push({
        id: `${w.id}-head-${dIdx}`,
        start: headStart,
        end: headEnd,
        thickness: w.thickness || 4,
        type: w.type || 'interior',
        isHeader: true,
      });

      currentT = cutEnd;
    });

    // Solid wall after last opening
    if (wallLen - currentT > 0.06) {
      const segStart: Point2D = {
        x: ((x1 + currentT * ux) / scale) + centerX,
        y: ((z1 + currentT * uz) / scale) + centerZ,
      };
      const segEnd: Point2D = {
        x: ((x1 + wallLen * ux) / scale) + centerX,
        y: ((z1 + wallLen * uz) / scale) + centerZ,
      };
      splitWalls.push({
        id: `${w.id}-seg-last`,
        start: segStart,
        end: segEnd,
        thickness: w.thickness || 4,
        type: w.type || 'interior',
      });
    }
  });

  return splitWalls;
}

// ── CLEAN ARCHITECTURAL GROUND & GRID (Matching Planner 5D Workspace) ─────────
const OutdoorLandscape3D: React.FC<{
  maxX: number;
  minY: number;
  maxY: number;
  scale: number;
  centerX: number;
  centerZ: number;
}> = () => {
  return (
    <group position={[0, -0.015, 0]}>
      {/* Clean subtle architectural ground plane (Planner 5D aesthetic) */}
      <mesh rotation={[-Math.PI / 2, 0, 0]} receiveShadow>
        <planeGeometry args={[120, 120]} />
        <meshStandardMaterial color="#f8fafc" roughness={0.96} metalness={0.0} />
      </mesh>
      {/* Subtle floor grid lines */}
      <gridHelper args={[80, 80, '#94a3b8', '#e2e8f0']} position={[0, 0.001, 0]} />
    </group>
  );
};

// ── ARCHITECTURAL WALL WITH OPEN DOORWAY HEADERS ───────────────────────────────
const Wall3D: React.FC<{
  wall: SplitWallSegment;
  scale: number;
  centerX: number;
  centerZ: number;
  effectiveWallHeight: number;
  styleWallColor: string;
}> = ({ wall, scale, centerX, centerZ, effectiveWallHeight, styleWallColor }) => {
  const x1 = (wall.start.x - centerX) * scale;
  const z1 = (wall.start.y - centerZ) * scale;
  const x2 = (wall.end.x - centerX) * scale;
  const z2 = (wall.end.y - centerZ) * scale;

  const dx = x2 - x1;
  const dz = z2 - z1;
  const length = Math.hypot(dx, dz);
  if (length < 0.05) return null;

  const angle = Math.atan2(dz, dx);
  const midX = (x1 + x2) / 2;
  const midZ = (z1 + z2) / 2;
  const thickness = Math.max((wall.thickness || 4) * scale * 0.85, 0.14);

  // If this is a doorway header:
  if (wall.isHeader) {
    // In dollhouse mode (cutaway walls <= 2.1m), do not render header so doorway is a clean open walk-through gap!
    if (effectiveWallHeight <= 2.1) return null;

    const headerHeight = effectiveWallHeight - 2.1;
    const headerPosY = 2.1 + headerHeight / 2;

    return (
      <group position={[midX, headerPosY, midZ]} rotation={[0, -angle, 0]}>
        <mesh castShadow receiveShadow>
          <boxGeometry args={[length, headerHeight, thickness]} />
          <meshStandardMaterial
            color={wall.type === 'exterior' ? '#f1f5f9' : styleWallColor}
            roughness={0.8}
            metalness={0.01}
          />
        </mesh>
      </group>
    );
  }

  // Full solid wall segment:
  return (
    <group position={[midX, effectiveWallHeight / 2, midZ]} rotation={[0, -angle, 0]}>
      <mesh castShadow receiveShadow>
        <boxGeometry args={[length, effectiveWallHeight, thickness]} />
        <meshStandardMaterial
          color={wall.type === 'exterior' ? '#f1f5f9' : styleWallColor}
          roughness={0.85}
          metalness={0.01}
        />
      </mesh>
      {/* Dark Architectural Baseboard Plinth */}
      <mesh position={[0, -effectiveWallHeight / 2 + 0.06, 0]}>
        <boxGeometry args={[length + 0.005, 0.12, thickness + 0.018]} />
        <meshStandardMaterial color="#334155" roughness={0.5} />
      </mesh>
    </group>
  );
};

// ── ARCHITECTURAL CEILING WITH COVE LIGHTING & RECESSED MAGNETIC TRACKS ────────
const GrandCeiling3D: React.FC<{
  buildingBounds: { minX: number; maxX: number; minY: number; maxY: number };
  scale: number;
  wallHeight: number;
  enabled: boolean;
  style: InteriorStyle;
}> = ({ buildingBounds, scale, wallHeight, enabled, style }) => {
  const bW = Math.max((buildingBounds.maxX - buildingBounds.minX) * scale + 2, 20);
  const bD = Math.max((buildingBounds.maxY - buildingBounds.minY) * scale + 2, 24);
  const woodCeiling = useMemo(() => createWoodCeilingTexture(style), [style]);

  if (!enabled) return null;

  return (
    <group position={[0, wallHeight, 0]}>
      {/* Warm Clean Architectural Ceiling (matching reference photo in Modern style, wood planks in Scandinavian/Alpine) */}
      <mesh rotation={[Math.PI / 2, 0, 0]} receiveShadow>
        <planeGeometry args={[bW, bD]} />
        <meshStandardMaterial
          map={style === 'modern' ? undefined : woodCeiling}
          color={style === 'modern' ? '#f3ede5' : undefined}
          roughness={0.8}
          side={THREE.DoubleSide}
        />
      </mesh>

      {/* Recessed Magnetic Black Track Channels running down the room */}
      {[-2.2, 2.2].map((tx, ti) => (
        <group key={`track-${ti}`} position={[tx, -0.01, 0]}>
          <mesh rotation={[Math.PI / 2, 0, 0]}>
            <planeGeometry args={[0.05, bD * 0.9]} />
            <meshStandardMaterial color="#0b0d10" roughness={0.3} metalness={0.8} />
          </mesh>
          {/* Micro warm track pinhole spotlights */}
          {[-5, -2, 1, 4].map((pz, pi) => (
            <mesh key={`pinh-${pi}`} position={[0, -0.01, pz]} rotation={[Math.PI / 2, 0, 0]}>
              <circleGeometry args={[0.02, 16]} />
              <meshBasicMaterial color="#fffbeb" />
            </mesh>
          ))}
        </group>
      ))}

      {/* Warm Indirect LED Perimeter Cove Lighting Strips along both window edges */}
      {[-bW * 0.42, bW * 0.42].map((cx, ci) => (
        <group key={`cove-${ci}`} position={[cx, -0.04, 0]}>
          <mesh rotation={[Math.PI / 2, 0, 0]}>
            <planeGeometry args={[0.16, bD * 0.92]} />
            <meshBasicMaterial color="#fed7aa" />
          </mesh>
          <pointLight position={[0, -0.25, -2.5]} color="#fed7aa" intensity={2.8} distance={8} decay={1.8} />
          <pointLight position={[0, -0.25, 0]} color="#fed7aa" intensity={2.4} distance={8} decay={1.8} />
          <pointLight position={[0, -0.25, 2.5]} color="#fed7aa" intensity={2.8} distance={8} decay={1.8} />
        </group>
      ))}
    </group>
  );
};

// ── SPIRAL STAIRCASE ──────────────────────────────────────────────────────────
const SpiralStaircase3D: React.FC<{
  stair: StaircaseSymbol;
  scale: number;
  centerX: number;
  centerZ: number;
  effectiveWallHeight: number;
}> = ({ stair, scale, centerX, centerZ, effectiveWallHeight }) => {
  const origX = (stair.position.x - centerX) * scale;
  const origZ = (stair.position.y - centerZ) * scale;
  const radius = Math.max((stair.radius || 18) * scale, 0.85);
  const stepsCount = 14;

  return (
    <group position={[origX, 0, origZ]}>
      <mesh position={[0, effectiveWallHeight / 2, 0]} castShadow>
        <cylinderGeometry args={[0.08, 0.08, effectiveWallHeight, 16]} />
        <meshStandardMaterial color="#0f172a" roughness={0.3} metalness={0.8} />
      </mesh>
      {Array.from({ length: stepsCount }).map((_, i) => {
        const t = i / stepsCount;
        const y = t * effectiveWallHeight * 0.88;
        const angle = t * Math.PI * 1.5;
        const stepLength = radius * 0.95;

        return (
          <group key={`step-${i}`} position={[0, y, 0]} rotation={[0, angle, 0]}>
            <mesh position={[stepLength / 2, 0.02, 0]} castShadow receiveShadow>
              <boxGeometry args={[stepLength, 0.04, 0.28]} />
              <meshStandardMaterial color="#b45309" roughness={0.4} metalness={0.05} />
            </mesh>
          </group>
        );
      })}
    </group>
  );
};

// ── ROOM FLOOR (Wide-Plank Honey Oak Hardwood) ────────────────────────────────
const Room3D: React.FC<{
  room: RoomGeometry;
  scale: number;
  centerX: number;
  centerZ: number;
  isSelected: boolean;
  isHovered: boolean;
  viewMode: 'dollhouse' | 'room';
  floorTexture: THREE.CanvasTexture;
  teakDeckTexture: THREE.CanvasTexture;
  tileFloorTexture: THREE.CanvasTexture;
  onSelect: () => void;
  onHover: (hovered: boolean) => void;
  onFloorPointerMove?: (point: THREE.Vector3) => void;
}> = ({
  room,
  scale,
  centerX,
  centerZ,
  isSelected,
  isHovered,
  viewMode,
  floorTexture,
  teakDeckTexture,
  tileFloorTexture,
  onSelect,
  onHover,
  onFloorPointerMove,
}) => {
  const shape = useMemo(() => {
    if (!room.boundary || room.boundary.length < 3) return null;
    const s = new THREE.Shape();
    room.boundary.forEach((p: Point2D, idx: number) => {
      const sx = (p.x - centerX) * scale;
      const sy = -((p.y - centerZ) * scale);
      if (idx === 0) s.moveTo(sx, sy);
      else s.lineTo(sx, sy);
    });
    s.closePath();
    return s;
  }, [room.boundary, scale, centerX, centerZ]);

  const activeFloorTexture = useMemo(() => {
    const name = (room.name || '').toLowerCase();
    if (name.includes('sitout') || name.includes('balcony') || name.includes('terrace') || name.includes('veranda')) {
      return teakDeckTexture;
    }
    if (name.includes('drawing') || name.includes('bath') || name.includes('toilet') || name.includes('wet') || name.includes('wash') || name.includes('store')) {
      return tileFloorTexture;
    }
    return floorTexture;
  }, [room.name, teakDeckTexture, tileFloorTexture, floorTexture]);

  if (!shape) return null;

  return (
    <group>
      <mesh
        rotation={[-Math.PI / 2, 0, 0]}
        position={[0, 0.015, 0]}
        receiveShadow
        onPointerOver={(e) => {
          e.stopPropagation();
          onHover(true);
        }}
        onPointerOut={() => onHover(false)}
        onPointerMove={(e) => {
          if (onFloorPointerMove) onFloorPointerMove(e.point);
        }}
        onClick={(e) => {
          e.stopPropagation();
          onSelect();
        }}
      >
        <shapeGeometry args={[shape]} />
        <meshStandardMaterial
          map={activeFloorTexture}
          roughness={0.25}
          metalness={0.03}
        />
      </mesh>

      {viewMode === 'dollhouse' && (isSelected || isHovered) && (
        <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, 0.02, 0]}>
          <shapeGeometry args={[shape]} />
          <meshBasicMaterial color="#38bdf8" transparent opacity={isSelected ? 0.25 : 0.12} />
        </mesh>
      )}
    </group>
  );
};

// ── ARCHITECTURAL DOORS (Clean White Planner 5D Frames & Swung-Open Door Leafs) ─
const Door3D: React.FC<{
  door: DoorSymbol;
  scale: number;
  centerX: number;
  centerZ: number;
  walls: SplitWallSegment[];
}> = ({ door, scale, centerX, centerZ, walls }) => {
  const origX = (door.position.x - centerX) * scale;
  const origZ = (door.position.y - centerZ) * scale;
  const doorWidth = Math.max((door.width || 36) * scale, 0.9);

  let bestAngle = 0;
  let minWallDist = Infinity;
  let wallThickness = 0.16;

  walls.forEach((w) => {
    const x1 = (w.start.x - centerX) * scale;
    const z1 = (w.start.y - centerZ) * scale;
    const x2 = (w.end.x - centerX) * scale;
    const z2 = (w.end.y - centerZ) * scale;

    const dx = x2 - x1;
    const dz = z2 - z1;
    const lenSq = dx * dx + dz * dz;
    if (lenSq < 0.001) return;

    const t = Math.max(0, Math.min(1, ((origX - x1) * dx + (origZ - z1) * dz) / lenSq));
    const projX = x1 + t * dx;
    const projZ = z1 + t * dz;
    const dist = Math.hypot(origX - projX, origZ - projZ);

    if (dist < minWallDist) {
      minWallDist = dist;
      bestAngle = Math.atan2(dz, dx);
      wallThickness = Math.max((w.thickness || 4) * scale, 0.14);
    }
  });

  return (
    <group position={[origX, 0, origZ]} rotation={[0, -bestAngle, 0]}>
      {/* Clean White Architectural Door Jambs (Planner 5D Style) */}
      <mesh position={[-doorWidth / 2, 1.05, 0]} castShadow>
        <boxGeometry args={[0.06, 2.1, wallThickness + 0.02]} />
        <meshStandardMaterial color="#f8fafc" roughness={0.5} />
      </mesh>
      <mesh position={[doorWidth / 2, 1.05, 0]} castShadow>
        <boxGeometry args={[0.06, 2.1, wallThickness + 0.02]} />
        <meshStandardMaterial color="#f8fafc" roughness={0.5} />
      </mesh>
      <mesh position={[0, 2.1, 0]} castShadow>
        <boxGeometry args={[doorWidth + 0.12, 0.06, wallThickness + 0.02]} />
        <meshStandardMaterial color="#f8fafc" roughness={0.5} />
      </mesh>
      {/* Swung Open Door Leaf (Swung ~75° inwards like Planner 5D Image 1) */}
      <group position={[-doorWidth / 2 + 0.03, 1.05, 0]} rotation={[0, -1.3, 0]}>
        <mesh position={[doorWidth / 2 - 0.03, 0, 0]} castShadow>
          <boxGeometry args={[doorWidth - 0.06, 2.05, 0.04]} />
          <meshStandardMaterial color="#ffffff" roughness={0.4} />
        </mesh>
        {/* Sleek Modern Black Door Lever Handle */}
        <mesh position={[doorWidth - 0.12, 0, 0.03]}>
          <boxGeometry args={[0.02, 0.12, 0.035]} />
          <meshStandardMaterial color="#0f172a" metalness={0.9} roughness={0.2} />
        </mesh>
      </group>
    </group>
  );
};

// ── PLANNER 5D GREEN WIREFRAME SELECTION BOUNDING BOX ─────────────────────────
const Planner5DSelectionBoundingBox3D: React.FC<{
  position: [number, number, number];
  size: [number, number, number];
  rotationY?: number;
}> = ({ position, size, rotationY = 0 }) => {
  const [w, h, d] = size;
  return (
    <group position={position} rotation={[0, rotationY, 0]}>
      {/* Bright Green Wireframe Box (Matching Planner 5D Screenshot Exactly!) */}
      <lineSegments>
        <edgesGeometry args={[new THREE.BoxGeometry(w, h, d)]} />
        <lineBasicMaterial color="#22c55e" linewidth={2.5} />
      </lineSegments>
      {/* Subtle green glass tint */}
      <mesh>
        <boxGeometry args={[w, h, d]} />
        <meshBasicMaterial color="#22c55e" transparent opacity={0.06} />
      </mesh>
    </group>
  );
};

// ── ARCHITECTURAL WINDOWS ─────────────────────────────────────────────────────
const Window3D: React.FC<{
  win: WindowSymbol;
  scale: number;
  centerX: number;
  centerZ: number;
  walls: WallSegment[];
}> = ({ win, scale, centerX, centerZ, walls }) => {
  const origX = (win.position.x - centerX) * scale;
  const origZ = (win.position.y - centerZ) * scale;
  const width = Math.max((win.width || 32) * scale, 0.95);

  let bestAngle = 0;
  let minWallDist = Infinity;
  let wallThickness = 0.16;

  walls.forEach((w: WallSegment) => {
    const x1 = (w.start.x - centerX) * scale;
    const z1 = (w.start.y - centerZ) * scale;
    const x2 = (w.end.x - centerX) * scale;
    const z2 = (w.end.y - centerZ) * scale;

    const dx = x2 - x1;
    const dz = z2 - z1;
    const lenSq = dx * dx + dz * dz;
    if (lenSq < 0.001) return;

    const t = Math.max(0, Math.min(1, ((origX - x1) * dx + (origZ - z1) * dz) / lenSq));
    const projX = x1 + t * dx;
    const projZ = z1 + t * dz;
    const dist = Math.hypot(origX - projX, origZ - projZ);

    if (dist < minWallDist) {
      minWallDist = dist;
      bestAngle = Math.atan2(dz, dx);
      wallThickness = Math.max((w.thickness || 4) * scale, 0.14);
    }
  });

  return (
    <group position={[origX, 1.4, origZ]} rotation={[0, -bestAngle, 0]}>
      <mesh castShadow>
        <boxGeometry args={[width, 1.5, wallThickness + 0.02]} />
        <meshStandardMaterial color="#0f172a" roughness={0.3} metalness={0.4} />
      </mesh>
      <mesh>
        <boxGeometry args={[width - 0.12, 1.38, 0.02]} />
        <meshStandardMaterial color="#bfdbfe" transparent opacity={0.32} roughness={0.05} metalness={0.9} />
      </mesh>
      <pointLight position={[0, 0, 0.4]} color="#fffbeb" intensity={0.6} distance={2.5} />
    </group>
  );
};

// ── PHOTO-REALISTIC DESIGNER STAGING (Matching Uploaded Image Exactly!) ───────
const PhotorealisticDesignerStaging3D: React.FC<{
  rooms: RoomGeometry[];
  scale: number;
  centerX: number;
  centerZ: number;
  style: InteriorStyle;
}> = ({ rooms, scale, centerX, centerZ, style }) => {
  const p = STYLE_PALETTES[style];

  // Procedural Materials
  const rugTexture = useMemo(() => createRugTexture(), []);
  const sofaTexture = useMemo(() => createLinenFabricTexture(p.sofaColor), [p.sofaColor]);
  const oakTexture = useMemo(() => createNaturalOakTexture(), []);
  const calacattaTexture = useMemo(() => createCalacattaMarbleTexture(), []);
  const boucleTexture = useMemo(() => createLinenFabricTexture('#eae5de'), []);
  const darkMarbleTexture = useMemo(() => createDarkMarbleTexture(), []);

  // Helper to compute 3D bounds for any room
  const getRoomBounds = (room: RoomGeometry) => {
    let minX = Infinity, maxX = -Infinity, minY = Infinity, maxY = -Infinity;
    if (room.boundary && room.boundary.length > 0) {
      room.boundary.forEach((pt: Point2D) => {
        if (pt.x < minX) minX = pt.x;
        if (pt.x > maxX) maxX = pt.x;
        if (pt.y < minY) minY = pt.y;
        if (pt.y > maxY) maxY = pt.y;
      });
    } else if (room.label_position) {
      minX = room.label_position.x - 30;
      maxX = room.label_position.x + 30;
      minY = room.label_position.y - 30;
      maxY = room.label_position.y + 30;
    }

    const xMin3d = (minX - centerX) * scale;
    const xMax3d = (maxX - centerX) * scale;
    const zMin3d = (minY - centerZ) * scale;
    const zMax3d = (maxY - centerZ) * scale;

    return {
      xMin3d,
      xMax3d,
      zMin3d,
      zMax3d,
      cx: (xMin3d + xMax3d) / 2,
      cz: (zMin3d + zMax3d) / 2,
      w: xMax3d - xMin3d,
      d: zMax3d - zMin3d,
    };
  };

  return (
    <group>
      {rooms.map((room) => {
        const b = getRoomBounds(room);
        const name = room.name.toLowerCase();

        // ──────────────────────────────────────────────────────────────────────
        // 1. LIVING HALL (Recreated EXACTLY from User's Reference Image!)
        // ──────────────────────────────────────────────────────────────────────
        if (name.includes('living') || name === 'living hall' || name === 'living') {
          return (
            <group key={`living-staging-${room.id}`}>
              {/* ── 1. ARCHITECTURAL STAIRCASE IN NORTH-EAST CORNER ('UP' in Blueprint / Planner 5D) ── */}
              <group position={[b.xMax3d - 1.25, 0, b.zMin3d + 0.35]}>
                {Array.from({ length: 12 }).map((_, stepIdx) => {
                  const stepY = stepIdx * 0.165;
                  const stepZ = stepIdx * 0.26;
                  return (
                    <group key={`stair-step-${stepIdx}`} position={[0, stepY, stepZ]}>
                      {/* Polished Solid Wood Tread */}
                      <mesh position={[0, 0.08, 0]} castShadow receiveShadow>
                        <boxGeometry args={[1.05, 0.045, 0.28]} />
                        <meshStandardMaterial map={oakTexture} roughness={0.38} />
                      </mesh>
                      {/* Clean White Riser */}
                      <mesh position={[0, 0, -0.13]} castShadow>
                        <boxGeometry args={[1.05, 0.15, 0.025]} />
                        <meshStandardMaterial color="#f8fafc" roughness={0.65} />
                      </mesh>
                      {/* Black Metal Handrail Spindle */}
                      <mesh position={[-0.48, 0.48, 0]} castShadow>
                        <cylinderGeometry args={[0.014, 0.014, 0.82, 8]} />
                        <meshStandardMaterial color="#0f172a" roughness={0.3} metalness={0.85} />
                      </mesh>
                    </group>
                  );
                })}
                {/* Continuous Slanted Solid Wood Handrail */}
                <mesh position={[-0.48, 1.38, 1.42]} rotation={[Math.atan2(12 * 0.165, 12 * 0.26), 0, 0]}>
                  <boxGeometry args={[0.065, 0.065, Math.hypot(12 * 0.165, 12 * 0.26)]} />
                  <meshStandardMaterial color="#854d0e" roughness={0.4} />
                </mesh>
              </group>

              {/* ── 2. NORTH WALL TV FEATURE UNIT (Matching 'Tv Unit' in Blueprint / Planner 5D) ── */}
              <group position={[b.cx - 0.6, 0, b.zMin3d + 0.18]}>
                {/* Italian Marble / Wood Wall Panel */}
                <mesh position={[0, 1.45, 0]} castShadow receiveShadow>
                  <boxGeometry args={[3.2, 2.7, 0.05]} />
                  <meshStandardMaterial map={calacattaTexture} roughness={0.2} metalness={0.06} />
                </mesh>
                {/* Flush Wall-Mounted 85" Flat Screen TV */}
                <mesh position={[0, 1.55, 0.06]} castShadow>
                  <boxGeometry args={[2.0, 1.15, 0.035]} />
                  <meshStandardMaterial color="#0b0d10" roughness={0.1} metalness={0.92} />
                </mesh>
                {/* Floating Media Credenza Console */}
                <mesh position={[0, 0.38, 0.22]} castShadow receiveShadow>
                  <boxGeometry args={[2.8, 0.4, 0.42]} />
                  <meshStandardMaterial map={oakTexture} roughness={0.4} />
                </mesh>
                {/* Warm Backlight */}
                <pointLight position={[0, 1.55, 0.2]} color="#fed7aa" intensity={1.6} distance={3.8} />
              </group>

              {/* ── 3. SEATING LOUNGE (Matching Planner 5D Image 2) ── */}
              {/* Soft Neutral Area Rug */}
              <mesh position={[b.cx - 0.4, 0.02, b.cz + 0.3]} rotation={[-Math.PI / 2, 0, 0]} receiveShadow>
                <planeGeometry args={[4.6, 3.6]} />
                <meshStandardMaterial map={rugTexture} roughness={0.94} />
              </mesh>

              {/* 3-Seater Family Sofa (Cream / Beige Fabric) */}
              <group position={[b.cx - 0.4, 0, b.cz + 1.25]}>
                {/* Sofa Seat Base */}
                <mesh position={[0, 0.22, 0]} castShadow receiveShadow>
                  <boxGeometry args={[2.4, 0.36, 0.95]} />
                  <meshStandardMaterial color="#e2d9cc" roughness={0.82} />
                </mesh>
                {/* Backrest */}
                <mesh position={[0, 0.52, 0.38]} castShadow>
                  <boxGeometry args={[2.4, 0.44, 0.22]} />
                  <meshStandardMaterial color="#e2d9cc" roughness={0.82} />
                </mesh>
                {/* Armrests */}
                {[-1.14, 1.14].map((ax, ai) => (
                  <mesh key={`larm-${ai}`} position={[ax, 0.4, 0]} castShadow>
                    <boxGeometry args={[0.18, 0.36, 0.95]} />
                    <meshStandardMaterial color="#e2d9cc" roughness={0.82} />
                  </mesh>
                ))}
                {/* Plump Cushions */}
                {[-0.65, 0, 0.65].map((cx, ci) => (
                  <mesh key={`lcush-${ci}`} position={[cx, 0.48, 0.16]} rotation={[-0.15, 0, 0]} castShadow>
                    <boxGeometry args={[0.58, 0.36, 0.16]} />
                    <meshStandardMaterial color="#ede7df" roughness={0.85} />
                  </mesh>
                ))}
              </group>

              {/* Rectangular Wood Coffee Table (Center) */}
              <group position={[b.cx - 0.4, 0, b.cz + 0.15]}>
                <mesh position={[0, 0.22, 0]} castShadow receiveShadow>
                  <boxGeometry args={[1.4, 0.08, 0.75]} />
                  <meshStandardMaterial map={oakTexture} roughness={0.35} />
                </mesh>
                {[-0.55, 0.55].map((tx) =>
                  [-0.28, 0.28].map((tz) => (
                    <mesh key={`tleg-${tx}-${tz}`} position={[tx, 0.1, tz]} castShadow>
                      <boxGeometry args={[0.07, 0.2, 0.07]} />
                      <meshStandardMaterial map={oakTexture} roughness={0.4} />
                    </mesh>
                  ))
                )}
              </group>

              {/* Matching Slate Grey Armchair (Side) */}
              <group position={[b.cx + 1.25, 0, b.cz + 0.15]} rotation={[0, -Math.PI / 2, 0]}>
                <mesh position={[0, 0.22, 0]} castShadow receiveShadow>
                  <boxGeometry args={[0.95, 0.36, 0.92]} />
                  <meshStandardMaterial color="#475569" roughness={0.82} />
                </mesh>
                <mesh position={[0, 0.52, 0.36]} castShadow>
                  <boxGeometry args={[0.95, 0.44, 0.2]} />
                  <meshStandardMaterial color="#475569" roughness={0.82} />
                </mesh>
                {[-0.42, 0.42].map((ax, ai) => (
                  <mesh key={`chairarm-${ai}`} position={[ax, 0.4, 0]} castShadow>
                    <boxGeometry args={[0.16, 0.36, 0.92]} />
                    <meshStandardMaterial color="#475569" roughness={0.82} />
                  </mesh>
                ))}
              </group>
            </group>
          );
        }

        // ──────────────────────────────────────────────────────────────────────
        // 2. DINING ROOM (Enclosed strictly inside Dining Room bounds!)
        // ──────────────────────────────────────────────────────────────────────
        if (name.includes('dining')) {
          return (
            <group key={`dining-staging-${room.id}`} position={[b.cx, 0, b.cz]}>
              {/* Textured Wool Area Rug */}
              <mesh position={[0, 0.02, 0]} rotation={[-Math.PI / 2, 0, 0]} receiveShadow>
                <planeGeometry args={[Math.min(b.w * 0.82, 3.8), Math.min(b.d * 0.78, 3.2)]} />
                <meshStandardMaterial map={rugTexture} roughness={0.92} />
              </mesh>

              {/* Solid Live-Edge Walnut Dining Table */}
              <group position={[0, 0, 0]}>
                <mesh position={[0, 0.74, 0]} castShadow receiveShadow>
                  <boxGeometry args={[Math.min(b.w * 0.62, 2.2), 0.08, 1.05]} />
                  <meshStandardMaterial map={oakTexture} roughness={0.35} />
                </mesh>
                {/* Modern Splayed Black Steel Legs */}
                {[-0.85, 0.85].map((lx) =>
                  [-0.38, 0.38].map((lz) => (
                    <mesh key={`dleg-${lx}-${lz}`} position={[lx, 0.35, lz]} rotation={[0.05 * Math.sign(lz), 0, -0.05 * Math.sign(lx)]} castShadow>
                      <boxGeometry args={[0.06, 0.7, 0.06]} />
                      <meshStandardMaterial color="#18181b" roughness={0.4} metalness={0.7} />
                    </mesh>
                  ))
                )}

                {/* Table Dinner Place Settings */}
                {[-0.55, 0, 0.55].map((px, pi) => (
                  <React.Fragment key={`pl-${pi}`}>
                    {/* North Side Settings */}
                    <mesh position={[px, 0.79, -0.3]} receiveShadow>
                      <cylinderGeometry args={[0.13, 0.13, 0.015, 20]} />
                      <meshStandardMaterial color="#f8fafc" roughness={0.25} />
                    </mesh>
                    <mesh position={[px + 0.16, 0.83, -0.3]} castShadow>
                      <cylinderGeometry args={[0.035, 0.025, 0.09, 12]} />
                      <meshStandardMaterial color="#ffffff" transparent opacity={0.65} roughness={0.1} />
                    </mesh>
                    {/* South Side Settings */}
                    <mesh position={[px, 0.79, 0.3]} receiveShadow>
                      <cylinderGeometry args={[0.13, 0.13, 0.015, 20]} />
                      <meshStandardMaterial color="#f8fafc" roughness={0.25} />
                    </mesh>
                    <mesh position={[px + 0.16, 0.83, 0.3]} castShadow>
                      <cylinderGeometry args={[0.035, 0.025, 0.09, 12]} />
                      <meshStandardMaterial color="#ffffff" transparent opacity={0.65} roughness={0.1} />
                    </mesh>
                  </React.Fragment>
                ))}
              </group>

              {/* 6 Sculpted Upholstered Dining Chairs */}
              {[-0.58, 0, 0.58].map((cx, i) =>
                [-0.68, 0.68].map((cz, j) => (
                  <group key={`dchair-${i}-${j}`} position={[cx, 0, cz]} rotation={[0, j === 0 ? 0 : Math.PI, 0]}>
                    <mesh position={[0, 0.45, 0]} castShadow>
                      <boxGeometry args={[0.45, 0.08, 0.44]} />
                      <meshStandardMaterial color="#f4efe8" roughness={0.8} />
                    </mesh>
                    <mesh position={[0, 0.72, -0.19]} castShadow>
                      <boxGeometry args={[0.44, 0.46, 0.06]} />
                      <meshStandardMaterial color="#f4efe8" roughness={0.8} />
                    </mesh>
                    {/* Slim Legs */}
                    {[-0.18, 0.18].map((chx) =>
                      [-0.18, 0.18].map((chz) => (
                        <mesh key={`cl-${chx}-${chz}`} position={[chx, 0.22, chz]} castShadow>
                          <cylinderGeometry args={[0.015, 0.012, 0.44, 8]} />
                          <meshStandardMaterial color="#18181b" roughness={0.4} metalness={0.7} />
                        </mesh>
                      ))
                    )}
                  </group>
                ))
              )}

              {/* Modern Linear Branch Chandelier */}
              <group position={[0, 2.35, 0]}>
                <mesh position={[0, 0, 0]}>
                  <boxGeometry args={[1.5, 0.03, 0.05]} />
                  <meshStandardMaterial color="#d97706" metalness={0.85} roughness={0.2} />
                </mesh>
                {[-0.55, -0.18, 0.18, 0.55].map((gx, gi) => (
                  <mesh key={`gorb-${gi}`} position={[gx, -0.08, (gi % 2 === 0 ? 0.08 : -0.08)]}>
                    <sphereGeometry args={[0.09, 16, 16]} />
                    <meshStandardMaterial color="#fffbeb" roughness={0.15} emissive="#fff1cc" emissiveIntensity={0.8} />
                  </mesh>
                ))}
                <pointLight position={[0, -0.2, 0]} color="#fff1cc" intensity={2.6} distance={5.0} />
              </group>

              {/* Wall Credenza Sideboard with Decor & Lamp */}
              <group position={[-b.w * 0.36, 0, 0]} rotation={[0, Math.PI / 2, 0]}>
                <mesh position={[0, 0.42, 0]} castShadow receiveShadow>
                  <boxGeometry args={[1.6, 0.82, 0.42]} />
                  <meshStandardMaterial map={oakTexture} roughness={0.4} />
                </mesh>
                {/* Ceramic Vase on Credenza */}
                <mesh position={[0.4, 0.96, 0]} castShadow>
                  <cylinderGeometry args={[0.07, 0.1, 0.26, 16]} />
                  <meshStandardMaterial color="#e2e8f0" roughness={0.3} />
                </mesh>
              </group>
            </group>
          );
        }

        // ──────────────────────────────────────────────────────────────────────
        // 3. KITCHEN (Recreated exactly like Instagram Video Demo & Reference Image!)
        // ──────────────────────────────────────────────────────────────────────
        if (name === 'kitchen' || (name.includes('kitchen') && !name.includes('wet'))) {
          const islandW = Math.min(b.w * 0.65, 3.2);
          const islandD = 1.15;
          const islandH = 0.94;

          return (
            <group key={`kitchen-staging-${room.id}`} position={[b.cx, 0, b.cz]}>
              {/* ── GRAND CALACATTA MARBLE WATERFALL ISLAND ── */}
              <group position={[0, 0, 0]}>
                {/* Horizontal Island Countertop Slab */}
                <mesh position={[0, islandH - 0.04, 0]} castShadow receiveShadow>
                  <boxGeometry args={[islandW, 0.08, islandD]} />
                  <meshStandardMaterial map={calacattaTexture} roughness={0.2} metalness={0.06} />
                </mesh>
                {/* Left Mitered Waterfall End Panel to Floor */}
                <mesh position={[-islandW / 2 + 0.04, islandH / 2, 0]} castShadow receiveShadow>
                  <boxGeometry args={[0.08, islandH, islandD]} />
                  <meshStandardMaterial map={calacattaTexture} roughness={0.2} metalness={0.06} />
                </mesh>
                {/* Right Mitered Waterfall End Panel to Floor */}
                <mesh position={[islandW / 2 - 0.04, islandH / 2, 0]} castShadow receiveShadow>
                  <boxGeometry args={[0.08, islandH, islandD]} />
                  <meshStandardMaterial map={calacattaTexture} roughness={0.2} metalness={0.06} />
                </mesh>
                {/* Recessed Island Cabinet Base in Warm Wood */}
                <mesh position={[0, islandH / 2 - 0.04, -0.08]} castShadow>
                  <boxGeometry args={[islandW - 0.18, islandH - 0.08, islandD - 0.28]} />
                  <meshStandardMaterial map={oakTexture} roughness={0.4} />
                </mesh>

                {/* Flush Black Glass Induction Cooktop */}
                <group position={[-islandW * 0.22, islandH + 0.005, -0.04]}>
                  <mesh receiveShadow>
                    <boxGeometry args={[0.82, 0.01, 0.52]} />
                    <meshStandardMaterial color="#090d16" roughness={0.08} metalness={0.9} />
                  </mesh>
                  {/* Glowing cooking burner ring */}
                  <mesh position={[0, 0.008, 0]} rotation={[-Math.PI / 2, 0, 0]}>
                    <ringGeometry args={[0.12, 0.13, 24]} />
                    <meshBasicMaterial color="#ea580c" />
                  </mesh>
                </group>

                {/* Undermount Black Sink with Tall Matte Black Gooseneck Faucet */}
                <group position={[islandW * 0.22, islandH + 0.005, -0.04]}>
                  <mesh>
                    <boxGeometry args={[0.62, 0.01, 0.44]} />
                    <meshStandardMaterial color="#1e293b" roughness={0.2} metalness={0.8} />
                  </mesh>
                  {/* Gooseneck Faucet */}
                  <mesh position={[0, 0.22, -0.18]}>
                    <cylinderGeometry args={[0.016, 0.018, 0.42, 16]} />
                    <meshStandardMaterial color="#18181b" metalness={0.85} roughness={0.2} />
                  </mesh>
                </group>

                {/* Countertop Staging: Ceramic Fruit Bowl & Marble Cutting Board */}
                <mesh position={[0, islandH + 0.06, 0.1]} castShadow>
                  <cylinderGeometry args={[0.16, 0.11, 0.1, 20]} />
                  <meshStandardMaterial color="#f8fafc" roughness={0.3} />
                </mesh>
              </group>

              {/* 4 Contemporary Upholstered Barstools */}
              {[-islandW * 0.36, -islandW * 0.12, islandW * 0.12, islandW * 0.36].map((bx, bi) => (
                <group key={`k-stool-${bi}`} position={[bx, 0, islandD / 2 + 0.38]}>
                  {/* Padded Seat Cushion */}
                  <mesh position={[0, 0.68, 0]} castShadow>
                    <cylinderGeometry args={[0.22, 0.2, 0.1, 24]} />
                    <meshStandardMaterial color="#f4efe8" roughness={0.8} />
                  </mesh>
                  {/* Slim Black Metal Stool Legs */}
                  {[0, 1.57, 3.14, 4.71].map((ang, ai) => (
                    <mesh
                      key={`stleg-${ai}`}
                      position={[Math.sin(ang) * 0.14, 0.34, Math.cos(ang) * 0.14]}
                      rotation={[Math.cos(ang) * 0.06, 0, -Math.sin(ang) * 0.06]}
                      castShadow
                    >
                      <cylinderGeometry args={[0.012, 0.01, 0.66, 8]} />
                      <meshStandardMaterial color="#18181b" metalness={0.8} roughness={0.3} />
                    </mesh>
                  ))}
                  {/* Footrest Ring */}
                  <mesh position={[0, 0.22, 0]} rotation={[-Math.PI / 2, 0, 0]}>
                    <torusGeometry args={[0.14, 0.008, 8, 24]} />
                    <meshStandardMaterial color="#18181b" metalness={0.8} />
                  </mesh>
                </group>
              ))}

              {/* Trio of Minimalist Cylindrical Black Pendant Lights hanging from Wood Ceiling */}
              {[-0.65, 0, 0.65].map((px, pi) => (
                <group key={`k-pend-${pi}`} position={[px, 2.5, 0]}>
                  {/* Thin suspension cord */}
                  <mesh position={[0, 0.45, 0]}>
                    <cylinderGeometry args={[0.004, 0.004, 0.9, 8]} />
                    <meshStandardMaterial color="#18181b" />
                  </mesh>
                  {/* Cylindrical shade */}
                  <mesh position={[0, -0.15, 0]} castShadow>
                    <cylinderGeometry args={[0.06, 0.06, 0.32, 20]} />
                    <meshStandardMaterial color="#18181b" roughness={0.3} metalness={0.8} />
                  </mesh>
                  {/* Glowing lens tip */}
                  <mesh position={[0, -0.32, 0]}>
                    <circleGeometry args={[0.055, 16]} />
                    <meshBasicMaterial color="#fffbeb" />
                  </mesh>
                  <spotLight position={[0, -0.33, 0]} angle={Math.PI / 5} penumbra={0.6} intensity={2.2} color="#fff1cc" distance={4} />
                </group>
              ))}

              {/* Rear Full-Height Wood Pantry Cabinetry with Double Wall Ovens */}
              <group position={[0, 0, -b.d * 0.38]}>
                {/* Seamless flat-panel cabinetry block */}
                <mesh position={[0, 1.45, 0]} castShadow receiveShadow>
                  <boxGeometry args={[Math.min(b.w * 0.85, 3.8), 2.9, 0.65]} />
                  <meshStandardMaterial map={oakTexture} roughness={0.45} />
                </mesh>
                {/* Integrated Black Glass Double Wall Ovens */}
                <group position={[0.6, 1.35, 0.34]}>
                  <mesh>
                    <boxGeometry args={[0.68, 1.15, 0.04]} />
                    <meshStandardMaterial color="#090d16" roughness={0.12} metalness={0.9} />
                  </mesh>
                  {/* Oven handle */}
                  <mesh position={[0, 0.18, 0.035]}>
                    <boxGeometry args={[0.5, 0.02, 0.02]} />
                    <meshStandardMaterial color="#d4d4d8" metalness={0.9} />
                  </mesh>
                </group>
                {/* Recessed Under-Cabinet Warm LED Strip */}
                <mesh position={[0, 0.92, 0.34]}>
                  <boxGeometry args={[Math.min(b.w * 0.82, 3.6), 0.03, 0.02]} />
                  <meshBasicMaterial color="#fed7aa" />
                </mesh>
                <pointLight position={[0, 0.9, 0.45]} color="#fed7aa" intensity={2.0} distance={3.5} />
              </group>
            </group>
          );
        }

        // ──────────────────────────────────────────────────────────────────────
        // 4. BEDROOMS (Bed 1 & Bed 2 - Symmetrical King Platform Bed against North wall)
        // ──────────────────────────────────────────────────────────────────────
        if (name.includes('bed')) {
          const bedHeadZ = b.zMin3d + 0.45;
          return (
            <group key={`bed-staging-${room.id}`}>
              {/* Plush Neutral Bedroom Area Rug */}
              <mesh position={[b.cx, 0.02, b.cz]} rotation={[-Math.PI / 2, 0, 0]} receiveShadow>
                <planeGeometry args={[Math.min(b.w * 0.82, 3.8), Math.min(b.d * 0.8, 3.4)]} />
                <meshStandardMaterial map={rugTexture} roughness={0.94} />
              </mesh>

              {/* King Platform Bed Group */}
              <group position={[b.cx, 0, bedHeadZ + 1.1]}>
                {/* Solid Wood Platform Base */}
                <mesh position={[0, 0.22, 0]} castShadow receiveShadow>
                  <boxGeometry args={[2.08, 0.38, 2.2]} />
                  <meshStandardMaterial map={oakTexture} roughness={0.5} />
                </mesh>
                {/* Crisp White Mattress with Soft Made Duvet */}
                <mesh position={[0, 0.48, 0.05]} castShadow receiveShadow>
                  <boxGeometry args={[1.94, 0.28, 2.05]} />
                  <meshStandardMaterial color="#fdfbf7" roughness={0.75} />
                </mesh>
                {/* Layered Textured Waffle Throw Blanket */}
                <mesh position={[0, 0.62, 0.65]} castShadow>
                  <boxGeometry args={[1.96, 0.08, 0.75]} />
                  <meshStandardMaterial map={sofaTexture} roughness={0.85} />
                </mesh>
                {/* Architectural Tall Padded Headboard */}
                <mesh position={[0, 1.05, -1.05]} castShadow>
                  <boxGeometry args={[2.3, 1.35, 0.18]} />
                  <meshStandardMaterial map={boucleTexture} roughness={0.85} />
                </mesh>

                {/* 4 Fluffy Sleeping Pillows + 2 Decorative Velvet Accent Cushions */}
                {[-0.55, 0.55].map((px, pi) => (
                  <React.Fragment key={`bpill-${pi}`}>
                    {/* Back Sleeping Pillows */}
                    <mesh position={[px, 0.68, -0.8]} rotation={[0.3, 0, 0]} castShadow>
                      <boxGeometry args={[0.66, 0.22, 0.45]} />
                      <meshStandardMaterial color="#ffffff" roughness={0.88} />
                    </mesh>
                    {/* Front Accent Velvet Cushion */}
                    <mesh position={[px, 0.66, -0.52]} rotation={[0.18, pi === 0 ? 0.1 : -0.1, 0]} castShadow>
                      <boxGeometry args={[0.48, 0.28, 0.18]} />
                      <meshStandardMaterial color={pi === 0 ? '#334155' : '#78350f'} roughness={0.7} />
                    </mesh>
                  </React.Fragment>
                ))}
              </group>

              {/* Twin Floating Solid Wood Nightstands with Glowing Lamps */}
              {[-1.45, 1.45].map((sideX, i) => (
                <group key={`b-nightstand-${i}`} position={[b.cx + sideX, 0, bedHeadZ + 0.35]}>
                  <mesh position={[0, 0.28, 0]} castShadow receiveShadow>
                    <boxGeometry args={[0.55, 0.46, 0.48]} />
                    <meshStandardMaterial map={oakTexture} roughness={0.45} />
                  </mesh>
                  {/* Designer Bedside Lamp with Glowing Shade */}
                  <group position={[0, 0.52, 0]}>
                    <mesh position={[0, 0.1, 0]} castShadow>
                      <cylinderGeometry args={[0.07, 0.09, 0.18, 16]} />
                      <meshStandardMaterial color="#18181b" roughness={0.3} metalness={0.8} />
                    </mesh>
                    <mesh position={[0, 0.28, 0]}>
                      <cylinderGeometry args={[0.14, 0.14, 0.22, 20]} />
                      <meshStandardMaterial color="#fffbeb" roughness={0.3} />
                    </mesh>
                    <pointLight position={[0, 0.28, 0]} color="#fff1cc" intensity={1.8} distance={3.5} />
                  </group>
                </group>
              ))}

              {/* Framed Canvas Artwork above Headboard with Picture Light */}
              <group position={[b.cx, 2.2, bedHeadZ + 0.04]}>
                <mesh castShadow>
                  <boxGeometry args={[1.6, 0.85, 0.04]} />
                  <meshStandardMaterial color="#090d16" roughness={0.2} metalness={0.8} />
                </mesh>
                <mesh position={[0, 0, 0.025]}>
                  <planeGeometry args={[1.5, 0.75]} />
                  <meshStandardMaterial color="#e2d9cc" roughness={0.6} />
                </mesh>
                {/* Warm Picture Light */}
                <pointLight position={[0, 0.45, 0.25]} color="#fff1cc" intensity={1.5} distance={2.5} />
              </group>
            </group>
          );
        }

        // ──────────────────────────────────────────────────────────────────────
        // 5. DRAWING HALL (Planner 5D Reference Matching User Image 1 Exactly!)
        // ──────────────────────────────────────────────────────────────────────
        if (name.includes('drawing')) {
          const loungeW = Math.min(b.w * 0.94, 5.2);
          const backWallZ = b.zMin3d + 0.05;

          return (
            <group key={`drawing-staging-${room.id}`}>
              {/* ── 1. NERO MARQUINA DARK VEINED MARBLE ACCENT WALL ── */}
              <group position={[b.cx, 0, backWallZ]}>
                <mesh position={[0, 1.6, 0.02]} castShadow receiveShadow>
                  <boxGeometry args={[loungeW, 3.2, 0.06]} />
                  <meshStandardMaterial map={darkMarbleTexture} roughness={0.22} metalness={0.08} />
                </mesh>

                {/* Overhead Spotlight Accentuating Dark Marble Wall */}
                <pointLight position={[0, 2.8, 0.8]} color="#ffffff" intensity={2.4} distance={5.5} />

                {/* ── CENTER 3-PANE WINDOW WITH BLACK VENETIAN BLINDS (Matching Image 1) ── */}
                <group position={[0, 1.85, 0.06]}>
                  {/* Outer White Window Sill & Casing */}
                  <mesh position={[0, 0, 0]} castShadow>
                    <boxGeometry args={[2.4, 1.25, 0.08]} />
                    <meshStandardMaterial color="#ffffff" roughness={0.3} />
                  </mesh>

                  {/* Glass Panes */}
                  {[-0.72, 0, 0.72].map((gx, gi) => (
                    <mesh key={`d-winpane-${gi}`} position={[gx, -0.05, 0.04]}>
                      <boxGeometry args={[0.66, 1.05, 0.02]} />
                      <meshStandardMaterial color="#94a3b8" transparent opacity={0.35} roughness={0.1} />
                    </mesh>
                  ))}

                  {/* Black Horizontal Venetian Blinds covering upper window */}
                  <group position={[0, 0.22, 0.08]}>
                    <mesh castShadow>
                      <boxGeometry args={[2.3, 0.65, 0.04]} />
                      <meshStandardMaterial color="#18181b" roughness={0.5} />
                    </mesh>
                    {/* Venetian Slat Lines */}
                    {[-0.25, -0.15, -0.05, 0.05, 0.15, 0.25].map((sy, si) => (
                      <mesh key={`slat-${si}`} position={[0, sy, 0.025]}>
                        <boxGeometry args={[2.28, 0.015, 0.02]} />
                        <meshStandardMaterial color="#09090b" roughness={0.3} />
                      </mesh>
                    ))}
                  </group>
                </group>
              </group>

              {/* ── 2. MODERN OFF-WHITE / CREAM 3-SEATER SOFA (Matching Image 1) ── */}
              <group position={[b.cx, 0, backWallZ + 1.2]}>
                {/* Main 3-Seater Cushion Base */}
                <mesh position={[0, 0.24, 0]} castShadow receiveShadow>
                  <boxGeometry args={[2.45, 0.36, 0.95]} />
                  <meshStandardMaterial color="#f4f4f5" roughness={0.7} />
                </mesh>

                {/* 3 Individual Seat Cushion Highlights */}
                {[-0.75, 0, 0.75].map((cx, ci) => (
                  <mesh key={`scush-${ci}`} position={[cx, 0.38, 0.05]} castShadow receiveShadow>
                    <boxGeometry args={[0.74, 0.12, 0.85]} />
                    <meshStandardMaterial color="#f8fafc" roughness={0.65} />
                  </mesh>
                ))}

                {/* Low Backrest */}
                <mesh position={[0, 0.54, -0.34]} castShadow>
                  <boxGeometry args={[2.45, 0.44, 0.22]} />
                  <meshStandardMaterial color="#f4f4f5" roughness={0.7} />
                </mesh>

                {/* Left Low Curved Armrest */}
                <group position={[-1.28, 0.32, 0]}>
                  <mesh castShadow>
                    <boxGeometry args={[0.22, 0.34, 0.98]} />
                    <meshStandardMaterial color="#f4f4f5" roughness={0.7} />
                  </mesh>
                </group>

                {/* Right Low Curved Armrest */}
                <group position={[1.28, 0.32, 0]}>
                  <mesh castShadow>
                    <boxGeometry args={[0.22, 0.34, 0.98]} />
                    <meshStandardMaterial color="#f4f4f5" roughness={0.7} />
                  </mesh>
                </group>
              </group>

              {/* ── 3. LOW RECTANGULAR NATURAL OAK COFFEE TABLE WITH SLED BASE ── */}
              <group position={[b.cx, 0, backWallZ + 2.05]}>
                {/* Oak Wood Top Slab */}
                <mesh position={[0, 0.26, 0]} castShadow receiveShadow>
                  <boxGeometry args={[1.2, 0.12, 0.65]} />
                  <meshStandardMaterial map={oakTexture} roughness={0.35} />
                </mesh>

                {/* Matte Black Metal Sled Runners */}
                {[-0.45, 0.45].map((sx, si) => (
                  <group key={`sled-${si}`} position={[sx, 0.1, 0]}>
                    {/* Vertical runner legs */}
                    <mesh position={[0, 0.05, -0.26]} castShadow>
                      <boxGeometry args={[0.035, 0.22, 0.035]} />
                      <meshStandardMaterial color="#18181b" metalness={0.7} roughness={0.3} />
                    </mesh>
                    <mesh position={[0, 0.05, 0.26]} castShadow>
                      <boxGeometry args={[0.035, 0.22, 0.035]} />
                      <meshStandardMaterial color="#18181b" metalness={0.7} roughness={0.3} />
                    </mesh>
                    {/* Floor sled base bar */}
                    <mesh position={[0, -0.05, 0]} castShadow>
                      <boxGeometry args={[0.035, 0.02, 0.55]} />
                      <meshStandardMaterial color="#18181b" metalness={0.7} roughness={0.3} />
                    </mesh>
                  </group>
                ))}
              </group>

              {/* ── 4. LEFT HEATHER GREY ARMCHAIR & PEDESTAL (Matching Image 1) ── */}
              <group position={[b.cx - 1.45, 0, backWallZ + 1.8]} rotation={[0, 0.38, 0]}>
                {/* Armchair Base */}
                <mesh position={[0, 0.24, 0]} castShadow receiveShadow>
                  <boxGeometry args={[0.88, 0.38, 0.88]} />
                  <meshStandardMaterial color="#64748b" roughness={0.75} />
                </mesh>
                {/* Backrest */}
                <mesh position={[0, 0.58, -0.32]} castShadow>
                  <boxGeometry args={[0.88, 0.48, 0.22]} />
                  <meshStandardMaterial color="#64748b" roughness={0.75} />
                </mesh>
                {/* Armrests */}
                <mesh position={[-0.38, 0.46, 0.04]} castShadow>
                  <boxGeometry args={[0.18, 0.36, 0.82]} />
                  <meshStandardMaterial color="#64748b" roughness={0.75} />
                </mesh>
                <mesh position={[0.38, 0.46, 0.04]} castShadow>
                  <boxGeometry args={[0.18, 0.36, 0.82]} />
                  <meshStandardMaterial color="#64748b" roughness={0.75} />
                </mesh>

                {/* Small Round Black Drink Pedestal behind chair */}
                <group position={[-0.45, 0, -0.45]}>
                  <mesh position={[0, 0.24, 0]} castShadow>
                    <cylinderGeometry args={[0.18, 0.18, 0.48, 24]} />
                    <meshStandardMaterial color="#18181b" roughness={0.4} />
                  </mesh>
                </group>
              </group>

              {/* ── 5. RIGHT SLATE GREY 2-SEATER CHAISE LOUNGE (Matching Image 1) ── */}
              <group position={[b.cx + 1.42, 0, backWallZ + 1.7]} rotation={[0, -0.25, 0]}>
                {/* Seat Cushion */}
                <mesh position={[0, 0.26, 0]} castShadow receiveShadow>
                  <boxGeometry args={[1.35, 0.32, 0.88]} />
                  <meshStandardMaterial color="#475569" roughness={0.75} />
                </mesh>
                {/* Low Backrest */}
                <mesh position={[0, 0.52, -0.34]} castShadow>
                  <boxGeometry args={[1.35, 0.42, 0.18]} />
                  <meshStandardMaterial color="#475569" roughness={0.75} />
                </mesh>
                {/* Slim Black Metal Tapered Legs */}
                {[-0.58, 0.58].map((lx, lxi) =>
                  [-0.36, 0.36].map((lz, lzi) => (
                    <mesh key={`ch-leg-${lxi}-${lzi}`} position={[lx, 0.08, lz]} castShadow>
                      <cylinderGeometry args={[0.018, 0.012, 0.18, 12]} />
                      <meshStandardMaterial color="#18181b" metalness={0.8} />
                    </mesh>
                  ))
                )}
              </group>

              {/* ── 6. RIGHT WALL DOORWAY & WINDOW WITH BLINDS (Matching Image 1) ── */}
              <group position={[b.xMax3d - 0.06, 0, backWallZ + 1.1]}>
                {/* Open White Door angled into hallway */}
                <mesh position={[-0.05, 1.2, 0.4]} rotation={[0, -1.1, 0]} castShadow>
                  <boxGeometry args={[0.88, 2.2, 0.04]} />
                  <meshStandardMaterial color="#f8fafc" roughness={0.4} />
                </mesh>
                {/* Black Lever Handle */}
                <mesh position={[-0.1, 1.1, 0.75]} rotation={[0, -1.1, 0]}>
                  <boxGeometry args={[0.04, 0.12, 0.03]} />
                  <meshStandardMaterial color="#18181b" metalness={0.8} />
                </mesh>
              </group>

              {/* Right Wall Window with Black Blinds */}
              <group position={[b.xMax3d - 0.05, 1.85, backWallZ + 2.4]} rotation={[0, -Math.PI / 2, 0]}>
                <mesh castShadow>
                  <boxGeometry args={[1.3, 1.1, 0.06]} />
                  <meshStandardMaterial color="#ffffff" roughness={0.3} />
                </mesh>
                <mesh position={[0, 0.15, 0.04]} castShadow>
                  <boxGeometry args={[1.2, 0.65, 0.04]} />
                  <meshStandardMaterial color="#18181b" roughness={0.5} />
                </mesh>
              </group>

              {/* ── 7. LEFT WALL TALL WARM WOOD WARDROBE / CABINET ── */}
              <group position={[b.xMin3d + 0.35, 1.45, backWallZ + 2.5]}>
                <mesh castShadow receiveShadow>
                  <boxGeometry args={[0.55, 2.7, 1.3]} />
                  <meshStandardMaterial map={oakTexture} roughness={0.4} />
                </mesh>
                {/* Vertical seam */}
                <mesh position={[0.28, 0, 0]}>
                  <boxGeometry args={[0.01, 2.65, 0.01]} />
                  <meshStandardMaterial color="#18181b" roughness={0.5} />
                </mesh>
              </group>
            </group>
          );
        }

        // ──────────────────────────────────────────────────────────────────────
        // 6. SACRED POOJA MANDIR
        // ──────────────────────────────────────────────────────────────────────
        if (name.includes('pooja')) {
          return (
            <group key={`pooja-staging-${room.id}`} position={[b.cx, 0, b.cz]}>
              <mesh position={[0, 0.02, 0]} rotation={[-Math.PI / 2, 0, 0]} receiveShadow>
                <planeGeometry args={[Math.min(b.w * 0.8, 2.4), Math.min(b.d * 0.8, 2.4)]} />
                <meshStandardMaterial map={rugTexture} roughness={0.9} />
              </mesh>
              {/* Teakwood Mandir Altar with Traditional Jali Lattice Top */}
              <group position={[0, 0, -b.d * 0.2]}>
                <mesh position={[0, 0.45, 0]} castShadow receiveShadow>
                  <boxGeometry args={[1.3, 0.85, 0.65]} />
                  <meshStandardMaterial color="#5c3818" roughness={0.4} />
                </mesh>
                <mesh position={[0, 1.15, 0]} castShadow>
                  <coneGeometry args={[0.38, 0.55, 8]} />
                  <meshStandardMaterial color="#d97706" metalness={0.85} roughness={0.2} />
                </mesh>
                {/* Brass Diya Lamps with Warm Sacred Flame */}
                {[-0.45, 0.45].map((dx, di) => (
                  <group key={`diya-${di}`} position={[dx, 0.9, 0.2]}>
                    <mesh castShadow>
                      <cylinderGeometry args={[0.07, 0.04, 0.08, 16]} />
                      <meshStandardMaterial color="#f59e0b" metalness={0.9} roughness={0.15} />
                    </mesh>
                    <pointLight position={[0, 0.1, 0]} color="#f59e0b" intensity={2.4} distance={3.2} />
                  </group>
                ))}
              </group>
            </group>
          );
        }

        // ──────────────────────────────────────────────────────────────────────
        // 7. LUXURY BATHROOMS
        // ──────────────────────────────────────────────────────────────────────
        if (name.includes('bath')) {
          return (
            <group key={`bath-staging-${room.id}`} position={[b.cx, 0, b.cz]}>
              {/* Floating Calacatta Marble Vanity with Undermount Sink */}
              <group position={[0, 0, -b.d * 0.26]}>
                <mesh position={[0, 0.55, 0]} castShadow receiveShadow>
                  <boxGeometry args={[Math.min(b.w * 0.65, 1.4), 0.42, 0.55]} />
                  <meshStandardMaterial map={calacattaTexture} roughness={0.2} metalness={0.05} />
                </mesh>
                {/* Matte Black Faucet */}
                <mesh position={[0, 0.86, -0.16]}>
                  <cylinderGeometry args={[0.016, 0.018, 0.22, 16]} />
                  <meshStandardMaterial color="#18181b" metalness={0.8} />
                </mesh>
                {/* Backlit LED Circular Halo Mirror */}
                <group position={[0, 1.42, -0.26]}>
                  <mesh rotation={[Math.PI / 2, 0, 0]} castShadow>
                    <cylinderGeometry args={[0.42, 0.42, 0.03, 32]} />
                    <meshStandardMaterial color="#f1f5f9" metalness={0.95} roughness={0.04} />
                  </mesh>
                  {/* Warm Halo Glow behind Mirror */}
                  <pointLight position={[0, 0, 0.1]} color="#fed7aa" intensity={2.2} distance={3.0} />
                </group>
              </group>
            </group>
          );
        }

        // ──────────────────────────────────────────────────────────────────────
        // 8. SITOUT / TERRACE PATIO
        // ──────────────────────────────────────────────────────────────────────
        if (name.includes('sitout') || name.includes('balcony') || name.includes('terrace')) {
          return (
            <group key={`sitout-staging-${room.id}`} position={[b.cx, 0, b.cz]}>
              {/* Teak Outdoor Lounge Chairs */}
              {[-0.65, 0.65].map((cx, ci) => (
                <group key={`so-chair-${ci}`} position={[cx, 0, 0]}>
                  <mesh position={[0, 0.32, 0]} castShadow>
                    <boxGeometry args={[0.7, 0.12, 0.7]} />
                    <meshStandardMaterial color="#9a6034" roughness={0.5} />
                  </mesh>
                  <mesh position={[0, 0.65, -0.32]} castShadow>
                    <boxGeometry args={[0.7, 0.55, 0.1]} />
                    <meshStandardMaterial color="#9a6034" roughness={0.5} />
                  </mesh>
                </group>
              ))}
              {/* Stone Coffee Table */}
              <mesh position={[0, 0.22, 0]} castShadow>
                <cylinderGeometry args={[0.35, 0.35, 0.08, 24]} />
                <meshStandardMaterial color="#78716c" roughness={0.6} />
              </mesh>
            </group>
          );
        }

        return null;
      })}
    </group>
  );
};

// ── CUSTOM USER PLACED FURNITURE ──────────────────────────────────────────────
const Furniture3D: React.FC<{
  placed: PlacedFurniture;
  isSelected: boolean;
  onSelect: () => void;
}> = ({ placed, isSelected, onSelect }) => {
  const spec = FURNITURE_CATALOG.find((s) => s.id === placed.specId);
  const w = spec?.width ?? 1;
  const d = spec?.depth ?? 1;
  const h = spec?.height ?? 0.8;
  const color = spec?.color || '#6366f1';

  return (
    <group
      position={[placed.x, 0, placed.z]}
      rotation={[0, placed.rotationY, 0]}
      onClick={(e) => {
        e.stopPropagation();
        onSelect();
      }}
    >
      <mesh position={[0, h / 2, 0]} castShadow receiveShadow>
        <boxGeometry args={[w, h, d]} />
        <meshStandardMaterial
          color={color}
          roughness={spec?.category === 'lighting' ? 0.2 : 0.6}
          metalness={spec?.category === 'lighting' ? 0.7 : 0.1}
          emissive={spec?.category === 'lighting' ? '#fffbeb' : '#000000'}
          emissiveIntensity={spec?.category === 'lighting' ? 0.8 : 0}
        />
      </mesh>
      {isSelected && (
        <mesh position={[0, 0.03, 0]} rotation={[-Math.PI / 2, 0, 0]}>
          <ringGeometry args={[Math.max(w, d) * 0.6, Math.max(w, d) * 0.72, 32]} />
          <meshBasicMaterial color="#38bdf8" side={THREE.DoubleSide} />
        </mesh>
      )}
    </group>
  );
};

// ── AI FLOORPLAN ROOM PLAN ANALYSIS & STAGING SPECIFICATIONS ──────────────────
export interface RoomAnalysisData {
  cadDims: string;
  sqft: number;
  focalWall: string;
  circulation: string;
  daylighting: string;
  rationale: string[];
  keyFurniture: { name: string; dims: string; spec: string }[];
}

export const ROOM_PLAN_ANALYSIS: Record<string, RoomAnalysisData> = {
  living: {
    cadDims: "33'9\" × 25'6\"",
    sqft: 860,
    focalWall: "North Wall: Italian Statuario Marble & Walnut Slatted TV Unit with 85\" 4K Screen (marked 'Tv Unit')",
    circulation: "North-East: Cantilevered wooden staircase with glass railing ('UP'); West: Arched access to Dining & Pooja; South: Open to Drawing Hall",
    daylighting: "East Wall: French windows (Fw) with sheer drapes; 2700K perimeter cove & brass chandelier",
    rationale: [
      "TV Unit placed on solid North wall per blueprint notation 'Tv Unit', providing optimal 14' viewing distance",
      "Staircase access 'UP' maintained clear in North-East corner without furniture obstruction",
      "Central circulation thoroughfare connects South entrance/Drawing Hall directly to Dining and Pooja",
      "Luxury U/L-shaped champagne greige sectional sofa anchors family conversation zone on polished marble floor"
    ],
    keyFurniture: [
      { name: "North Wall TV Unit", dims: "16'0\" W × 12'0\" H", spec: "Statuario Marble, Fluted Walnut & 85\" 4K Display" },
      { name: "Architectural Staircase", dims: "Cantilevered Floating Steps", spec: "Warm Wood Treads with Frameless Glass Balustrade ('UP')" },
      { name: "Family Sectional Sofa", dims: "12'0\" × 9'6\"", spec: "Champagne Greige Performance Fabric with Down Topper" },
    ]
  },
  drawing: {
    cadDims: "22'0\" × 22'3\"",
    sqft: 490,
    focalWall: "West Wall: Fluted Oak Acoustic Panel TV Unit with 75\" 4K Screen & Ambient Backlight (marked 'Tv Unit')",
    circulation: "South: Double-leaf Main Door (MD) from 30'0\" x 8'0\" Sitout veranda; North: Open portal to Living Hall",
    daylighting: "East: French windows (Fw); warm 2700K indirect LED false ceiling lighting",
    rationale: [
      "TV Unit placed on West wall per blueprint notation 'Tv Unit', keeping main entry sightline grand and open",
      "Formal guest sofa suite arranged for conversation upon entering through Main Door (MD)",
      "Direct wide portal opens North into the family Living Hall"
    ],
    keyFurniture: [
      { name: "Formal Leather Sofa Suite", dims: "8'6\" × 3'4\"", spec: "Cognac Saddle Leather & Cream Bouclé" },
      { name: "West Wall TV Console", dims: "84\" × 18\" × 14\"", spec: "American Walnut & Fluted Accents" },
      { name: "Marble Coffee Table", dims: "48\" × 32\"", spec: "Calacatta Gold Marble & Brass Plinth" },
    ]
  },
  kitchen: {
    cadDims: "24'0\" × 22'3\"",
    sqft: 534,
    focalWall: "Center: Quartz Island & Dual-Tone Cabinetry with Cooktop & Chimney",
    circulation: "Internal doorways to Wet Kitchen (16'0\" × 10'0\") and Store Room (8'6\" × 4'3\")",
    daylighting: "Dual linear architectural brass pendants (2700K, 95+ CRI) over island prep surface",
    rationale: [
      "Waterfall island serves as both prep surface and social dining breakfast bar",
      "Fluted natural oak cabinetry with concealed soft-close Blum hardware",
      "Internal access to Wet Kitchen and Store maintained with wide clear aisles"
    ],
    keyFurniture: [
      { name: "Quartz Waterfall Island", dims: "10'0\" × 3'6\" × 36\"", spec: "Calacatta Oro Quartz Slab" },
      { name: "Counter Stools (4x)", dims: "18\" × 18\" × 26\"", spec: "Solid White Oak & Bouclé Upholstery" },
      { name: "Linear Brass Pendants", dims: "48\" Length", spec: "Brushed Brass & Warm LED Diffusers" },
    ]
  },
  dining: {
    cadDims: "12'3\" × 11'0\"",
    sqft: 135,
    focalWall: "Center: 8-Seater Contemporary Dining Table with Upholstered Dining Chairs",
    circulation: "Direct wide opening into Living Hall (East) and Kitchen (South)",
    daylighting: "French window (Fw) on West wall bringing in natural daylight; linear brass pendant above",
    rationale: [
      "Table length scaled to the 12'3\" × 11'0\" space leaving 3'6\" chair pullback room",
      "Wide open archway connects seamlessly into the Grand Living Hall",
      "Sleek crockery unit positioned on wall for tableware storage"
    ],
    keyFurniture: [
      { name: "8-Person Dining Table", dims: "7'6\" × 3'6\" × 30\"", spec: "Italian Marble Top & Solid Oak Legs" },
      { name: "Upholstered Chairs (8x)", dims: "20\" × 22\" × 32\"", spec: "Textured Cream Bouclé & Black Metal" },
      { name: "Brass Linear Chandelier", dims: "48\" Length", spec: "Brushed Brass & Warm Opal Diffusers" },
    ]
  },
  bed1: {
    cadDims: "16'0\" × 22'0\"",
    sqft: 352,
    focalWall: "North Wall: Oatmeal Linen King Platform Bed with Padded Headboard & Pendant Drops",
    circulation: "Private doorway to attached Dress (6'5\" × 10'3\") and Bathroom (6'5\" × 11'0\")",
    daylighting: "Window (W3) on exterior wall with sheer drapes; dual floating brass drop pendants",
    rationale: [
      "King platform bed aligned on quietest structural wall away from main living hall",
      "Direct private access into dedicated 6'5\" x 10'3\" dressing room and luxury ensuite",
      "Floating walnut nightstands maintain continuous floor sweep"
    ],
    keyFurniture: [
      { name: "King Platform Bed", dims: "6'6\" × 7'0\" × 42\"", spec: "Belgian Oatmeal Linen & White Oak Plinth" },
      { name: "Floating Nightstands (2x)", dims: "24\" × 16\" × 8\"", spec: "American Walnut & Soft-Close Drawers" },
      { name: "Walk-in Dressing Portal", dims: "6'5\" × 10'3\"", spec: "Dedicated Dressing Room Transition" },
    ]
  },
  bed2: {
    cadDims: "16'0\" × 22'0\"",
    sqft: 352,
    focalWall: "North Wall: Charcoal Woven Queen Platform Bed with Natural Oak Slat Accents",
    circulation: "Private doorway to attached Dress (6'5\" × 10'3\") and Bathroom (6'5\" × 11'0\")",
    daylighting: "Window (W3) on exterior wall; articulated brass gooseneck reading sconces",
    rationale: [
      "Charcoal textured upholstery creates cozy boutique hotel aesthetic for guests",
      "Integrated desk/vanity console along window wall taking advantage of natural daylight",
      "Direct private access to attached walk-in dressing and ensuite bath"
    ],
    keyFurniture: [
      { name: "Queen Platform Bed", dims: "5'6\" × 6'8\" × 40\"", spec: "Charcoal Woven Fabric & Oak Trim" },
      { name: "Brass Gooseneck Sconces", dims: "12\" Reach", spec: "Antiqued Brass with Rotary Dimmers" },
      { name: "Attached Dress Room", dims: "6'5\" × 10'3\"", spec: "Built-In Wardrobes & Vanity" },
    ]
  },
  pooja: {
    cadDims: "12'3\" × 12'0\"",
    sqft: 147,
    focalWall: "East Wall: Hand-Carved Teakwood Sanctum Mandir with Backlit Brass Jaali Screen",
    circulation: "Sacred sanctum directly adjoining Living Hall per Vastu principles",
    daylighting: "2200K temple gold warm glow with flickering brass diyas and hanging brass bells",
    rationale: [
      "Strict Vastu orientation: Deities face West so worshippers face East during prayers",
      "Intricately carved Burma teakwood mandir with stepped sanctum plinth",
      "Solid brass hanging temple bells and soft 2200K backlight create spiritual ambiance"
    ],
    keyFurniture: [
      { name: "Carved Teakwood Mandir", dims: "6'0\" W × 7'6\" H × 24\" D", spec: "Burma Teakwood with Traditional Carvings" },
      { name: "Backlit Jaali Screen", dims: "8'0\" W × 9'0\" H", spec: "Laser-Cut Brass with 2200K Diffused LED" },
      { name: "Hanging Brass Bells", dims: "Set of 5", spec: "Pure Cast Brass with Traditional Chains" },
    ]
  }
};

export const getRoomPlanAnalysis = (roomName: string): RoomAnalysisData => {
  const r = (roomName || '').toLowerCase();
  if (r.includes('living') || r === 'living hall') return ROOM_PLAN_ANALYSIS.living;
  if (r.includes('drawing')) return ROOM_PLAN_ANALYSIS.drawing;
  if (r.includes('kitchen') && !r.includes('wet')) return ROOM_PLAN_ANALYSIS.kitchen;
  if (r.includes('dining')) return ROOM_PLAN_ANALYSIS.dining;
  if (r.includes('bed 1') || r.includes('bed-1') || r.includes('master')) return ROOM_PLAN_ANALYSIS.bed1;
  if (r.includes('bed 2') || r.includes('bed-2')) return ROOM_PLAN_ANALYSIS.bed2;
  if (r.includes('bed')) return ROOM_PLAN_ANALYSIS.bed1;
  if (r.includes('pooja')) return ROOM_PLAN_ANALYSIS.pooja;
  return ROOM_PLAN_ANALYSIS.living;
};



// ── REAL PERSON FIRST-PERSON CAMERA CONTROLLER ─────────────────────────────────
const RoomCameraController: React.FC<{
  camPos: THREE.Vector3;
  camYaw: number;
  camPitch: number;
  fov?: number;
}> = ({ camPos, camYaw, camPitch, fov = 64 }) => {
  const { camera } = useThree();

  useFrame(() => {
    const persp = camera as THREE.PerspectiveCamera;
    if (persp.fov !== fov) {
      persp.fov = fov;
      persp.updateProjectionMatrix();
    }
    camera.position.set(camPos.x, camPos.y, camPos.z);
    const forwardX = Math.sin(camYaw) * Math.cos(camPitch);
    const forwardY = Math.sin(camPitch);
    const forwardZ = Math.cos(camYaw) * Math.cos(camPitch);
    camera.lookAt(
      camPos.x + forwardX * 6,
      camPos.y + forwardY * 6,
      camPos.z + forwardZ * 6
    );
  });

  return null;
};

// ── MAIN EXPORT COMPONENT ─────────────────────────────────────────────────────
export const FloorplanViewer3D: React.FC<Props> = ({
  geometry,
  placedFurniture = [],
  pendingFurniture = null,
  onFurniturePlaced,
  onSelectFurniture,
  selectedFurnitureUid,
}) => {
  const [dollhouseWallHeight, setDollhouseWallHeight] = useState<number>(1.2);
  const [isNightMode, setIsNightMode] = useState<boolean>(false);
  const [activeStyle, setActiveStyle] = useState<InteriorStyle>('modern');

  const [viewMode, setViewMode] = useState<'dollhouse' | 'room'>('dollhouse');
  const [roomRenderEngine, setRoomRenderEngine] = useState<'360' | 'ai'>('360');
  const [activeRoomId, setActiveRoomId] = useState<string | null>(null);
  const [hoveredRoomId, setHoveredRoomId] = useState<string | null>(null);

  // Human Eye Level: 1.50m seated/standing perspective
  const [camPos, setCamPos] = useState<THREE.Vector3>(new THREE.Vector3(0, 1.50, 0));
  const [camYaw, setCamYaw] = useState<number>(Math.PI);
  const [camPitch, setCamPitch] = useState<number>(0.0);
  const [roomFov, setRoomFov] = useState<number>(64);
  const [showMinimap, setShowMinimap] = useState<boolean>(false);

  const controlsRef = useRef<any>(null);
  const isDraggingRef = useRef<boolean>(false);
  const lastMouseRef = useRef<{ x: number; y: number }>({ x: 0, y: 0 });

  const {
    metadata,
    rooms = [],
    walls = [],
    doors = [],
    windows = [],
    stairs = [],
  } = geometry;

  const floorTexture = useMemo(() => createHardwoodFloorTexture(activeStyle), [activeStyle]);
  const teakDeckTexture = useMemo(() => createTeakDeckTexture(), []);
  const tileFloorTexture = useMemo(() => createTileFloorTexture(), []);

  const [hideRoof, setHideRoof] = useState<boolean>(false);
  const [showRoofTooltip, setShowRoofTooltip] = useState<boolean>(false);

  // Architectural Bounds
  const buildingBounds = useMemo(() => {
    let minX = Infinity;
    let maxX = -Infinity;
    let minY = Infinity;
    let maxY = -Infinity;

    rooms.forEach((r: RoomGeometry) => {
      (r.boundary || []).forEach((p: Point2D) => {
        if (p.x < minX) minX = p.x;
        if (p.x > maxX) maxX = p.x;
        if (p.y < minY) minY = p.y;
        if (p.y > maxY) maxY = p.y;
      });
      if (r.label_position) {
        if (r.label_position.x < minX) minX = r.label_position.x;
        if (r.label_position.x > maxX) maxX = r.label_position.x;
        if (r.label_position.y < minY) minY = r.label_position.y;
        if (r.label_position.y > maxY) maxY = r.label_position.y;
      }
    });

    if (minX !== Infinity && maxX > minX && maxY > minY) {
      const bWidth = maxX - minX;
      const bHeight = maxY - minY;
      return {
        minX,
        maxX,
        minY,
        maxY,
        centerX: (minX + maxX) / 2,
        centerZ: (minY + maxY) / 2,
        size: Math.max(bWidth, bHeight),
      };
    }

    const w = metadata?.page_dimensions?.width || 800;
    const h = metadata?.page_dimensions?.height || 1000;
    return {
      minX: 0,
      maxX: w,
      minY: 0,
      maxY: h,
      centerX: w / 2,
      centerZ: h / 2,
      size: Math.max(w, h),
    };
  }, [rooms, metadata?.page_dimensions]);

  const centerX = buildingBounds.centerX;
  const centerZ = buildingBounds.centerZ;
  const scale = useMemo(() => 16.5 / Math.max(buildingBounds.size, 80), [buildingBounds.size]);

  // Architectural Doors
  const allDoors = useMemo<DoorSymbol[]>(() => {
    const list: DoorSymbol[] = [...doors];
    if (!rooms || rooms.length === 0) return list;

    rooms.forEach((r: RoomGeometry) => {
      let minX = Infinity, maxX = -Infinity, minY = Infinity, maxY = -Infinity;
      if (r.boundary && r.boundary.length > 0) {
        r.boundary.forEach((p: Point2D) => {
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
        (d: DoorSymbol) =>
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
          const dPrev = Math.hypot(prev.x - centerX, prev.y - centerZ);
          const dCurr = Math.hypot(curr.x - centerX, curr.y - centerZ);
          return dCurr < dPrev ? curr : prev;
        });

        list.push({
          id: `derived-door-${r.id}`,
          position: best,
          width: 36,
          swing: 'inward_right',
        });
      }
    });

    return list;
  }, [doors, rooms, centerX, centerZ]);

  // Clean walls with real walk-through doorway openings (Planner 5D architecture)
  const splitWalls = useMemo(
    () => deriveCleanWallsWithDoorways(rooms, allDoors, scale, centerX, centerZ, walls),
    [rooms, allDoors, scale, centerX, centerZ, walls]
  );

  const activeRoom = useMemo(() => {
    if (!activeRoomId || !rooms) return null;
    return rooms.find((r: RoomGeometry) => r.id === activeRoomId) || null;
  }, [activeRoomId, rooms]);

  const effectiveWallHeight = viewMode === 'room' ? 3.2 : dollhouseWallHeight;

  // Active Room Focal Furniture Bounding Box (Planner 5D Green Wireframe)
  const activeRoomBoundingBox = useMemo(() => {
    if (viewMode !== 'room' || !activeRoom) return null;
    let minX = Infinity, maxX = -Infinity, minY = Infinity, maxY = -Infinity;
    if (activeRoom.boundary && activeRoom.boundary.length > 0) {
      activeRoom.boundary.forEach((pt: Point2D) => {
        if (pt.x < minX) minX = pt.x;
        if (pt.x > maxX) maxX = pt.x;
        if (pt.y < minY) minY = pt.y;
        if (pt.y > maxY) maxY = pt.y;
      });
    } else if (activeRoom.label_position) {
      minX = activeRoom.label_position.x - 30;
      maxX = activeRoom.label_position.x + 30;
      minY = activeRoom.label_position.y - 30;
      maxY = activeRoom.label_position.y + 30;
    }

    const xMin3d = (minX - centerX) * scale;
    const xMax3d = (maxX - centerX) * scale;
    const zMin3d = (minY - centerZ) * scale;
    const zMax3d = (maxY - centerZ) * scale;
    const cx = (xMin3d + xMax3d) / 2;
    const cz = (zMin3d + zMax3d) / 2;

    const name = (activeRoom.name || '').toLowerCase();
    if (name.includes('bed')) {
      const bedHeadZ = zMin3d + 0.45;
      return {
        position: [cx, 0.68, bedHeadZ + 1.1] as [number, number, number],
        size: [2.35, 1.35, 2.3] as [number, number, number],
        label: 'King Platform Bed',
      };
    }
    if (name.includes('living')) {
      return {
        position: [cx - 0.4, 0.45, cz + 1.25] as [number, number, number],
        size: [2.55, 0.95, 1.15] as [number, number, number],
        label: 'Family Sofa Suite',
      };
    }
    if (name.includes('drawing')) {
      return {
        position: [cx - 0.5, 0.45, cz] as [number, number, number],
        size: [2.55, 0.95, 1.15] as [number, number, number],
        label: 'Formal Sofa Suite',
      };
    }
    if (name.includes('dining')) {
      return {
        position: [cx, 0.48, cz] as [number, number, number],
        size: [2.3, 0.95, 1.25] as [number, number, number],
        label: 'Dining Table Set',
      };
    }
    if (name.includes('kitchen') && !name.includes('wet')) {
      return {
        position: [cx, 0.48, cz] as [number, number, number],
        size: [3.3, 0.96, 1.25] as [number, number, number],
        label: 'Waterfall Island',
      };
    }
    return null;
  }, [viewMode, activeRoom, scale, centerX, centerZ]);

  // Real Person Room Vantage Point Calculation (Matching Uploaded Image View Exactly!)
  const handleEnterRoom = useCallback(
    (room: RoomGeometry) => {
      setActiveRoomId(room.id);
      setViewMode('room');
      setRoomRenderEngine('360');
      setRoomFov(64);

      let minX = Infinity, maxX = -Infinity, minY = Infinity, maxY = -Infinity;
      if (room.boundary && room.boundary.length > 0) {
        room.boundary.forEach((p: Point2D) => {
          if (p.x < minX) minX = p.x;
          if (p.x > maxX) maxX = p.x;
          if (p.y < minY) minY = p.y;
          if (p.y > maxY) maxY = p.y;
        });
      } else if (room.label_position) {
        minX = room.label_position.x - 30;
        maxX = room.label_position.x + 30;
        minY = room.label_position.y - 30;
        maxY = room.label_position.y + 30;
      }

      const xMin3d = (minX - centerX) * scale;
      const xMax3d = (maxX - centerX) * scale;
      const zMin3d = (minY - centerZ) * scale;
      const zMax3d = (maxY - centerZ) * scale;

      const roomCenterX = (xMin3d + xMax3d) / 2;
      const roomCenterZ = (zMin3d + zMax3d) / 2;

      const rName = room.name.toLowerCase();

      // LIVING HALL: Symmetrical One-Point Perspective looking North at the Marble TV Unit & Floating Staircase!
      if (rName.includes('living') || rName === 'living hall' || rName === 'living') {
        const eyeX = roomCenterX;
        const eyeZ = zMax3d - 0.25;
        setCamPos(new THREE.Vector3(eyeX, 1.45, eyeZ));

        // Look straight North at the blueprint TV Unit
        setCamYaw(Math.PI);
        setCamPitch(0.0);
      }
      // BEDROOMS: Stand at door looking North directly at the Bed & Pillows
      else if (rName.includes('bed')) {
        const eyeX = roomCenterX;
        const eyeZ = zMax3d - 0.75;
        setCamPos(new THREE.Vector3(eyeX, 1.55, eyeZ));

        setCamYaw(Math.PI);
        setCamPitch(-0.04);
      }
      // DINING ROOM: Enter from doorway looking West at the dining table
      else if (rName.includes('dining')) {
        const eyeX = xMax3d - 0.6;
        const eyeZ = roomCenterZ;
        setCamPos(new THREE.Vector3(eyeX, 1.55, eyeZ));

        setCamYaw(-Math.PI / 2);
        setCamPitch(-0.04);
      }
      // KITCHEN: Enter looking at the waterfall island
      else if (rName.includes('kitchen') && !rName.includes('wet')) {
        const eyeX = xMax3d - 0.8;
        const eyeZ = roomCenterZ;
        setCamPos(new THREE.Vector3(eyeX, 1.55, eyeZ));

        setCamYaw(-Math.PI / 2);
        setCamPitch(-0.03);
      }
      // DRAWING HALL: Look North directly at the Dark Marble Accent Wall and Cream Sofa Suite (Planner 5D Reference)
      else if (rName.includes('drawing')) {
        const eyeX = roomCenterX;
        const eyeZ = zMax3d - 0.45;
        setCamPos(new THREE.Vector3(eyeX, 1.45, eyeZ));

        setCamYaw(Math.PI);
        setCamPitch(-0.03);
      }
      // POOJA ROOM
      else if (rName.includes('pooja')) {
        const eyeX = xMax3d - 0.55;
        const eyeZ = roomCenterZ;
        setCamPos(new THREE.Vector3(eyeX, 1.55, eyeZ));

        setCamYaw(-Math.PI / 2);
        setCamPitch(-0.03);
      }
      // BATHROOMS
      else if (rName.includes('bath')) {
        const eyeX = roomCenterX;
        const eyeZ = zMax3d - 0.55;
        setCamPos(new THREE.Vector3(eyeX, 1.55, eyeZ));

        setCamYaw(Math.PI);
        setCamPitch(-0.03);
      }
      // OTHER ROOMS
      else {
        const eyeX = roomCenterX;
        const eyeZ = zMax3d - 0.7;
        setCamPos(new THREE.Vector3(eyeX, 1.55, eyeZ));

        const angle = Math.atan2(roomCenterX - eyeX, roomCenterZ - eyeZ);
        setCamYaw(angle || Math.PI);
        setCamPitch(0.0);
      }
    },
    [centerX, centerZ, scale]
  );

  const handleExitToDollhouse = useCallback(() => {
    setViewMode('dollhouse');
    setActiveRoomId(null);
  }, []);

  // Keyboard navigation when inside a room
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (['INPUT', 'TEXTAREA'].includes((e.target as HTMLElement)?.tagName)) return;
      if (e.key === 'Escape' && viewMode === 'room') {
        handleExitToDollhouse();
        return;
      }
      if (viewMode !== 'room') return;

      const step = 0.35;
      if (e.key === 'ArrowUp' || e.key === 'w' || e.key === 'W') {
        setCamPos((prev) => new THREE.Vector3(prev.x + Math.sin(camYaw) * step, 1.48, prev.z + Math.cos(camYaw) * step));
      } else if (e.key === 'ArrowDown' || e.key === 's' || e.key === 'S') {
        setCamPos((prev) => new THREE.Vector3(prev.x - Math.sin(camYaw) * step, 1.48, prev.z - Math.cos(camYaw) * step));
      } else if (e.key === 'ArrowLeft' || e.key === 'a' || e.key === 'A') {
        setCamYaw((y) => y + 0.08);
      } else if (e.key === 'ArrowRight' || e.key === 'd' || e.key === 'D') {
        setCamYaw((y) => y - 0.08);
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [viewMode, camYaw, handleExitToDollhouse]);

  const handlePointerDown = (e: React.PointerEvent<HTMLDivElement>) => {
    if (viewMode !== 'room') return;
    if (e.button === 0) {
      isDraggingRef.current = true;
      lastMouseRef.current = { x: e.clientX, y: e.clientY };
      try {
        e.currentTarget.setPointerCapture(e.pointerId);
      } catch {}
    }
  };

  const handlePointerMove = (e: React.PointerEvent<HTMLDivElement>) => {
    if (viewMode === 'room' && isDraggingRef.current) {
      const deltaX = e.clientX - lastMouseRef.current.x;
      const deltaY = e.clientY - lastMouseRef.current.y;
      lastMouseRef.current = { x: e.clientX, y: e.clientY };
      // Smooth continuous 360-degree panoramic rotation
      setCamYaw((y) => (y - deltaX * 0.0055) % (Math.PI * 2));
      setCamPitch((p) => Math.max(-1.15, Math.min(1.15, p - deltaY * 0.0045)));
    }
  };

  const handlePointerUp = (e: React.PointerEvent<HTMLDivElement>) => {
    isDraggingRef.current = false;
    try {
      e.currentTarget.releasePointerCapture(e.pointerId);
    } catch {}
  };

  const handleWheel = (e: React.WheelEvent<HTMLDivElement>) => {
    if (viewMode === 'room') {
      setRoomFov((prev) => Math.max(38, Math.min(84, prev + (e.deltaY > 0 ? 3 : -3))));
    }
  };

  const currentPalette = STYLE_PALETTES[activeStyle];

  return (
    <div className="flex flex-col bg-slate-950 border border-slate-800 rounded-2xl overflow-hidden shadow-2xl relative select-none">
      {/* ── TOP STREAMLINED CONTROLS BAR ────────────────────────────────────── */}
      <div className="flex flex-wrap items-center justify-between px-4 py-2.5 bg-slate-950/95 border-b border-slate-800 gap-3 z-10 backdrop-blur-md">
        {/* Left: View Mode Indicator & Active Room Info */}
        <div className="flex items-center gap-3">
          <div className="flex items-center gap-1.5 px-3 py-1 bg-gradient-to-r from-sky-500 to-indigo-600 rounded-lg text-white text-xs font-bold shadow-md shadow-sky-500/20">
            <Sparkles className="w-3.5 h-3.5 text-amber-300" />
            <span>
              {viewMode === 'room'
                ? roomRenderEngine === '360'
                  ? '360° ROOM WALKTHROUGH'
                  : 'AI STUDIO PHOTO'
                : '3D DOLLHOUSE (ROOF OFF)'}
            </span>
          </div>

          <div className="flex items-center gap-2 pl-1">
            <span className="text-white font-bold text-sm tracking-wide">
              {activeRoom ? activeRoom.name : 'Click any room on floor or map to view virtually'}
            </span>
            {activeRoom?.dimensions && (
              <span className="px-2 py-0.5 rounded bg-slate-800 border border-slate-700 text-xs font-mono text-sky-300">
                {activeRoom.dimensions}
              </span>
            )}
          </div>
        </div>

        {/* Center: Style Switcher */}
        <div className="flex items-center gap-1.5 bg-slate-900/90 border border-slate-800 p-1 rounded-xl">
          <span className="text-[11px] text-slate-400 font-medium px-2 flex items-center gap-1">
            <Palette className="w-3.5 h-3.5 text-indigo-400" />
            <span className="hidden sm:inline">Style:</span>
          </span>
          {(['modern', 'scandinavian', 'luxury'] as InteriorStyle[]).map((st) => {
            const pal = STYLE_PALETTES[st];
            const isAct = activeStyle === st;
            return (
              <button
                key={st}
                onClick={() => setActiveStyle(st)}
                className={`text-xs px-2.5 py-1 rounded-lg flex items-center gap-1 transition-all font-semibold cursor-pointer ${
                  isAct
                    ? 'bg-indigo-600 text-white shadow-md shadow-indigo-500/25 ring-1 ring-indigo-400'
                    : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800'
                }`}
                title={pal.description}
              >
                <span>{pal.icon}</span>
                <span>{pal.name}</span>
              </button>
            );
          })}
        </div>

        {/* Right: Planner 5D Style View Controls + Render + Hide Roof */}
        <div className="flex items-center gap-2">
          {/* 1. View Mode Toggles (Planner 5D Dollhouse vs 3D Room Walkthrough) */}
          <div className="flex items-center gap-1 bg-slate-900 border border-slate-800 p-0.5 rounded-lg">
            <button
              onClick={handleExitToDollhouse}
              className={`text-xs px-2.5 py-1 rounded-md font-semibold flex items-center gap-1.5 transition-all cursor-pointer ${
                viewMode === 'dollhouse'
                  ? 'bg-amber-500 text-slate-950 font-bold shadow-md shadow-amber-500/20'
                  : 'text-slate-400 hover:text-slate-200'
              }`}
              title="Top-down 3D Dollhouse view with roof off"
            >
              <Home className="w-3.5 h-3.5" />
              <span>3D Dollhouse</span>
            </button>

            <button
              onClick={() => {
                const targetRoom = activeRoom || rooms[0];
                if (targetRoom) handleEnterRoom(targetRoom);
              }}
              className={`text-xs px-2.5 py-1 rounded-md font-semibold flex items-center gap-1.5 transition-all cursor-pointer ${
                viewMode === 'room' && roomRenderEngine === '360'
                  ? 'bg-gradient-to-r from-sky-500 to-indigo-600 text-white shadow-md'
                  : 'text-slate-400 hover:text-slate-200'
              }`}
              title="3D Room Walkthrough (Look 360°, Walk with WASD)"
            >
              <Eye className="w-3.5 h-3.5 text-amber-300" />
              <span>First-Person 3D</span>
            </button>
          </div>

          {/* 2. Planner 5D "Render" Button (AI HD Photorealistic Studio Render) */}
          <button
            onClick={() => {
              if (!activeRoom && rooms.length > 0) setActiveRoomId(rooms[0].id);
              setViewMode('room');
              setRoomRenderEngine((prev) => (prev === 'ai' ? '360' : 'ai'));
            }}
            className={`text-xs px-3 py-1.5 rounded-lg flex items-center gap-1.5 font-bold transition-all cursor-pointer ${
              roomRenderEngine === 'ai' && viewMode === 'room'
                ? 'bg-indigo-600 text-white shadow-lg shadow-indigo-500/30 ring-1 ring-indigo-400'
                : 'bg-slate-900 hover:bg-slate-800 text-slate-200 border border-slate-700/80 hover:border-slate-500'
            }`}
            title="Generate & View AI Photorealistic HD Room Render"
          >
            <Camera className="w-3.5 h-3.5 text-sky-400" />
            <span>Render</span>
          </button>

          {/* 3. Planner 5D "Hide Roof" Button */}
          <div className="relative">
            <button
              onClick={() => {
                setHideRoof((prev) => !prev);
                setShowRoofTooltip(false);
              }}
              className={`text-xs px-2.5 py-1.5 rounded-lg flex items-center gap-1.5 font-semibold transition-all cursor-pointer ${
                hideRoof
                  ? 'bg-sky-600 text-white shadow-md shadow-sky-600/30'
                  : 'bg-slate-900 hover:bg-slate-800 text-slate-300 border border-slate-800'
              }`}
              title="Toggle Ceiling / Roof on/off"
            >
              <Layers className="w-3.5 h-3.5 text-indigo-400" />
              <span className="hidden sm:inline">{hideRoof ? 'Roof Hidden' : 'Hide Roof'}</span>
            </button>

            {/* Planner 5D Blue Tooltip: "Hide roof" feature is available now */}
            {showRoofTooltip && (
              <div className="absolute top-10 right-0 z-50 whitespace-nowrap bg-sky-500 text-white text-[11px] font-bold px-3 py-1.5 rounded-xl shadow-xl flex items-center gap-1.5 animate-bounce">
                <span>"Hide roof" feature is available now</span>
                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    setShowRoofTooltip(false);
                  }}
                  className="hover:text-sky-200 ml-1 text-xs"
                >
                  <X className="w-3 h-3" />
                </button>
              </div>
            )}
          </div>

          {/* Cutaway Wall Slider in Dollhouse Mode */}
          {viewMode === 'dollhouse' && (
            <div className="flex items-center gap-2 bg-slate-900 px-2.5 py-1 rounded-lg border border-slate-800">
              <Sliders className="w-3.5 h-3.5 text-slate-400" />
              <span className="text-[11px] text-slate-400">Walls:</span>
              <input
                type="range"
                min="0.6"
                max="3.0"
                step="0.1"
                value={dollhouseWallHeight}
                onChange={(e) => setDollhouseWallHeight(parseFloat(e.target.value))}
                className="w-14 h-1.5 bg-slate-700 rounded-lg appearance-none cursor-pointer accent-indigo-500"
              />
              <span className="text-xs text-indigo-400 font-mono">{dollhouseWallHeight.toFixed(1)}m</span>
            </div>
          )}

          <button
            onClick={() => setIsNightMode((prev) => !prev)}
            className="p-1.5 rounded-lg border border-slate-800 bg-slate-900 hover:bg-slate-800 text-slate-300 hover:text-white transition-colors cursor-pointer"
            title={isNightMode ? 'Switch to Daylight' : 'Switch to Sunset / Evening Glow'}
          >
            {isNightMode ? <Sun className="w-4 h-4 text-amber-400" /> : <Moon className="w-4 h-4 text-indigo-400" />}
          </button>

          <button
            onClick={() => {
              if (controlsRef.current) controlsRef.current.reset();
              setCamYaw(Math.PI);
              setCamPitch(0.0);
            }}
            className="p-1.5 rounded-lg border border-slate-800 bg-slate-900 hover:bg-slate-800 text-slate-300 hover:text-white transition-colors cursor-pointer"
            title="Reset View"
          >
            <RotateCcw className="w-4 h-4" />
          </button>
        </div>
      </div>

      {/* ── 3D CANVAS VIEWPORT ─────────────────────────────────────────────────── */}
      <div
        className={`w-full h-[640px] relative select-none ${
          isNightMode ? 'bg-[#080d1a]' : 'bg-[#18202f]'
        }`}
        onPointerDown={handlePointerDown}
        onPointerMove={handlePointerMove}
        onPointerUp={handlePointerUp}
        onPointerLeave={handlePointerUp}
        onWheel={handleWheel}
      >
        {viewMode === 'room' && roomRenderEngine === 'ai' && activeRoom ? (
          <AIPhotorealisticRoomView
            room={activeRoom}
            activeStyle={activeStyle}
            isNightMode={isNightMode}
            onExitToDollhouse={handleExitToDollhouse}
            onSwitchTo3DWalkthrough={() => setRoomRenderEngine('360')}
          />
        ) : (
          <Canvas
            shadows
            gl={{
              antialias: true,
              toneMapping: THREE.ACESFilmicToneMapping,
              toneMappingExposure: 1.15,
            }}
            camera={{ position: [0, 16, 14], fov: 50 }}
            className={`w-full h-full ${
              viewMode === 'room'
                ? 'cursor-grab active:cursor-grabbing'
                : 'cursor-pointer'
            }`}
          >
            {viewMode === 'dollhouse' && (
              <OrbitControls
                ref={controlsRef}
                makeDefault
                minDistance={4}
                maxDistance={50}
                maxPolarAngle={Math.PI / 2.05}
                enablePan={true}
                panSpeed={1.4}
                rotateSpeed={0.8}
                enableDamping={true}
                dampingFactor={0.08}
              />
            )}

            {viewMode === 'room' && (
              <RoomCameraController
                camPos={camPos}
                camYaw={camYaw}
                camPitch={camPitch}
                fov={roomFov}
              />
            )}

            {/* LUXURY ARCHITECTURAL LIGHTING */}
            {isNightMode ? (
              <>
                <ambientLight intensity={0.3} color="#1e1e38" />
                <pointLight position={[0, 4, 0]} intensity={3.5} color="#fed7aa" distance={25} decay={1.5} castShadow />
                <spotLight position={[0, 8, 0]} angle={Math.PI / 4} penumbra={0.6} intensity={2.5} color="#fff1cc" castShadow />
              </>
            ) : (
              <>
                <ambientLight intensity={currentPalette.ambientLightIntensity} color={currentPalette.ambientLightColor} />
                <directionalLight
                  position={[18, 9, 1]}
                  intensity={1.9}
                  color="#fed7aa"
                  castShadow
                  shadow-mapSize={[2048, 2048]}
                  shadow-bias={-0.0002}
                  shadow-camera-near={0.5}
                  shadow-camera-far={60}
                  shadow-camera-left={-20}
                  shadow-camera-right={20}
                  shadow-camera-top={20}
                  shadow-camera-bottom={-20}
                />
                <hemisphereLight args={['#fed7aa', '#78350f', 0.42]} />

                {viewMode === 'room' && (
                  <pointLight position={[camPos.x, 2.7, camPos.z]} intensity={2.2} distance={14} color="#fffaf0" decay={1.4} />
                )}
              </>
            )}

            {/* ── 3D CAD ARCHITECTURE & STAGING (ALWAYS RENDERED IN BOTH MODES!) ── */}
            {/* OUTDOOR LANDSCAPE & PATIO TERRACE */}
            <OutdoorLandscape3D
              maxX={buildingBounds.maxX}
              minY={buildingBounds.minY}
              maxY={buildingBounds.maxY}
              scale={scale}
              centerX={centerX}
              centerZ={centerZ}
            />

            {/* BASE GROUND PLINTH */}
            <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, -0.01, 0]} receiveShadow>
              <planeGeometry args={[buildingBounds.size * scale + 6, buildingBounds.size * scale + 6]} />
              <meshStandardMaterial color="#1e293b" roughness={0.85} />
            </mesh>

            {/* SOFT CONTACT SHADOWS */}
            <ContactShadows
              position={[0, -0.005, 0]}
              opacity={0.55}
              scale={32}
              blur={1.8}
              far={10}
              resolution={1024}
              color="#000000"
            />

            {/* 1. ROOM FLOORS WITH PLANNER 5D TEXTURES (Teak Deck for Sitout, Tiles for Bath/Kitchen) */}
            {rooms.map((room: RoomGeometry) => (
              <Room3D
                key={room.id}
                room={room}
                scale={scale}
                centerX={centerX}
                centerZ={centerZ}
                isSelected={activeRoomId === room.id}
                isHovered={hoveredRoomId === room.id}
                viewMode={viewMode}
                floorTexture={floorTexture}
                teakDeckTexture={teakDeckTexture}
                tileFloorTexture={tileFloorTexture}
                onSelect={() => handleEnterRoom(room)}
                onHover={(hovered) => setHoveredRoomId(hovered ? room.id : null)}
                onFloorPointerMove={(pt) => {
                  if (pendingFurniture && onFurniturePlaced) {
                    onFurniturePlaced({
                      uid: `pf-${Date.now()}`,
                      specId: pendingFurniture.spec.id,
                      x: pt.x,
                      y: 0,
                      z: pt.z,
                      rotationY: 0,
                    });
                  }
                }}
              />
            ))}

            {/* 2. ARCHITECTURAL WALLS WITH OPEN DOORWAYS */}
            {splitWalls.map((wall: SplitWallSegment) => (
              <Wall3D
                key={wall.id}
                wall={wall}
                scale={scale}
                centerX={centerX}
                centerZ={centerZ}
                effectiveWallHeight={effectiveWallHeight}
                styleWallColor={currentPalette.wallColor}
              />
            ))}

            {/* 3. SPIRAL STAIRCASE */}
            {stairs.map((stair: StaircaseSymbol) => (
              <SpiralStaircase3D
                key={stair.id}
                stair={stair}
                scale={scale}
                centerX={centerX}
                centerZ={centerZ}
                effectiveWallHeight={effectiveWallHeight}
              />
            ))}

            {/* CEILING (Active in First-Person Room Mode unless Hide Roof is clicked) */}
            <GrandCeiling3D
              buildingBounds={buildingBounds}
              scale={scale}
              wallHeight={effectiveWallHeight}
              enabled={viewMode === 'room' && !hideRoof}
              style={activeStyle}
            />

            {/* 4. DOORS WITH OPEN SWING LEAF */}
            {allDoors.map((door: DoorSymbol) => (
              <Door3D key={door.id} door={door} scale={scale} centerX={centerX} centerZ={centerZ} walls={splitWalls} />
            ))}

            {/* 5. WINDOWS */}
            {windows.map((win: WindowSymbol) => (
              <Window3D key={win.id} win={win} scale={scale} centerX={centerX} centerZ={centerZ} walls={splitWalls as any} />
            ))}

            {/* 6. PHOTO-REALISTIC DESIGNER STAGING MATCHING BLUEPRINT */}
            <PhotorealisticDesignerStaging3D
              rooms={rooms}
              scale={scale}
              centerX={centerX}
              centerZ={centerZ}
              style={activeStyle}
            />

            {/* 8. USER CUSTOM PLACED FURNITURE */}
            {placedFurniture.map((pf: PlacedFurniture) => (
              <Furniture3D
                key={pf.uid}
                placed={pf}
                isSelected={selectedFurnitureUid === pf.uid}
                onSelect={() => onSelectFurniture && onSelectFurniture(pf.uid)}
              />
            ))}
          </Canvas>
        )}

        {/* ── PLANNER 5D FLOATING LEFT VERTICAL TOOLBAR ── */}
        <div className="pointer-events-auto absolute left-3 top-1/2 -translate-y-1/2 z-20 flex flex-col items-center gap-2 bg-white/95 backdrop-blur-md border border-slate-200/90 p-1.5 rounded-2xl shadow-xl">
          <button
            onClick={() => setShowMinimap((m) => !m)}
            className="w-8 h-8 rounded-xl text-slate-700 hover:text-indigo-600 hover:bg-slate-100 flex items-center justify-center transition-colors cursor-pointer"
            title="Toggle 2D Floor Plan"
          >
            <Search className="w-4 h-4" />
          </button>
          <button
            onClick={handleExitToDollhouse}
            className={`w-8 h-8 rounded-xl flex items-center justify-center transition-colors cursor-pointer ${
              viewMode === 'dollhouse' ? 'bg-amber-500 text-white shadow-sm' : 'text-slate-700 hover:text-amber-600 hover:bg-slate-100'
            }`}
            title="3D Dollhouse View"
          >
            <Home className="w-4 h-4" />
          </button>
          <button
            onClick={() => {
              const target = activeRoom || rooms[0];
              if (target) handleEnterRoom(target);
            }}
            className={`w-8 h-8 rounded-xl flex items-center justify-center transition-colors cursor-pointer ${
              viewMode === 'room' && roomRenderEngine === '360' ? 'bg-indigo-600 text-white shadow-sm' : 'text-slate-700 hover:text-indigo-600 hover:bg-slate-100'
            }`}
            title="First-Person 3D Room Walkthrough"
          >
            <Armchair className="w-4 h-4" />
          </button>
          <button
            onClick={() => {
              setActiveStyle((s) => (s === 'modern' ? 'scandinavian' : s === 'scandinavian' ? 'luxury' : 'modern'));
            }}
            className="w-8 h-8 rounded-xl text-slate-700 hover:text-indigo-600 hover:bg-slate-100 flex items-center justify-center transition-colors cursor-pointer"
            title="Switch Style / Materials"
          >
            <Palette className="w-4 h-4" />
          </button>
          <button
            onClick={() => {
              setHideRoof((r) => !r);
              setShowRoofTooltip(false);
            }}
            className={`w-8 h-8 rounded-xl flex items-center justify-center transition-colors cursor-pointer ${
              hideRoof ? 'text-indigo-600 bg-indigo-50' : 'text-slate-700 hover:text-indigo-600 hover:bg-slate-100'
            }`}
            title="Toggle Ceiling / Roof"
          >
            <Layers className="w-4 h-4" />
          </button>
          <button
            onClick={() => {
              if (controlsRef.current) controlsRef.current.reset();
              setCamYaw(Math.PI);
              setCamPitch(0.0);
            }}
            className="w-8 h-8 rounded-xl text-slate-700 hover:text-indigo-600 hover:bg-slate-100 flex items-center justify-center transition-colors cursor-pointer"
            title="Reset Perspective"
          >
            <RotateCcw className="w-4 h-4" />
          </button>
        </div>

        {/* ── 2D BLUEPRINT HUD CARD (Top-Left, Minimizable) ───────────────────── */}
        {showMinimap ? (
          <div className="pointer-events-auto absolute top-4 left-14 z-30 w-64 sm:w-72 bg-[#0c182b]/88 backdrop-blur-md rounded-2xl border border-sky-400/35 p-3 shadow-2xl flex flex-col gap-2 transition-all">
            <div className="flex items-center justify-between text-xs pb-1.5 border-b border-sky-500/20">
              <div className="flex items-center gap-2">
                <span className="px-1.5 py-0.5 rounded bg-sky-950/80 border border-sky-600/40 font-mono text-[11px] font-bold text-sky-300">
                  {activeRoom
                    ? `0${rooms.findIndex((r: RoomGeometry) => r.id === activeRoom.id) + 1}/0${rooms.length}`
                    : `01/0${rooms.length || 9}`}
                </span>
                <span className="font-bold text-slate-100 tracking-wider text-[11px] uppercase">
                  2D Floor Plan
                </span>
              </div>
              <button
                onClick={() => setShowMinimap(false)}
                className="text-slate-400 hover:text-white p-0.5 rounded transition-colors cursor-pointer"
                title="Minimize 2D Floor Plan"
              >
                <Maximize2 className="w-3 h-3" />
              </button>
            </div>

            <div className="w-full h-44 bg-[#050e1c] rounded-xl overflow-hidden relative border border-sky-900/50">
              <svg
                viewBox={`${buildingBounds.minX - 10} ${buildingBounds.minY - 10} ${buildingBounds.maxX - buildingBounds.minX + 20} ${buildingBounds.maxY - buildingBounds.minY + 20}`}
                className="w-full h-full"
              >
                <defs>
                  <pattern id="hudGrid" width="20" height="20" patternUnits="userSpaceOnUse">
                    <path d="M 20 0 L 0 0 0 20" fill="none" stroke="rgba(56, 189, 248, 0.08)" strokeWidth="0.5" />
                  </pattern>
                </defs>
                <rect
                  x={buildingBounds.minX - 10}
                  y={buildingBounds.minY - 10}
                  width={buildingBounds.maxX - buildingBounds.minX + 20}
                  height={buildingBounds.maxY - buildingBounds.minY + 20}
                  fill="url(#hudGrid)"
                />

                {rooms.map((r: RoomGeometry) => {
                  const isAct = activeRoomId === r.id;
                  const ptsStr = (r.boundary || []).map((p: Point2D) => `${p.x},${p.y}`).join(' ');
                  return (
                    <g key={`hud-r-${r.id}`} className="cursor-pointer" onClick={() => handleEnterRoom(r)}>
                      {ptsStr ? (
                        <polygon
                          points={ptsStr}
                          fill={isAct ? 'rgba(217, 119, 6, 0.45)' : 'rgba(15, 30, 56, 0.65)'}
                          stroke={isAct ? '#f59e0b' : '#38bdf8'}
                          strokeWidth={isAct ? '2' : '0.9'}
                          className="transition-all hover:fill-sky-500/30"
                        />
                      ) : null}
                    </g>
                  );
                })}

                {splitWalls.map((w: SplitWallSegment) => (
                  <line
                    key={`hud-w-${w.id}`}
                    x1={w.start.x}
                    y1={w.start.y}
                    x2={w.end.x}
                    y2={w.end.y}
                    stroke="#ffffff"
                    strokeWidth="1.6"
                    strokeLinecap="round"
                  />
                ))}

                <path
                  d={`M ${centerX} ${buildingBounds.maxY - 15} Q ${centerX + 20} ${(buildingBounds.minY + buildingBounds.maxY) / 2 + 10} ${centerX + camPos.x / scale} ${centerZ + camPos.z / scale}`}
                  fill="none"
                  stroke="#fbbf24"
                  strokeWidth="1.2"
                  strokeDasharray="3 3"
                  opacity={viewMode === 'room' ? 0.8 : 0.4}
                />

                {viewMode === 'room' && (
                  <g
                    transform={`translate(${centerX + camPos.x / scale}, ${centerZ + camPos.z / scale}) rotate(${((-camYaw + Math.PI) * 180) / Math.PI})`}
                  >
                    <path
                      d="M 0 0 L -20 38 L 20 38 Z"
                      fill="rgba(245, 158, 11, 0.35)"
                      stroke="#f59e0b"
                      strokeWidth="1"
                    />
                    <circle cx="0" cy="0" r="5" fill="none" stroke="#fbbf24" strokeWidth="0.8" opacity="0.6" />
                    <circle cx="0" cy="0" r="3.2" fill="#fbbf24" stroke="#ffffff" strokeWidth="1" />
                  </g>
                )}
              </svg>

              <div className="absolute bottom-1.5 left-2 right-2 flex justify-between items-center text-[9px] text-sky-400 font-medium">
                <span className="font-mono text-slate-300">12' CEILING HEIGHT</span>
                <span className="uppercase tracking-wider text-amber-400 font-semibold">Click room to view</span>
              </div>
            </div>
          </div>
        ) : (
          <button
            onClick={() => setShowMinimap(true)}
            className="pointer-events-auto absolute top-4 left-14 z-30 px-3 py-1.5 bg-[#0c182b]/90 backdrop-blur-md rounded-xl border border-sky-400/40 text-sky-300 hover:text-white text-xs font-semibold flex items-center gap-1.5 shadow-xl transition-all cursor-pointer"
          >
            <Compass className="w-3.5 h-3.5" />
            <span>Show 2D Floor Plan</span>
          </button>
        )}

        {/* ── PLANNER 5D MINIMAL BOTTOM-LEFT AREA BADGE (Matching Image 1 Exactly) ── */}
        <div className="pointer-events-auto absolute bottom-3 left-4 z-20 flex items-center gap-2">
          <div className="flex items-center gap-1 bg-white/95 backdrop-blur-md border border-slate-200/90 px-2 py-1 rounded-xl shadow-lg">
            <button
              onClick={() => {
                setCamYaw((y) => y + Math.PI / 8);
              }}
              className="p-1 hover:bg-slate-100 rounded-lg text-slate-600 hover:text-slate-900 transition-colors cursor-pointer"
              title="Rotate Camera Left"
            >
              <RotateCcw className="w-3.5 h-3.5" />
            </button>
            <button
              onClick={() => {
                setCamYaw((y) => y - Math.PI / 8);
              }}
              className="p-1 hover:bg-slate-100 rounded-lg text-slate-600 hover:text-slate-900 transition-colors cursor-pointer"
              title="Rotate Camera Right"
            >
              <RotateCcw className="w-3.5 h-3.5 transform scale-x-[-1]" />
            </button>
          </div>

          <div className="bg-white/95 backdrop-blur-md border border-slate-200/90 px-2.5 py-1 rounded-xl shadow-lg flex items-center gap-1.5 text-xs font-semibold text-slate-800">
            <Maximize2 className="w-3 h-3 text-slate-500" />
            <span>
              {activeRoom ? `${activeRoom.name} • 337 m²` : '337 m²'}
            </span>
          </div>
        </div>
      </div>

      {/* ── BOTTOM ROOM QUICK TELEPORT BAR ─────────────────────────────────────── */}
      <div className="px-4 py-2 bg-slate-900 border-t border-slate-800 flex items-center gap-2 overflow-x-auto text-xs no-scrollbar">
        <span className="text-[11px] font-bold text-sky-400 uppercase tracking-wider whitespace-nowrap pl-1">
          Rooms:
        </span>
        {rooms.map((r: RoomGeometry) => {
          const isAct = activeRoomId === r.id;
          return (
            <button
              key={r.id}
              onClick={() => handleEnterRoom(r)}
              className={`px-3 py-1 rounded-lg font-medium whitespace-nowrap flex items-center gap-1.5 transition-all cursor-pointer ${
                isAct
                  ? 'bg-amber-500 text-slate-950 font-bold shadow-md shadow-amber-500/20'
                  : 'bg-slate-800 hover:bg-slate-700 text-slate-300 hover:text-white border border-slate-700/60'
              }`}
            >
              <Eye className="w-3 h-3" />
              <span>{r.name}</span>
            </button>
          );
        })}
      </div>
    </div>
  );
};
