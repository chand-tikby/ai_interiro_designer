index_path = '/Users/puspharaj/Documents/Projects/ai-interior-designer/index.html'

with open(index_path, 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Update #room-actions-row HTML to host the 3 AI-recommended dropdowns
old_select_html = '''      <select id="ceiling-light-select" class="action-select" onchange="changeCeilingLight(this.value)" title="Choose Ceiling Light Fixture">
        <option value="chandelier">Ceiling: Brass Ring Chandelier</option>
        <option value="linear">Ceiling: Linear Globe Pendant</option>
        <option value="sputnik">Ceiling: Sputnik Starburst</option>
        <option value="pendant">Ceiling: Trio Dome Pendants</option>
        <option value="fan">Ceiling: Walnut Ceiling Fan</option>
        <option value="flush">Ceiling: Flush LED Halo</option>
      </select>'''

new_selects_html = '''      <select id="ceiling-light-select" class="action-select" onchange="changeCeilingLight(this.value)" title="AI-Recommended Ceiling Lights"></select>
      <select id="focus-light-select" class="action-select" onchange="changeFocusLight(this.value)" title="AI-Recommended Focus Lights"></select>
      <select id="furniture-style-select" class="action-select" onchange="changeFurnitureStyle(this.value)" title="AI-Recommended Furniture Styles"></select>'''

assert old_select_html in code, "old_select_html not found"
code = code.replace(old_select_html, new_selects_html, 1)

# 2. Add AI_ROOM_RECOMMENDATIONS, roomFocusFixtures, roomMaterialPacks, and switchers
anchor = '    const roomCeilingFixtures = {};'
assert anchor in code, "roomCeilingFixtures anchor not found"

ai_catalog_js = '''    const AI_ROOM_RECOMMENDATIONS = {
      living: {
        ceiling: [
          { id: 'chandelier', label: '★ AI Ceiling: Brass Ring Chandelier' },
          { id: 'sputnik', label: 'Ceiling: Sputnik Starburst' },
          { id: 'linear', label: 'Ceiling: Linear Globe Pendant' },
          { id: 'fan', label: 'Ceiling: Walnut Ceiling Fan' }
        ],
        focus: [
          { id: 'warm_recessed', label: '★ AI Focus: 2700K Warm Recessed Spots' },
          { id: 'brass_track', label: 'Focus: Brushed Brass Art Track' },
          { id: 'gallery_pin', label: 'Focus: Gallery Pin-Spot Wash' },
          { id: 'cove_ambient', label: 'Focus: Perimeter Cove Wash' }
        ],
        furniture: [
          { id: 'lv_warmth', label: '★ AI Furniture: Belgian Linen + Marble' },
          { id: 'lv_emerald', label: 'Furniture: Emerald Velvet + Brass' },
          { id: 'lv_charcoal', label: 'Furniture: Nordic Charcoal + Oak' }
        ]
      },
      drawing: {
        ceiling: [
          { id: 'sputnik', label: '★ AI Ceiling: Sputnik Starburst' },
          { id: 'chandelier', label: 'Ceiling: Brass Ring Chandelier' },
          { id: 'linear', label: 'Ceiling: Linear Globe Pendant' },
          { id: 'flush', label: 'Ceiling: Flush LED Halo' }
        ],
        focus: [
          { id: 'gallery_pin', label: '★ AI Focus: Gallery Pin-Spot Wash' },
          { id: 'brass_track', label: 'Focus: Brushed Brass Art Track' },
          { id: 'warm_recessed', label: 'Focus: 2700K Warm Recessed Spots' }
        ],
        furniture: [
          { id: 'dw_formal', label: '★ AI Furniture: Cream + Nero Marquina' },
          { id: 'dw_sage', label: 'Furniture: Sage Linen + Walnut' },
          { id: 'dw_dark', label: 'Furniture: Executive Charcoal + Brass' }
        ]
      },
      bed1: {
        ceiling: [
          { id: 'fan', label: '★ AI Ceiling: Walnut Ceiling Fan' },
          { id: 'chandelier', label: 'Ceiling: Brass Ring Chandelier' },
          { id: 'flush', label: 'Ceiling: Flush LED Halo' }
        ],
        focus: [
          { id: 'warm_recessed', label: '★ AI Focus: 2700K Bedside Warm Spots' },
          { id: 'cove_ambient', label: 'Focus: Soft Cove Wall Wash' },
          { id: 'brass_track', label: 'Focus: Brass Art Track' }
        ],
        furniture: [
          { id: 'b1_tufted', label: '★ AI Furniture: Tufted Grey + Sage King' },
          { id: 'b1_walnut', label: 'Furniture: Warm Walnut + Ochre King' },
          { id: 'b1_charcoal', label: 'Furniture: Hotel Noir Velvet King' }
        ]
      },
      bed2: {
        ceiling: [
          { id: 'fan', label: '★ AI Ceiling: Oak Ceiling Fan' },
          { id: 'sputnik', label: 'Ceiling: Sputnik Starburst' },
          { id: 'flush', label: 'Ceiling: Flush LED Halo' }
        ],
        focus: [
          { id: 'task_cool', label: '★ AI Focus: 4000K Study Task Spots' },
          { id: 'warm_recessed', label: 'Focus: 2700K Warm Recessed Spots' },
          { id: 'brass_track', label: 'Focus: Brushed Brass Track' }
        ],
        furniture: [
          { id: 'b2_study', label: '★ AI Furniture: Ochre Queen + Oak Study' },
          { id: 'b2_sage', label: 'Furniture: Botanical Sage + Walnut' },
          { id: 'b2_slate', label: 'Furniture: Minimalist Slate Studio' }
        ]
      },
      kitchen: {
        ceiling: [
          { id: 'pendant', label: '★ AI Ceiling: Trio Dome Pendants' },
          { id: 'linear', label: 'Ceiling: Linear Globe Pendant' },
          { id: 'flush', label: 'Ceiling: Flush LED Halo' }
        ],
        focus: [
          { id: 'task_cool', label: '★ AI Focus: 4000K Counter Task Spots' },
          { id: 'brass_track', label: 'Focus: Brushed Brass Island Track' },
          { id: 'warm_recessed', label: 'Focus: 2700K Warm Recessed Spots' }
        ],
        furniture: [
          { id: 'kt_navy_sage', label: '★ AI Furniture: Navy Island + Sage' },
          { id: 'kt_walnut', label: 'Furniture: Warm Walnut + Calacatta' },
          { id: 'kt_charcoal', label: 'Furniture: Matte Charcoal + Carrara' }
        ]
      },
      dining: {
        ceiling: [
          { id: 'linear', label: '★ AI Ceiling: Linear Globe Pendant' },
          { id: 'chandelier', label: 'Ceiling: Brass Ring Chandelier' },
          { id: 'pendant', label: 'Ceiling: Trio Dome Pendants' }
        ],
        focus: [
          { id: 'warm_recessed', label: '★ AI Focus: 2700K Dining Wash Spots' },
          { id: 'gallery_pin', label: 'Focus: Table Centerpiece Pin-Spot' },
          { id: 'cove_ambient', label: 'Focus: Perimeter Cove Wash' }
        ],
        furniture: [
          { id: 'dn_oak', label: '★ AI Furniture: European Oak + Cream' },
          { id: 'dn_marble', label: 'Furniture: Calacatta Top + Sage' },
          { id: 'dn_walnut', label: 'Furniture: Dark Walnut + Charcoal' }
        ]
      },
      pooja: {
        ceiling: [
          { id: 'pendant', label: '★ AI Ceiling: Brass Temple Pendants' },
          { id: 'chandelier', label: 'Ceiling: Brass Ring Chandelier' },
          { id: 'flush', label: 'Ceiling: Flush LED Halo' }
        ],
        focus: [
          { id: 'gallery_pin', label: '★ AI Focus: Sanctum Altar Pin-Spot' },
          { id: 'warm_recessed', label: 'Focus: 2700K Warm Recessed Spots' }
        ],
        furniture: [
          { id: 'pj_teak', label: '★ AI Furniture: Carved Teak + Marble' },
          { id: 'pj_marble', label: 'Furniture: White Marble + Brass' }
        ]
      },
      wetkitchen: {
        ceiling: [
          { id: 'flush', label: '★ AI Ceiling: Flush LED Halo' },
          { id: 'linear', label: 'Ceiling: Linear Utility Pendant' }
        ],
        focus: [
          { id: 'task_cool', label: '★ AI Focus: 4500K Utility Task Spots' },
          { id: 'brass_track', label: 'Focus: Directional Track Spots' }
        ],
        furniture: [
          { id: 'wk_slate', label: '★ AI Furniture: Slate Utility + Marble' },
          { id: 'wk_oak', label: 'Furniture: Natural Oak + Granite' }
        ]
      },
      sitout: {
        ceiling: [
          { id: 'fan', label: '★ AI Ceiling: Teak Veranda Fan' },
          { id: 'pendant', label: 'Ceiling: Trio Dome Pendants' },
          { id: 'flush', label: 'Ceiling: Flush LED Halo' }
        ],
        focus: [
          { id: 'warm_recessed', label: '★ AI Focus: 2700K Warm Veranda Spots' },
          { id: 'cove_ambient', label: 'Focus: Soft Evening Wash' }
        ],
        furniture: [
          { id: 'st_cane', label: '★ AI Furniture: Natural Cane + Cream' },
          { id: 'st_sage', label: 'Furniture: Teak Rattan + Sage' }
        ]
      }
    };

    function getRecommendationsForRoom(roomId) {
      if (AI_ROOM_RECOMMENDATIONS[roomId]) return AI_ROOM_RECOMMENDATIONS[roomId];
      if (roomId.startsWith('bath')) {
        return {
          ceiling: [{ id: 'flush', label: '★ AI Ceiling: Moisture-Safe LED Halo' }],
          focus: [
            { id: 'task_cool', label: '★ AI Focus: 4000K Vanity Task Spots' },
            { id: 'warm_recessed', label: 'Focus: 2700K Spa Warm Spots' }
          ],
          furniture: [
            { id: 'bt_walnut', label: '★ AI Furniture: Walnut + Calacatta' },
            { id: 'bt_slate', label: 'Furniture: Spa Charcoal + Marble' }
          ]
        };
      }
      if (roomId.startsWith('dress')) {
        return {
          ceiling: [
            { id: 'flush', label: '★ AI Ceiling: Flush LED Halo' },
            { id: 'sputnik', label: 'Ceiling: Boutique Sputnik' }
          ],
          focus: [
            { id: 'warm_recessed', label: '★ AI Focus: 3000K Wardrobe Spots' },
            { id: 'brass_track', label: 'Focus: Brushed Brass Track' }
          ],
          furniture: [
            { id: 'dr_walnut', label: '★ AI Furniture: Walnut + Sage Ottoman' },
            { id: 'dr_oak', label: 'Furniture: Light Oak + Cream Velvet' }
          ]
        };
      }
      return {
        ceiling: [{ id: 'flush', label: '★ AI Ceiling: Flush LED Halo' }],
        focus: [{ id: 'task_cool', label: '★ AI Focus: 4000K Utility Spots' }],
        furniture: [{ id: 'st_default', label: '★ AI Furniture: Modular Oak Shelving' }]
      };
    }

    const roomFocusFixtures = {};
    const roomFurnitureState = {};
    const roomMaterials = {};

    function createFocusFixtureMesh(style) {
      const g = new THREE.Group();
      const brass = new THREE.MeshStandardMaterial({ color: '#d4af37', metalness: 0.85, roughness: 0.24 });
      const darkMat = new THREE.MeshStandardMaterial({ color: '#1e293b', metalness: 0.7, roughness: 0.35 });
      const glowWarm = new THREE.MeshStandardMaterial({ color: '#fff8e7', emissive: '#ffcf87', emissiveIntensity: 1.4 });
      const glowCool = new THREE.MeshStandardMaterial({ color: '#f8fafc', emissive: '#e0f2fe', emissiveIntensity: 1.4 });

      if (style === 'brass_track') {
        const rail = new THREE.Mesh(new THREE.BoxGeometry(5.6, 0.08, 0.14), brass);
        rail.position.set(0, 9.92, -3.5); g.add(rail);
        [-2.0, 0, 2.0].forEach(tx => {
          const head = new THREE.Mesh(new THREE.CylinderGeometry(0.14, 0.18, 0.45, 14), brass);
          head.position.set(tx, 9.68, -3.5); head.rotation.x = 0.45; g.add(head);
          const lens = new THREE.Mesh(new THREE.CircleGeometry(0.15, 12), glowWarm);
          lens.position.set(tx, 9.48, -3.32); lens.rotation.x = Math.PI / 2 + 0.45; g.add(lens);
        });
      } else if (style === 'gallery_pin') {
        [[-3.0, -3.5], [3.0, -3.5], [-3.0, 3.5], [3.0, 3.5]].forEach(([px, pz]) => {
          const trim = new THREE.Mesh(new THREE.RingGeometry(0.18, 0.3, 16), darkMat);
          trim.rotation.x = Math.PI / 2; trim.position.set(px, 9.96, pz); g.add(trim);
          const lens = new THREE.Mesh(new THREE.CircleGeometry(0.18, 16), glowWarm);
          lens.rotation.x = Math.PI / 2; lens.position.set(px, 9.95, pz); g.add(lens);
        });
      } else if (style === 'task_cool') {
        [[-3.2, -3.2], [3.2, -3.2], [-3.2, 3.2], [3.2, 3.2]].forEach(([px, pz]) => {
          const lens = new THREE.Mesh(new THREE.CircleGeometry(0.24, 16), glowCool);
          lens.rotation.x = Math.PI / 2; lens.position.set(px, 9.95, pz); g.add(lens);
        });
      }
      return g;
    }

    function registerRoomFocusLight(roomId, parentGroup, defaultStyle) {
      const slot = new THREE.Group();
      parentGroup.add(slot);
      roomFocusFixtures[roomId] = { slot, currentStyle: defaultStyle };
      setRoomFocusLight(roomId, defaultStyle);
    }

    function setRoomFocusLight(roomId, style) {
      const entry = roomFocusFixtures[roomId];
      if (entry) {
        while (entry.slot.children.length > 0) entry.slot.remove(entry.slot.children[0]);
        entry.currentStyle = style;
        entry.slot.add(createFocusFixtureMesh(style));
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
      applyFurniturePreset(currentRoomId, presetId);
      const recs = getRecommendationsForRoom(currentRoomId);
      const chosen = recs.furniture.find(f => f.id === presetId);
      const furnEl = document.getElementById('card-furniture');
      const room = ROOMS.find(r => r.id === currentRoomId);
      if (furnEl && room && chosen) {
        furnEl.textContent = `${chosen.label.replace('★ AI Furniture: ', '').replace('Furniture: ', '')} — ${room.furnitureText || room.furniture.map(f => f.name).join(', ')}`;
      }
    }

    function updateRoomInfoCardLighting() {
      if (!currentRoomId) return;
      const room = ROOMS.find(r => r.id === currentRoomId);
      if (!room) return;
      const recs = getRecommendationsForRoom(currentRoomId);
      const cId = roomCeilingFixtures[currentRoomId]?.currentStyle;
      const fId = roomFocusFixtures[currentRoomId]?.currentStyle;
      const cLabel = recs.ceiling.find(x => x.id === cId)?.label.replace('★ AI Ceiling: ', '').replace('Ceiling: ', '') || cId;
      const fLabel = recs.focus.find(x => x.id === fId)?.label.replace('★ AI Focus: ', '').replace('Focus: ', '') || fId;
      const lightEl = document.getElementById('card-lighting');
      if (lightEl) lightEl.textContent = `${cLabel} + ${fLabel} • ${room.lighting}`;
    }

    function applyFurniturePreset(roomId, presetId) {
      roomFurnitureState[roomId] = presetId;
      const m = roomMaterials[roomId];
      if (!m) return;
      const presets = {
        lv_warmth: { primary: '#dfd9ce', accent: '#5d7a68', pillow: '#a85a44', wood: '#4a2e1b' },
        lv_emerald: { primary: '#3d6352', accent: '#c48b3b', pillow: '#dfd9ce', wood: '#5a3a22' },
        lv_charcoal: { primary: '#374151', accent: '#64748b', pillow: '#c48b3b', wood: '#2c1e16' },
        dw_formal: { primary: '#dfd9ce', accent: '#5c6672', pillow: '#a85a44', wood: '#6e4726' },
        dw_sage: { primary: '#5d7a68', accent: '#dfd9ce', pillow: '#c48b3b', wood: '#4a2e1b' },
        dw_dark: { primary: '#2b3440', accent: '#475569', pillow: '#d4af37', wood: '#1f1612' },
        b1_tufted: { primary: '#5c6672', accent: '#5d7a68', pillow: '#a85a44', wood: '#4a2e1b' },
        b1_walnut: { primary: '#4a2e1b', accent: '#c48b3b', pillow: '#dfd9ce', wood: '#3b2314' },
        b1_charcoal: { primary: '#1e293b', accent: '#475569', pillow: '#d4af37', wood: '#18181b' },
        b2_study: { primary: '#5c6672', accent: '#c48b3b', pillow: '#dfd9ce', wood: '#6e4726' },
        b2_sage: { primary: '#3d6352', accent: '#5d7a68', pillow: '#a85a44', wood: '#4a2e1b' },
        b2_slate: { primary: '#334155', accent: '#475569', pillow: '#94a3b8', wood: '#27272a' },
        kt_navy_sage: { primary: '#182c44', accent: '#5a7d66', pillow: '#6e4726', wood: '#1f2421' },
        kt_walnut: { primary: '#5a3a22', accent: '#7c5838', pillow: '#3d281a', wood: '#2d2a26' },
        kt_charcoal: { primary: '#27272a', accent: '#3f3f46', pillow: '#18181b', wood: '#111827' },
        dn_oak: { primary: '#a67b5b', accent: '#dfd9ce', pillow: '#4a2e1b', wood: '#4a2e1b' },
        dn_marble: { primary: '#eae6df', accent: '#5d7a68', pillow: '#4a2e1b', wood: '#3b2314' },
        dn_walnut: { primary: '#4a2e1b', accent: '#334155', pillow: '#27272a', wood: '#27170e' },
        pj_teak: { primary: '#4a2e1b', accent: '#a85a44', pillow: '#d4af37', wood: '#4a2e1b' },
        pj_marble: { primary: '#ebe6de', accent: '#c48b3b', pillow: '#d4af37', wood: '#cfc8bc' },
        bt_walnut: { primary: '#4a2e1b', accent: '#ebe6de', pillow: '#cbd5e1', wood: '#4a2e1b' },
        bt_slate: { primary: '#27272a', accent: '#374151', pillow: '#94a3b8', wood: '#18181b' },
        dr_walnut: { primary: '#4a2e1b', accent: '#5d7a68', pillow: '#d4af37', wood: '#4a2e1b' },
        dr_oak: { primary: '#9c7353', accent: '#dfd9ce', pillow: '#d4af37', wood: '#8c6445' },
        wk_slate: { primary: '#5c6672', accent: '#6e4726', pillow: '#334155', wood: '#1f2421' },
        wk_oak: { primary: '#8c6445', accent: '#4a2e1b', pillow: '#334155', wood: '#27272a' },
        st_cane: { primary: '#a67b5b', accent: '#dfd9ce', pillow: '#5d7a68', wood: '#8c6445' },
        st_sage: { primary: '#6e4726', accent: '#5d7a68', pillow: '#c48b3b', wood: '#4a2e1b' }
      };
      const p = presets[presetId];
      if (!p) return;
      if (m.primary) m.primary.color.set(p.primary);
      if (m.accent) m.accent.color.set(p.accent);
      if (m.pillow) m.pillow.color.set(p.pillow);
      if (m.wood) m.wood.color.set(p.wood);
    }

'''

code = code.replace(anchor, ai_catalog_js + anchor, 1)

# 3. Wire per-room materials & registerRoomFocusLight in buildDetailedFurniture()
# Master Bedroom (b1)
code = code.replace(
    '      // ── 1. MASTER BEDROOM (Bed 1) ──\n      const b1 = new THREE.Group();',
    '''      // ── 1. MASTER BEDROOM (Bed 1) ──
      const b1 = new THREE.Group();
      const b1HeadMat = darkFabric.clone();
      const b1DuvetMat = sageFabric.clone();
      const b1ShamMat = terraFabric.clone();
      const b1WoodMat = walnutMat.clone();
      roomMaterials['bed1'] = { primary: b1HeadMat, accent: b1DuvetMat, pillow: b1ShamMat, wood: b1WoodMat };
      roomFurnitureState['bed1'] = 'b1_tufted';
      registerRoomFocusLight('bed1', b1, 'warm_recessed');'''
)
code = code.replace(
    '      const hb1 = new THREE.Mesh(new THREE.BoxGeometry(7.6, 4.4, 0.5), darkFabric);',
    '      const hb1 = new THREE.Mesh(new THREE.BoxGeometry(7.6, 4.4, 0.5), b1HeadMat);'
)
code = code.replace(
    '      const duvet1 = new THREE.Mesh(new THREE.BoxGeometry(6.75, 0.32, 4.4), sageFabric);',
    '      const duvet1 = new THREE.Mesh(new THREE.BoxGeometry(6.75, 0.32, 4.4), b1DuvetMat);'
)
code = code.replace(
    '        const sham = new THREE.Mesh(new THREE.BoxGeometry(1.4, 0.45, 0.8), terraFabric);',
    '        const sham = new THREE.Mesh(new THREE.BoxGeometry(1.4, 0.45, 0.8), b1ShamMat);'
)
code = code.replace(
    '        const ns = new THREE.Mesh(new THREE.BoxGeometry(1.9, 1.7, 1.6), walnutMat);',
    '        const ns = new THREE.Mesh(new THREE.BoxGeometry(1.9, 1.7, 1.6), b1WoodMat);'
)

# Baths (bt)
code = code.replace(
    '      function buildBath(roomId, cx, cz, w, d) {\n        const bt = new THREE.Group();',
    '''      function buildBath(roomId, cx, cz, w, d) {
        const bt = new THREE.Group();
        const btVanMat = walnutMat.clone();
        const btTopMat = calaMat.clone();
        roomMaterials[roomId] = { primary: btVanMat, accent: btTopMat };
        roomFurnitureState[roomId] = 'bt_walnut';
        registerRoomFocusLight(roomId, bt, 'task_cool');'''
)
code = code.replace(
    '        const van = new THREE.Mesh(new THREE.BoxGeometry(4.4, 2.2, 1.7), walnutMat);',
    '        const van = new THREE.Mesh(new THREE.BoxGeometry(4.4, 2.2, 1.7), btVanMat);'
)
code = code.replace(
    '        const vanTop = new THREE.Mesh(new THREE.BoxGeometry(4.5, 0.16, 1.8), calaMat);',
    '        const vanTop = new THREE.Mesh(new THREE.BoxGeometry(4.5, 0.16, 1.8), btTopMat);'
)

# Dress rooms (dr)
code = code.replace(
    '      function buildDress(roomId, cx, cz) {\n        const dr = new THREE.Group();',
    '''      function buildDress(roomId, cx, cz) {
        const dr = new THREE.Group();
        const drWoodMat = walnutMat.clone();
        const drOttMat = sageFabric.clone();
        roomMaterials[roomId] = { primary: drWoodMat, accent: drOttMat };
        roomFurnitureState[roomId] = 'dr_walnut';
        registerRoomFocusLight(roomId, dr, 'warm_recessed');'''
)
code = code.replace(
    '        const wrd = new THREE.Mesh(new THREE.BoxGeometry(5.5, 9.0, 2.0), walnutMat);',
    '        const wrd = new THREE.Mesh(new THREE.BoxGeometry(5.5, 9.0, 2.0), drWoodMat);'
)
code = code.replace(
    '        const ottoman = new THREE.Mesh(new THREE.CylinderGeometry(1.1, 1.1, 1.3, 24), sageFabric);',
    '        const ottoman = new THREE.Mesh(new THREE.CylinderGeometry(1.1, 1.1, 1.3, 24), drOttMat);'
)

# Bed 2
code = code.replace(
    '      // ── 4. BEDROOM 2 (Guest / Study Suite) ──\n      const b2 = new THREE.Group();',
    '''      // ── 4. BEDROOM 2 (Guest / Study Suite) ──
      const b2 = new THREE.Group();
      const b2HeadMat = greyFabric.clone();
      const b2DuvetMat = ochreFabric.clone();
      const b2WoodMat = oakMat.clone();
      roomMaterials['bed2'] = { primary: b2HeadMat, accent: b2DuvetMat, wood: b2WoodMat };
      roomFurnitureState['bed2'] = 'b2_study';
      registerRoomFocusLight('bed2', b2, 'task_cool');'''
)
code = code.replace(
    '      const hb2 = new THREE.Mesh(new THREE.BoxGeometry(6.8, 4.0, 0.45), greyFabric);',
    '      const hb2 = new THREE.Mesh(new THREE.BoxGeometry(6.8, 4.0, 0.45), b2HeadMat);'
)
code = code.replace(
    '      const duvet2 = new THREE.Mesh(new THREE.BoxGeometry(6.3, 0.28, 4.2), ochreFabric);',
    '      const duvet2 = new THREE.Mesh(new THREE.BoxGeometry(6.3, 0.28, 4.2), b2DuvetMat);'
)
code = code.replace(
    '      const deskTop = new THREE.Mesh(new THREE.BoxGeometry(5.2, 0.16, 2.2), oakMat);',
    '      const deskTop = new THREE.Mesh(new THREE.BoxGeometry(5.2, 0.16, 2.2), b2WoodMat);'
)

# Pooja
code = code.replace(
    '      // ── 5. POOJA SANCTUM ──\n      const pj = new THREE.Group();',
    '''      // ── 5. POOJA SANCTUM ──
      const pj = new THREE.Group();
      const pjWoodMat = walnutMat.clone();
      const pjRugMat = terraFabric.clone();
      roomMaterials['pooja'] = { primary: pjWoodMat, accent: pjRugMat };
      roomFurnitureState['pooja'] = 'pj_teak';
      registerRoomFocusLight('pooja', pj, 'gallery_pin');'''
)
code = code.replace(
    '      const mBase = new THREE.Mesh(new THREE.BoxGeometry(5.4, 2.6, 2.8), walnutMat);',
    '      const mBase = new THREE.Mesh(new THREE.BoxGeometry(5.4, 2.6, 2.8), pjWoodMat);'
)
code = code.replace(
    '      const prayerRug = new THREE.Mesh(new THREE.PlaneGeometry(5.0, 4.5), terraFabric);',
    '      const prayerRug = new THREE.Mesh(new THREE.PlaneGeometry(5.0, 4.5), pjRugMat);'
)

# Dining
code = code.replace(
    '      // ── 6. DINING ROOM ──\n      const dn = new THREE.Group();',
    '''      // ── 6. DINING ROOM ──
      const dn = new THREE.Group();
      const dnTableMat = oakMat.clone();
      const dnChairMat = creamFabric.clone();
      const dnSideMat = walnutMat.clone();
      roomMaterials['dining'] = { primary: dnTableMat, accent: dnChairMat, wood: dnSideMat };
      roomFurnitureState['dining'] = 'dn_oak';
      registerRoomFocusLight('dining', dn, 'warm_recessed');'''
)
code = code.replace(
    '      const dt = new THREE.Mesh(new THREE.BoxGeometry(4.4, 0.25, 8.4), oakMat);',
    '      const dt = new THREE.Mesh(new THREE.BoxGeometry(4.4, 0.25, 8.4), dnTableMat);'
)
code = code.replace(
    '          const seat = new THREE.Mesh(new THREE.BoxGeometry(1.5, 0.22, 1.5), creamFabric);',
    '          const seat = new THREE.Mesh(new THREE.BoxGeometry(1.5, 0.22, 1.5), dnChairMat);'
)
code = code.replace(
    '          const back = new THREE.Mesh(new THREE.BoxGeometry(1.5, 1.6, 0.22), creamFabric);',
    '          const back = new THREE.Mesh(new THREE.BoxGeometry(1.5, 1.6, 0.22), dnChairMat);'
)
code = code.replace(
    '      const sideb = new THREE.Mesh(new THREE.BoxGeometry(5.6, 2.8, 1.5), walnutMat);',
    '      const sideb = new THREE.Mesh(new THREE.BoxGeometry(5.6, 2.8, 1.5), dnSideMat);'
)

# Living Hall
code = code.replace(
    '      // ── 7. LIVING HALL (Grand Pavilion, Chandelier, Fireplace, Sectional, Spiral Staircase) ──\n      const lv = new THREE.Group();',
    '''      // ── 7. LIVING HALL (Grand Pavilion, Chandelier, Fireplace, Sectional, Spiral Staircase) ──
      const lv = new THREE.Group();
      const lvSofaMat = creamFabric.clone();
      const lvAccentMat = sageFabric.clone();
      const lvPillowMat = terraFabric.clone();
      const lvWoodMat = walnutMat.clone();
      roomMaterials['living'] = { primary: lvSofaMat, accent: lvAccentMat, pillow: lvPillowMat, wood: lvWoodMat };
      roomFurnitureState['living'] = 'lv_warmth';
      registerRoomFocusLight('living', lv, 'warm_recessed');'''
)
code = code.replace(
    '      addSofa(lv, 0.5, 4.2, 14.0, 3.6, Math.PI, creamFabric, [sageFabric, terraFabric, ochreFabric]);\n      addSofa(lv, -5.2, -1.8, 8.2, 3.4, Math.PI / 2, creamFabric, [ochreFabric, sageFabric]);\n\n      // 2 Accent Lounge Armchairs & Side Table\n      addArmchair(lv, 6.8, -3.0, -Math.PI * 0.65, sageFabric);\n      addArmchair(lv, 6.8, 1.5, -Math.PI * 0.45, greyFabric);',
    '''      addSofa(lv, 0.5, 4.2, 14.0, 3.6, Math.PI, lvSofaMat, [lvAccentMat, lvPillowMat, ochreFabric]);
      addSofa(lv, -5.2, -1.8, 8.2, 3.4, Math.PI / 2, lvSofaMat, [ochreFabric, lvAccentMat]);

      // 2 Accent Lounge Armchairs & Side Table
      addArmchair(lv, 6.8, -3.0, -Math.PI * 0.65, lvAccentMat);
      addArmchair(lv, 6.8, 1.5, -Math.PI * 0.45, lvAccentMat);'''
)
code = code.replace(
    '      const ctBase1 = new THREE.Mesh(new THREE.CylinderGeometry(1.9, 1.9, 1.0, 28), walnutMat);',
    '      const ctBase1 = new THREE.Mesh(new THREE.CylinderGeometry(1.9, 1.9, 1.0, 28), lvWoodMat);'
)

# Kitchen
code = code.replace(
    '      const navyIslandMat = new THREE.MeshStandardMaterial({ color: 0x182c44, roughness: 0.45 });\n      const goldBrassMat = new THREE.MeshStandardMaterial({ color: 0xd4af37, metalness: 0.85, roughness: 0.22 });\n      const sageCabinetMat = new THREE.MeshStandardMaterial({ color: 0x5a7d66, roughness: 0.42 });',
    '''      const navyIslandMat = new THREE.MeshStandardMaterial({ color: 0x182c44, roughness: 0.45 });
      const goldBrassMat = new THREE.MeshStandardMaterial({ color: 0xd4af37, metalness: 0.85, roughness: 0.22 });
      const sageCabinetMat = new THREE.MeshStandardMaterial({ color: 0x5a7d66, roughness: 0.42 });
      roomMaterials['kitchen'] = { primary: navyIslandMat, accent: sageCabinetMat };
      roomFurnitureState['kitchen'] = 'kt_navy_sage';
      registerRoomFocusLight('kitchen', kt, 'task_cool');'''
)

# Drawing Hall
code = code.replace(
    '      // ── 9. DRAWING HALL (Formal Lounge with Chandelier, Sofa, Media Unit & Marble Wall) ──\n      const dw = new THREE.Group();',
    '''      // ── 9. DRAWING HALL (Formal Lounge with Chandelier, Sofa, Media Unit & Marble Wall) ──
      const dw = new THREE.Group();
      const dwSofaMat = creamFabric.clone();
      const dwAccentMat = greyFabric.clone();
      const dwPillowMat = terraFabric.clone();
      const dwWoodMat = oakMat.clone();
      roomMaterials['drawing'] = { primary: dwSofaMat, accent: dwAccentMat, pillow: dwPillowMat, wood: dwWoodMat };
      roomFurnitureState['drawing'] = 'dw_formal';
      registerRoomFocusLight('drawing', dw, 'gallery_pin');'''
)
code = code.replace(
    '      addSofa(dw, 0, -6.0, 9.2, 3.4, 0, creamFabric, [terraFabric, ochreFabric]);',
    '      addSofa(dw, 0, -6.0, 9.2, 3.4, 0, dwSofaMat, [dwPillowMat, ochreFabric]);'
)
code = code.replace(
    '      addArmchair(dw, -6.2, -2.2, 0.55, greyFabric);\n      addSofa(dw, 6.2, -2.2, 4.8, 3.0, -0.55, darkFabric, [ochreFabric]);',
    '      addArmchair(dw, -6.2, -2.2, 0.55, dwAccentMat);\n      addSofa(dw, 6.2, -2.2, 4.8, 3.0, -0.55, dwAccentMat, [ochreFabric]);'
)
code = code.replace(
    '      const dwTable = new THREE.Mesh(new THREE.BoxGeometry(4.4, 0.25, 2.6), oakMat);',
    '      const dwTable = new THREE.Mesh(new THREE.BoxGeometry(4.4, 0.25, 2.6), dwWoodMat);'
)

# Wet Kitchen
code = code.replace(
    '      const wk = new THREE.Group();\n      wk.position.set(8.8, 0, 78.8);',
    '''      const wk = new THREE.Group();
      wk.position.set(8.8, 0, 78.8);
      const wkCabMat = greyFabric.clone();
      const wkWallMat = oakMat.clone();
      roomMaterials['wetkitchen'] = { primary: wkCabMat, accent: wkWallMat };
      roomFurnitureState['wetkitchen'] = 'wk_slate';
      registerRoomFocusLight('wetkitchen', wk, 'task_cool');'''
)
code = code.replace(
    '      const wkCounter = new THREE.Mesh(new THREE.BoxGeometry(2.2, 2.7, 7.6), greyFabric);',
    '      const wkCounter = new THREE.Mesh(new THREE.BoxGeometry(2.2, 2.7, 7.6), wkCabMat);'
)
code = code.replace(
    '      const wkUp = new THREE.Mesh(new THREE.BoxGeometry(1.2, 2.3, 6.2), oakMat);',
    '      const wkUp = new THREE.Mesh(new THREE.BoxGeometry(1.2, 2.3, 6.2), wkWallMat);'
)

# Sitout
code = code.replace(
    '      // ── 11. SITOUT (Covered Veranda with Cane Lounge, Tea Table, Palms & Ceiling Fan) ──\n      const st = new THREE.Group();',
    '''      // ── 11. SITOUT (Covered Veranda with Cane Lounge, Tea Table, Palms & Ceiling Fan) ──
      const st = new THREE.Group();
      const stCaneMat = oakMat.clone();
      const stCushMat = creamFabric.clone();
      roomMaterials['sitout'] = { primary: stCaneMat, accent: stCushMat };
      roomFurnitureState['sitout'] = 'st_cane';
      registerRoomFocusLight('sitout', st, 'warm_recessed');'''
)
code = code.replace(
    '        const cSeat = new THREE.Mesh(new THREE.CylinderGeometry(1.5, 1.25, 1.4, 20), oakMat);',
    '        const cSeat = new THREE.Mesh(new THREE.CylinderGeometry(1.5, 1.25, 1.4, 20), stCaneMat);'
)
code = code.replace(
    '        const cCush = new THREE.Mesh(new THREE.CylinderGeometry(1.38, 1.38, 0.28, 20), creamFabric);',
    '        const cCush = new THREE.Mesh(new THREE.CylinderGeometry(1.38, 1.38, 0.28, 20), stCushMat);'
)
code = code.replace(
    '        const cBack = new THREE.Mesh(new THREE.CylinderGeometry(1.55, 1.45, 1.2, 20, 1, true, Math.PI * 0.2, Math.PI * 1.6), oakMat);',
    '        const cBack = new THREE.Mesh(new THREE.CylinderGeometry(1.55, 1.45, 1.2, 20, 1, true, Math.PI * 0.2, Math.PI * 1.6), stCaneMat);'
)

# 4. Update enterRoom() to populate the 3 AI-recommended dropdowns dynamically for that room
old_enter_sync = '''      const clSelect = document.getElementById('ceiling-light-select');
      const activeStyle = roomCeilingFixtures[roomId]?.currentStyle || 'chandelier';
      if (clSelect) clSelect.value = activeStyle;
      const lightEl = document.getElementById('card-lighting');
      if (lightEl) lightEl.textContent = `${CEILING_LIGHT_LABELS[activeStyle] || activeStyle} • ${room.lighting}`;'''

new_enter_sync = '''      const recs = getRecommendationsForRoom(roomId);
      const clSelect = document.getElementById('ceiling-light-select');
      if (clSelect) {
        clSelect.innerHTML = recs.ceiling.map(o => `<option value="${o.id}">${o.label}</option>`).join('');
        clSelect.value = roomCeilingFixtures[roomId]?.currentStyle || recs.ceiling[0].id;
      }
      const flSelect = document.getElementById('focus-light-select');
      if (flSelect) {
        flSelect.innerHTML = recs.focus.map(o => `<option value="${o.id}">${o.label}</option>`).join('');
        flSelect.value = roomFocusFixtures[roomId]?.currentStyle || recs.focus[0].id;
      }
      const frSelect = document.getElementById('furniture-style-select');
      if (frSelect) {
        frSelect.innerHTML = recs.furniture.map(o => `<option value="${o.id}">${o.label}</option>`).join('');
        frSelect.value = roomFurnitureState[roomId] || recs.furniture[0].id;
      }
      updateRoomInfoCardLighting();'''

assert old_enter_sync in code, "old_enter_sync not found"
code = code.replace(old_enter_sync, new_enter_sync, 1)

# 5. Update changeCeilingLight to also call updateRoomInfoCardLighting()
old_chg_ceil = '''    function changeCeilingLight(style) {
      if (!currentRoomId) return;
      setRoomCeilingLight(currentRoomId, style);
      const room = ROOMS.find(r => r.id === currentRoomId);
      if (room) {
        const lightEl = document.getElementById('card-lighting');
        const label = CEILING_LIGHT_LABELS[style] || style;
        if (lightEl) lightEl.textContent = `${label} • ${room.lighting}`;
      }
    }'''

new_chg_ceil = '''    function changeCeilingLight(style) {
      if (!currentRoomId) return;
      setRoomCeilingLight(currentRoomId, style);
      updateRoomInfoCardLighting();
    }'''

assert old_chg_ceil in code, "old_chg_ceil not found"
code = code.replace(old_chg_ceil, new_chg_ceil, 1)

# 6. Update setupRoomLighting(room) to reflect active Focus Light style (color, angle, intensity)
old_setup_room = '''      // Dedicated recessed ceiling spotlight (balanced so surfaces retain texture & depth)
      const isCool = (room.floor === 'tile' && room.id !== 'sitout');
      const spot = new THREE.SpotLight(isCool ? '#f8fafc' : '#ffe8cc', 0.95);
      spot.position.set(cx, 9.6, cz);
      spot.target.position.set(cx, 0, cz);
      spot.angle = Math.PI / 2.6;
      spot.penumbra = 0.75;
      spot.distance = 28;
      spot.castShadow = true;
      lightsGroup.add(spot);
      lightsGroup.add(spot.target);'''

new_setup_room = '''      const fStyle = roomFocusFixtures[room.id]?.currentStyle || ((room.floor === 'tile' && room.id !== 'sitout') ? 'task_cool' : 'warm_recessed');
      let spotColor = '#ffe8cc', spotIntensity = 0.95, spotAngle = Math.PI / 2.6, spotTargetZ = cz;
      if (fStyle === 'task_cool') { spotColor = '#f1f5f9'; spotIntensity = 1.1; }
      else if (fStyle === 'gallery_pin') { spotColor = '#ffd89b'; spotIntensity = 1.25; spotAngle = Math.PI / 4.5; spotTargetZ = cz - 4.0; }
      else if (fStyle === 'brass_track') { spotColor = '#ffe0b2'; spotIntensity = 1.1; spotAngle = Math.PI / 3.4; spotTargetZ = cz - 3.0; }
      else if (fStyle === 'cove_ambient') { spotColor = '#ffd296'; spotIntensity = 0.75; spotAngle = Math.PI / 2.1; }

      const spot = new THREE.SpotLight(spotColor, spotIntensity);
      spot.position.set(cx, 9.6, cz);
      spot.target.position.set(cx, 0, spotTargetZ);
      spot.angle = spotAngle;
      spot.penumbra = 0.75;
      spot.distance = 28;
      spot.castShadow = true;
      lightsGroup.add(spot);
      lightsGroup.add(spot.target);'''

assert old_setup_room in code, "old_setup_room not found"
code = code.replace(old_setup_room, new_setup_room, 1)

with open(index_path, 'w', encoding='utf-8') as f:
    f.write(code)

print("AI Room Recommendations for Ceiling Lights, Focus Lights & Furniture added successfully!")

