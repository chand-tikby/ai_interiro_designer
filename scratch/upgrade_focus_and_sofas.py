index_path = '/Users/puspharaj/Documents/Projects/ai-interior-designer/index.html'

with open(index_path, 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Update AI_ROOM_RECOMMENDATIONS furniture labels to reflect full geometric sofa/layout swaps
old_lv_furn = '''        furniture: [
          { id: 'lv_warmth', label: '★ AI Furniture: Belgian Linen + Marble' },
          { id: 'lv_emerald', label: 'Furniture: Emerald Velvet + Brass' },
          { id: 'lv_charcoal', label: 'Furniture: Nordic Charcoal + Oak' }
        ]'''
new_lv_furn = '''        furniture: [
          { id: 'lv_warmth', label: '★ AI Sofa: L-Sectional + Marble Nesting' },
          { id: 'lv_symmetrical', label: 'Sofa: Twin Facing Emerald Velvet' },
          { id: 'lv_curved', label: 'Sofa: U-Shape Bouclé Lounge + Ottomans' }
        ]'''
assert old_lv_furn in code
code = code.replace(old_lv_furn, new_lv_furn, 1)

old_dw_furn = '''        furniture: [
          { id: 'dw_formal', label: '★ AI Furniture: Cream + Nero Marquina' },
          { id: 'dw_sage', label: 'Furniture: Sage Linen + Walnut' },
          { id: 'dw_dark', label: 'Furniture: Executive Charcoal + Brass' }
        ]'''
new_dw_furn = '''        furniture: [
          { id: 'dw_formal', label: '★ AI Sofa: 3-Seater + Chaise + Armchair' },
          { id: 'dw_twin', label: 'Sofa: Twin Facing Sage Loveseats' },
          { id: 'dw_sectional', label: 'Sofa: Executive Charcoal L-Sectional' }
        ]'''
assert old_dw_furn in code
code = code.replace(old_dw_furn, new_dw_furn, 1)

old_b1_furn = '''        furniture: [
          { id: 'b1_tufted', label: '★ AI Furniture: Tufted Grey + Sage King' },
          { id: 'b1_walnut', label: 'Furniture: Warm Walnut + Ochre King' },
          { id: 'b1_charcoal', label: 'Furniture: Hotel Noir Velvet King' }
        ]'''
new_b1_furn = '''        furniture: [
          { id: 'b1_tufted', label: '★ AI Bed: Tufted King + Lounge Chair' },
          { id: 'b1_canopy', label: 'Bed: Walnut 4-Poster Canopy + Bench' },
          { id: 'b1_japandi', label: 'Bed: Low Japandi Platform + Daybed' }
        ]'''
assert old_b1_furn in code
code = code.replace(old_b1_furn, new_b1_furn, 1)

old_b2_furn = '''        furniture: [
          { id: 'b2_study', label: '★ AI Furniture: Ochre Queen + Oak Study' },
          { id: 'b2_sage', label: 'Furniture: Botanical Sage + Walnut' },
          { id: 'b2_slate', label: 'Furniture: Minimalist Slate Studio' }
        ]'''
new_b2_furn = '''        furniture: [
          { id: 'b2_study', label: '★ AI Bed: Queen + South Study Desk' },
          { id: 'b2_daybed', label: 'Sofa: Executive Daybed + Reading Chair' },
          { id: 'b2_twin', label: 'Bed: Dual Twin Guest Beds' }
        ]'''
assert old_b2_furn in code
code = code.replace(old_b2_furn, new_b2_furn, 1)

old_dn_furn = '''        furniture: [
          { id: 'dn_oak', label: '★ AI Furniture: European Oak + Cream' },
          { id: 'dn_marble', label: 'Furniture: Calacatta Top + Sage' },
          { id: 'dn_walnut', label: 'Furniture: Dark Walnut + Charcoal' }
        ]'''
new_dn_furn = '''        furniture: [
          { id: 'dn_oak', label: '★ AI Dining: 8-Seater Rectangular Oak' },
          { id: 'dn_round', label: 'Dining: 6-Seater Round Marble Pedestal' },
          { id: 'dn_banquet', label: 'Dining: Walnut Table + Tufted Bench' }
        ]'''
assert old_dn_furn in code
code = code.replace(old_dn_furn, new_dn_furn, 1)

old_st_furn = '''        furniture: [
          { id: 'st_cane', label: '★ AI Furniture: Natural Cane + Cream' },
          { id: 'st_sage', label: 'Furniture: Teak Rattan + Sage' }
        ]'''
new_st_furn = '''        furniture: [
          { id: 'st_cane', label: '★ AI Sitout: Twin Cane Lounge Chairs' },
          { id: 'st_loveseat', label: 'Sofa: Outdoor Rattan Loveseat + Tables' }
        ]'''
assert old_st_furn in code
code = code.replace(old_st_furn, new_st_furn, 1)

# 2. Replace createFocusFixtureMesh / registerRoomFocusLight / setRoomFocusLight / changeFurnitureStyle
#    so focus lights ALWAYS render at the room's exact default downlight coordinates (`coords`),
#    and furniture swaps rebuild the actual 3D sofa/furniture geometry!
old_focus_block_start = '    function createFocusFixtureMesh(style) {'
old_focus_block_end = '    function applyFurniturePreset(roomId, presetId) {'
s_fb = code.find(old_focus_block_start)
e_fb = code.find(old_focus_block_end)
assert s_fb != -1 and e_fb != -1, "focus block not found"

new_focus_and_sofa_js = '''    const roomDynamicFurnitureSlots = {};
    const roomFurnitureBuilders = {};

    function createFocusFixtureMesh(style, coords) {
      const g = new THREE.Group();
      const brass = new THREE.MeshStandardMaterial({ color: '#d4af37', metalness: 0.85, roughness: 0.24 });
      const darkMat = new THREE.MeshStandardMaterial({ color: '#1e293b', metalness: 0.7, roughness: 0.35 });
      const ceramic = new THREE.MeshStandardMaterial({ color: '#f1efe9', roughness: 0.25 });
      const glowWarm = new THREE.MeshStandardMaterial({ color: '#fff8e7', emissive: '#ffcf87', emissiveIntensity: 1.4 });
      const glowCool = new THREE.MeshStandardMaterial({ color: '#f8fafc', emissive: '#e0f2fe', emissiveIntensity: 1.4 });

      const pts = (coords && coords.length) ? coords : [[0, 0]];
      pts.forEach(([px, pz]) => {
        if (style === 'brass_track') {
          // Brushed brass surface spotlight canister at each default light position
          const base = new THREE.Mesh(new THREE.CylinderGeometry(0.28, 0.28, 0.08, 16), brass);
          base.position.set(px, 9.95, pz); g.add(base);
          const can = new THREE.Mesh(new THREE.CylinderGeometry(0.16, 0.18, 0.42, 14), brass);
          can.position.set(px, 9.7, pz); can.rotation.x = 0.25; g.add(can);
          const lens = new THREE.Mesh(new THREE.CircleGeometry(0.15, 14), glowWarm);
          lens.position.set(px, 9.5, pz + 0.09); lens.rotation.x = Math.PI / 2 + 0.25; g.add(lens);
        } else if (style === 'gallery_pin') {
          // Dark architectural gimbal pin-spot trim at each default light position
          const trim = new THREE.Mesh(new THREE.RingGeometry(0.20, 0.36, 18), darkMat);
          trim.rotation.x = Math.PI / 2; trim.position.set(px, 9.96, pz); g.add(trim);
          const inner = new THREE.Mesh(new THREE.CylinderGeometry(0.18, 0.18, 0.14, 16), darkMat);
          inner.position.set(px, 9.92, pz); g.add(inner);
          const lens = new THREE.Mesh(new THREE.CircleGeometry(0.16, 16), glowWarm);
          lens.rotation.x = Math.PI / 2; lens.position.set(px, 9.84, pz); g.add(lens);
        } else if (style === 'task_cool') {
          // Crisp 4000K recessed task downlight at each default light position
          const bezel = new THREE.Mesh(new THREE.RingGeometry(0.24, 0.38, 18), ceramic);
          bezel.rotation.x = Math.PI / 2; bezel.position.set(px, 9.96, pz); g.add(bezel);
          const lens = new THREE.Mesh(new THREE.CircleGeometry(0.24, 18), glowCool);
          lens.rotation.x = Math.PI / 2; lens.position.set(px, 9.95, pz); g.add(lens);
        } else if (style === 'cove_ambient') {
          // Soft brass-rimmed halo downlight at each default light position
          const bezel = new THREE.Mesh(new THREE.RingGeometry(0.26, 0.42, 20), brass);
          bezel.rotation.x = Math.PI / 2; bezel.position.set(px, 9.96, pz); g.add(bezel);
          const lens = new THREE.Mesh(new THREE.CircleGeometry(0.26, 20), glowWarm);
          lens.rotation.x = Math.PI / 2; lens.position.set(px, 9.95, pz); g.add(lens);
        } else {
          // warm_recessed (default)
          const bezel = new THREE.Mesh(new THREE.RingGeometry(0.22, 0.35, 18), ceramic);
          bezel.rotation.x = Math.PI / 2; bezel.position.set(px, 9.96, pz); g.add(bezel);
          const lens = new THREE.Mesh(new THREE.CircleGeometry(0.22, 18), glowWarm);
          lens.rotation.x = Math.PI / 2; lens.position.set(px, 9.95, pz); g.add(lens);
        }
      });
      return g;
    }

    function registerRoomFocusLight(roomId, parentGroup, defaultStyle, coords) {
      const slot = new THREE.Group();
      parentGroup.add(slot);
      roomFocusFixtures[roomId] = { slot, currentStyle: defaultStyle, coords: coords || [[0, 0]] };
      setRoomFocusLight(roomId, defaultStyle);
    }

    function setRoomFocusLight(roomId, style) {
      const entry = roomFocusFixtures[roomId];
      if (entry) {
        while (entry.slot.children.length > 0) entry.slot.remove(entry.slot.children[0]);
        entry.currentStyle = style;
        entry.slot.add(createFocusFixtureMesh(style, entry.coords));
      }
      if (currentRoomId === roomId && isInsideRoom) {
        const room = ROOMS.find(r => r.id === roomId);
        if (room) setupRoomLighting(room);
      }
    }

    function changeFocusLight(style) {
      if (!currentRoomId) return;
      setRoomFocusLight(currentRoomId, style);
      updateRoomInfoCardLighting();
    }

    function changeFurnitureStyle(presetId) {
      if (!currentRoomId) return;
      roomFurnitureState[currentRoomId] = presetId;
      if (roomFurnitureBuilders[currentRoomId]) {
        const slot = roomDynamicFurnitureSlots[currentRoomId];
        if (slot) {
          while (slot.children.length > 0) slot.remove(slot.children[0]);
          roomFurnitureBuilders[currentRoomId](slot, presetId);
        }
      } else {
        applyFurniturePreset(currentRoomId, presetId);
      }
      const recs = getRecommendationsForRoom(currentRoomId);
      const chosen = recs.furniture.find(f => f.id === presetId);
      const furnEl = document.getElementById('card-furniture');
      const room = ROOMS.find(r => r.id === currentRoomId);
      if (furnEl && room && chosen) {
        const cleanLabel = chosen.label.replace(/^★ AI [^:]+: /, '').replace(/^[^:]+: /, '');
        furnEl.textContent = `${cleanLabel} — ${room.furnitureText || room.furniture.map(f => f.name).join(', ')}`;
      }
    }

    function updateRoomInfoCardLighting() {
      if (!currentRoomId) return;
      const room = ROOMS.find(r => r.id === currentRoomId);
      if (!room) return;
      const recs = getRecommendationsForRoom(currentRoomId);
      const cId = roomCeilingFixtures[currentRoomId]?.currentStyle;
      const fId = roomFocusFixtures[currentRoomId]?.currentStyle;
      const cLabel = recs.ceiling.find(x => x.id === cId)?.label.replace(/^★ AI [^:]+: /, '').replace(/^[^:]+: /, '') || cId;
      const fLabel = recs.focus.find(x => x.id === fId)?.label.replace(/^★ AI [^:]+: /, '').replace(/^[^:]+: /, '') || fId;
      const lightEl = document.getElementById('card-lighting');
      if (lightEl) lightEl.textContent = `${cLabel} + ${fLabel} • ${room.lighting}`;
    }

'''

code = code[:s_fb] + new_focus_and_sofa_js + code[e_fb:]

# 3. Replace static addDownlights calls with registerRoomFocusLight(..., coords) and remove duplicate registerRoomFocusLight calls
focus_swaps = [
    # Bed 1
    ("      registerRoomFocusLight('bed1', b1, 'warm_recessed');", ""),
    ("      addDownlights(b1, [[-4.5, -3.5], [4.5, -3.5], [-4.5, 5.5], [4.5, 5.5]]);",
     "      registerRoomFocusLight('bed1', b1, 'warm_recessed', [[-4.5, -3.5], [4.5, -3.5], [-4.5, 5.5], [4.5, 5.5]]);"),
    # Baths
    ("        registerRoomFocusLight(roomId, bt, 'task_cool');", ""),
    ("        addDownlights(bt, [[0, -2.0], [0, 2.0]], true);",
     "        registerRoomFocusLight(roomId, bt, 'task_cool', [[0, -2.0], [0, 2.0]]);"),
    # Dress
    ("        registerRoomFocusLight(roomId, dr, 'warm_recessed');", ""),
    ("        addDownlights(dr, [[0, -1.5], [0, 1.5]], false);",
     "        registerRoomFocusLight(roomId, dr, 'warm_recessed', [[0, -1.5], [0, 1.5]]);"),
    # Bed 2
    ("      registerRoomFocusLight('bed2', b2, 'task_cool');", ""),
    ("      addDownlights(b2, [[-4, -3], [4, -3], [-4, 6], [4, 6]]);",
     "      registerRoomFocusLight('bed2', b2, 'task_cool', [[-4, -3], [4, -3], [-4, 6], [4, 6]]);"),
    # Pooja
    ("      registerRoomFocusLight('pooja', pj, 'gallery_pin');", ""),
    ("      addDownlights(pj, [[-2.8, -1.5], [2.8, -1.5], [-2.8, 2.5], [2.8, 2.5]]);",
     "      registerRoomFocusLight('pooja', pj, 'gallery_pin', [[-2.8, -1.5], [2.8, -1.5], [-2.8, 2.5], [2.8, 2.5]]);"),
    # Dining
    ("      registerRoomFocusLight('dining', dn, 'warm_recessed');", ""),
    ("      addDownlights(dn, [[-3.5, -3.5], [3.5, -3.5], [-3.5, 3.5], [3.5, 3.5]]);",
     "      registerRoomFocusLight('dining', dn, 'warm_recessed', [[-3.5, -3.5], [3.5, -3.5], [-3.5, 3.5], [3.5, 3.5]]);"),
    # Living Hall
    ("      registerRoomFocusLight('living', lv, 'warm_recessed');", ""),
    ("      addDownlights(lv, [[-10, -8], [0, -8], [10, -8], [-10, 6], [0, 6], [10, 6]]);",
     "      registerRoomFocusLight('living', lv, 'warm_recessed', [[-10, -8], [0, -8], [10, -8], [-10, 6], [0, 6], [10, 6]]);"),
    # Kitchen (replace static downlightsGroup with registerRoomFocusLight at exact same 6 coordinates!)
    ("      registerRoomFocusLight('kitchen', kt, 'task_cool');", ""),
    ('''      // --- 7. CEILING DOWNLIGHT RECESSED TRIMS ---
      const downlightsGroup = new THREE.Group();
      downlightsGroup.position.set(0, 9.97, 0);
      [[-6, -4], [0, -4], [6, -4], [-6, 2], [0, 2], [6, 2]].forEach(([dx, dz]) => {
        const dlBezel = new THREE.Mesh(new THREE.RingGeometry(0.25, 0.38, 16), new THREE.MeshBasicMaterial({ color: 0xffffff, side: THREE.DoubleSide }));
        dlBezel.rotation.x = Math.PI / 2;
        dlBezel.position.set(dx, 0, dz);
        downlightsGroup.add(dlBezel);
        const dlCenter = new THREE.Mesh(new THREE.CircleGeometry(0.25, 16), new THREE.MeshBasicMaterial({ color: 0xfffbeb, side: THREE.DoubleSide }));
        dlCenter.rotation.x = Math.PI / 2;
        dlCenter.position.set(dx, -0.005, dz);
        downlightsGroup.add(dlCenter);
      });
      kt.add(downlightsGroup);''',
     "      registerRoomFocusLight('kitchen', kt, 'task_cool', [[-6, -4], [0, -4], [6, -4], [-6, 2], [0, 2], [6, 2]]);"),
    # Drawing Hall
    ("      registerRoomFocusLight('drawing', dw, 'gallery_pin');", ""),
    ("      addDownlights(dw, [[-6.5, -7.5], [6.5, -7.5], [-6.5, 4.5], [6.5, 4.5]]);",
     "      registerRoomFocusLight('drawing', dw, 'gallery_pin', [[-6.5, -7.5], [6.5, -7.5], [-6.5, 4.5], [6.5, 4.5]]);"),
    # Wet Kitchen
    ("      registerRoomFocusLight('wetkitchen', wk, 'task_cool');", ""),
    ("      addDownlights(wk, [[-3.5, 0], [0, 0], [3.5, 0]], true);",
     "      registerRoomFocusLight('wetkitchen', wk, 'task_cool', [[-3.5, 0], [0, 0], [3.5, 0]]);"),
    # Store
    ("      addDownlights(st_rm, [[0, 0]], true);",
     "      registerRoomFocusLight('store', st_rm, 'task_cool', [[0, 0]]);"),
    # Sitout
    ("      registerRoomFocusLight('sitout', st, 'warm_recessed');", ""),
    ("      addDownlights(st, [[-7, 0], [7, 0]]);",
     "      registerRoomFocusLight('sitout', st, 'warm_recessed', [[-7, 0], [7, 0]]);")
]

for old, new in focus_swaps:
    assert old in code, f"Focus swap target not found: {old[:60]}"
    code = code.replace(old, new, 1)

# 4. Build true swappable 3D sofa / furniture layouts for Living Hall, Drawing Hall, Bedroom 1, Bedroom 2, Dining, and Sitout!

# 4a. Living Hall swappable sofa/table/chair slot
old_lv_seating = '''      // Sculpted L-Shaped Sectional Sofa (main run + chaise return + cushions + throw pillows)
      addSofa(lv, 0.5, 4.2, 14.0, 3.6, Math.PI, lvSofaMat, [lvAccentMat, lvPillowMat, ochreFabric]);
      addSofa(lv, -5.2, -1.8, 8.2, 3.4, Math.PI / 2, lvSofaMat, [ochreFabric, lvAccentMat]);

      // 2 Accent Lounge Armchairs & Side Table
      addArmchair(lv, 6.8, -3.0, -Math.PI * 0.65, lvAccentMat);
      addArmchair(lv, 6.8, 1.5, -Math.PI * 0.45, lvAccentMat);
      const sideTbl = new THREE.Mesh(new THREE.CylinderGeometry(0.95, 0.95, 1.65, 20), marbleMat);
      sideTbl.position.set(7.5, 0.82, -0.8); sideTbl.castShadow = true; lv.add(sideTbl);

      // Twin Nesting Coffee Tables (Calacatta Marble + Brass Base + Decor)
      const ctBase1 = new THREE.Mesh(new THREE.CylinderGeometry(1.9, 1.9, 1.0, 28), lvWoodMat);
      ctBase1.position.set(-0.2, 0.5, -1.6); ctBase1.castShadow = true; lv.add(ctBase1);
      const ctTop1 = new THREE.Mesh(new THREE.CylinderGeometry(2.3, 2.3, 0.16, 32), calaMat);
      ctTop1.position.set(-0.2, 1.08, -1.6); ctTop1.castShadow = true; lv.add(ctTop1);
      const ctTop2 = new THREE.Mesh(new THREE.CylinderGeometry(1.4, 1.4, 0.14, 24), marbleMat);
      ctTop2.position.set(2.1, 1.32, -2.5); ctTop2.castShadow = true; lv.add(ctTop2);
      const ctLeg2 = new THREE.Mesh(new THREE.CylinderGeometry(0.9, 0.9, 1.25, 20), brassMat);
      ctLeg2.position.set(2.1, 0.62, -2.5); lv.add(ctLeg2);
      // Coffee table books & vase
      const bkStack = new THREE.Mesh(new THREE.BoxGeometry(1.2, 0.25, 0.9), darkFabric);
      bkStack.position.set(-0.6, 1.28, -1.4); bkStack.rotation.y = 0.25; lv.add(bkStack);
      const lvVase = new THREE.Mesh(new THREE.CylinderGeometry(0.22, 0.34, 0.85, 16), ceramicMat);
      lvVase.position.set(0.4, 1.58, -1.9); lv.add(lvVase);'''

new_lv_seating = '''      const lvFurnSlot = new THREE.Group();
      lv.add(lvFurnSlot);
      roomDynamicFurnitureSlots['living'] = lvFurnSlot;
      roomFurnitureBuilders['living'] = function(slot, presetId) {
        if (presetId === 'lv_symmetrical') {
          // Twin Facing 3-Seater Emerald Velvet Sofas + Rectangular Walnut & Brass Coffee Table + Ottomans
          const emMat = new THREE.MeshStandardMaterial({ color: '#335947', roughness: 0.8 });
          addSofa(slot, -5.8, -1.0, 10.5, 3.5, Math.PI / 2, emMat, [ochreFabric, creamFabric]);
          addSofa(slot, 5.8, -1.0, 10.5, 3.5, -Math.PI / 2, emMat, [ochreFabric, creamFabric]);
          // Rectangular Walnut & Brass Coffee Table
          const rectTop = new THREE.Mesh(new THREE.BoxGeometry(3.6, 0.22, 6.2), walnutMat);
          rectTop.position.set(0, 1.35, -1.0); rectTop.castShadow = true; slot.add(rectTop);
          [[-1.5, -3.5], [1.5, -3.5], [-1.5, 1.5], [1.5, 1.5]].forEach(([lx, lz]) => {
            const leg = new THREE.Mesh(new THREE.CylinderGeometry(0.06, 0.05, 1.25, 10), brassMat);
            leg.position.set(lx, 0.62, lz); slot.add(leg);
          });
          const tray = new THREE.Mesh(new THREE.BoxGeometry(1.8, 0.08, 2.2), brassMat);
          tray.position.set(0, 1.5, -1.0); slot.add(tray);
          // Twin Tufted Ottomans facing fireplace
          [-2.2, 2.2].forEach(ox => {
            const ott = new THREE.Mesh(new THREE.CylinderGeometry(1.25, 1.25, 1.2, 24), creamFabric);
            ott.position.set(ox, 0.6, 5.2); ott.castShadow = true; slot.add(ott);
          });
        } else if (presetId === 'lv_curved') {
          // U-Shaped Bouclé Lounge + Swivel Barrel Chairs + Low Travertine Drum Table
          const chMat = new THREE.MeshStandardMaterial({ color: '#374151', roughness: 0.85 });
          addSofa(slot, 0, 4.8, 12.0, 3.5, Math.PI, chMat, [ochreFabric, creamFabric]);
          addSofa(slot, -6.2, -1.0, 8.0, 3.3, Math.PI / 2, creamFabric, [terraFabric]);
          addSofa(slot, 6.2, -1.0, 8.0, 3.3, -Math.PI / 2, creamFabric, [terraFabric]);
          // Oversized Round Travertine Drum Coffee Table
          const drum = new THREE.Mesh(new THREE.CylinderGeometry(2.8, 2.8, 1.15, 32), calaMat);
          drum.position.set(0, 0.58, -0.8); drum.castShadow = true; slot.add(drum);
          const lvVase = new THREE.Mesh(new THREE.CylinderGeometry(0.25, 0.38, 0.95, 16), ceramicMat);
          lvVase.position.set(0, 1.62, -0.8); slot.add(lvVase);
        } else {
          // Default AI Pick: L-Shaped Belgian Linen Sectional + 2 Accent Armchairs + Twin Nesting Marble Tables
          addSofa(slot, 0.5, 4.2, 14.0, 3.6, Math.PI, creamFabric, [sageFabric, terraFabric, ochreFabric]);
          addSofa(slot, -5.2, -1.8, 8.2, 3.4, Math.PI / 2, creamFabric, [ochreFabric, sageFabric]);
          addArmchair(slot, 6.8, -3.0, -Math.PI * 0.65, sageFabric);
          addArmchair(slot, 6.8, 1.5, -Math.PI * 0.45, greyFabric);
          const sideTbl = new THREE.Mesh(new THREE.CylinderGeometry(0.95, 0.95, 1.65, 20), marbleMat);
          sideTbl.position.set(7.5, 0.82, -0.8); sideTbl.castShadow = true; slot.add(sideTbl);
          const ctBase1 = new THREE.Mesh(new THREE.CylinderGeometry(1.9, 1.9, 1.0, 28), walnutMat);
          ctBase1.position.set(-0.2, 0.5, -1.6); ctBase1.castShadow = true; slot.add(ctBase1);
          const ctTop1 = new THREE.Mesh(new THREE.CylinderGeometry(2.3, 2.3, 0.16, 32), calaMat);
          ctTop1.position.set(-0.2, 1.08, -1.6); ctTop1.castShadow = true; slot.add(ctTop1);
          const ctTop2 = new THREE.Mesh(new THREE.CylinderGeometry(1.4, 1.4, 0.14, 24), marbleMat);
          ctTop2.position.set(2.1, 1.32, -2.5); ctTop2.castShadow = true; slot.add(ctTop2);
          const ctLeg2 = new THREE.Mesh(new THREE.CylinderGeometry(0.9, 0.9, 1.25, 20), brassMat);
          ctLeg2.position.set(2.1, 0.62, -2.5); slot.add(ctLeg2);
          const bkStack = new THREE.Mesh(new THREE.BoxGeometry(1.2, 0.25, 0.9), darkFabric);
          bkStack.position.set(-0.6, 1.28, -1.4); bkStack.rotation.y = 0.25; slot.add(bkStack);
          const lvVase = new THREE.Mesh(new THREE.CylinderGeometry(0.22, 0.34, 0.85, 16), ceramicMat);
          lvVase.position.set(0.4, 1.58, -1.9); slot.add(lvVase);
        }
      };
      roomFurnitureBuilders['living'](lvFurnSlot, 'lv_warmth');'''

assert old_lv_seating in code, "old_lv_seating not found"
code = code.replace(old_lv_seating, new_lv_seating, 1)

# 4b. Drawing Hall swappable sofa/table/chair slot
old_dw_seating = '''      // Sculpted Cream 3-Seater Sofa
      addSofa(dw, 0, -6.0, 9.2, 3.4, 0, dwSofaMat, [dwPillowMat, ochreFabric]);
      // Low Walnut Coffee Table with Books & Vase
      const dwTable = new THREE.Mesh(new THREE.BoxGeometry(4.4, 0.25, 2.6), dwWoodMat);
      dwTable.position.set(0, 1.25, -1.8); dwTable.castShadow = true; dw.add(dwTable);
      [[-1.8, -1.0], [1.8, -1.0], [-1.8, 1.0], [1.8, 1.0]].forEach(([lx, lz]) => {
        const leg = new THREE.Mesh(new THREE.CylinderGeometry(0.05, 0.04, 1.2, 8), metalMat);
        leg.position.set(lx, 0.6, -1.8 + lz); dw.add(leg);
      });
      const dwVase = new THREE.Mesh(new THREE.CylinderGeometry(0.2, 0.3, 0.75, 14), ceramicMat);
      dwVase.position.set(-0.6, 1.75, -1.8); dw.add(dwVase);
      // Left Armchair & Right Chaise
      addArmchair(dw, -6.2, -2.2, 0.55, dwAccentMat);
      addSofa(dw, 6.2, -2.2, 4.8, 3.0, -0.55, dwAccentMat, [ochreFabric]);'''

new_dw_seating = '''      const dwFurnSlot = new THREE.Group();
      dw.add(dwFurnSlot);
      roomDynamicFurnitureSlots['drawing'] = dwFurnSlot;
      roomFurnitureBuilders['drawing'] = function(slot, presetId) {
        if (presetId === 'dw_twin') {
          // Twin Facing Sage Linen Loveseats + Round Marble & Brass Coffee Table
          addSofa(slot, -5.2, -2.5, 7.6, 3.2, Math.PI / 2, sageFabric, [ochreFabric, creamFabric]);
          addSofa(slot, 5.2, -2.5, 7.6, 3.2, -Math.PI / 2, sageFabric, [ochreFabric, creamFabric]);
          const rTop = new THREE.Mesh(new THREE.CylinderGeometry(2.1, 2.1, 0.16, 28), calaMat);
          rTop.position.set(0, 1.3, -2.5); rTop.castShadow = true; slot.add(rTop);
          const rBase = new THREE.Mesh(new THREE.CylinderGeometry(0.9, 1.1, 1.2, 20), brassMat);
          rBase.position.set(0, 0.6, -2.5); slot.add(rBase);
        } else if (presetId === 'dw_sectional') {
          // Executive Charcoal L-Sectional + Swivel Chair + Smoked Oak Plinth Table
          addSofa(slot, -1.0, -6.0, 11.5, 3.5, 0, darkFabric, [ochreFabric, terraFabric]);
          addSofa(slot, -5.2, -1.2, 7.2, 3.3, Math.PI / 2, darkFabric, [ochreFabric]);
          addArmchair(slot, 6.0, -1.5, -0.65, greyFabric);
          const pTbl = new THREE.Mesh(new THREE.BoxGeometry(4.6, 0.9, 2.8), walnutMat);
          pTbl.position.set(0.2, 0.45, -1.5); pTbl.castShadow = true; slot.add(pTbl);
        } else {
          // Default AI Pick: Cream 3-Seater + Left Armchair + Right Chaise + Sled Coffee Table
          addSofa(slot, 0, -6.0, 9.2, 3.4, 0, creamFabric, [terraFabric, ochreFabric]);
          const dwTable = new THREE.Mesh(new THREE.BoxGeometry(4.4, 0.25, 2.6), oakMat);
          dwTable.position.set(0, 1.25, -1.8); dwTable.castShadow = true; slot.add(dwTable);
          [[-1.8, -1.0], [1.8, -1.0], [-1.8, 1.0], [1.8, 1.0]].forEach(([lx, lz]) => {
            const leg = new THREE.Mesh(new THREE.CylinderGeometry(0.05, 0.04, 1.2, 8), metalMat);
            leg.position.set(lx, 0.6, -1.8 + lz); slot.add(leg);
          });
          const dwVase = new THREE.Mesh(new THREE.CylinderGeometry(0.2, 0.3, 0.75, 14), ceramicMat);
          dwVase.position.set(-0.6, 1.75, -1.8); slot.add(dwVase);
          addArmchair(slot, -6.2, -2.2, 0.55, greyFabric);
          addSofa(slot, 6.2, -2.2, 4.8, 3.0, -0.55, darkFabric, [ochreFabric]);
        }
      };
      roomFurnitureBuilders['drawing'](dwFurnSlot, 'dw_formal');'''

assert old_dw_seating in code, "old_dw_seating not found"
code = code.replace(old_dw_seating, new_dw_seating, 1)

# 4c. Sitout swappable Cane Lounge Chairs vs Outdoor Rattan Loveseat Sofa
old_st_seating = '''      [-5.5, 5.5].forEach(sx => {
        const cGroup = new THREE.Group();
        cGroup.position.set(sx, 0, 0);
        cGroup.rotation.y = sx < 0 ? 0.45 : -0.45;
        const cSeat = new THREE.Mesh(new THREE.CylinderGeometry(1.5, 1.25, 1.4, 20), stCaneMat);
        cSeat.position.set(0, 0.7, 0); cSeat.castShadow = true; cGroup.add(cSeat);
        const cCush = new THREE.Mesh(new THREE.CylinderGeometry(1.38, 1.38, 0.28, 20), stCushMat);
        cCush.position.set(0, 1.52, 0); cGroup.add(cCush);
        const cBack = new THREE.Mesh(new THREE.CylinderGeometry(1.55, 1.45, 1.2, 20, 1, true, Math.PI * 0.2, Math.PI * 1.6), stCaneMat);
        cBack.position.set(0, 2.0, 0); cGroup.add(cBack);
        st.add(cGroup);
      });
      const rTab = new THREE.Mesh(new THREE.CylinderGeometry(1.5, 1.5, 0.14, 24), oakMat);
      rTab.position.set(0, 1.45, 0); rTab.castShadow = true; st.add(rTab);
      const rLeg = new THREE.Mesh(new THREE.CylinderGeometry(0.45, 0.65, 1.4, 16), metalMat);
      rLeg.position.set(0, 0.7, 0); st.add(rLeg);'''

new_st_seating = '''      const stFurnSlot = new THREE.Group();
      st.add(stFurnSlot);
      roomDynamicFurnitureSlots['sitout'] = stFurnSlot;
      roomFurnitureBuilders['sitout'] = function(slot, presetId) {
        if (presetId === 'st_loveseat') {
          addSofa(slot, 0, -1.2, 8.2, 3.0, 0, sageFabric, [creamFabric, ochreFabric]);
          const rTab = new THREE.Mesh(new THREE.BoxGeometry(3.8, 0.14, 1.8), oakMat);
          rTab.position.set(0, 1.35, 1.8); rTab.castShadow = true; slot.add(rTab);
        } else {
          [-5.5, 5.5].forEach(sx => {
            const cGroup = new THREE.Group();
            cGroup.position.set(sx, 0, 0);
            cGroup.rotation.y = sx < 0 ? 0.45 : -0.45;
            const cSeat = new THREE.Mesh(new THREE.CylinderGeometry(1.5, 1.25, 1.4, 20), oakMat);
            cSeat.position.set(0, 0.7, 0); cSeat.castShadow = true; cGroup.add(cSeat);
            const cCush = new THREE.Mesh(new THREE.CylinderGeometry(1.38, 1.38, 0.28, 20), creamFabric);
            cCush.position.set(0, 1.52, 0); cGroup.add(cCush);
            const cBack = new THREE.Mesh(new THREE.CylinderGeometry(1.55, 1.45, 1.2, 20, 1, true, Math.PI * 0.2, Math.PI * 1.6), oakMat);
            cBack.position.set(0, 2.0, 0); cGroup.add(cBack);
            slot.add(cGroup);
          });
          const rTab = new THREE.Mesh(new THREE.CylinderGeometry(1.5, 1.5, 0.14, 24), oakMat);
          rTab.position.set(0, 1.45, 0); rTab.castShadow = true; slot.add(rTab);
          const rLeg = new THREE.Mesh(new THREE.CylinderGeometry(0.45, 0.65, 1.4, 16), metalMat);
          rLeg.position.set(0, 0.7, 0); slot.add(rLeg);
        }
      };
      roomFurnitureBuilders['sitout'](stFurnSlot, 'st_cane');'''

assert old_st_seating in code, "old_st_seating not found"
code = code.replace(old_st_seating, new_st_seating, 1)

# 4d. Dining Table & Chairs swappable geometry (8-Seater Rectangular vs 6-Seater Round Marble vs Walnut + Bench)
old_dn_table = '''      const dt = new THREE.Mesh(new THREE.BoxGeometry(4.4, 0.25, 8.4), dnTableMat);
      dt.position.set(0, 2.55, 0); dt.castShadow = true; dt.receiveShadow = true; dn.add(dt);
      [-2.7, 2.7].forEach(tz => {
        const tleg = new THREE.Mesh(new THREE.BoxGeometry(3.2, 2.4, 0.45), walnutMat);
        tleg.position.set(0, 1.2, tz); tleg.castShadow = true; dn.add(tleg);
      });
      // Centerpiece Vase & Bowls
      const dVase = new THREE.Mesh(new THREE.CylinderGeometry(0.25, 0.35, 0.9, 16), ceramicMat);
      dVase.position.set(0, 3.1, 0); dn.add(dVase);
      // 8 Sculpted Dining Chairs (legs + padded seat + curved back)
      [-2.5, 2.5].forEach(cx => {
        [-2.9, -0.95, 0.95, 2.9].forEach(cz => {
          const ch = new THREE.Group();
          ch.position.set(cx, 0, cz);
          ch.rotation.y = cx > 0 ? -Math.PI / 2 : Math.PI / 2;
          const seat = new THREE.Mesh(new THREE.BoxGeometry(1.5, 0.22, 1.5), dnChairMat);
          seat.position.set(0, 1.55, 0); seat.castShadow = true; ch.add(seat);
          const back = new THREE.Mesh(new THREE.BoxGeometry(1.5, 1.6, 0.22), dnChairMat);
          back.position.set(0, 2.4, -0.65); back.rotation.x = -0.1; back.castShadow = true; ch.add(back);
          [[-0.6, -0.6], [0.6, -0.6], [-0.6, 0.6], [0.6, 0.6]].forEach(([lx, lz]) => {
            const leg = new THREE.Mesh(new THREE.CylinderGeometry(0.06, 0.04, 1.5, 8), walnutMat);
            leg.position.set(lx, 0.75, lz); ch.add(leg);
          });
          dn.add(ch);
        });
      });'''

new_dn_table = '''      const dnFurnSlot = new THREE.Group();
      dn.add(dnFurnSlot);
      roomDynamicFurnitureSlots['dining'] = dnFurnSlot;
      roomFurnitureBuilders['dining'] = function(slot, presetId) {
        function makeDiningChair(cx, cz, rotY, fabMat) {
          const ch = new THREE.Group();
          ch.position.set(cx, 0, cz); ch.rotation.y = rotY;
          const seat = new THREE.Mesh(new THREE.BoxGeometry(1.5, 0.22, 1.5), fabMat);
          seat.position.set(0, 1.55, 0); seat.castShadow = true; ch.add(seat);
          const back = new THREE.Mesh(new THREE.BoxGeometry(1.5, 1.6, 0.22), fabMat);
          back.position.set(0, 2.4, -0.65); back.rotation.x = -0.1; back.castShadow = true; ch.add(back);
          [[-0.6, -0.6], [0.6, -0.6], [-0.6, 0.6], [0.6, 0.6]].forEach(([lx, lz]) => {
            const leg = new THREE.Mesh(new THREE.CylinderGeometry(0.06, 0.04, 1.5, 8), walnutMat);
            leg.position.set(lx, 0.75, lz); ch.add(leg);
          });
          slot.add(ch);
        }
        if (presetId === 'dn_round') {
          const rTop = new THREE.Mesh(new THREE.CylinderGeometry(3.3, 3.3, 0.22, 36), calaMat);
          rTop.position.set(0, 2.55, 0); rTop.castShadow = true; slot.add(rTop);
          const ped = new THREE.Mesh(new THREE.CylinderGeometry(0.85, 1.35, 2.4, 24), walnutMat);
          ped.position.set(0, 1.2, 0); slot.add(ped);
          const dVase = new THREE.Mesh(new THREE.CylinderGeometry(0.25, 0.35, 0.9, 16), ceramicMat);
          dVase.position.set(0, 3.1, 0); slot.add(dVase);
          for (let i = 0; i < 6; i++) {
            const a = (i / 6) * Math.PI * 2;
            makeDiningChair(Math.cos(a) * 4.1, Math.sin(a) * 4.1, -a - Math.PI / 2, sageFabric);
          }
        } else if (presetId === 'dn_banquet') {
          const dt = new THREE.Mesh(new THREE.BoxGeometry(4.2, 0.25, 8.2), walnutMat);
          dt.position.set(0, 2.55, 0); dt.castShadow = true; slot.add(dt);
          [-2.7, 2.7].forEach(tz => {
            const tleg = new THREE.Mesh(new THREE.BoxGeometry(3.0, 2.4, 0.4), metalMat);
            tleg.position.set(0, 1.2, tz); slot.add(tleg);
          });
          const dVase = new THREE.Mesh(new THREE.CylinderGeometry(0.25, 0.35, 0.9, 16), brassMat);
          dVase.position.set(0, 3.1, 0); slot.add(dVase);
          const bench = new THREE.Mesh(new THREE.BoxGeometry(1.6, 1.45, 7.6), darkFabric);
          bench.position.set(-2.5, 0.85, 0); bench.castShadow = true; slot.add(bench);
          [-2.9, -0.95, 0.95, 2.9].forEach(cz => makeDiningChair(2.5, cz, -Math.PI / 2, greyFabric));
        } else {
          const dt = new THREE.Mesh(new THREE.BoxGeometry(4.4, 0.25, 8.4), oakMat);
          dt.position.set(0, 2.55, 0); dt.castShadow = true; dt.receiveShadow = true; slot.add(dt);
          [-2.7, 2.7].forEach(tz => {
            const tleg = new THREE.Mesh(new THREE.BoxGeometry(3.2, 2.4, 0.45), walnutMat);
            tleg.position.set(0, 1.2, tz); tleg.castShadow = true; slot.add(tleg);
          });
          const dVase = new THREE.Mesh(new THREE.CylinderGeometry(0.25, 0.35, 0.9, 16), ceramicMat);
          dVase.position.set(0, 3.1, 0); slot.add(dVase);
          [-2.5, 2.5].forEach(cx => {
            [-2.9, -0.95, 0.95, 2.9].forEach(cz => makeDiningChair(cx, cz, cx > 0 ? -Math.PI / 2 : Math.PI / 2, creamFabric));
          });
        }
      };
      roomFurnitureBuilders['dining'](dnFurnSlot, 'dn_oak');'''

assert old_dn_table in code, "old_dn_table not found"
code = code.replace(old_dn_table, new_dn_table, 1)

with open(index_path, 'w', encoding='utf-8') as f:
    f.write(code)

print("Upgraded focus lights to default coordinates and added full geometric sofa/furniture customization!")

