// ─── Furniture Catalog Types ──────────────────────────────────────────────────

export type FurnitureCategory =
  | 'living'
  | 'bedroom'
  | 'dining'
  | 'kitchen'
  | 'bathroom'
  | 'storage'
  | 'lighting'
  | 'outdoor';

export interface FurnitureSpec {
  id: string;
  name: string;
  category: FurnitureCategory;
  icon: string;           // emoji icon for sidebar
  // Real-world dimensions in metres
  width: number;
  depth: number;
  height: number;
  color: string;          // base body colour
  accentColor?: string;   // cushions / legs / secondary part
  // For rendering style
  shape: 'box' | 'cylinder' | 'lshape' | 'circle';
  roughness?: number;
  metalness?: number;
  // AI suggestion: which room names (lowercase keywords) this fits
  suitableFor: string[];
}

export interface PlacedFurniture {
  uid: string;            // unique instance id
  specId: string;         // references FurnitureSpec.id
  // 3D world position (metres)
  x: number;
  y: number;
  z: number;
  rotationY: number;      // radians, rotation around vertical axis
  roomId?: string;        // which room it belongs to
}

// ─── Furniture Catalog ────────────────────────────────────────────────────────

export const FURNITURE_CATALOG: FurnitureSpec[] = [
  // ── Living Room ──
  {
    id: 'sofa-3seat',
    name: '3-Seat Sofa',
    category: 'living',
    icon: '🛋️',
    width: 2.1, depth: 0.9, height: 0.85,
    color: '#a67c6e', accentColor: '#8b6557',
    shape: 'box', roughness: 0.8, metalness: 0.0,
    suitableFor: ['living', 'hall', 'drawing', 'lounge'],
  },
  {
    id: 'sofa-2seat',
    name: '2-Seat Sofa',
    category: 'living',
    icon: '🛋️',
    width: 1.6, depth: 0.85, height: 0.82,
    color: '#c4a882', accentColor: '#a08060',
    shape: 'box', roughness: 0.8, metalness: 0.0,
    suitableFor: ['living', 'hall', 'bed', 'drawing'],
  },
  {
    id: 'coffee-table',
    name: 'Coffee Table',
    category: 'living',
    icon: '☕',
    width: 1.1, depth: 0.6, height: 0.42,
    color: '#6b4c3b', accentColor: '#8b6555',
    shape: 'box', roughness: 0.4, metalness: 0.1,
    suitableFor: ['living', 'hall', 'drawing'],
  },
  {
    id: 'tv-unit',
    name: 'TV Unit',
    category: 'living',
    icon: '📺',
    width: 1.8, depth: 0.45, height: 0.55,
    color: '#3d2b1f', accentColor: '#1a1a1a',
    shape: 'box', roughness: 0.5, metalness: 0.2,
    suitableFor: ['living', 'hall', 'bed', 'drawing'],
  },
  {
    id: 'armchair',
    name: 'Armchair',
    category: 'living',
    icon: '🪑',
    width: 0.85, depth: 0.85, height: 0.9,
    color: '#8d6e63', accentColor: '#6d4c41',
    shape: 'box', roughness: 0.75, metalness: 0.0,
    suitableFor: ['living', 'hall', 'drawing', 'bed'],
  },
  {
    id: 'bookshelf',
    name: 'Bookshelf',
    category: 'living',
    icon: '📚',
    width: 1.0, depth: 0.35, height: 1.9,
    color: '#5d4037', accentColor: '#4e342e',
    shape: 'box', roughness: 0.6, metalness: 0.05,
    suitableFor: ['living', 'study', 'bed', 'drawing'],
  },

  // ── Bedroom ──
  {
    id: 'bed-king',
    name: 'King Bed',
    category: 'bedroom',
    icon: '🛏️',
    width: 1.93, depth: 2.13, height: 0.55,
    color: '#d4a97a', accentColor: '#8b6555',
    shape: 'box', roughness: 0.7, metalness: 0.0,
    suitableFor: ['bed', 'master'],
  },
  {
    id: 'bed-queen',
    name: 'Queen Bed',
    category: 'bedroom',
    icon: '🛏️',
    width: 1.52, depth: 2.03, height: 0.52,
    color: '#c8a882', accentColor: '#7d5a4f',
    shape: 'box', roughness: 0.7, metalness: 0.0,
    suitableFor: ['bed', 'guest'],
  },
  {
    id: 'bed-single',
    name: 'Single Bed',
    category: 'bedroom',
    icon: '🛏️',
    width: 0.9, depth: 1.9, height: 0.48,
    color: '#c4b5a0', accentColor: '#7d6855',
    shape: 'box', roughness: 0.7, metalness: 0.0,
    suitableFor: ['bed', 'child', 'guest'],
  },
  {
    id: 'wardrobe',
    name: 'Wardrobe',
    category: 'bedroom',
    icon: '🚪',
    width: 1.8, depth: 0.6, height: 2.1,
    color: '#5d4037', accentColor: '#4e342e',
    shape: 'box', roughness: 0.5, metalness: 0.15,
    suitableFor: ['bed', 'dress', 'master'],
  },
  {
    id: 'dresser',
    name: 'Dresser / Dressing Table',
    category: 'bedroom',
    icon: '🪞',
    width: 1.0, depth: 0.5, height: 1.5,
    color: '#8d6e63', accentColor: '#6d4c41',
    shape: 'box', roughness: 0.5, metalness: 0.3,
    suitableFor: ['dress', 'bed', 'master'],
  },
  {
    id: 'bedside-table',
    name: 'Bedside Table',
    category: 'bedroom',
    icon: '🌙',
    width: 0.5, depth: 0.45, height: 0.55,
    color: '#6b4c3b',
    shape: 'box', roughness: 0.5, metalness: 0.05,
    suitableFor: ['bed', 'master', 'guest'],
  },

  // ── Dining ──
  {
    id: 'dining-table-6',
    name: 'Dining Table (6-seat)',
    category: 'dining',
    icon: '🍽️',
    width: 1.8, depth: 0.9, height: 0.76,
    color: '#6b4c3b', accentColor: '#5d4037',
    shape: 'box', roughness: 0.45, metalness: 0.05,
    suitableFor: ['dining', 'kitchen', 'hall'],
  },
  {
    id: 'dining-table-4',
    name: 'Dining Table (4-seat)',
    category: 'dining',
    icon: '🍽️',
    width: 1.2, depth: 0.8, height: 0.76,
    color: '#795548', accentColor: '#6d4c41',
    shape: 'box', roughness: 0.45, metalness: 0.05,
    suitableFor: ['dining', 'kitchen'],
  },
  {
    id: 'dining-chair',
    name: 'Dining Chair',
    category: 'dining',
    icon: '🪑',
    width: 0.45, depth: 0.48, height: 0.9,
    color: '#8d6e63',
    shape: 'box', roughness: 0.6, metalness: 0.05,
    suitableFor: ['dining', 'kitchen'],
  },

  // ── Kitchen ──
  {
    id: 'kitchen-counter',
    name: 'Kitchen Counter',
    category: 'kitchen',
    icon: '🍳',
    width: 2.4, depth: 0.6, height: 0.9,
    color: '#eceff1', accentColor: '#b0bec5',
    shape: 'box', roughness: 0.3, metalness: 0.4,
    suitableFor: ['kitchen', 'wet kitchen'],
  },
  {
    id: 'kitchen-island',
    name: 'Kitchen Island',
    category: 'kitchen',
    icon: '🏝️',
    width: 1.2, depth: 0.8, height: 0.9,
    color: '#f5f5f5', accentColor: '#9e9e9e',
    shape: 'box', roughness: 0.25, metalness: 0.45,
    suitableFor: ['kitchen'],
  },
  {
    id: 'fridge',
    name: 'Refrigerator',
    category: 'kitchen',
    icon: '🧊',
    width: 0.75, depth: 0.7, height: 1.8,
    color: '#eceff1', accentColor: '#b0bec5',
    shape: 'box', roughness: 0.2, metalness: 0.6,
    suitableFor: ['kitchen', 'wet kitchen'],
  },

  // ── Bathroom ──
  {
    id: 'bathtub',
    name: 'Bathtub',
    category: 'bathroom',
    icon: '🛁',
    width: 1.7, depth: 0.75, height: 0.55,
    color: '#eceff1',
    shape: 'box', roughness: 0.15, metalness: 0.3,
    suitableFor: ['bath'],
  },
  {
    id: 'vanity',
    name: 'Vanity / Washbasin Cabinet',
    category: 'bathroom',
    icon: '🪥',
    width: 0.9, depth: 0.5, height: 0.85,
    color: '#eceff1', accentColor: '#b0bec5',
    shape: 'box', roughness: 0.2, metalness: 0.35,
    suitableFor: ['bath'],
  },

  // ── Storage ──
  {
    id: 'storage-cabinet',
    name: 'Storage Cabinet',
    category: 'storage',
    icon: '📦',
    width: 1.2, depth: 0.45, height: 1.8,
    color: '#6d4c41',
    shape: 'box', roughness: 0.6, metalness: 0.05,
    suitableFor: ['store', 'kitchen', 'bath', 'bed'],
  },
  {
    id: 'shoe-rack',
    name: 'Shoe Rack',
    category: 'storage',
    icon: '👟',
    width: 0.9, depth: 0.35, height: 1.0,
    color: '#8d6e63',
    shape: 'box', roughness: 0.6, metalness: 0.0,
    suitableFor: ['store', 'sitout', 'pooja'],
  },

  // ── Lighting ──
  {
    id: 'floor-lamp',
    name: 'Floor Lamp',
    category: 'lighting',
    icon: '💡',
    width: 0.4, depth: 0.4, height: 1.65,
    color: '#ffd54f', accentColor: '#f5a623',
    shape: 'cylinder', roughness: 0.4, metalness: 0.6,
    suitableFor: ['living', 'bed', 'drawing', 'hall'],
  },
  {
    id: 'table-lamp',
    name: 'Table Lamp',
    category: 'lighting',
    icon: '🕯️',
    width: 0.3, depth: 0.3, height: 0.5,
    color: '#ffe082', accentColor: '#f5a623',
    shape: 'cylinder', roughness: 0.5, metalness: 0.3,
    suitableFor: ['bed', 'living', 'drawing'],
  },

  // ── Outdoor / Sitout ──
  {
    id: 'outdoor-chair',
    name: 'Outdoor Chair',
    category: 'outdoor',
    icon: '🪑',
    width: 0.6, depth: 0.6, height: 0.9,
    color: '#78909c',
    shape: 'box', roughness: 0.7, metalness: 0.3,
    suitableFor: ['sitout', 'outdoor', 'balcony'],
  },
  {
    id: 'outdoor-table',
    name: 'Outdoor Table',
    category: 'outdoor',
    icon: '🌿',
    width: 0.9, depth: 0.9, height: 0.74,
    color: '#607d8b',
    shape: 'cylinder', roughness: 0.6, metalness: 0.3,
    suitableFor: ['sitout', 'outdoor', 'balcony'],
  },
];

// ─── AI Suggestion Engine ─────────────────────────────────────────────────────

export function getAISuggestionsForRoom(roomName: string): FurnitureSpec[] {
  const lc = roomName.toLowerCase();
  return FURNITURE_CATALOG.filter((f) =>
    f.suitableFor.some((kw) => lc.includes(kw))
  );
}

export const CATEGORY_META: Record<FurnitureCategory, { label: string; emoji: string; color: string }> = {
  living:   { label: 'Living Room', emoji: '🛋️', color: 'indigo' },
  bedroom:  { label: 'Bedroom',     emoji: '🛏️', color: 'purple' },
  dining:   { label: 'Dining',      emoji: '🍽️', color: 'amber' },
  kitchen:  { label: 'Kitchen',     emoji: '🍳', color: 'orange' },
  bathroom: { label: 'Bathroom',    emoji: '🛁', color: 'sky' },
  storage:  { label: 'Storage',     emoji: '📦', color: 'slate' },
  lighting: { label: 'Lighting',    emoji: '💡', color: 'yellow' },
  outdoor:  { label: 'Outdoor',     emoji: '🌿', color: 'green' },
};

