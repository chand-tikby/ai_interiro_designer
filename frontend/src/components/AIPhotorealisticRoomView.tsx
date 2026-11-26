import React, { useState } from 'react';
import {
  Sparkles,
  Layers,
  X,
  Check,
  Eye,
  Box,
  Home,
} from 'lucide-react';
import type { RoomGeometry } from '../types/floorplan';
import type { InteriorStyle } from './FloorplanViewer3D';

export interface RoomHotspot {
  id: string;
  x: number; // percentage 0-100
  y: number; // percentage 0-100
  title: string;
  category: 'furniture' | 'lighting' | 'architecture' | 'material';
  dimensions?: string;
  material?: string;
  lightingSpec?: string;
  description: string;
  iconType?: 'sofa' | 'fireplace' | 'lamp' | 'table' | 'window' | 'tv' | 'kitchen';
}

interface RoomDesignData {
  title: string;
  subtitle: string;
  image: Record<InteriorStyle, string>;
  ambientColor: string;
  hotspots: RoomHotspot[];
}

const ROOM_CATALOG: Record<string, RoomDesignData> = {
  living: {
    title: 'Grand Living Hall (33\'9" × 25\'6")',
    subtitle: 'Statuario Marble TV Unit • Cantilever Staircase (UP) • Adjoining Dining & Pooja Portals',
    image: {
      modern: '/rooms/living-hall-modern.jpg?v=6',
      scandinavian: '/rooms/living-hall-modern.jpg?v=6',
      luxury: '/rooms/living-hall-modern.jpg?v=6',
    },
    ambientColor: 'rgba(251, 146, 60, 0.12)',
    hotspots: [
      {
        id: 'lh-tv',
        x: 50,
        y: 44,
        title: 'Custom Statuario Marble & Walnut TV Unit',
        category: 'architecture',
        dimensions: "16'0\" W × 12'0\" H • Solid North Wall ('Tv Unit')",
        material: 'Bookmatched Italian Statuario marble slab with fluted American walnut vertical acoustic slats',
        lightingSpec: 'Flush 85" 4K TV with 2700K ambient LED perimeter halo glow',
        description: 'Located on the North wall per blueprint notation "Tv Unit", providing optimal 14\' viewing distance from the family sectional.',
        iconType: 'tv',
      },
      {
        id: 'lh-stairs',
        x: 84,
        y: 45,
        title: 'Architectural Cantilever Floating Staircase ("UP")',
        category: 'architecture',
        dimensions: 'Floating wood treads with 12mm frameless tempered glass balustrade',
        material: 'Solid white oak steps embedded into structural RCC wall',
        description: 'Located in the North-East corner matching blueprint stair notation "UP", accessing the first floor.',
        iconType: 'window',
      },
      {
        id: 'lh-dining-arch',
        x: 18,
        y: 52,
        title: 'Adjoining Dining & Pooja Transition',
        category: 'architecture',
        dimensions: 'Wide cased architectural opening (8\'0" width)',
        description: 'Direct seamless connection into the 12\'3" × 11\'0" Dining Room and sacred Pooja room on the West.',
        iconType: 'table',
      },
      {
        id: 'lh-sofa',
        x: 50,
        y: 74,
        title: 'Deep-Profile Family Lounge Sectional',
        category: 'furniture',
        dimensions: "12'0\" × 9'6\" • 38\" depth • 16\" seat height",
        material: 'Champagne greige textured performance weave with high-resilience down-blend topper',
        description: 'Expansive family seating zone arranged to enjoy both the media TV wall and central social conversation.',
        iconType: 'sofa',
      },
      {
        id: 'lh-table',
        x: 50,
        y: 84,
        title: 'Custom Marble & Walnut Coffee Table',
        category: 'furniture',
        dimensions: '60" × 36" • 14" height',
        material: 'Honed Calacatta marble top on solid walnut pedestal base',
        description: 'Low-profile centerpiece coffee table complementing the Italian marble flooring.',
        iconType: 'table',
      },
      {
        id: 'lh-lighting',
        x: 50,
        y: 15,
        title: 'Architectural Gypsum Ceiling & Recessed Cove',
        category: 'lighting',
        lightingSpec: '2700K Warm Dim LED cove trough + deep-baffle magnetic track spotlights',
        description: 'Indirect ceiling wash delivering glare-free 300 lux illumination across the 860 sq ft hall.',
        iconType: 'lamp',
      },
    ],
  },
  kitchen: {
    title: 'Gourmet Chef Kitchen & Social Island',
    subtitle: 'Waterfall Quartz Island • Fluted Cabinetry • Architectural Brass Pendants',
    image: {
      modern: '/rooms/kitchen-modern.jpg?v=3',
      scandinavian: '/rooms/kitchen-modern.jpg?v=3',
      luxury: '/rooms/kitchen-modern.jpg?v=3',
    },
    ambientColor: 'rgba(254, 215, 170, 0.1)',
    hotspots: [
      {
        id: 'k-island',
        x: 44,
        y: 68,
        title: 'Waterfall Calacatta Quartz Island',
        category: 'architecture',
        dimensions: "10'0\" × 4'0\" • 36\" height • 3\" mitered edge",
        material: 'Calacatta Oro engineered quartz with continuous bookmatched waterfall end panels',
        description: 'Central culinary island accommodating 4 counter stools, prep sink, and concealed trash/recycling.',
        iconType: 'kitchen',
      },
      {
        id: 'k-stools',
        x: 36,
        y: 80,
        title: 'Low-Back Oak Counter Stools',
        category: 'furniture',
        dimensions: '26" seat height • Set of 4',
        material: 'Solid white oak legs with stain-resistant textured cream bouclé cushions',
        description: 'Ergonomic counter seating designed to tuck flush beneath the island overhang.',
        iconType: 'sofa',
      },
      {
        id: 'k-pendants',
        x: 48,
        y: 30,
        title: 'Linear Brushed Brass Island Pendants',
        category: 'lighting',
        lightingSpec: '2700K Warm White • 900 lm each • Diffuse downward glow',
        material: 'Satin brushed solid brass rod with frosted opal glass diffuser',
        description: 'Minimalist vertical lighting emphasizing ceiling height while spotlighting the island surface.',
        iconType: 'lamp',
      },
      {
        id: 'k-cooktop',
        x: 52,
        y: 57,
        title: 'Flush Induction Cooktop & Hidden Extractor',
        category: 'furniture',
        dimensions: '36" 5-Zone Cooktop',
        material: 'Black ceramic glass with integrated downdraft acoustic extraction (700 CFM)',
        description: 'Seamless glass cooktop keeping sightlines completely clear to the living area.',
        iconType: 'kitchen',
      },
      {
        id: 'k-pots',
        x: 68,
        y: 15,
        title: 'Deep-Baffle Architectural Downlights',
        category: 'lighting',
        lightingSpec: '3000K Clean Prep White • CRI 97 • 850 lm • Anti-glare',
        description: 'Precisely positioned recessed potlights spaced along prep counters for zero-shadow food preparation.',
        iconType: 'lamp',
      },
    ],
  },
  dining: {
    title: 'Formal Dining Pavilion',
    subtitle: 'Solid Ash 8-Seater Table • Cane Cantilever Chairs • Sculptural Chandelier',
    image: {
      modern: '/rooms/dining-hall.jpg?v=3',
      scandinavian: '/rooms/dining-hall.jpg?v=3',
      luxury: '/rooms/dining-hall.jpg?v=3',
    },
    ambientColor: 'rgba(253, 186, 116, 0.1)',
    hotspots: [
      {
        id: 'd-table',
        x: 50,
        y: 65,
        title: 'Solid Ash 8-Person Dining Table',
        category: 'furniture',
        dimensions: "8'0\" × 3'6\" • 30\" height",
        material: 'Solid natural ash with soft bevelled radius corners and flared elliptical timber legs',
        description: 'Generous dining table comfortably seating 8 guests for family gatherings and dinner parties.',
        iconType: 'table',
      },
      {
        id: 'd-chairs',
        x: 35,
        y: 68,
        title: 'Cane & Oak Cantilever Dining Chairs',
        category: 'furniture',
        dimensions: 'Set of 8 chairs',
        material: 'Natural French woven rattan cane back with curved steam-bent oak frame and padded leather seat',
        description: 'Lightweight, breathable dining chairs combining timeless craft with ergonomic lumbar support.',
        iconType: 'sofa',
      },
      {
        id: 'd-chandelier',
        x: 50,
        y: 28,
        title: 'Architectural Multi-Globe Chandelier',
        category: 'lighting',
        lightingSpec: '2700K Ambient Glow • Dimmable to 1% • 2,400 total lumens',
        material: 'Blackened bronze armature with hand-blown acid-etched opal glass spheres',
        description: 'Sculptural lighting focal point floating 34" above table level.',
        iconType: 'lamp',
      },
    ],
  },
  drawing: {
    title: 'Executive Drawing Room & Media Suite',
    subtitle: 'Acoustic Wood Slats • Low-Profile Leather Lounge • 75" Flush Display',
    image: {
      modern: '/rooms/drawing-hall.jpg?v=3',
      scandinavian: '/rooms/drawing-hall.jpg?v=3',
      luxury: '/rooms/drawing-hall.jpg?v=3',
    },
    ambientColor: 'rgba(249, 115, 22, 0.12)',
    hotspots: [
      {
        id: 'dr-sofa',
        x: 32,
        y: 68,
        title: 'Low-Profile Saddle Leather Sectional',
        category: 'furniture',
        dimensions: "9'2\" × 6'8\" • 36\" depth • 15\" seat height",
        material: 'Full-grain Italian saddle leather in warm cognac with double-stitch top seams',
        description: 'Ground-hugging lounge sofa designed for cinematic immersion and relaxed conversation.',
        iconType: 'sofa',
      },
      {
        id: 'dr-tv',
        x: 56,
        y: 38,
        title: 'Flush 75" 4K OLED Display & Slats',
        category: 'architecture',
        dimensions: "75\" diagonal • 65\" × 37\"",
        material: 'Acoustic fluted walnut wall panelling with dark sound-absorbing felt backing',
        lightingSpec: 'Concealed 2700K perimeter LED bias backlight reducing eye strain',
        description: 'Gallery-style media wall with acoustic treatment for studio-grade audio dampening.',
        iconType: 'tv',
      },
      {
        id: 'dr-credenza',
        x: 56,
        y: 62,
        title: 'Floating American Walnut Credenza',
        category: 'furniture',
        dimensions: "7'0\" length • 18\" depth • 16\" height (Wall Hung)",
        material: 'Solid American walnut with acoustic fabric speaker grille doors and internal ventilation',
        description: 'Wall-hung media credenza housing AV receivers, gaming consoles, and hidden cable channels.',
        iconType: 'table',
      },
      {
        id: 'dr-potlights',
        x: 30,
        y: 16,
        title: 'Anti-Glare Warm Recessed Downlights',
        category: 'lighting',
        lightingSpec: '3000K Warm White • 95 CRI • 38° beam angle with honeycomb louver',
        description: 'Precision task lighting configured on independent zone dimmers.',
        iconType: 'lamp',
      },
    ],
  },
  bed1: {
    title: 'Master Bedroom Sanctuary (Bed 1)',
    subtitle: 'King Platform Bed • Floating Nightstands • Fluted Wardrobes • Bedside Pendants',
    image: {
      modern: '/rooms/bed-1.jpg?v=3',
      scandinavian: '/rooms/bed-1.jpg?v=3',
      luxury: '/rooms/bed-1.jpg?v=3',
    },
    ambientColor: 'rgba(254, 240, 138, 0.1)',
    hotspots: [
      {
        id: 'b1-bed',
        x: 50,
        y: 62,
        title: 'King Upholstered Platform Bed',
        category: 'furniture',
        dimensions: "7'2\" × 7'6\" (Accommodates 76\" × 80\" King Mattress)",
        material: 'Oatmeal textured linen upholstered headboard with integrated solid oak side wings',
        description: 'Low-slung minimalist platform bed with breathable slatted mattress support.',
        iconType: 'sofa',
      },
      {
        id: 'b1-pendant',
        x: 24,
        y: 48,
        title: 'Bedside Micro-Drop Pendants',
        category: 'lighting',
        lightingSpec: '2400K Ultra-Warm Candle Glow • 300 lm • Touch-dimming at headboard',
        material: 'Hand-blown reeded glass globe with brass cable collar',
        description: 'Replaces bulky bedside lamps, keeping nightstand tabletops completely clear.',
        iconType: 'lamp',
      },
      {
        id: 'b1-wardrobe',
        x: 82,
        y: 50,
        title: 'Fluted Glass Full-Height Wardrobe',
        category: 'architecture',
        dimensions: "10'0\" width • 9'6\" height",
        material: 'Anodized bronze aluminum frame with fluted tempered glass and internal warm LED sensor strips',
        description: 'Floor-to-ceiling built-in storage with integrated drawer organizers and accessory trays.',
        iconType: 'window',
      },
    ],
  },
  bed2: {
    title: 'Guest Bedroom Suite (Bed 2)',
    subtitle: 'Queen Fabric Platform • Brass Sconces • Natural Oak Planks',
    image: {
      modern: '/rooms/bed-2.jpg?v=3',
      scandinavian: '/rooms/bed-2.jpg?v=3',
      luxury: '/rooms/bed-2.jpg?v=3',
    },
    ambientColor: 'rgba(254, 240, 138, 0.1)',
    hotspots: [
      {
        id: 'b2-bed',
        x: 50,
        y: 62,
        title: 'Queen Fabric Platform Bed',
        category: 'furniture',
        dimensions: "5'6\" × 7'0\" • 14\" platform height",
        material: 'Woven charcoal textured performance fabric with padded ergonomic backrest',
        description: 'Inviting guest bed with breathable wool underlay and hotel-grade percale linens.',
        iconType: 'sofa',
      },
      {
        id: 'b2-sconce',
        x: 28,
        y: 45,
        title: 'Articulated Brass Reading Sconces',
        category: 'lighting',
        lightingSpec: '2700K Warm Light • 400 lm • Directional 25° lens',
        material: 'Brushed brass with rotary knurled dimmer switch',
        description: 'Wall-mounted directional reading light for comfortable evening relaxation.',
        iconType: 'lamp',
      },
    ],
  },
  pooja: {
    title: 'Sacred Pooja Sanctum',
    subtitle: 'Hand-Carved Teakwood Mandir • Brass Bell Accents • Warm Amber Backlighting',
    image: {
      modern: '/rooms/pooja-room.jpg?v=3',
      scandinavian: '/rooms/pooja-room.jpg?v=3',
      luxury: '/rooms/pooja-room.jpg?v=3',
    },
    ambientColor: 'rgba(245, 158, 11, 0.15)',
    hotspots: [
      {
        id: 'pj-mandir',
        x: 50,
        y: 50,
        title: 'Hand-Carved Teak Sanctum',
        category: 'architecture',
        dimensions: "5'0\" × 3'0\" • 8'0\" height",
        material: 'Old-growth Burmese teakwood with traditional brass filigree detailing and tiered gopuram crown',
        description: 'Consecrated spiritual altar designed strictly according to Vastu Shastra principles.',
        iconType: 'fireplace',
      },
      {
        id: 'pj-light',
        x: 50,
        y: 30,
        title: 'Warm 2200K Sanctum Backlight',
        category: 'lighting',
        lightingSpec: '2200K Deep Amber Glow • 800 lm • Indirect halo illumination',
        description: 'Creates a serene, meditative golden glow highlighting deity idols and brass diyas.',
        iconType: 'lamp',
      },
    ],
  },
  bath: {
    title: 'Spa Bathroom Suite',
    subtitle: 'Honed Calacatta Marble Vanity • Frameless Glass Rain Shower • Backlit LED Mirror',
    image: {
      modern: '/rooms/bed-1.jpg?v=3',
      scandinavian: '/rooms/bed-1.jpg?v=3',
      luxury: '/rooms/bed-1.jpg?v=3',
    },
    ambientColor: 'rgba(56, 189, 248, 0.1)',
    hotspots: [
      {
        id: 'ba-vanity',
        x: 48,
        y: 60,
        title: 'Floating Calacatta Marble Vanity',
        category: 'architecture',
        dimensions: "60\" width • 22\" depth",
        material: 'Honed marble top with integrated rectangular undermount basin and brushed nickel fixtures',
        description: 'Sleek wall-hung vanity with deep soft-close storage drawers.',
        iconType: 'kitchen',
      },
      {
        id: 'ba-mirror',
        x: 48,
        y: 34,
        title: 'Anti-Fog Backlit Halo LED Mirror',
        category: 'lighting',
        lightingSpec: '3000K Natural White • CRI 98 • Dimmable perimeter glow',
        description: 'Shadow-free face illumination with touch-sensor defogger pad.',
        iconType: 'lamp',
      },
    ],
  },
  dress: {
    title: 'Bespoke Dressing Suite',
    subtitle: 'Fluted Glass Wardrobes • Internal LED Sensor Illuminators • Center Accessory Island',
    image: {
      modern: '/rooms/bed-1.jpg?v=3',
      scandinavian: '/rooms/bed-1.jpg?v=3',
      luxury: '/rooms/bed-1.jpg?v=3',
    },
    ambientColor: 'rgba(254, 215, 170, 0.1)',
    hotspots: [
      {
        id: 'dr-wardrobe',
        x: 50,
        y: 50,
        title: 'Full-Height Fluted Glass Wardrobe',
        category: 'architecture',
        dimensions: "12'0\" width • 9'6\" height",
        material: 'Smoked bronze aluminum frame with fluted tempered safety glass',
        lightingSpec: 'Automatic 2700K warm LED sensor activation upon opening',
        description: 'Integrated organization system with velvet-lined watch and jewelry drawers.',
        iconType: 'window',
      },
    ],
  },
};

