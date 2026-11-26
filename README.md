# Ground Floor Architectural 3D Walkthrough

An interactive, photo-realistic 3D walkthrough web application built for the 4,537 sq. ft ground-floor residential building plan on a 74' x 135' plot.

## Highlights
- **Single Self-Contained Web App**: Built in a single `index.html` file using Three.js (r128) via CDN with **no build steps or external bundlers required**.
- **Accurate CAD Plan Reproduction**: Traced to exact real-world dimensions in feet (1 unit = 1 ft):
  - **Building Footprint**: 48'3" wide x 83'6" deep (4,537 sq ft built-up area), 10'0" wall height.
  - **Plot & Grounds**: 74'0" x 135'0" plot with perimeter compound wall, driveway paving, gated entry, landscape garden patches, and trees.
  - **All 14 Rooms Mapped**:
    - Bedroom 1 (Master): 16'0" x 22'0"
    - Master Bath (Bath 1): 6'5" x 11'0"
    - Master Dress (Dress 1): 6'5" x 10'3"
    - Bedroom 2 (Guest / Study): 16'0" x 22'0"
    - Guest Bath (Bath 2): 6'5" x 11'0"
    - Guest Dress (Dress 2): 6'5" x 10'3"
    - Pooja Sanctum: 12'3" x 12'0" (with beside 3'0" verandah corridor)
    - Formal Dining: 12'3" x 11'0"
    - Store Room: 8'6" x 4'3"
    - Grand Living Hall: 33'9" x 25'6" (with East corner spiral staircase)
    - Gourmet Kitchen: 24'0" x 22'3"
    - Common Bath (Bath 3): 7'3" x 5'0"
    - Formal Drawing Hall: 22'0" x 22'3"
    - Wet Kitchen / Utility: 16'0" x 10'0"
    - Sitout (Entrance Veranda): 30'0" x 8'0"
- **Joinery Details**:
  - Main Doors (`MD`): 3'6" x 7'0"
  - Standard Doors (`D`): 3'0" x 7'0"
  - Toilet / Dress Doors (`D2`): 2'6" x 7'0"
  - Windows (`W2` 3'0"x4'0", `W3` 4'0"x4'0", `Fw` 6'0"x5'0")
  - Ventilators (`V`): 3'0" x 2'0"
  - Columns: `C1` (0'9" x 1'6") and `C3` (0'9" x 2'0")

## Key Features

### 1. Overview & Dollhouse Modes
- **Preset Camera Angles**: `Overview` (isometric angle), `Top Plan` (orthographic plan view), and `Front` (street facade).
- **Interactive Toggles**:
  - `Roof Off / On`: Toggle flat roof slab and 2.5 ft perimeter parapet.
  - `Cutaway Walls`: Seamlessly cut walls from 10 ft down to 3.8 ft architectural dollhouse height.
  - `Room Labels`: 3D floating viewport badges displaying room names, dimensions, and square footage.
  - `Furniture`: Show/hide bespoke interior staging.
  - `Daylight`: Toggle realistic sun directional light with soft shadow mapping.

### 2. Immersive Room Walkthrough
- Click any room floor (via 3D raycasting) or select from the bottom carousel strip.
- Smooth camera flight to human eye level (5.3 ft) inside the selected room.
- Roof closes automatically overhead to simulate the real enclosed interior.
- **Room Controls**:
  - Drag mouse to look 360° (pitch & yaw).
  - `W`, `A`, `S`, `D` or Arrow Keys to walk inside room bounds.
  - Scroll wheel to zoom (FOV 35° to 85°).
  - Auto 360° Turntable button (`Look Around`).
  - `Esc` or `Exit Room` button to return to Dollhouse mode.
  - `Prev Room` / `Next Room` quick navigation.

### 3. Procedural Realism & Lighting
- **No plain boxes**: Shaped geometry (rounded contours, bevels, turned legs, fluted panels, tufting, layered mattresses and duvets, brass bells, tiered mandir domes, stone fireplaces, and waterfall island counters).
- **Procedural PBR Textures**:
  - Warm honey-oak wide-plank hardwood
  - Nero Marquina dark graphite marble with white veining
  - Calacatta Gold marble with warm veining
  - Ceramic bathroom & kitchen tiles with grout lines
  - Teakwood outdoor decking
  - Hand-hewn dry-stack limestone
  - Sisal/jute rugs, bouclé & linen upholstery
  - Garden lawn and asphalt/stone pavers
- **Dynamic Lighting Engine**:
  - Active room spotlighting (2700K warm white in living/bedrooms, 4000K daylight in kitchen/baths, 2200K amber glow in pooja).
  - ACES Filmic tone mapping and sRGB gamma correction.

## Assumptions Made Where Plan Was Unclear
1. **Ceiling Height**: The plan specifies a 10 ft wall height; ceiling height is modeled at 10.0 ft with 0.5 ft roof slab and 2.5 ft perimeter parapet.
2. **Door Assignments**:
   - Main Entrance from Sitout into Drawing Hall and Living Hall East Garden exit use `MD` (3'6" x 7'0").
   - Bedrooms, Kitchen, Store, and Pooja use standard `D` (3'0" x 7'0").
   - Bathrooms and Dressing Rooms use `D2` (2'6" x 7'0").
   - Living Hall to Dining connection is an open 10' wide architectural archway.
3. **Compound & Setbacks**:
   - Plot dimensions are 74'0" x 135'0" (9,990 sq ft plot area).
   - The 48'3" x 83'6" building is centrally positioned with ~12'9" side setbacks, a 28' front setback for lawn/walkway, and an East-side driveway leading to the entrance porch.
4. **Spiral Staircase**:
   - Positioned in the East corner of the Living Hall (radius 3'2", 16 spiral treads with center support pole and handrail winding to upper floor).

## How to Run
Simply open `index.html` in any modern web browser, or serve it via any static file server:
```bash
python3 -m http.server 3333
# Then open http://localhost:3333/index.html in your browser
```

