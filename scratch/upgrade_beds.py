index_path = '/Users/puspharaj/Documents/Projects/ai-interior-designer/index.html'

with open(index_path, 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Expand AI_ROOM_RECOMMENDATIONS for bed1 & bed2
old_b1_rec = '''      bed1: {
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
      },'''

new_b1_b2_rec = '''      bed1: {
        ceiling: buildRoomList(ALL_CEILING_OPTIONS, ['fan', 'double_fan', 'chandelier', 'woven_rattan']),
        focus: buildRoomList(ALL_FOCUS_OPTIONS, ['warm_recessed', 'cove_ambient', 'copper_pendant_spot']),
        furniture: [
          { id: 'b1_tufted', label: '★ AI Bed: Tufted King + Lounge Chair' },
          { id: 'b1_canopy', label: '★ AI Bed: Walnut 4-Poster Canopy + Bench' },
          { id: 'b1_wingback', label: 'Bed: Emerald Wingback King + Ottoman' },
          { id: 'b1_japandi', label: 'Bed: Low Japandi Oak Platform' },
          { id: 'b1_sleigh', label: 'Bed: Classic Walnut Sleigh Bed' },
          { id: 'b1_floating', label: 'Bed: Floating LED Platform King' }
        ]
      },
      bed2: {
        ceiling: buildRoomList(ALL_CEILING_OPTIONS, ['fan', 'double_fan', 'sputnik', 'flush']),
        focus: buildRoomList(ALL_FOCUS_OPTIONS, ['task_cool', 'warm_recessed', 'square_gimbal']),
        furniture: [
          { id: 'b2_study', label: '★ AI Bed: Queen + South Study Desk' },
          { id: 'b2_daybed', label: '★ AI Sofa: Executive Daybed + Chair' },
          { id: 'b2_twin', label: 'Bed: Dual Twin Guest Beds' },
          { id: 'b2_bunk_loft', label: 'Bed: Timber & Steel Loft Bunk Bed' },
          { id: 'b2_canopy', label: 'Bed: Matte Black Canopy Queen' },
          { id: 'b2_murphy', label: 'Bed: Slatted Oak Feature Queen' }
        ]
      },'''

assert old_b1_rec in code, "old_b1_rec not found"
code = code.replace(old_b1_rec, new_b1_b2_rec, 1)

# 2. Wrap Bedroom 1 bed into roomFurnitureBuilders['bed1']
old_b1_bed = '''      // Tufted King Bed
      const hb1 = new THREE.Mesh(new THREE.BoxGeometry(7.6, 4.4, 0.5), b1HeadMat);
      hb1.position.set(0, 2.2, -3.5); hb1.castShadow = true; b1.add(hb1);
      for (let t = -3.0; t <= 3.0; t += 1.0) {
        const panel = new THREE.Mesh(new THREE.BoxGeometry(0.88, 3.8, 0.14), greyFabric);
        panel.position.set(t, 2.3, -3.22); b1.add(panel);
      }
      const bedBase1 = new THREE.Mesh(new THREE.BoxGeometry(6.9, 0.65, 7.4), walnutMat);
      bedBase1.position.set(0, 0.4, 0.3); b1.add(bedBase1);
      const mat1 = new THREE.Mesh(new THREE.BoxGeometry(6.6, 0.9, 7.1), creamFabric);
      mat1.position.set(0, 1.15, 0.3); mat1.castShadow = true; b1.add(mat1);
      const duvet1 = new THREE.Mesh(new THREE.BoxGeometry(6.75, 0.32, 4.4), b1DuvetMat);
      duvet1.position.set(0, 1.68, 1.65); duvet1.castShadow = true; b1.add(duvet1);
      [-1.7, 1.7].forEach(px => {
        const pil = new THREE.Mesh(new THREE.BoxGeometry(2.3, 0.45, 1.4), creamFabric);
        pil.position.set(px, 1.82, -2.1); pil.rotation.x = -0.25; pil.castShadow = true; b1.add(pil);
        const sham = new THREE.Mesh(new THREE.BoxGeometry(1.4, 0.45, 0.8), b1ShamMat);
        sham.position.set(px, 1.85, -1.3); sham.rotation.x = -0.3; b1.add(sham);
      });
      // Nightstands & Glowing Table Lamps
      [-4.6, 4.6].forEach(nx => {
        const ns = new THREE.Mesh(new THREE.BoxGeometry(1.9, 1.7, 1.6), b1WoodMat);
        ns.position.set(nx, 0.85, -2.9); ns.castShadow = true; b1.add(ns);
        const lBase = new THREE.Mesh(new THREE.CylinderGeometry(0.18, 0.28, 0.7, 14), brassMat);
        lBase.position.set(nx, 2.05, -2.9); b1.add(lBase);
        const lShade = new THREE.Mesh(new THREE.CylinderGeometry(0.35, 0.5, 0.65, 16), glowWarmMat);
        lShade.position.set(nx, 2.65, -2.9); b1.add(lShade);
      });'''

new_b1_bed = '''      const b1BedSlot = new THREE.Group();
      b1.add(b1BedSlot);
      roomDynamicFurnitureSlots['bed1'] = b1BedSlot;
      roomFurnitureBuilders['bed1'] = function(slot, presetId) {
        function addNightstands(distX, woodM) {
          [-distX, distX].forEach(nx => {
            const ns = new THREE.Mesh(new THREE.BoxGeometry(1.9, 1.7, 1.6), woodM);
            ns.position.set(nx, 0.85, -2.9); ns.castShadow = true; slot.add(ns);
            const lBase = new THREE.Mesh(new THREE.CylinderGeometry(0.18, 0.28, 0.7, 14), brassMat);
            lBase.position.set(nx, 2.05, -2.9); slot.add(lBase);
            const lShade = new THREE.Mesh(new THREE.CylinderGeometry(0.35, 0.5, 0.65, 16), glowWarmMat);
            lShade.position.set(nx, 2.65, -2.9); slot.add(lShade);
          });
        }
        function addBedBody(w, d, baseY, baseH, baseM, duvetM, shamM) {
          const base = new THREE.Mesh(new THREE.BoxGeometry(w, baseH, d), baseM);
          base.position.set(0, baseY + baseH / 2, 0.3); base.castShadow = true; slot.add(base);
          const mat = new THREE.Mesh(makeBeveledBox(w - 0.3, 0.9, d - 0.3, 0.12), creamFabric);
          mat.position.set(0, baseY + baseH + 0.45, 0.3); mat.castShadow = true; slot.add(mat);
          const duv = new THREE.Mesh(makeBeveledBox(w - 0.15, 0.34, d * 0.6, 0.10), duvetM);
          duv.position.set(0, baseY + baseH + 0.96, 1.65); duv.castShadow = true; slot.add(duv);
          const py = baseY + baseH + 1.1;
          [-1.65, 1.65].forEach(px => {
            const pil = new THREE.Mesh(makeBeveledBox(2.2, 0.42, 1.35, 0.12), creamFabric);
            pil.position.set(px, py, -2.1); pil.rotation.x = -0.25; pil.castShadow = true; slot.add(pil);
            const sham = new THREE.Mesh(makeBeveledBox(1.4, 0.42, 0.8, 0.10), shamM);
            sham.position.set(px, py + 0.05, -1.3); sham.rotation.x = -0.3; slot.add(sham);
          });
        }

        if (presetId === 'b1_canopy') {
          // 4-Poster Walnut Canopy Frame + Tufted Bench at Foot
          [[-3.45, -3.45], [3.45, -3.45], [-3.45, 4.05], [3.45, 4.05]].forEach(([px, pz]) => {
            const post = new THREE.Mesh(new THREE.CylinderGeometry(0.14, 0.16, 7.6, 12), walnutMat);
            post.position.set(px, 3.8, pz); post.castShadow = true; slot.add(post);
          });
          [[0, -3.45, 7.1, 0.2], [0, 4.05, 7.1, 0.2], [-3.45, 0.3, 0.2, 7.7], [3.45, 0.3, 0.2, 7.7]].forEach(([rx, rz, rw, rd]) => {
            const rail = new THREE.Mesh(new THREE.BoxGeometry(rw, 0.2, rd), walnutMat);
            rail.position.set(rx, 7.55, rz); slot.add(rail);
          });
          const hb = new THREE.Mesh(makeBeveledBox(6.8, 3.6, 0.4, 0.10), greyFabric);
          hb.position.set(0, 2.2, -3.4); slot.add(hb);
          addBedBody(6.8, 7.4, 0.2, 0.55, walnutMat, sageFabric, ochreFabric);
          // End-of-bed bench
          const bench = new THREE.Mesh(makeBeveledBox(5.2, 0.65, 1.6, 0.12), creamFabric);
          bench.position.set(0, 1.25, 5.2); bench.castShadow = true; slot.add(bench);
          [[-2.2, 4.6], [2.2, 4.6], [-2.2, 5.8], [2.2, 5.8]].forEach(([bx, bz]) => {
            const bleg = new THREE.Mesh(new THREE.CylinderGeometry(0.06, 0.05, 0.9, 8), walnutMat);
            bleg.position.set(bx, 0.45, bz); slot.add(bleg);
          });
          addNightstands(4.7, walnutMat);
        } else if (presetId === 'b1_wingback') {
          const emMat = new THREE.MeshStandardMaterial({ color: '#2e5242', roughness: 0.78 });
          const hb = new THREE.Mesh(makeBeveledBox(7.8, 4.8, 0.45, 0.12), emMat);
          hb.position.set(0, 2.4, -3.5); hb.castShadow = true; slot.add(hb);
          [-3.75, 3.75].forEach((wx, idx) => {
            const wing = new THREE.Mesh(makeBeveledBox(0.45, 4.8, 1.5, 0.10), emMat);
            wing.position.set(wx, 2.4, -2.9); wing.rotation.y = idx === 0 ? 0.25 : -0.25; slot.add(wing);
          });
          addBedBody(6.9, 7.4, 0.15, 0.6, darkFabric, ochreFabric, terraFabric);
          const ott = new THREE.Mesh(new THREE.CylinderGeometry(1.4, 1.4, 1.35, 24), emMat);
          ott.position.set(0, 0.68, 5.4); ott.castShadow = true; slot.add(ott);
          addNightstands(5.0, walnutMat);
        } else if (presetId === 'b1_japandi') {
          // Low-Profile Wide Oak Platform + Floating Integrated Side Shelves
          const plat = new THREE.Mesh(new THREE.BoxGeometry(10.8, 0.45, 8.2), oakMat);
          plat.position.set(0, 0.25, 0.1); plat.castShadow = true; slot.add(plat);
          const slatHb = new THREE.Mesh(new THREE.BoxGeometry(10.8, 3.2, 0.3), oakMat);
          slatHb.position.set(0, 1.6, -3.8); slot.add(slatHb);
          addBedBody(6.6, 7.2, 0.0, 0.45, oakMat, creamFabric, sageFabric);
          [-4.4, 4.4].forEach(nx => {
            const lamp = new THREE.Mesh(new THREE.CylinderGeometry(0.32, 0.45, 0.85, 16), glowWarmMat);
            lamp.position.set(nx, 0.9, -2.9); slot.add(lamp);
          });
        } else if (presetId === 'b1_sleigh') {
          // Curved Walnut Sleigh Headboard & Footboard
          const hb = new THREE.Mesh(new THREE.BoxGeometry(7.2, 4.2, 0.45), walnutMat);
          hb.position.set(0, 2.1, -3.6); hb.rotation.x = -0.18; hb.castShadow = true; slot.add(hb);
          const fb = new THREE.Mesh(new THREE.BoxGeometry(7.2, 2.4, 0.4), walnutMat);
          fb.position.set(0, 1.2, 4.1); fb.rotation.x = 0.18; fb.castShadow = true; slot.add(fb);
          addBedBody(6.8, 7.2, 0.2, 0.6, walnutMat, terraFabric, ochreFabric);
          addNightstands(4.7, walnutMat);
        } else if (presetId === 'b1_floating') {
          // Cantilevered Dark Slate Floating Platform with Warm Under-Bed LED Glow
          const hb = new THREE.Mesh(makeBeveledBox(8.4, 4.2, 0.45, 0.12), darkFabric);
          hb.position.set(0, 2.1, -3.5); slot.add(hb);
          const led = new THREE.Mesh(new THREE.BoxGeometry(6.2, 0.15, 6.8), glowWarmMat);
          led.position.set(0, 0.15, 0.3); slot.add(led);
          addBedBody(7.0, 7.4, 0.25, 0.55, metalMat, greyFabric, ochreFabric);
          addNightstands(4.9, darkFabric);
        } else {
          // Default AI Pick: Channel-Tufted King
          const hb1 = new THREE.Mesh(new THREE.BoxGeometry(7.6, 4.4, 0.5), darkFabric);
          hb1.position.set(0, 2.2, -3.5); hb1.castShadow = true; slot.add(hb1);
          for (let t = -3.0; t <= 3.0; t += 1.0) {
            const panel = new THREE.Mesh(new THREE.BoxGeometry(0.88, 3.8, 0.14), greyFabric);
            panel.position.set(t, 2.3, -3.22); slot.add(panel);
          }
          addBedBody(6.9, 7.4, 0.08, 0.65, walnutMat, sageFabric, terraFabric);
          addNightstands(4.6, walnutMat);
        }
      };
      roomFurnitureBuilders['bed1'](b1BedSlot, 'b1_tufted');'''

assert old_b1_bed in code, "old_b1_bed not found"
code = code.replace(old_b1_bed, new_b1_bed, 1)

# 3. Wrap Bedroom 2 bed + desk into roomFurnitureBuilders['bed2']
old_b2_bed = '''      const hb2 = new THREE.Mesh(new THREE.BoxGeometry(6.8, 4.0, 0.45), b2HeadMat);
      hb2.position.set(0, 2.0, -3.3); hb2.castShadow = true; b2.add(hb2);
      const mat2 = new THREE.Mesh(new THREE.BoxGeometry(6.2, 1.25, 6.8), creamFabric);
      mat2.position.set(0, 0.85, 0.2); mat2.castShadow = true; b2.add(mat2);
      const duvet2 = new THREE.Mesh(new THREE.BoxGeometry(6.3, 0.28, 4.2), b2DuvetMat);
      duvet2.position.set(0, 1.55, 1.5); b2.add(duvet2);
      [-1.5, 1.5].forEach(px => {
        const pil = new THREE.Mesh(new THREE.BoxGeometry(2.1, 0.4, 1.3), creamFabric);
        pil.position.set(px, 1.65, -2.0); pil.rotation.x = -0.22; b2.add(pil);
      });
      [-4.1, 4.1].forEach(nx => {
        const ns = new THREE.Mesh(new THREE.BoxGeometry(1.6, 1.6, 1.4), oakMat);
        ns.position.set(nx, 0.8, -2.9); ns.castShadow = true; b2.add(ns);
        const lamp = new THREE.Mesh(new THREE.CylinderGeometry(0.3, 0.42, 0.9, 14), glowWarmMat);
        lamp.position.set(nx, 2.05, -2.9); b2.add(lamp);
      });'''

new_b2_bed = '''      const b2BedSlot = new THREE.Group();
      b2.add(b2BedSlot);
      roomDynamicFurnitureSlots['bed2'] = b2BedSlot;
      roomFurnitureBuilders['bed2'] = function(slot, presetId) {
        if (presetId === 'b2_twin') {
          // Dual Twin Guest Beds with Shared Center Nightstand
          [-2.8, 2.8].forEach(bx => {
            const hb = new THREE.Mesh(makeBeveledBox(3.4, 3.6, 0.4, 0.1), greyFabric);
            hb.position.set(bx, 1.8, -3.3); slot.add(hb);
            const mat = new THREE.Mesh(makeBeveledBox(3.2, 1.0, 6.6, 0.1), creamFabric);
            mat.position.set(bx, 0.8, 0.1); mat.castShadow = true; slot.add(mat);
            const duv = new THREE.Mesh(makeBeveledBox(3.25, 0.28, 4.0, 0.08), sageFabric);
            duv.position.set(bx, 1.38, 1.3); slot.add(duv);
            const pil = new THREE.Mesh(makeBeveledBox(1.8, 0.4, 1.2, 0.1), creamFabric);
            pil.position.set(bx, 1.5, -2.2); pil.rotation.x = -0.2; slot.add(pil);
          });
          const ns = new THREE.Mesh(new THREE.BoxGeometry(1.6, 1.6, 1.4), walnutMat);
          ns.position.set(0, 0.8, -2.9); slot.add(ns);
          const lamp = new THREE.Mesh(new THREE.CylinderGeometry(0.3, 0.42, 0.9, 14), glowWarmMat);
          lamp.position.set(0, 2.05, -2.9); slot.add(lamp);
        } else if (presetId === 'b2_daybed') {
          // Executive Daybed Sofa + Reading Armchair + Round Side Table
          addSofa(slot, 0, -2.0, 8.2, 3.6, 0, sageFabric, [ochreFabric, creamFabric]);
          addArmchair(slot, -4.5, 4.5, 0.65, creamFabric);
          const sTbl = new THREE.Mesh(new THREE.CylinderGeometry(1.0, 1.0, 1.5, 20), walnutMat);
          sTbl.position.set(-1.8, 0.75, 4.8); slot.add(sTbl);
        } else if (presetId === 'b2_bunk_loft') {
          // Timber & Steel 2-Tier Loft Bunk Bed with Ladder
          [[-3.2, -3.3], [3.2, -3.3], [-3.2, 3.6], [3.2, 3.6]].forEach(([px, pz]) => {
            const post = new THREE.Mesh(new THREE.BoxGeometry(0.28, 7.2, 0.28), metalMat);
            post.position.set(px, 3.6, pz); post.castShadow = true; slot.add(post);
          });
          // Lower & Upper Mattresses
          [1.0, 4.8].forEach((by, bi) => {
            const frame = new THREE.Mesh(new THREE.BoxGeometry(6.4, 0.25, 6.9), oakMat);
            frame.position.set(0, by, 0.15); slot.add(frame);
            const mat = new THREE.Mesh(makeBeveledBox(6.0, 0.75, 6.5, 0.1), creamFabric);
            mat.position.set(0, by + 0.5, 0.15); slot.add(mat);
            const duv = new THREE.Mesh(makeBeveledBox(6.05, 0.25, 4.0, 0.08), bi === 0 ? ochreFabric : sageFabric);
            duv.position.set(0, by + 0.95, 1.4); slot.add(duv);
          });
          // Ladder on right
          [-0.4, 0.4].forEach(lz => {
            const rail = new THREE.Mesh(new THREE.CylinderGeometry(0.05, 0.05, 5.2, 8), metalMat);
            rail.position.set(3.4, 2.6, lz); slot.add(rail);
          });
          for (let ry = 1.0; ry <= 4.6; ry += 0.9) {
            const rung = new THREE.Mesh(new THREE.CylinderGeometry(0.04, 0.04, 0.85, 8), oakMat);
            rung.rotation.x = Math.PI / 2; rung.position.set(3.4, ry, 0); slot.add(rung);
          }
        } else if (presetId === 'b2_canopy') {
          [[-3.1, -3.3], [3.1, -3.3], [-3.1, 3.6], [3.1, 3.6]].forEach(([px, pz]) => {
            const post = new THREE.Mesh(new THREE.CylinderGeometry(0.09, 0.09, 7.4, 10), metalMat);
            post.position.set(px, 3.7, pz); slot.add(post);
          });
          [[0, -3.3, 6.2, 0.14], [0, 3.6, 6.2, 0.14], [-3.1, 0.15, 0.14, 6.9], [3.1, 0.15, 0.14, 6.9]].forEach(([rx, rz, rw, rd]) => {
            const rail = new THREE.Mesh(new THREE.BoxGeometry(rw, 0.14, rd), metalMat);
            rail.position.set(rx, 7.35, rz); slot.add(rail);
          });
          const mat = new THREE.Mesh(makeBeveledBox(6.0, 1.1, 6.6, 0.12), creamFabric);
          mat.position.set(0, 0.85, 0.2); slot.add(mat);
          const duv = new THREE.Mesh(makeBeveledBox(6.1, 0.28, 4.2, 0.1), sageFabric);
          duv.position.set(0, 1.5, 1.4); slot.add(duv);
        } else if (presetId === 'b2_murphy') {
          // Slatted Oak Feature Wall Headboard
          for (let sx = -4.2; sx <= 4.2; sx += 0.4) {
            const sl = new THREE.Mesh(new THREE.BoxGeometry(0.2, 7.8, 0.18), oakMat);
            sl.position.set(sx, 3.9, -3.5); slot.add(sl);
          }
          const mat = new THREE.Mesh(makeBeveledBox(6.2, 1.1, 6.8, 0.12), creamFabric);
          mat.position.set(0, 0.8, 0.2); slot.add(mat);
          const duv = new THREE.Mesh(makeBeveledBox(6.3, 0.28, 4.2, 0.1), darkFabric);
          duv.position.set(0, 1.45, 1.4); slot.add(duv);
        } else {
          // Default AI Pick: Queen Bed
          const hb2 = new THREE.Mesh(new THREE.BoxGeometry(6.8, 4.0, 0.45), greyFabric);
          hb2.position.set(0, 2.0, -3.3); hb2.castShadow = true; slot.add(hb2);
          const mat2 = new THREE.Mesh(new THREE.BoxGeometry(6.2, 1.25, 6.8), creamFabric);
          mat2.position.set(0, 0.85, 0.2); mat2.castShadow = true; slot.add(mat2);
          const duvet2 = new THREE.Mesh(new THREE.BoxGeometry(6.3, 0.28, 4.2), ochreFabric);
          duvet2.position.set(0, 1.55, 1.5); slot.add(duvet2);
          [-1.5, 1.5].forEach(px => {
            const pil = new THREE.Mesh(new THREE.BoxGeometry(2.1, 0.4, 1.3), creamFabric);
            pil.position.set(px, 1.65, -2.0); pil.rotation.x = -0.22; slot.add(pil);
          });
          [-4.1, 4.1].forEach(nx => {
            const ns = new THREE.Mesh(new THREE.BoxGeometry(1.6, 1.6, 1.4), oakMat);
            ns.position.set(nx, 0.8, -2.9); ns.castShadow = true; slot.add(ns);
            const lamp = new THREE.Mesh(new THREE.CylinderGeometry(0.3, 0.42, 0.9, 14), glowWarmMat);
            lamp.position.set(nx, 2.05, -2.9); slot.add(lamp);
          });
        }
      };
      roomFurnitureBuilders['bed2'](b2BedSlot, 'b2_study');'''

assert old_b2_bed in code, "old_b2_bed not found"
code = code.replace(old_b2_bed, new_b2_bed, 1)

# 4. Add distinct SVG thumbnails for all new bed types!
old_bed_svg = "      if (id === 'b1_canopy') {"
new_bed_svgs = '''      if (id === 'b1_canopy' || id === 'b2_canopy') {
        const postC = id === 'b2_canopy' ? '#1e293b' : '#6e4726';
        return `<svg viewBox="0 0 120 66" width="100%" height="100%">
          <line x1="30" y1="8" x2="30" y2="56" stroke="${postC}" stroke-width="3"/>
          <line x1="90" y1="8" x2="90" y2="56" stroke="${postC}" stroke-width="3"/>
          <line x1="30" y1="10" x2="90" y2="10" stroke="${postC}" stroke-width="3"/>
          <rect x="33" y="22" width="54" height="18" rx="2" fill="#475569"/>
          <rect x="33" y="34" width="54" height="20" rx="2" fill="#5d7a68"/>
          <rect x="38" y="26" width="18" height="9" rx="2" fill="#f1f5f9"/>
          <rect x="64" y="26" width="18" height="9" rx="2" fill="#f1f5f9"/>
          <rect x="14" y="38" width="12" height="14" rx="2" fill="#6e4726"/>
          <rect x="94" y="38" width="12" height="14" rx="2" fill="#6e4726"/>
        </svg>`;
      }
      if (id === 'b1_wingback') {
        return `<svg viewBox="0 0 120 66" width="100%" height="100%">
          <rect x="24" y="12" width="72" height="26" rx="3" fill="#2e5242"/>
          <rect x="22" y="12" width="8" height="32" rx="2" fill="#1e3a2e"/>
          <rect x="90" y="12" width="8" height="32" rx="2" fill="#1e3a2e"/>
          <rect x="30" y="30" width="60" height="24" rx="3" fill="#c48b3b"/>
          <rect x="36" y="22" width="20" height="9" rx="2" fill="#f1f5f9"/>
          <rect x="64" y="22" width="20" height="9" rx="2" fill="#f1f5f9"/>
        </svg>`;
      }
      if (id === 'b1_sleigh') {
        return `<svg viewBox="0 0 120 66" width="100%" height="100%">
          <path d="M26 14 Q32 28 28 52 L92 52 Q94 38 92 32 L28 32 Z" fill="#6e4726"/>
          <rect x="32" y="28" width="56" height="20" rx="3" fill="#a85a44"/>
          <rect x="36" y="21" width="20" height="8" rx="2" fill="#f1f5f9"/>
          <rect x="64" y="21" width="20" height="8" rx="2" fill="#f1f5f9"/>
        </svg>`;
      }
      if (id === 'b1_floating') {
        return `<svg viewBox="0 0 120 66" width="100%" height="100%">
          <rect x="22" y="14" width="76" height="22" rx="3" fill="#1e293b"/>
          <rect x="28" y="30" width="64" height="18" rx="2" fill="#475569"/>
          <rect x="34" y="49" width="52" height="4" rx="2" fill="#ffcf87"/>
          <rect x="36" y="22" width="20" height="8" rx="2" fill="#f1f5f9"/>
          <rect x="64" y="22" width="20" height="8" rx="2" fill="#f1f5f9"/>
        </svg>`;
      }
      if (id === 'b2_bunk_loft') {
        return `<svg viewBox="0 0 120 66" width="100%" height="100%">
          <line x1="28" y1="8" x2="28" y2="58" stroke="#64748b" stroke-width="3"/>
          <line x1="88" y1="8" x2="88" y2="58" stroke="#64748b" stroke-width="3"/>
          <rect x="28" y="18" width="60" height="10" rx="2" fill="#5d7a68"/>
          <rect x="28" y="42" width="60" height="12" rx="2" fill="#c48b3b"/>
          <line x1="94" y1="16" x2="94" y2="58" stroke="#94a3b8" stroke-width="2"/>
          <line x1="88" y1="26" x2="94" y2="26" stroke="#94a3b8" stroke-width="2"/>
          <line x1="88" y1="36" x2="94" y2="36" stroke="#94a3b8" stroke-width="2"/>
          <line x1="88" y1="46" x2="94" y2="46" stroke="#94a3b8" stroke-width="2"/>
        </svg>`;
      }
      if (id === 'b2_daybed') return sofaSVG('#5d7a68', '#70947f', '#6e4726', '#c48b3b', '3seat', '#6e4726');
      if (id === '__unused_canopy_placeholder') {'''

assert old_bed_svg in code, "old_bed_svg not found"
code = code.replace(old_bed_svg, new_bed_svgs, 1)

with open(index_path, 'w', encoding='utf-8') as f:
    f.write(code)

print("Upgraded Bedroom 1 & Bedroom 2 with 6 real 3D bed types each!")