interface Props {
  room: RoomGeometry;
  activeStyle: InteriorStyle;
  isNightMode: boolean;
  onExitToDollhouse: () => void;
  onSwitchTo3DWalkthrough: () => void;
}

export const AIPhotorealisticRoomView: React.FC<Props> = ({
  room,
  activeStyle,
  isNightMode,
  onExitToDollhouse,
  onSwitchTo3DWalkthrough,
}) => {
  const [selectedHotspot, setSelectedHotspot] = useState<RoomHotspot | null>(null);
  const [showHotspots, setShowHotspots] = useState<boolean>(true);
  const [activeCategoryFilter, setActiveCategoryFilter] = useState<'all' | 'furniture' | 'lighting' | 'architecture'>('all');

  const rName = (room?.name || '').toLowerCase();

  // Match room to catalog entry
  const catalogKey = React.useMemo(() => {
    if (rName.includes('living') || rName === 'living hall') return 'living';
    if (rName.includes('drawing')) return 'drawing';
    if (rName.includes('kitchen') && !rName.includes('wet')) return 'kitchen';
    if (rName.includes('dining')) return 'dining';
    if (rName.includes('bed 1') || rName.includes('bed-1') || rName.includes('master')) return 'bed1';
    if (rName.includes('bed 2') || rName.includes('bed-2')) return 'bed2';
    if (rName.includes('bed')) return 'bed1';
    if (rName.includes('pooja')) return 'pooja';
    if (rName.includes('bath')) return 'bath';
    if (rName.includes('dress')) return 'dress';
    // Fallbacks
    if (rName.includes('wet kitchen')) return 'kitchen';
    return 'living';
  }, [rName]);

  const roomData = ROOM_CATALOG[catalogKey] || ROOM_CATALOG.living;
  const currentImage = roomData.image[activeStyle] || roomData.image.modern;

  const filteredHotspots = React.useMemo(() => {
    if (activeCategoryFilter === 'all') return roomData.hotspots;
    return roomData.hotspots.filter((h) => h.category === activeCategoryFilter);
  }, [roomData.hotspots, activeCategoryFilter]);

  return (
    <div className="w-full h-full relative overflow-hidden select-none bg-slate-950 flex flex-col items-center justify-center">
      {/* ── HIGH RESOLUTION PHOTOREALISTIC INTERIOR CANVAS ── */}
      <div className="w-full h-full relative overflow-hidden flex items-center justify-center">
        <img
          src={currentImage}
          alt={roomData.title}
          className={`w-full h-full object-cover transition-all duration-700 ${
            isNightMode
              ? 'brightness-[0.78] contrast-[1.12] hue-rotate-[-4deg]'
              : 'brightness-[1.02] contrast-[1.04]'
          }`}
        />

        {/* Cinematic Vignette & Warm Golden Sunset Lighting Atmosphere */}
        <div
          className="absolute inset-0 pointer-events-none transition-opacity duration-700"
          style={{
            background: isNightMode
              ? 'radial-gradient(ellipse at 50% 60%, rgba(30, 27, 75, 0.25) 0%, rgba(2, 6, 23, 0.75) 100%)'
              : 'radial-gradient(ellipse at 50% 45%, rgba(254, 215, 170, 0.14) 0%, rgba(15, 23, 42, 0.42) 100%)',
          }}
        />

        {/* ── FLOATING INTERACTIVE FURNITURE & LIGHTING HOTSPOTS ── */}
        {showHotspots && (
          <div className="absolute inset-0 pointer-events-none">
            {filteredHotspots.map((hotspot) => {
              const isSelected = selectedHotspot?.id === hotspot.id;
              const isLighting = hotspot.category === 'lighting';
              const isFurniture = hotspot.category === 'furniture';

              return (
                <div
                  key={hotspot.id}
                  style={{ left: `${hotspot.x}%`, top: `${hotspot.y}%` }}
                  className="absolute -translate-x-1/2 -translate-y-1/2 pointer-events-auto z-20 group"
                >
                  {/* Outer Pulsing Aura Ring */}
                  <div
                    className={`absolute inset-0 -m-2 rounded-full animate-ping opacity-40 ${
                      isLighting
                        ? 'bg-amber-400'
                        : isFurniture
                        ? 'bg-sky-400'
                        : 'bg-emerald-400'
                    }`}
                  />

                  {/* Hotspot Action Button */}
                  <button
                    onClick={() => setSelectedHotspot(isSelected ? null : hotspot)}
                    className={`relative flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-bold transition-all transform shadow-2xl cursor-pointer ${
                      isSelected
                        ? 'bg-amber-400 text-slate-950 scale-110 ring-4 ring-amber-400/40'
                        : isLighting
                        ? 'bg-amber-500/90 hover:bg-amber-400 text-slate-950 hover:scale-105'
                        : isFurniture
                        ? 'bg-sky-600/90 hover:bg-sky-500 text-white hover:scale-105'
                        : 'bg-emerald-600/90 hover:bg-emerald-500 text-white hover:scale-105'
                    }`}
                  >
                    {isLighting ? (
                      <Sparkles className="w-3.5 h-3.5" />
                    ) : isFurniture ? (
                      <Box className="w-3.5 h-3.5" />
                    ) : (
                      <Layers className="w-3.5 h-3.5" />
                    )}
                    <span className="hidden sm:inline text-[11px] font-semibold tracking-tight">
                      {hotspot.title}
                    </span>
                  </button>

                  {/* Hover Quick Tooltip (when not selected) */}
                  {!isSelected && (
                    <div className="absolute bottom-full left-1/2 -translate-x-1/2 mb-2 hidden group-hover:flex flex-col items-center pointer-events-none z-30">
                      <div className="bg-slate-950/95 backdrop-blur-md text-white text-[11px] font-medium px-3 py-1.5 rounded-xl border border-slate-700/80 shadow-2xl whitespace-nowrap flex items-center gap-2">
                        <span className="font-bold text-amber-300">{hotspot.title}</span>
                        {hotspot.dimensions && (
                          <span className="text-slate-400 text-[10px] font-mono border-l border-slate-700 pl-2">
                            {hotspot.dimensions}
                          </span>
                        )}
                      </div>
                      <div className="w-2 h-2 bg-slate-950 border-r border-b border-slate-700 rotate-45 -mt-1" />
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        )}

        {/* ── SELECTED ITEM SPECIFICATION DRAWER / FLOATING CARD ── */}
        {selectedHotspot && (
          <div className="absolute bottom-6 right-6 z-30 w-80 sm:w-96 bg-slate-950/92 backdrop-blur-xl border border-sky-400/40 rounded-2xl p-4 shadow-2xl animate-in fade-in slide-in-from-bottom-4 duration-300">
            <div className="flex items-start justify-between pb-2 border-b border-slate-800">
              <div className="flex flex-col">
                <div className="flex items-center gap-1.5">
                  <span
                    className={`text-[9px] uppercase tracking-widest px-2 py-0.5 rounded font-bold ${
                      selectedHotspot.category === 'lighting'
                        ? 'bg-amber-500/20 text-amber-300 border border-amber-500/30'
                        : selectedHotspot.category === 'furniture'
                        ? 'bg-sky-500/20 text-sky-300 border border-sky-500/30'
                        : 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/30'
                    }`}
                  >
                    {selectedHotspot.category}
                  </span>
                  <span className="text-xs text-slate-400 font-mono">SPECIFICATION</span>
                </div>
                <h4 className="text-white font-bold text-base mt-1 tracking-tight">
                  {selectedHotspot.title}
                </h4>
              </div>
              <button
                onClick={() => setSelectedHotspot(null)}
                className="text-slate-400 hover:text-white p-1 rounded-lg hover:bg-slate-800 transition-colors cursor-pointer"
              >
                <X className="w-4 h-4" />
              </button>
            </div>

            <p className="text-slate-300 text-xs mt-2.5 leading-relaxed font-normal">
              {selectedHotspot.description}
            </p>

            <div className="mt-3.5 space-y-2 bg-slate-900/80 rounded-xl p-2.5 border border-slate-800/80 text-[11px]">
              {selectedHotspot.dimensions && (
                <div className="flex items-start justify-between gap-2">
                  <span className="text-slate-400 font-medium whitespace-nowrap">Dimensions:</span>
                  <span className="text-sky-300 font-mono text-right">{selectedHotspot.dimensions}</span>
                </div>
              )}
              {selectedHotspot.material && (
                <div className="flex items-start justify-between gap-2">
                  <span className="text-slate-400 font-medium whitespace-nowrap">Material:</span>
                  <span className="text-slate-200 text-right">{selectedHotspot.material}</span>
                </div>
              )}
              {selectedHotspot.lightingSpec && (
                <div className="flex items-start justify-between gap-2">
                  <span className="text-amber-400 font-medium whitespace-nowrap">Lighting:</span>
                  <span className="text-amber-200 font-mono text-right">{selectedHotspot.lightingSpec}</span>
                </div>
              )}
            </div>

            <div className="mt-3 flex items-center justify-between text-[11px] text-slate-400 pt-1">
              <span className="flex items-center gap-1 text-emerald-400 font-semibold">
                <Check className="w-3.5 h-3.5" />
                <span>Architecturally Fitted to Plan</span>
              </span>
              <button
                onClick={() => setSelectedHotspot(null)}
                className="text-xs text-sky-400 hover:text-sky-300 font-semibold cursor-pointer"
              >
                Done
              </button>
            </div>
          </div>
        )}

        {/* ── TOP-RIGHT HOTSPOT CATEGORY FILTER CONTROLS ── */}
        <div className="absolute top-4 right-4 z-20 flex items-center gap-2">
          {/* Toggle Hotspots */}
          <button
            onClick={() => setShowHotspots((prev) => !prev)}
            className={`px-3 py-1.5 rounded-xl text-xs font-bold flex items-center gap-1.5 backdrop-blur-md border shadow-xl transition-all cursor-pointer ${
              showHotspots
                ? 'bg-indigo-600/90 hover:bg-indigo-500 text-white border-indigo-400/40 shadow-indigo-500/20'
                : 'bg-slate-900/80 hover:bg-slate-800 text-slate-400 border-slate-700'
            }`}
            title="Toggle item and lighting tags overlay"
          >
            <Sparkles className="w-3.5 h-3.5 text-amber-300" />
            <span>{showHotspots ? 'Tags: ON' : 'Tags: OFF'}</span>
          </button>

          {/* Filter Pills */}
          {showHotspots && (
            <div className="hidden md:flex items-center gap-1 bg-slate-950/80 backdrop-blur-md border border-slate-800 p-1 rounded-xl text-xs">
              {(
                [
                  { id: 'all', label: 'All Items' },
                  { id: 'furniture', label: '🛋️ Furniture' },
                  { id: 'lighting', label: '💡 Lighting' },
                  { id: 'architecture', label: '🏛️ Architecture' },
                ] as const
              ).map((cat) => (
                <button
                  key={cat.id}
                  onClick={() => setActiveCategoryFilter(cat.id)}
                  className={`px-2 py-0.5 rounded-lg text-[11px] font-semibold transition-all cursor-pointer ${
                    activeCategoryFilter === cat.id
                      ? 'bg-slate-800 text-sky-300 shadow-sm'
                      : 'text-slate-400 hover:text-white'
                  }`}
                >
                  {cat.label}
                </button>
              ))}
            </div>
          )}
        </div>

        {/* ── BOTTOM HUD FLOATING BAR: ENGINE STATUS & SWITCHER ── */}
        <div className="absolute bottom-4 left-1/2 -translate-x-1/2 z-20 pointer-events-auto">
          <div className="flex items-center gap-3 px-4 py-2 bg-slate-950/90 backdrop-blur-md rounded-2xl border border-sky-500/30 shadow-2xl text-xs">
            <div className="flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
              <span className="font-bold text-white tracking-wide">
                AI Photorealistic Studio View
              </span>
              <span className="text-slate-400 hidden sm:inline">•</span>
              <span className="text-sky-300 text-[11px] font-mono hidden sm:inline">
                Natural PBR Lighting & Materials
              </span>
            </div>

            <div className="h-4 w-px bg-slate-800 mx-1" />

            <button
              onClick={onExitToDollhouse}
              className="px-2.5 py-1 rounded-lg bg-amber-500 hover:bg-amber-400 text-slate-950 font-bold text-[11px] flex items-center gap-1 transition-all cursor-pointer shadow-md shadow-amber-500/20"
              title="Return to 3D dollhouse floorplan view"
            >
              <Home className="w-3.5 h-3.5" />
              <span>Dollhouse</span>
            </button>

            <button
              onClick={onSwitchTo3DWalkthrough}
              className="px-2.5 py-1 rounded-lg bg-sky-600 hover:bg-sky-500 text-white font-semibold text-[11px] flex items-center gap-1 transition-all cursor-pointer shadow-md shadow-sky-600/20"
              title="Switch to 360° interactive room walkthrough (Drag mouse to look around 360°, WASD to walk)"
            >
              <Eye className="w-3.5 h-3.5" />
              <span>360° Room View</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};
