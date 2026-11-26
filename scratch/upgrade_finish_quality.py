index_path = '/Users/puspharaj/Documents/Projects/ai-interior-designer/index.html'

with open(index_path, 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Upgrade createCeilingFixtureMesh('chandelier') to 3-Tier Concentric Brass & Glowing LED Halo Chandelier
old_chand = '''      if (style === 'chandelier') {
        const canopy = new THREE.Mesh(new THREE.CylinderGeometry(0.35, 0.35, 0.1, 20), brass);
        canopy.position.set(0, 9.95, 0); g.add(canopy);
        const rod = new THREE.Mesh(new THREE.CylinderGeometry(0.04, 0.04, 2.2, 12), brass);
        rod.position.set(0, 8.85, 0); g.add(rod);
        const ring = new THREE.Mesh(new THREE.TorusGeometry(2.3, 0.06, 12, 40), brass);
        ring.rotation.x = Math.PI / 2; ring.position.set(0, 7.75, 0); g.add(ring);
        const innerRing = new THREE.Mesh(new THREE.TorusGeometry(1.3, 0.045, 10, 32), brass);
        innerRing.rotation.x = Math.PI / 2; innerRing.position.set(0, 7.35, 0); g.add(innerRing);
        for (let i = 0; i < 10; i++) {
          const a = (i / 10) * Math.PI * 2;
          const gl = new THREE.Mesh(new THREE.SphereGeometry(0.22, 14, 14), glowWarm);
          gl.position.set(Math.cos(a) * 2.3, 7.75, Math.sin(a) * 2.3);
          g.add(gl);
        }
        const pt = new THREE.PointLight('#ffdca8', 0.9, 20, 1.6);
        pt.position.set(0, 7.4, 0); g.add(pt);
      }'''

new_chand = '''      if (style === 'chandelier') {
        // 3-Tier Sculptural Brass & Glowing LED Halo Ring Chandelier suspended by thin black cables
        const canopy = new THREE.Mesh(new THREE.CylinderGeometry(0.45, 0.45, 0.12, 24), brass);
        canopy.position.set(0, 9.94, 0); g.add(canopy);
        const tiers = [
          { r: 2.4, y: 7.9, ox: 0.0, oz: 0.0 },
          { r: 1.75, y: 7.45, ox: 0.25, oz: -0.15 },
          { r: 1.1, y: 7.05, ox: -0.15, oz: 0.2 }
        ];
        tiers.forEach(t => {
          const outerBrass = new THREE.Mesh(new THREE.TorusGeometry(t.r, 0.055, 14, 48), brass);
          outerBrass.rotation.x = Math.PI / 2;
          outerBrass.position.set(t.ox, t.y + 0.03, t.oz);
          g.add(outerBrass);
          const ledHalo = new THREE.Mesh(new THREE.TorusGeometry(t.r - 0.05, 0.05, 12, 48), glowWarm);
          ledHalo.rotation.x = Math.PI / 2;
          ledHalo.position.set(t.ox, t.y - 0.03, t.oz);
          g.add(ledHalo);
        });
        // 3 ultra-thin black suspension cables
        [0, 2.1, 4.2].forEach(a => {
          const cx = Math.cos(a) * 2.35, cz = Math.sin(a) * 2.35;
          const cable = new THREE.Mesh(new THREE.CylinderGeometry(0.015, 0.015, 2.05, 6), darkMetal);
          cable.position.set(cx, 8.95, cz); g.add(cable);
        });
        const pt = new THREE.PointLight('#ffe4b8', 0.95, 22, 1.5);
        pt.position.set(0, 7.3, 0); g.add(pt);
      }'''

assert old_chand in code, "old_chand not found"
code = code.replace(old_chand, new_chand, 1)

# 2. Add crisp white architectural skirting/baseboards along walls in buildWallsWithCutouts
old_walls_end = '''        mesh.userData = { defaultHeight: wH, origY: wH / 2, isWall: true };
        houseGroup.add(mesh);
        wallMeshes.push(mesh);
      });'''

new_walls_end = '''        mesh.userData = { defaultHeight: wH, origY: wH / 2, isWall: true };
        houseGroup.add(mesh);
        wallMeshes.push(mesh);
        if (!ext) {
          const skirtMat = new THREE.MeshStandardMaterial({ color: '#f4f2ed', roughness: 0.45 });
          const skirt = new THREE.Mesh(new THREE.BoxGeometry(ww + 0.04, 0.35, wd + 0.04), skirtMat);
          skirt.position.set(wx, 0.175, wz);
          houseGroup.add(skirt);
        }
      });'''

assert old_walls_end in code, "old_walls_end not found"
code = code.replace(old_walls_end, new_walls_end, 1)

# 3. Upgrade addPlant() to Tall Architectural Bird-of-Paradise Palms with curved elongated green leaves
old_plant = '''      function addPlant(parent, x, z, scale = 1.0) {
        const pl = new THREE.Group();
        pl.position.set(x, 0, z);
        pl.scale.setScalar(scale);
        const pot = new THREE.Mesh(new THREE.CylinderGeometry(0.65, 0.48, 1.35, 20), ceramicMat);
        pot.position.set(0, 0.68, 0); pot.castShadow = true; pl.add(pot);
        const soil = new THREE.Mesh(new THREE.CylinderGeometry(0.6, 0.6, 0.06, 16), walnutMat);
        soil.position.set(0, 1.33, 0); pl.add(soil);
        const trunk = new THREE.Mesh(new THREE.CylinderGeometry(0.06, 0.1, 2.8, 10), walnutMat);
        trunk.position.set(0, 2.5, 0); pl.add(trunk);
        for (let i = 0; i < 12; i++) {
          const a = (i / 12) * Math.PI * 2 * 1.7;
          const h = 2.4 + (i / 12) * 2.2;
          const r = 0.45 + (1 - i / 14) * 0.45;
          const leaf = new THREE.Mesh(new THREE.SphereGeometry(0.42, 10, 8), i % 2 === 0 ? leafMat : leafLightMat);
          leaf.scale.set(1.2, 0.35, 0.85);
          leaf.position.set(Math.cos(a) * r, h, Math.sin(a) * r);
          leaf.rotation.set(0.3, -a, 0.25);
          leaf.castShadow = true;
          pl.add(leaf);
        }
        parent.add(pl);
      }'''

new_plant = '''      function addPlant(parent, x, z, scale = 1.0, terracotta = false) {
        const pl = new THREE.Group();
        pl.position.set(x, 0, z);
        pl.scale.setScalar(scale);
        const potMat = terracotta ? new THREE.MeshStandardMaterial({ color: '#a85a3a', roughness: 0.72 }) : ceramicMat;
        const pot = new THREE.Mesh(new THREE.CylinderGeometry(0.68, 0.46, 1.4, 24), potMat);
        pot.position.set(0, 0.7, 0); pot.castShadow = true; pl.add(pot);
        const soil = new THREE.Mesh(new THREE.CylinderGeometry(0.62, 0.62, 0.06, 18), walnutMat);
        soil.position.set(0, 1.38, 0); pl.add(soil);
        // Tall Bird-of-Paradise / Banana Palm stems & elongated curved broad leaves
        const leafShape = new THREE.Shape();
        leafShape.moveTo(0, 0);
        leafShape.quadraticCurveTo(0.42, 0.7, 0.26, 1.65);
        leafShape.quadraticCurveTo(0, 2.05, -0.26, 1.65);
        leafShape.quadraticCurveTo(-0.42, 0.7, 0, 0);
        const bladeGeo = new THREE.ShapeGeometry(leafShape, 8);
        for (let i = 0; i < 9; i++) {
          const a = (i / 9) * Math.PI * 2 + (i % 2) * 0.25;
          const stemH = 2.0 + (i % 3) * 0.85;
          const stem = new THREE.Mesh(new THREE.CylinderGeometry(0.03, 0.05, stemH, 8), leafMat);
          stem.position.set(Math.cos(a) * 0.16, 1.3 + stemH / 2, Math.sin(a) * 0.16);
          stem.rotation.z = -Math.cos(a) * 0.22;
          stem.rotation.x = Math.sin(a) * 0.22;
          pl.add(stem);
          const blade = new THREE.Mesh(bladeGeo, i % 2 === 0 ? leafMat : leafLightMat);
          blade.position.set(Math.cos(a) * (0.28 + (i % 3) * 0.12), 1.3 + stemH * 0.9, Math.sin(a) * (0.28 + (i % 3) * 0.12));
          blade.rotation.y = -a + Math.PI / 2;
          blade.rotation.x = 0.55 + (i % 3) * 0.18;
          blade.castShadow = true;
          pl.add(blade);
        }
        parent.add(pl);
      }'''

assert old_plant in code, "old_plant not found"
code = code.replace(old_plant, new_plant, 1)

# 4. Upgrade addSofa() to Beveled/Rounded Plush Upholstery + Tapered Legs
old_sofa = '''      function addSofa(parent, x, z, w, d, rotY, fabMat, pillowMats) {
        const sf = new THREE.Group();
        sf.position.set(x, 0, z);
        sf.rotation.y = rotY;
        // 4 tapered walnut legs
        [[-w / 2 + 0.3, -d / 2 + 0.3], [w / 2 - 0.3, -d / 2 + 0.3], [-w / 2 + 0.3, d / 2 - 0.3], [w / 2 - 0.3, d / 2 - 0.3]].forEach(([lx, lz]) => {
          const leg = new THREE.Mesh(new THREE.CylinderGeometry(0.08, 0.04, 0.45, 10), walnutMat);
          leg.position.set(lx, 0.225, lz); sf.add(leg);
        });
        // Base plinth
        const base = new THREE.Mesh(new THREE.BoxGeometry(w, 0.65, d), fabMat);
        base.position.set(0, 0.75, 0); base.castShadow = true; base.receiveShadow = true; sf.add(base);
        // Seat cushions (segmented)
        const numCush = Math.max(2, Math.round(w / 2.8));
        const cw = (w - 0.9) / numCush;
        for (let i = 0; i < numCush; i++) {
          const cx = -w / 2 + 0.45 + cw / 2 + i * cw;
          const cush = new THREE.Mesh(new THREE.BoxGeometry(cw - 0.06, 0.45, d - 0.5), fabMat);
          cush.position.set(cx, 1.28, 0.15); cush.castShadow = true; sf.add(cush);
          // Backrest cushion
          const backC = new THREE.Mesh(new THREE.BoxGeometry(cw - 0.08, 1.15, 0.55), fabMat);
          backC.position.set(cx, 1.95, -d / 2 + 0.45);
          backC.rotation.x = -0.14;
          backC.castShadow = true; sf.add(backC);
        }
        // Back frame & rounded armrests
        const backFrame = new THREE.Mesh(new THREE.BoxGeometry(w, 1.6, 0.45), fabMat);
        backFrame.position.set(0, 1.65, -d / 2 + 0.22); sf.add(backFrame);
        [-w / 2 + 0.25, w / 2 - 0.25].forEach(ax => {
          const arm = new THREE.Mesh(new THREE.BoxGeometry(0.5, 1.3, d), fabMat);
          arm.position.set(ax, 1.45, 0); arm.castShadow = true; sf.add(arm);
        });
        // Throw pillows
        if (pillowMats && pillowMats.length) {
          [-w / 2 + 0.85, w / 2 - 0.85].forEach((px, idx) => {
            const pil = new THREE.Mesh(new THREE.BoxGeometry(0.85, 0.85, 0.28), pillowMats[idx % pillowMats.length]);
            pil.position.set(px, 1.75, -d / 2 + 0.85);
            pil.rotation.set(-0.25, idx === 0 ? 0.35 : -0.35, 0.1);
            pil.castShadow = true; sf.add(pil);
          });
        }
        parent.add(sf);
      }'''

new_sofa = '''      function makeBeveledBox(w, h, d, r = 0.12) {
        const s = new THREE.Shape();
        const hw = Math.max(0.05, w / 2 - r), hh = Math.max(0.05, h / 2 - r);
        s.moveTo(-hw, -hh); s.lineTo(hw, -hh); s.lineTo(hw, hh); s.lineTo(-hw, hh); s.closePath();
        const g = new THREE.ExtrudeGeometry(s, { depth: Math.max(0.05, d - 2 * r), bevelEnabled: true, bevelThickness: r, bevelSize: r, bevelSegments: 3 });
        g.center();
        return g;
      }

      function addSofa(parent, x, z, w, d, rotY, fabMat, pillowMats) {
        const sf = new THREE.Group();
        sf.position.set(x, 0, z);
        sf.rotation.y = rotY;
        // 4 tapered walnut legs
        [[-w / 2 + 0.32, -d / 2 + 0.32], [w / 2 - 0.32, -d / 2 + 0.32], [-w / 2 + 0.32, d / 2 - 0.32], [w / 2 - 0.32, d / 2 - 0.32]].forEach(([lx, lz]) => {
          const leg = new THREE.Mesh(new THREE.CylinderGeometry(0.08, 0.04, 0.5, 10), walnutMat);
          leg.position.set(lx, 0.25, lz); sf.add(leg);
        });
        // Beveled upholstered base plinth
        const base = new THREE.Mesh(makeBeveledBox(w, 0.58, d, 0.10), fabMat);
        base.position.set(0, 0.76, 0); base.castShadow = true; base.receiveShadow = true; sf.add(base);
        // Plush beveled seat & back cushions
        const numCush = Math.max(2, Math.round(w / 2.8));
        const cw = (w - 1.0) / numCush;
        for (let i = 0; i < numCush; i++) {
          const cx = -w / 2 + 0.5 + cw / 2 + i * cw;
          const cush = new THREE.Mesh(makeBeveledBox(cw - 0.06, 0.48, d - 0.55, 0.14), fabMat);
          cush.position.set(cx, 1.28, 0.15); cush.castShadow = true; sf.add(cush);
          const backC = new THREE.Mesh(makeBeveledBox(cw - 0.08, 1.18, 0.56, 0.14), fabMat);
          backC.position.set(cx, 1.98, -d / 2 + 0.48);
          backC.rotation.x = -0.15;
          backC.castShadow = true; sf.add(backC);
        }
        // Beveled back frame & rounded armrests
        const backFrame = new THREE.Mesh(makeBeveledBox(w, 1.65, 0.48, 0.10), fabMat);
        backFrame.position.set(0, 1.68, -d / 2 + 0.24); sf.add(backFrame);
        [-w / 2 + 0.28, w / 2 - 0.28].forEach(ax => {
          const arm = new THREE.Mesh(makeBeveledBox(0.56, 1.35, d, 0.16), fabMat);
          arm.position.set(ax, 1.48, 0); arm.castShadow = true; sf.add(arm);
        });
        // Plush beveled throw pillows
        if (pillowMats && pillowMats.length) {
          [-w / 2 + 0.88, w / 2 - 0.88].forEach((px, idx) => {
            const pil = new THREE.Mesh(makeBeveledBox(0.88, 0.88, 0.30, 0.12), pillowMats[idx % pillowMats.length]);
            pil.position.set(px, 1.78, -d / 2 + 0.88);
            pil.rotation.set(-0.26, idx === 0 ? 0.38 : -0.38, 0.12);
            pil.castShadow = true; sf.add(pil);
          });
        }
        parent.add(sf);
      }'''

assert old_sofa in code, "old_sofa not found"
code = code.replace(old_sofa, new_sofa, 1)

# 5. Add reusable Slatted Wood TV Feature Wall + Floating 3-Drawer Credenza helper & wire into Living Hall & Drawing Hall
helper_anchor = '      function addFramedArt('
slatted_tv_helper = '''      function addSlattedTVWall(parent, x, z, rotY, w = 9.2) {
        const tg = new THREE.Group();
        tg.position.set(x, 0, z);
        tg.rotation.y = rotY;
        // Dark acoustic felt backing
        const back = new THREE.Mesh(new THREE.BoxGeometry(w, 9.6, 0.12), metalMat);
        back.position.set(0, 4.8, 0); tg.add(back);
        // Vertical walnut slats
        const slatMat = new THREE.MeshStandardMaterial({ color: '#7a4b2a', roughness: 0.45 });
        for (let sx = -w / 2 + 0.2; sx <= w / 2 - 0.2; sx += 0.36) {
          const slat = new THREE.Mesh(new THREE.BoxGeometry(0.18, 9.5, 0.14), slatMat);
          slat.position.set(sx, 4.8, 0.12);
          slat.castShadow = true; tg.add(slat);
        }
        // Floating 3-Drawer Walnut Credenza with Brass Pulls
        const cred = new THREE.Mesh(new THREE.BoxGeometry(w * 0.72, 1.15, 1.35), slatMat);
        cred.position.set(0, 1.85, 0.82); cred.castShadow = true; tg.add(cred);
        [-w * 0.22, 0, w * 0.22].forEach(dx => {
          const pull = new THREE.Mesh(new THREE.BoxGeometry(0.65, 0.04, 0.06), brassMat);
          pull.position.set(dx, 1.95, 1.52); tg.add(pull);
        });
        // 75" Black OLED TV
        const tv = new THREE.Mesh(new THREE.BoxGeometry(w * 0.62, 3.3, 0.12), metalMat);
        tv.position.set(0, 5.1, 0.26); tv.castShadow = true; tg.add(tv);
        // Two white ceramic vases on floating console
        [-w * 0.28, w * 0.28].forEach((vx, idx) => {
          const vase = new THREE.Mesh(new THREE.CylinderGeometry(0.16, 0.26, 0.85, 16), ceramicMat);
          vase.position.set(vx, 2.85, 0.85); tg.add(vase);
          if (idx === 0) {
            [0xffb3c6, 0xffffff, 0xfde047].forEach((fc, fi) => {
              const fl = new THREE.Mesh(new THREE.SphereGeometry(0.1, 8, 8), new THREE.MeshStandardMaterial({ color: fc }));
              fl.position.set(vx + (fi - 1) * 0.12, 3.45 + (fi % 2) * 0.1, 0.85); tg.add(fl);
            });
          }
        });
        parent.add(tg);
      }

'''

assert helper_anchor in code, "helper_anchor not found"
code = code.replace(helper_anchor, slatted_tv_helper + helper_anchor, 1)

# Add Slatted TV Wall on Living Hall South Wall (facing North into Living Hall, right beside the open Dining sightline!)
# Also replace Living Hall's default coffee table with the Oval White Marble & Brass-Legged Table + Colorful Books + Brass Tray
old_lv_tables = '''          const ctBase1 = new THREE.Mesh(new THREE.CylinderGeometry(1.9, 1.9, 1.0, 28), walnutMat);
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
          lvVase.position.set(0.4, 1.58, -1.9); slot.add(lvVase);'''

new_lv_tables = '''          // Sleek Oval White Marble Coffee Table with Slender Brass Legs
          const ovalTop = new THREE.Mesh(new THREE.CylinderGeometry(2.2, 2.2, 0.14, 36), ceramicMat);
          ovalTop.scale.set(1.35, 1.0, 0.85);
          ovalTop.position.set(0, 1.25, -1.4); ovalTop.castShadow = true; slot.add(ovalTop);
          [[-1.8, -2.2], [1.8, -2.2], [-1.8, -0.6], [1.8, -0.6]].forEach(([lx, lz]) => {
            const leg = new THREE.Mesh(new THREE.CylinderGeometry(0.05, 0.04, 1.2, 10), brassMat);
            leg.position.set(lx, 0.6, lz); slot.add(leg);
          });
          // Stacked colorful hardcover books & brass tray with ceramic vase
          [0xb91c1c, 0x15803d, 0xfef3c7].forEach((bc, bi) => {
            const bk = new THREE.Mesh(new THREE.BoxGeometry(1.0 - bi * 0.08, 0.16, 0.75), new THREE.MeshStandardMaterial({ color: bc, roughness: 0.6 }));
            bk.position.set(-0.7, 1.4 + bi * 0.16, -1.5); bk.rotation.y = 0.15; slot.add(bk);
          });
          const tray = new THREE.Mesh(new THREE.CylinderGeometry(0.65, 0.65, 0.05, 24), brassMat);
          tray.position.set(0.95, 1.35, -1.2); slot.add(tray);
          const lvVase = new THREE.Mesh(new THREE.CylinderGeometry(0.18, 0.28, 0.7, 16), ceramicMat);
          lvVase.position.set(0.95, 1.72, -1.2); slot.add(lvVase);'''

assert old_lv_tables in code, "old_lv_tables not found"
code = code.replace(old_lv_tables, new_lv_tables, 1)

# Add Slatted TV Feature Wall to Living Hall South Wall (x: -1.5, z: 12.8 facing North) & Drawing Hall South Wall
code = code.replace(
    "      // Window Curtains on East Wall\n      addCurtains(lv, 16.5, 5.2, -1.5, 9.5, 6.5, -Math.PI / 2);",
    "      // Slatted Walnut TV Feature Wall on South Wall (right beside the open Dining archway)\n      addSlattedTVWall(lv, -1.5, 12.85, Math.PI, 9.5);\n      // Window Curtains on East Wall\n      addCurtains(lv, 16.5, 5.2, -1.5, 9.5, 6.5, -Math.PI / 2);"
)

# Upgrade Drawing Hall's media console to Slatted Walnut TV Wall too
old_dw_tv = '''      // Fluted Oak TV Media Console on South/Side Wall
      const dwConsole = new THREE.Mesh(new THREE.BoxGeometry(8.0, 1.4, 1.5), oakMat);
      dwConsole.position.set(0, 0.7, 8.8); dwConsole.castShadow = true; dw.add(dwConsole);
      const dwTV = new THREE.Mesh(new THREE.BoxGeometry(6.2, 3.4, 0.12), metalMat);
      dwTV.position.set(0, 4.3, 9.5); dw.add(dwTV);'''
new_dw_tv = "      addSlattedTVWall(dw, 0, 10.6, Math.PI, 9.0);"
assert old_dw_tv in code, "old_dw_tv not found"
code = code.replace(old_dw_tv, new_dw_tv, 1)

# Upgrade Dining Sideboard to 2-Tier Dark Walnut & Glass Crockery Cabinet
old_dn_side = '''      // Sideboard / Crockery Unit on North Wall & Curtains on West Window
      const sideb = new THREE.Mesh(new THREE.BoxGeometry(5.6, 2.8, 1.5), dnSideMat);
      sideb.position.set(0, 1.4, -4.5); sideb.castShadow = true; dn.add(sideb);'''
new_dn_side = '''      // 2-Tier Dark Walnut Crockery & Sideboard Unit on North Wall
      const sideb = new THREE.Mesh(new THREE.BoxGeometry(6.8, 2.5, 1.5), walnutMat);
      sideb.position.set(0, 1.25, -4.6); sideb.castShadow = true; dn.add(sideb);
      const sideTop = new THREE.Mesh(new THREE.BoxGeometry(6.9, 0.14, 1.6), ceramicMat);
      sideTop.position.set(0, 2.57, -4.6); dn.add(sideTop);
      const upperCrock = new THREE.Mesh(new THREE.BoxGeometry(6.4, 3.2, 1.1), darkFabric);
      upperCrock.position.set(0, 5.6, -4.8); upperCrock.castShadow = true; dn.add(upperCrock);
      [-2.2, -0.7, 0.7, 2.2].forEach(hx => {
        const pull = new THREE.Mesh(new THREE.BoxGeometry(0.45, 0.04, 0.05), brassMat);
        pull.position.set(hx, 4.8, -4.22); dn.add(pull);
      });'''
assert old_dn_side in code, "old_dn_side not found"
code = code.replace(old_dn_side, new_dn_side, 1)

# Use terracotta pot on one Living Hall plant for warmth
code = code.replace(
    "      addPlant(lv, -9.8, -8.5, 1.35);\n      addPlant(lv, 11.2, 7.2, 1.15);",
    "      addPlant(lv, -9.8, -8.5, 1.35, true);\n      addPlant(lv, 11.2, 7.2, 1.15, false);"
)

with open(index_path, 'w', encoding='utf-8') as f:
    f.write(code)

print("Finish quality upgraded successfully!")

