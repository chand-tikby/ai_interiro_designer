index_path = '/Users/puspharaj/Documents/Projects/ai-interior-designer/index.html'

with open(index_path, 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Expand CEILING_LIGHT_LABELS
old_labels = '''    const CEILING_LIGHT_LABELS = {
      chandelier: '3-Tier Brass Halo Chandelier',
      drum_trio: 'Trio Cream Drum Pendants',
      crystal_ring: 'Crystal & Gold Ring Chandelier',
      linear: 'Linear Opal Globe Pendant',
      sputnik: 'Modern Sputnik Starburst',
      pendant: 'Trio Brass Dome Pendants',
      fan: 'Walnut & Brass Ceiling Fan',
      flush: 'Minimalist Flush LED Halo'
    };'''

new_labels = '''    const CEILING_LIGHT_LABELS = {
      chandelier: '3-Tier Brass Halo Chandelier',
      crystal_ring: 'Crystal & Gold Ring Chandelier',
      glass_cluster: 'Cascading Glass Globe Cluster',
      geometric_grid: 'Architectural Black & Brass Grid',
      drum_trio: 'Trio Cream Drum Pendants',
      woven_rattan: 'Woven Rattan Dome Pendant',
      linear: 'Linear Opal Globe Pendant',
      sputnik: 'Modern Sputnik Starburst',
      pendant: 'Trio Brass Dome Pendants',
      fan: 'Walnut & Brass Ceiling Fan',
      double_fan: 'Matte Black 5-Blade Fan + LED',
      flush: 'Minimalist Flush LED Halo'
    };'''

assert old_labels in code, "old_labels not found"
code = code.replace(old_labels, new_labels, 1)

# 2. Add 4 new 3D ceiling fixtures in createCeilingFixtureMesh
old_flush = '''      } else {
        // flush LED halo'''

new_fixtures = '''      } else if (style === 'glass_cluster') {
        const canopy = new THREE.Mesh(new THREE.CylinderGeometry(0.65, 0.65, 0.1, 24), brass);
        canopy.position.set(0, 9.95, 0); g.add(canopy);
        const orbs = [
          [0, 7.1, 0, 0.36], [-0.65, 7.6, 0.45, 0.28], [0.65, 7.8, -0.4, 0.30],
          [-0.45, 8.2, -0.6, 0.25], [0.55, 7.35, 0.55, 0.26]
        ];
        orbs.forEach(([ox, oy, oz, r]) => {
          const h = 9.95 - oy;
          const cord = new THREE.Mesh(new THREE.CylinderGeometry(0.015, 0.015, h, 6), darkMetal);
          cord.position.set(ox, oy + h / 2, oz); g.add(cord);
          const orb = new THREE.Mesh(new THREE.SphereGeometry(r, 16, 16), glowWarm);
          orb.position.set(ox, oy, oz); g.add(orb);
        });
        const pt = new THREE.PointLight('#ffe8c8', 0.95, 20, 1.5);
        pt.position.set(0, 7.4, 0); g.add(pt);
      } else if (style === 'woven_rattan') {
        const cord = new THREE.Mesh(new THREE.CylinderGeometry(0.03, 0.03, 2.3, 8), darkMetal);
        cord.position.set(0, 8.85, 0); g.add(cord);
        const rattanMat = new THREE.MeshStandardMaterial({ color: '#b5895a', roughness: 0.85, side: THREE.DoubleSide });
        const shade = new THREE.Mesh(new THREE.SphereGeometry(1.35, 24, 16, 0, Math.PI * 2, 0, Math.PI * 0.6), rattanMat);
        shade.position.set(0, 7.7, 0); shade.castShadow = true; g.add(shade);
        const bulb = new THREE.Mesh(new THREE.SphereGeometry(0.28, 12, 12), glowWarm);
        bulb.position.set(0, 7.35, 0); g.add(bulb);
        const pt = new THREE.PointLight('#ffdca8', 0.9, 18, 1.6);
        pt.position.set(0, 7.1, 0); g.add(pt);
      } else if (style === 'geometric_grid') {
        [-1.8, 1.8].forEach(rx => {
          const rod = new THREE.Mesh(new THREE.CylinderGeometry(0.025, 0.025, 1.8, 8), darkMetal);
          rod.position.set(rx, 9.1, 0); g.add(rod);
        });
        const frame = new THREE.Mesh(new THREE.BoxGeometry(4.4, 0.12, 2.2), darkMetal);
        frame.position.set(0, 8.2, 0); g.add(frame);
        [-1.5, 0, 1.5].forEach(bx => {
          const bar = new THREE.Mesh(new THREE.BoxGeometry(0.1, 0.14, 2.1), glowWarm);
          bar.position.set(bx, 8.15, 0); g.add(bar);
        });
        const pt = new THREE.PointLight('#fff0d8', 0.9, 20, 1.5);
        pt.position.set(0, 7.8, 0); g.add(pt);
      } else if (style === 'double_fan') {
        const rod = new THREE.Mesh(new THREE.CylinderGeometry(0.06, 0.06, 1.0, 12), darkMetal);
        rod.position.set(0, 9.5, 0); g.add(rod);
        const hub = new THREE.Mesh(new THREE.CylinderGeometry(0.38, 0.38, 0.25, 20), darkMetal);
        hub.position.set(0, 8.9, 0); g.add(hub);
        const dome = new THREE.Mesh(new THREE.CylinderGeometry(0.32, 0.32, 0.1, 20), glowWarm);
        dome.position.set(0, 8.75, 0); g.add(dome);
        for (let i = 0; i < 5; i++) {
          const blade = new THREE.Mesh(new THREE.BoxGeometry(2.2, 0.04, 0.36), darkMetal);
          const a = (i / 5) * Math.PI * 2;
          blade.position.set(Math.cos(a) * 1.2, 8.92, Math.sin(a) * 1.2);
          blade.rotation.y = -a;
          g.add(blade);
        }
        const pt = new THREE.PointLight('#ffe8cc', 0.7, 16, 1.6);
        pt.position.set(0, 8.4, 0); g.add(pt);
      } else {
        // flush LED halo'''

assert old_flush in code, "old_flush not found"
code = code.replace(old_flush, new_fixtures, 1)

# 3. Add 3 new Focus Light styles in createFocusFixtureMesh
old_focus_else = '''        } else {
          // warm_recessed (default)'''

new_focus_styles = '''        } else if (style === 'square_gimbal') {
          const trim = new THREE.Mesh(new THREE.BoxGeometry(0.62, 0.06, 0.62), darkMat);
          trim.position.set(px, 9.96, pz); g.add(trim);
          const lens = new THREE.Mesh(new THREE.BoxGeometry(0.42, 0.08, 0.42), glowWarm);
          lens.position.set(px, 9.94, pz); g.add(lens);
        } else if (style === 'copper_pendant_spot') {
          const cyl = new THREE.Mesh(new THREE.CylinderGeometry(0.14, 0.14, 0.65, 16), brass);
          cyl.position.set(px, 9.65, pz); g.add(cyl);
          const lens = new THREE.Mesh(new THREE.CircleGeometry(0.13, 14), glowWarm);
          lens.rotation.x = Math.PI / 2; lens.position.set(px, 9.32, pz); g.add(lens);
        } else if (style === 'daylight_panel') {
          const ring = new THREE.Mesh(new THREE.RingGeometry(0.28, 0.42, 20), ceramic);
          ring.rotation.x = Math.PI / 2; ring.position.set(px, 9.96, pz); g.add(ring);
          const lens = new THREE.Mesh(new THREE.CircleGeometry(0.28, 20), glowCool);
          lens.rotation.x = Math.PI / 2; lens.position.set(px, 9.95, pz); g.add(lens);
        } else {
          // warm_recessed (default)'''

assert old_focus_else in code, "old_focus_else not found"
code = code.replace(old_focus_else, new_focus_styles, 1)

# 4. Expand AI_ROOM_RECOMMENDATIONS with ~10 Ceiling Lights, 8 Focus Lights, and 6-8 Furniture options
old_recs_start = '    const AI_ROOM_RECOMMENDATIONS = {'
old_recs_end = '    function getRecommendationsForRoom(roomId) {'
s_r = code.find(old_recs_start)
e_r = code.find(old_recs_end)
assert s_r != -1 and e_r != -1

new_recs = '''    const ALL_CEILING_OPTIONS = [
      { id: 'chandelier', label: '3-Tier Brass Halo Chandelier' },
      { id: 'crystal_ring', label: 'Crystal & Gold Ring Chandelier' },
      { id: 'glass_cluster', label: 'Cascading Glass Globe Cluster' },
      { id: 'geometric_grid', label: 'Architectural Black & Brass Grid' },
      { id: 'drum_trio', label: 'Trio Cream Drum Pendants' },
      { id: 'woven_rattan', label: 'Woven Rattan Dome Pendant' },
      { id: 'linear', label: 'Linear Opal Globe Pendant' },
      { id: 'sputnik', label: 'Modern Sputnik Starburst' },
      { id: 'pendant', label: 'Trio Brass Dome Pendants' },
      { id: 'fan', label: 'Walnut & Brass Ceiling Fan' },
      { id: 'double_fan', label: 'Matte Black 5-Blade Fan + LED' },
      { id: 'flush', label: 'Minimalist Flush LED Halo' }
    ];

    const ALL_FOCUS_OPTIONS = [
      { id: 'warm_recessed', label: '2700K Warm Recessed Spots' },
      { id: 'brass_track', label: 'Brushed Brass Spot Canisters' },
      { id: 'gallery_pin', label: 'Dark Gallery Pin-Spot Wash' },
      { id: 'square_gimbal', label: 'Architectural Square Gimbal' },
      { id: 'copper_pendant_spot', label: 'Mini Brass Cylinder Spots' },
      { id: 'task_cool', label: '4000K Crisp Task Spots' },
      { id: 'daylight_panel', label: '5000K Studio Daylight Spots' },
      { id: 'cove_ambient', label: 'Brass Halo + Cove Wash' }
    ];

    function buildRoomList(allOpts, aiIds) {
      const aiSet = new Set(aiIds);
      const top = aiIds.map(id => {
        const o = allOpts.find(x => x.id === id);
        return o ? { id: o.id, label: '★ AI: ' + o.label } : null;
      }).filter(Boolean);
      const rest = allOpts.filter(o => !aiSet.has(o.id));
      return [...top, ...rest];
    }

    const AI_ROOM_RECOMMENDATIONS = {
      living: {
        ceiling: buildRoomList(ALL_CEILING_OPTIONS, ['chandelier', 'crystal_ring', 'glass_cluster', 'sputnik']),
        focus: buildRoomList(ALL_FOCUS_OPTIONS, ['warm_recessed', 'brass_track', 'gallery_pin']),
        furniture: [
          { id: 'lv_warmth', label: '★ AI Sofa: L-Sectional + Oval Marble' },
          { id: 'lv_symmetrical', label: '★ AI Sofa: Twin Emerald Velvet' },
          { id: 'lv_curved', label: 'Sofa: U-Shape Bouclé + Drum Table' },
          { id: 'lv_modular', label: 'Sofa: Modular Pit + Travertine' },
          { id: 'lv_chesterfield', label: 'Sofa: Cognac Tufted + Glass Brass' },
          { id: 'lv_japandi', label: 'Sofa: Low Japandi Oak + Poufs' },
          { id: 'lv_conversation', label: 'Sofa: 4-Chair Club Lounge + Marble' },
          { id: 'lv_nordic', label: 'Sofa: Nordic Sage L-Sofa + Walnut' }
        ]
      },
      drawing: {
        ceiling: buildRoomList(ALL_CEILING_OPTIONS, ['sputnik', 'chandelier', 'geometric_grid', 'crystal_ring']),
        focus: buildRoomList(ALL_FOCUS_OPTIONS, ['gallery_pin', 'square_gimbal', 'brass_track']),
        furniture: [
          { id: 'dw_formal', label: '★ AI Sofa: 3-Seater + Chaise + Chair' },
          { id: 'dw_twin', label: '★ AI Sofa: Twin Facing Sage Loveseats' },
          { id: 'dw_sectional', label: 'Sofa: Charcoal L-Sectional' },
          { id: 'dw_boucle', label: 'Sofa: Curved Bouclé + Twin Chairs' },
          { id: 'dw_cognac', label: 'Sofa: Cognac Lounge + Black Marble' },
          { id: 'dw_club', label: 'Sofa: 4-Piece Club Seating + Brass' }
        ]
      },
      bed1: {
        ceiling: buildRoomList(ALL_CEILING_OPTIONS, ['fan', 'double_fan', 'chandelier', 'woven_rattan']),
        focus: buildRoomList(ALL_FOCUS_OPTIONS, ['warm_recessed', 'cove_ambient', 'copper_pendant_spot']),
        furniture: [
          { id: 'b1_tufted', label: '★ AI Bed: Tufted King + Lounge Chair' },
          { id: 'b1_canopy', label: '★ AI Bed: Walnut 4-Poster Canopy' },
          { id: 'b1_japandi', label: 'Bed: Low Japandi Platform' },
          { id: 'b1_walnut', label: 'Bed: Warm Walnut + Ochre King' },
          { id: 'b1_charcoal', label: 'Bed: Hotel Noir Velvet King' }
        ]
      },
      bed2: {
        ceiling: buildRoomList(ALL_CEILING_OPTIONS, ['fan', 'double_fan', 'sputnik', 'flush']),
        focus: buildRoomList(ALL_FOCUS_OPTIONS, ['task_cool', 'warm_recessed', 'square_gimbal']),
        furniture: [
          { id: 'b2_study', label: '★ AI Bed: Queen + South Study Desk' },
          { id: 'b2_daybed', label: 'Sofa: Executive Daybed + Chair' },
          { id: 'b2_twin', label: 'Bed: Dual Twin Guest Beds' },
          { id: 'b2_sage', label: 'Bed: Botanical Sage + Walnut' },
          { id: 'b2_slate', label: 'Bed: Minimalist Slate Studio' }
        ]
      },
      kitchen: {
        ceiling: buildRoomList(ALL_CEILING_OPTIONS, ['pendant', 'drum_trio', 'linear', 'geometric_grid']),
        focus: buildRoomList(ALL_FOCUS_OPTIONS, ['task_cool', 'daylight_panel', 'brass_track']),
        furniture: [
          { id: 'kt_navy_sage', label: '★ AI Kitchen: Navy Island + Sage' },
          { id: 'kt_walnut', label: 'Kitchen: Warm Walnut + Calacatta' },
          { id: 'kt_charcoal', label: 'Kitchen: Matte Charcoal + Carrara' }
        ]
      },
      dining: {
        ceiling: buildRoomList(ALL_CEILING_OPTIONS, ['linear', 'drum_trio', 'chandelier', 'crystal_ring']),
        focus: buildRoomList(ALL_FOCUS_OPTIONS, ['warm_recessed', 'gallery_pin', 'copper_pendant_spot']),
        furniture: [
          { id: 'dn_oak', label: '★ AI Dining: 8-Seater Rectangular Oak' },
          { id: 'dn_round', label: '★ AI Dining: 6-Seater Round Marble' },
          { id: 'dn_banquet', label: 'Dining: Walnut Table + Tufted Bench' },
          { id: 'dn_glass', label: 'Dining: Glass Top + Brass Chairs' },
          { id: 'dn_oval_walnut', label: 'Dining: Dark Walnut + Bouclé Chairs' }
        ]
      },
      pooja: {
        ceiling: buildRoomList(ALL_CEILING_OPTIONS, ['pendant', 'glass_cluster', 'chandelier']),
        focus: buildRoomList(ALL_FOCUS_OPTIONS, ['gallery_pin', 'warm_recessed', 'cove_ambient']),
        furniture: [
          { id: 'pj_teak', label: '★ AI Sanctum: Carved Teak + Marble' },
          { id: 'pj_marble', label: 'Sanctum: White Marble + Brass' }
        ]
      },
      wetkitchen: {
        ceiling: buildRoomList(ALL_CEILING_OPTIONS, ['flush', 'linear', 'geometric_grid']),
        focus: buildRoomList(ALL_FOCUS_OPTIONS, ['daylight_panel', 'task_cool']),
        furniture: [
          { id: 'wk_slate', label: '★ AI Utility: Slate + Marble' },
          { id: 'wk_oak', label: 'Utility: Natural Oak + Granite' }
        ]
      },
      sitout: {
        ceiling: buildRoomList(ALL_CEILING_OPTIONS, ['fan', 'woven_rattan', 'double_fan', 'pendant']),
        focus: buildRoomList(ALL_FOCUS_OPTIONS, ['warm_recessed', 'cove_ambient']),
        furniture: [
          { id: 'st_cane', label: '★ AI Sitout: Twin Cane Lounge Chairs' },
          { id: 'st_loveseat', label: 'Sofa: Outdoor Rattan Loveseat' }
        ]
      }
    };

'''

code = code[:s_r] + new_recs + code[e_r:]

# 5. Add new Living Hall & Drawing Hall & Dining furniture geometry builders
old_lv_mod_end = "        } else if (presetId === 'lv_curved') {"
new_lv_builders = '''        } else if (presetId === 'lv_chesterfield') {
          const cogMat = new THREE.MeshStandardMaterial({ color: '#8b4523', roughness: 0.55 });
          addSofa(slot, 0.2, 4.2, 12.0, 3.6, Math.PI, cogMat, [creamFabric, ochreFabric]);
          addArmchair(slot, -6.4, -1.5, Math.PI * 0.45, creamFabric);
          addArmchair(slot, 6.4, -1.5, -Math.PI * 0.45, creamFabric);
          const gTop = new THREE.Mesh(new THREE.BoxGeometry(4.8, 0.12, 2.8), glassMat);
          gTop.position.set(0, 1.32, -1.2); slot.add(gTop);
          const gFrame = new THREE.Mesh(new THREE.BoxGeometry(4.9, 0.1, 2.9), brassMat);
          gFrame.position.set(0, 1.22, -1.2); slot.add(gFrame);
          [[-2.2, -2.4], [2.2, -2.4], [-2.2, 0.0], [2.2, 0.0]].forEach(([lx, lz]) => {
            const leg = new THREE.Mesh(new THREE.CylinderGeometry(0.05, 0.05, 1.2, 10), brassMat);
            leg.position.set(lx, 0.6, lz); slot.add(leg);
          });
        } else if (presetId === 'lv_japandi') {
          const linMat = new THREE.MeshStandardMaterial({ color: '#d8d2c5', roughness: 0.9 });
          addSofa(slot, 0, 4.0, 13.5, 3.8, Math.PI, linMat, [sageFabric]);
          const lowTbl = new THREE.Mesh(new THREE.BoxGeometry(5.5, 0.55, 3.2), oakMat);
          lowTbl.position.set(0, 0.28, -1.2); lowTbl.castShadow = true; slot.add(lowTbl);
          [-3.8, 3.8].forEach(px => {
            const pouf = new THREE.Mesh(new THREE.CylinderGeometry(1.4, 1.4, 0.75, 24), terraFabric);
            pouf.position.set(px, 0.38, -1.2); slot.add(pouf);
          });
        } else if (presetId === 'lv_conversation') {
          [[-5.0, -3.5, 0.7], [5.0, -3.5, -0.7], [-5.0, 2.5, 2.3], [5.0, 2.5, -2.3]].forEach(([ax, az, rot]) => {
            addArmchair(slot, ax, az, rot, creamFabric);
          });
          const rTop = new THREE.Mesh(new THREE.CylinderGeometry(2.5, 2.5, 0.18, 32), calaMat);
          rTop.position.set(0, 1.25, -0.5); rTop.castShadow = true; slot.add(rTop);
          const rPed = new THREE.Mesh(new THREE.CylinderGeometry(0.9, 1.2, 1.15, 20), walnutMat);
          rPed.position.set(0, 0.58, -0.5); slot.add(rPed);
        } else if (presetId === 'lv_nordic') {
          addSofa(slot, 0.5, 4.2, 13.8, 3.5, Math.PI, sageFabric, [creamFabric, ochreFabric]);
          addSofa(slot, -5.2, -1.5, 8.0, 3.3, Math.PI / 2, sageFabric, [creamFabric]);
          addArmchair(slot, 6.8, -1.0, -Math.PI * 0.55, darkFabric);
          const w1 = new THREE.Mesh(new THREE.CylinderGeometry(2.0, 2.0, 0.14, 28), walnutMat);
          w1.position.set(-0.5, 1.2, -1.5); w1.castShadow = true; slot.add(w1);
          const w2 = new THREE.Mesh(new THREE.CylinderGeometry(1.3, 1.3, 0.14, 24), oakMat);
          w2.position.set(1.7, 1.4, -2.1); w2.castShadow = true; slot.add(w2);
        } else if (presetId === 'lv_curved') {'''

assert old_lv_mod_end in code, "old_lv_mod_end not found"
code = code.replace(old_lv_mod_end, new_lv_builders, 1)

# Add dw_cognac & dw_club in Drawing Hall
old_dw_mod_end = "        } else if (presetId === 'dw_sectional') {"
new_dw_builders = '''        } else if (presetId === 'dw_cognac') {
          const cogMat = new THREE.MeshStandardMaterial({ color: '#8b4523', roughness: 0.55 });
          addSofa(slot, 0, -5.8, 9.6, 3.4, 0, cogMat, [creamFabric, ochreFabric]);
          addArmchair(slot, -5.8, -1.8, 0.55, darkFabric);
          const mTop = new THREE.Mesh(new THREE.BoxGeometry(4.4, 0.25, 2.4), marbleMat);
          mTop.position.set(0, 1.25, -1.8); mTop.castShadow = true; slot.add(mTop);
        } else if (presetId === 'dw_club') {
          [[-4.2, -4.5, 0.6], [4.2, -4.5, -0.6], [-4.2, 0.5, 2.4], [4.2, 0.5, -2.4]].forEach(([ax, az, rot]) => {
            addArmchair(slot, ax, az, rot, greyFabric);
          });
          const bTop = new THREE.Mesh(new THREE.CylinderGeometry(2.0, 2.0, 0.16, 28), calaMat);
          bTop.position.set(0, 1.25, -2.0); bTop.castShadow = true; slot.add(bTop);
          const bBase = new THREE.Mesh(new THREE.CylinderGeometry(0.6, 0.9, 1.15, 20), brassMat);
          bBase.position.set(0, 0.58, -2.0); slot.add(bBase);
        } else if (presetId === 'dw_sectional') {'''

assert old_dw_mod_end in code, "old_dw_mod_end not found"
code = code.replace(old_dw_mod_end, new_dw_builders, 1)

# Add dn_glass & dn_oval_walnut in Dining
old_dn_else = "        } else {\n          const dt = new THREE.Mesh(new THREE.BoxGeometry(4.4, 0.25, 8.4), oakMat);"
new_dn_builders = '''        } else if (presetId === 'dn_glass') {
          const dt = new THREE.Mesh(new THREE.BoxGeometry(4.4, 0.12, 8.2), glassMat);
          dt.position.set(0, 2.55, 0); slot.add(dt);
          [-2.6, 2.6].forEach(tz => {
            const bleg = new THREE.Mesh(new THREE.BoxGeometry(2.8, 2.45, 0.16), brassMat);
            bleg.position.set(0, 1.22, tz); slot.add(bleg);
          });
          [-2.5, 2.5].forEach(cx => {
            [-2.8, 0, 2.8].forEach(cz => makeDiningChair(cx, cz, cx > 0 ? -Math.PI / 2 : Math.PI / 2, darkFabric));
          });
        } else if (presetId === 'dn_oval_walnut') {
          const oval = new THREE.Mesh(new THREE.CylinderGeometry(2.4, 2.4, 0.22, 32), walnutMat);
          oval.scale.set(1.0, 1.0, 1.75); oval.position.set(0, 2.55, 0); oval.castShadow = true; slot.add(oval);
          const ped = new THREE.Mesh(new THREE.CylinderGeometry(0.8, 1.2, 2.4, 20), brassMat);
          ped.position.set(0, 1.2, 0); slot.add(ped);
          [-2.5, 2.5].forEach(cx => {
            [-2.4, 0, 2.4].forEach(cz => makeDiningChair(cx, cz, cx > 0 ? -Math.PI / 2 : Math.PI / 2, creamFabric));
          });
        } else {
          const dt = new THREE.Mesh(new THREE.BoxGeometry(4.4, 0.25, 8.4), oakMat);'''

assert old_dn_else in code, "old_dn_else not found"
code = code.replace(old_dn_else, new_dn_builders, 1)

# 6. Add SVG thumbnails for new ceiling & focus & furniture options
old_thumb_ret = "      if (id === 'fan') return"
new_thumb_cases = '''      if (id === 'glass_cluster') return `<svg viewBox="0 0 120 66" width="100%" height="100%"><line x1="45" y1="0" x2="45" y2="28" stroke="#94a3b8" stroke-width="1"/><line x1="60" y1="0" x2="60" y2="42" stroke="#94a3b8" stroke-width="1"/><line x1="76" y1="0" x2="76" y2="22" stroke="#94a3b8" stroke-width="1"/><circle cx="45" cy="32" r="7" fill="#fff3c4"/><circle cx="60" cy="46" r="9" fill="#ffe4b5"/><circle cx="76" cy="26" r="6" fill="#fff3c4"/></svg>`;
        if (id === 'woven_rattan') return `<svg viewBox="0 0 120 66" width="100%" height="100%"><line x1="60" y1="0" x2="60" y2="18" stroke="#94a3b8" stroke-width="1.5"/><path d="M28 42 A32 24 0 0 1 92 42 Z" fill="#b5895a"/><circle cx="60" cy="42" r="5" fill="#fff3c4"/></svg>`;
        if (id === 'geometric_grid') return `<svg viewBox="0 0 120 66" width="100%" height="100%"><line x1="32" y1="0" x2="32" y2="24" stroke="#94a3b8" stroke-width="1.5"/><line x1="88" y1="0" x2="88" y2="24" stroke="#94a3b8" stroke-width="1.5"/><rect x="22" y="24" width="76" height="10" rx="2" fill="#1e293b" stroke="#d4af37" stroke-width="1.5"/><line x1="34" y1="34" x2="86" y2="34" stroke="#fff3c4" stroke-width="2.5"/></svg>`;
        if (id === 'double_fan') return `<svg viewBox="0 0 120 66" width="100%" height="100%"><line x1="60" y1="0" x2="60" y2="24" stroke="#94a3b8" stroke-width="2"/><path d="M18 28 L54 30 L54 34 L18 32 Z" fill="#334155"/><path d="M66 30 L102 28 L102 32 L66 34 Z" fill="#334155"/><circle cx="60" cy="33" r="7" fill="#1e293b" stroke="#fff3c4" stroke-width="2"/></svg>`;
        if (id === 'fan') return'''

assert old_thumb_ret in code, "old_thumb_ret not found"
code = code.replace(old_thumb_ret, new_thumb_cases, 1)

old_focus_thumb = "        if (id === 'task_cool') return"
new_focus_thumbs = '''        if (id === 'square_gimbal') return `<svg viewBox="0 0 120 66" width="100%" height="100%"><rect x="46" y="14" width="28" height="10" rx="1" fill="#334155"/><rect x="52" y="16" width="16" height="6" fill="#ffe4b5"/><polygon points="48,24 72,24 88,62 32,62" fill="rgba(255,228,181,0.22)"/></svg>`;
        if (id === 'copper_pendant_spot') return `<svg viewBox="0 0 120 66" width="100%" height="100%"><rect x="34" y="8" width="8" height="22" rx="2" fill="#d4af37"/><rect x="78" y="8" width="8" height="22" rx="2" fill="#d4af37"/><polygon points="30,30 46,30 54,62 22,62" fill="rgba(255,228,181,0.22)"/><polygon points="74,30 90,30 98,62 66,62" fill="rgba(255,228,181,0.22)"/></svg>`;
        if (id === 'daylight_panel') return `<svg viewBox="0 0 120 66" width="100%" height="100%"><ellipse cx="60" cy="18" rx="18" ry="5" fill="#f8fafc"/><polygon points="42,20 78,20 96,62 24,62" fill="rgba(241,245,249,0.22)"/></svg>`;
        if (id === 'task_cool') return'''

assert old_focus_thumb in code, "old_focus_thumb not found"
code = code.replace(old_focus_thumb, new_focus_thumbs, 1)

# Clean up label stripping in renderCustomizeGrid & updateRoomInfoCardLighting
code = code.replace(
    "const cleanTitle = opt.label.replace(/^★ AI [^:]+: /, '').replace(/^[^:]+: /, '');",
    "const cleanTitle = opt.label.replace(/^★ AI(:| [^:]+:) /, '').replace(/^[^:]+: /, '');"
)
code = code.replace(
    "replace(/^★ AI [^:]+: /, '').replace(/^[^:]+: /, '')",
    "replace(/^★ AI(:| [^:]+:) /, '').replace(/^[^:]+: /, '')"
)

with open(index_path, 'w', encoding='utf-8') as f:
    f.write(code)

print("Expanded ceiling lights (12), focus lights (8), and furniture presets successfully!")

