import re

index_path = '/Users/puspharaj/Documents/Projects/ai-interior-designer/index.html'

with open(index_path, 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Fix exposure and global lighting so rooms are richly lit without white blowout
code = code.replace(
    'renderer.toneMappingExposure = 1.15;',
    'renderer.toneMappingExposure = 0.90;'
)

old_setup_lighting = '''    function setupLighting() {
      hemiLight = new THREE.HemisphereLight('#f8fafc', '#1e293b', 0.65);
      scene.add(hemiLight);

      ambientLight = new THREE.AmbientLight('#fffbeb', 0.45);
      scene.add(ambientLight);

      sunLight = new THREE.DirectionalLight('#fff5ea', 1.8);'''

new_setup_lighting = '''    function setupLighting() {
      hemiLight = new THREE.HemisphereLight('#f1f5f9', '#1e293b', 0.42);
      scene.add(hemiLight);

      ambientLight = new THREE.AmbientLight('#fffbeb', 0.25);
      scene.add(ambientLight);

      sunLight = new THREE.DirectionalLight('#fff5ea', 0.95);'''

assert old_setup_lighting in code, "setupLighting not found"
code = code.replace(old_setup_lighting, new_setup_lighting, 1)

# Update toggleDaylight intensities to match balanced exposure
code = code.replace(
    'sunLight.intensity = daylightEnabled ? 1.8 : 0.0;',
    'sunLight.intensity = daylightEnabled ? 0.95 : 0.0;'
)
code = code.replace(
    'hemiLight.intensity = daylightEnabled ? 0.65 : 0.2;',
    'hemiLight.intensity = daylightEnabled ? 0.42 : 0.18;'
)
code = code.replace(
    'ambientLight.intensity = daylightEnabled ? 0.45 : 0.15;',
    'ambientLight.intensity = daylightEnabled ? 0.25 : 0.12;'
)

# 2. Warm architectural wall & ceiling tones so they don't clip to flat #FFFFFF
code = code.replace(
    "const ceilMat = new THREE.MeshStandardMaterial({ color: '#f8fafc', roughness: 0.8 });",
    "const ceilMat = new THREE.MeshStandardMaterial({ color: '#eae6df', roughness: 0.92 });"
)
code = code.replace(
    "const wallMat = new THREE.MeshStandardMaterial({ color: '#f8fafc', roughness: 0.65 });",
    "const wallMat = new THREE.MeshStandardMaterial({ color: '#e5e0d8', roughness: 0.85 });"
)

# 3. Balance per-room lighting in setupRoomLighting
old_room_light = '''      // Dedicated recessed ceiling spotlight
      const spot = new THREE.SpotLight(room.floor === 'tile' ? '#f8fafc' : '#fed7aa', 2.8);
      spot.position.set(cx, 9.6, cz);
      spot.target.position.set(cx, 0, cz);
      spot.angle = Math.PI / 3;
      spot.penumbra = 0.6;
      spot.distance = 25;
      spot.castShadow = true;
      lightsGroup.add(spot);
      lightsGroup.add(spot.target);

      // Warm ambient room fill
      const pt = new THREE.PointLight('#fff1cc', 1.8, 20);
      pt.position.set(cx, 7.5, cz);
      lightsGroup.add(pt);'''

new_room_light = '''      // Dedicated recessed ceiling spotlight (balanced so surfaces retain texture & depth)
      const isCool = (room.floor === 'tile' && room.id !== 'sitout');
      const spot = new THREE.SpotLight(isCool ? '#f8fafc' : '#ffe8cc', 0.95);
      spot.position.set(cx, 9.6, cz);
      spot.target.position.set(cx, 0, cz);
      spot.angle = Math.PI / 2.6;
      spot.penumbra = 0.75;
      spot.distance = 28;
      spot.castShadow = true;
      lightsGroup.add(spot);
      lightsGroup.add(spot.target);

      // Warm ambient room fill
      const pt = new THREE.PointLight(isCool ? '#f1f5f9' : '#ffdcb8', 0.65, 26, 1.5);
      pt.position.set(cx, 7.8, cz);
      lightsGroup.add(pt);'''

assert old_room_light in code, "setupRoomLighting not found"
code = code.replace(old_room_light, new_room_light, 1)

# 4. Replace buildDetailedFurniture() with rich, shaped, staged furniture & ceiling lights for ALL rooms
furn_start = code.find('    // ── HIGH-REALISM SHAPED PROCEDURAL FURNITURE ──────────────────────────────────')
furn_end = code.find('    // ── 3D FLOATING ROOM LABELS ───────────────────────────────────────────────────')
assert furn_start != -1 and furn_end != -1, "Furniture bounds not found"

# Extract the existing Kitchen block (from "// 8. GOURMET KITCHEN" to "furnitureGroup.add(kt);") so we preserve it intact!
kt_start = code.find('      // 8. GOURMET KITCHEN')
kt_end = code.find('      furnitureGroup.add(kt);') + len('      furnitureGroup.add(kt);')
assert kt_start != -1 and kt_end != -1, "Kitchen block not found"
kitchen_block = code[kt_start:kt_end]

new_furniture_code = '''    // ── HIGH-REALISM SHAPED PROCEDURAL FURNITURE & CEILING LIGHTS ─────────────────
    function buildDetailedFurniture() {
      const oakMat = new THREE.MeshStandardMaterial({ map: TEXTURES.hardwood, roughness: 0.45 });
      const walnutMat = new THREE.MeshStandardMaterial({ color: '#4a2e1b', roughness: 0.42 });
      const marbleMat = new THREE.MeshStandardMaterial({ map: TEXTURES.darkMarble, roughness: 0.25 });
      const calaMat = new THREE.MeshStandardMaterial({ map: TEXTURES.calacatta, roughness: 0.22 });
      const stoneMat = new THREE.MeshStandardMaterial({ map: TEXTURES.stone, color: '#cfc8bc', roughness: 0.8 });
      const rugMat = new THREE.MeshStandardMaterial({ map: TEXTURES.rug, color: '#cfc7ba', roughness: 0.95 });
      const metalMat = new THREE.MeshStandardMaterial({ color: '#18181b', metalness: 0.8, roughness: 0.3 });
      const brassMat = new THREE.MeshStandardMaterial({ color: '#d4af37', metalness: 0.85, roughness: 0.24 });
      const chromeMat = new THREE.MeshStandardMaterial({ color: '#e2e8f0', metalness: 0.9, roughness: 0.18 });
      const creamFabric = new THREE.MeshStandardMaterial({ color: '#dfd9ce', roughness: 0.85 });
      const greyFabric = new THREE.MeshStandardMaterial({ color: '#5c6672', roughness: 0.85 });
      const darkFabric = new THREE.MeshStandardMaterial({ color: '#2b3440', roughness: 0.85 });
      const sageFabric = new THREE.MeshStandardMaterial({ color: '#5d7a68', roughness: 0.85 });
      const terraFabric = new THREE.MeshStandardMaterial({ color: '#a85a44', roughness: 0.85 });
      const ochreFabric = new THREE.MeshStandardMaterial({ color: '#c48b3b', roughness: 0.85 });
      const glassMat = new THREE.MeshStandardMaterial({ color: '#93c5fd', transparent: true, opacity: 0.35, roughness: 0.1 });
      const glowWarmMat = new THREE.MeshStandardMaterial({ color: '#fff8e7', emissive: '#ffcf87', emissiveIntensity: 1.4, roughness: 0.3 });
      const glowCoolMat = new THREE.MeshStandardMaterial({ color: '#f8fafc', emissive: '#e0f2fe', emissiveIntensity: 1.3, roughness: 0.3 });
      const ceramicMat = new THREE.MeshStandardMaterial({ color: '#f1efe9', roughness: 0.25 });
      const leafMat = new THREE.MeshStandardMaterial({ color: '#2d5a36', roughness: 0.55, side: THREE.DoubleSide });
      const leafLightMat = new THREE.MeshStandardMaterial({ color: '#3f7848', roughness: 0.55, side: THREE.DoubleSide });

      // ── REUSABLE SHAPED DECOR & LIGHTING HELPERS ──
      function addDownlights(parent, coords, cool = false) {
        const lensMat = cool ? glowCoolMat : glowWarmMat;
        coords.forEach(([dx, dz]) => {
          const bezel = new THREE.Mesh(new THREE.RingGeometry(0.22, 0.35, 18), ceramicMat);
          bezel.rotation.x = Math.PI / 2;
          bezel.position.set(dx, 9.96, dz);
          parent.add(bezel);
          const lens = new THREE.Mesh(new THREE.CircleGeometry(0.22, 18), lensMat);
          lens.rotation.x = Math.PI / 2;
          lens.position.set(dx, 9.95, dz);
          parent.add(lens);
        });
      }

      function addTrayCeiling(parent, w, d) {
        const trayMat = new THREE.MeshStandardMaterial({ color: '#e6e2da', roughness: 0.9 });
        const coveMat = new THREE.MeshStandardMaterial({ color: '#fff4dc', emissive: '#ffd28a', emissiveIntensity: 0.85 });
        const b = 1.2, drop = 0.45;
        // 4 perimeter soffit beams
        [
          [0, -d / 2 + b / 2, w, b],
          [0, d / 2 - b / 2, w, b],
          [-w / 2 + b / 2, 0, b, d - 2 * b],
          [w / 2 - b / 2, 0, b, d - 2 * b]
        ].forEach(([sx, sz, sw, sd]) => {
          const beam = new THREE.Mesh(new THREE.BoxGeometry(sw, drop, sd), trayMat);
          beam.position.set(sx, 10.0 - drop / 2, sz);
          parent.add(beam);
        });
        // Inner warm LED cove glow border
        [
          [0, -d / 2 + b, w - 2 * b, 0.08],
          [0, d / 2 - b, w - 2 * b, 0.08],
          [-w / 2 + b, 0, 0.08, d - 2 * b],
          [w / 2 - b, 0, 0.08, d - 2 * b]
        ].forEach(([cx, cz, cw, cd]) => {
          const strip = new THREE.Mesh(new THREE.BoxGeometry(cw, 0.08, cd), coveMat);
          strip.position.set(cx, 9.65, cz);
          parent.add(strip);
        });
      }

      function addChandelier(parent, x, z, radius = 2.2, globes = 8) {
        const ch = new THREE.Group();
        ch.position.set(x, 0, z);
        const canopy = new THREE.Mesh(new THREE.CylinderGeometry(0.35, 0.35, 0.1, 20), brassMat);
        canopy.position.set(0, 9.95, 0); ch.add(canopy);
        const rod = new THREE.Mesh(new THREE.CylinderGeometry(0.04, 0.04, 2.2, 12), brassMat);
        rod.position.set(0, 8.85, 0); ch.add(rod);
        const ring = new THREE.Mesh(new THREE.TorusGeometry(radius, 0.06, 12, 40), brassMat);
        ring.rotation.x = Math.PI / 2;
        ring.position.set(0, 7.75, 0); ch.add(ring);
        if (radius > 1.8) {
          const innerRing = new THREE.Mesh(new THREE.TorusGeometry(radius * 0.55, 0.045, 10, 32), brassMat);
          innerRing.rotation.x = Math.PI / 2;
          innerRing.position.set(0, 7.35, 0); ch.add(innerRing);
        }
        for (let i = 0; i < globes; i++) {
          const a = (i / globes) * Math.PI * 2;
          const gl = new THREE.Mesh(new THREE.SphereGeometry(0.22, 14, 14), glowWarmMat);
          gl.position.set(Math.cos(a) * radius, 7.75, Math.sin(a) * radius);
          ch.add(gl);
        }
        const chLight = new THREE.PointLight('#ffdca8', 0.9, 20, 1.6);
        chLight.position.set(0, 7.4, 0);
        ch.add(chLight);
        parent.add(ch);
      }

      function addCeilingFan(parent, x, z, bladeMat = walnutMat) {
        const fan = new THREE.Group();
        fan.position.set(x, 0, z);
        const rod = new THREE.Mesh(new THREE.CylinderGeometry(0.06, 0.06, 1.1, 12), metalMat);
        rod.position.set(0, 9.45, 0); fan.add(rod);
        const hub = new THREE.Mesh(new THREE.CylinderGeometry(0.35, 0.35, 0.25, 20), brassMat);
        hub.position.set(0, 8.85, 0); fan.add(hub);
        const lightDome = new THREE.Mesh(new THREE.SphereGeometry(0.28, 16, 12, 0, Math.PI * 2, 0, Math.PI / 2), glowWarmMat);
        lightDome.rotation.x = Math.PI;
        lightDome.position.set(0, 8.75, 0); fan.add(lightDome);
        for (let i = 0; i < 3; i++) {
          const blade = new THREE.Mesh(new THREE.BoxGeometry(2.1, 0.04, 0.42), bladeMat);
          const a = (i / 3) * Math.PI * 2;
          blade.position.set(Math.cos(a) * 1.15, 8.88, Math.sin(a) * 1.15);
          blade.rotation.y = -a;
          fan.add(blade);
        }
        parent.add(fan);
      }

      function addPlant(parent, x, z, scale = 1.0) {
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
      }

      function addFloorLamp(parent, x, z, rotY = 0) {
        const fl = new THREE.Group();
        fl.position.set(x, 0, z);
        fl.rotation.y = rotY;
        const base = new THREE.Mesh(new THREE.CylinderGeometry(0.65, 0.7, 0.9, 20), marbleMat);
        base.position.set(0, 0.45, 0); base.castShadow = true; fl.add(base);
        const stem = new THREE.Mesh(new THREE.CylinderGeometry(0.035, 0.045, 5.2, 10), brassMat);
        stem.position.set(0, 3.0, 0); fl.add(stem);
        const arm = new THREE.Mesh(new THREE.TorusGeometry(1.5, 0.035, 8, 24, Math.PI * 0.65), brassMat);
        arm.position.set(1.5, 5.5, 0);
        arm.rotation.z = Math.PI * 0.35;
        fl.add(arm);
        const shade = new THREE.Mesh(new THREE.SphereGeometry(0.55, 20, 14, 0, Math.PI * 2, 0, Math.PI / 2), brassMat);
        shade.rotation.x = Math.PI;
        shade.position.set(2.4, 6.2, 0); fl.add(shade);
        const bulb = new THREE.Mesh(new THREE.SphereGeometry(0.18, 10, 10), glowWarmMat);
        bulb.position.set(2.4, 6.1, 0); fl.add(bulb);
        const fLight = new THREE.PointLight('#ffdca8', 0.55, 10, 1.8);
        fLight.position.set(2.4, 5.9, 0); fl.add(fLight);
        parent.add(fl);
      }

      function addFramedArt(parent, x, y, z, w, h, rotY = 0, accentColor = '#b45309') {
        const art = new THREE.Group();
        art.position.set(x, y, z);
        art.rotation.y = rotY;
        const frame = new THREE.Mesh(new THREE.BoxGeometry(w, h, 0.12), walnutMat);
        art.add(frame);
        const mat = new THREE.Mesh(new THREE.BoxGeometry(w - 0.25, h - 0.25, 0.14), ceramicMat);
        art.add(mat);
        const canvas = new THREE.Mesh(new THREE.BoxGeometry(w - 0.6, h - 0.6, 0.16), new THREE.MeshStandardMaterial({ color: '#2b3a4a', roughness: 0.7 }));
        art.add(canvas);
        const shape1 = new THREE.Mesh(new THREE.BoxGeometry((w - 0.8) * 0.45, (h - 0.8) * 0.6, 0.18), new THREE.MeshStandardMaterial({ color: accentColor, roughness: 0.6 }));
        shape1.position.set(-w * 0.12, h * 0.05, 0);
        art.add(shape1);
        const shape2 = new THREE.Mesh(new THREE.CylinderGeometry(h * 0.18, h * 0.18, 0.18, 20), brassMat);
        shape2.rotation.x = Math.PI / 2;
        shape2.position.set(w * 0.16, -h * 0.08, 0);
        art.add(shape2);
        parent.add(art);
      }

      function addCurtains(parent, x, y, z, w, h, rotY = 0) {
        const cg = new THREE.Group();
        cg.position.set(x, y, z);
        cg.rotation.y = rotY;
        const rod = new THREE.Mesh(new THREE.CylinderGeometry(0.04, 0.04, w + 1.2, 10), brassMat);
        rod.rotation.z = Math.PI / 2;
        rod.position.set(0, h / 2 + 0.15, 0.15);
        cg.add(rod);
        const sheer = new THREE.Mesh(new THREE.PlaneGeometry(w, h), new THREE.MeshStandardMaterial({ color: '#f5f2eb', transparent: true, opacity: 0.45, side: THREE.DoubleSide }));
        sheer.position.set(0, 0, 0.06);
        cg.add(sheer);
        [-w / 2 - 0.15, w / 2 + 0.15].forEach(px => {
          for (let f = -1; f <= 1; f++) {
            const pleat = new THREE.Mesh(new THREE.CylinderGeometry(0.18, 0.22, h, 10), greyFabric);
            pleat.position.set(px + f * 0.22, 0, 0.16);
            pleat.castShadow = true;
            cg.add(pleat);
          }
        });
        parent.add(cg);
      }

      function addSofa(parent, x, z, w, d, rotY, fabMat, pillowMats) {
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
      }

      function addArmchair(parent, x, z, rotY, fabMat) {
        addSofa(parent, x, z, 3.0, 2.8, rotY, fabMat, [ochreFabric]);
      }

      // ── 1. MASTER BEDROOM (Bed 1) ──
      const b1 = new THREE.Group();
      b1.position.set(8.8, 0, 7.5);
      // Tufted King Bed
      const hb1 = new THREE.Mesh(new THREE.BoxGeometry(7.6, 4.4, 0.5), darkFabric);
      hb1.position.set(0, 2.2, -3.5); hb1.castShadow = true; b1.add(hb1);
      for (let t = -3.0; t <= 3.0; t += 1.0) {
        const panel = new THREE.Mesh(new THREE.BoxGeometry(0.88, 3.8, 0.14), greyFabric);
        panel.position.set(t, 2.3, -3.22); b1.add(panel);
      }
      const bedBase1 = new THREE.Mesh(new THREE.BoxGeometry(6.9, 0.65, 7.4), walnutMat);
      bedBase1.position.set(0, 0.4, 0.3); b1.add(bedBase1);
      const mat1 = new THREE.Mesh(new THREE.BoxGeometry(6.6, 0.9, 7.1), creamFabric);
      mat1.position.set(0, 1.15, 0.3); mat1.castShadow = true; b1.add(mat1);
      const duvet1 = new THREE.Mesh(new THREE.BoxGeometry(6.75, 0.32, 4.4), sageFabric);
      duvet1.position.set(0, 1.68, 1.65); duvet1.castShadow = true; b1.add(duvet1);
      [-1.7, 1.7].forEach(px => {
        const pil = new THREE.Mesh(new THREE.BoxGeometry(2.3, 0.45, 1.4), creamFabric);
        pil.position.set(px, 1.82, -2.1); pil.rotation.x = -0.25; pil.castShadow = true; b1.add(pil);
        const sham = new THREE.Mesh(new THREE.BoxGeometry(1.4, 0.45, 0.8), terraFabric);
        sham.position.set(px, 1.85, -1.3); sham.rotation.x = -0.3; b1.add(sham);
      });
      // Nightstands & Glowing Table Lamps
      [-4.6, 4.6].forEach(nx => {
        const ns = new THREE.Mesh(new THREE.BoxGeometry(1.9, 1.7, 1.6), walnutMat);
        ns.position.set(nx, 0.85, -2.9); ns.castShadow = true; b1.add(ns);
        const lBase = new THREE.Mesh(new THREE.CylinderGeometry(0.18, 0.28, 0.7, 14), brassMat);
        lBase.position.set(nx, 2.05, -2.9); b1.add(lBase);
        const lShade = new THREE.Mesh(new THREE.CylinderGeometry(0.35, 0.5, 0.65, 16), glowWarmMat);
        lShade.position.set(nx, 2.65, -2.9); b1.add(lShade);
      });
      // Rug, Framed Art, Lounge Chair, Curtains, TV Unit
      const r1 = new THREE.Mesh(new THREE.PlaneGeometry(12.5, 14.0), rugMat);
      r1.rotation.x = -Math.PI / 2; r1.position.set(0, 0.03, 1.5); r1.receiveShadow = true; b1.add(r1);
      addFramedArt(b1, 0, 6.2, -6.5, 4.2, 2.6, 0, '#5d7a68');
      addArmchair(b1, -5.2, 9.5, 0.65, sageFabric);
      addPlant(b1, 5.8, 12.2, 0.9);
      addCurtains(b1, -7.8, 5.2, 3.0, 4.5, 6.5, Math.PI / 2);
      const tvc1 = new THREE.Mesh(new THREE.BoxGeometry(7.0, 1.4, 1.5), walnutMat);
      tvc1.position.set(0, 0.7, 14.2); tvc1.castShadow = true; b1.add(tvc1);
      const tv1 = new THREE.Mesh(new THREE.BoxGeometry(5.5, 3.0, 0.12), metalMat);
      tv1.position.set(0, 4.2, 14.8); tv1.castShadow = true; b1.add(tv1);
      addTrayCeiling(b1, 15.0, 21.0);
      addCeilingFan(b1, 0, 1.0, walnutMat);
      addDownlights(b1, [[-4.5, -3.5], [4.5, -3.5], [-4.5, 5.5], [4.5, 5.5]]);
      furnitureGroup.add(b1);

      // ── 2. MASTER BATH (Bath 1) & GUEST BATH 2 (Bath 2) & COMMON BATH (Bath 3) ──
      function buildBath(cx, cz, w, d) {
        const bt = new THREE.Group();
        bt.position.set(cx, 0, cz);
        const van = new THREE.Mesh(new THREE.BoxGeometry(4.4, 2.2, 1.7), walnutMat);
        van.position.set(0, 1.4, -d / 2 + 1.2); van.castShadow = true; bt.add(van);
        const vanTop = new THREE.Mesh(new THREE.BoxGeometry(4.5, 0.16, 1.8), calaMat);
        vanTop.position.set(0, 2.58, -d / 2 + 1.2); bt.add(vanTop);
        const basin = new THREE.Mesh(new THREE.CylinderGeometry(0.65, 0.55, 0.35, 20), ceramicMat);
        basin.position.set(0, 2.8, -d / 2 + 1.2); bt.add(basin);
        const faucet = new THREE.Mesh(new THREE.TorusGeometry(0.22, 0.03, 8, 14, Math.PI), chromeMat);
        faucet.position.set(0, 3.1, -d / 2 + 0.75); bt.add(faucet);
        // Backlit LED Mirror
        const mirGlow = new THREE.Mesh(new THREE.BoxGeometry(4.0, 2.9, 0.06), glowCoolMat);
        mirGlow.position.set(0, 5.0, -d / 2 + 0.32); bt.add(mirGlow);
        const mir = new THREE.Mesh(new THREE.BoxGeometry(3.8, 2.7, 0.08), new THREE.MeshStandardMaterial({ color: '#cbd5e1', roughness: 0.08, metalness: 0.92 }));
        mir.position.set(0, 5.0, -d / 2 + 0.36); bt.add(mir);
        // Glass Shower & Rain Showerhead
        const shw = new THREE.Mesh(new THREE.BoxGeometry(w - 1.2, 7.6, 0.08), glassMat);
        shw.position.set(0, 3.8, 0.8); bt.add(shw);
        const head = new THREE.Mesh(new THREE.CylinderGeometry(0.45, 0.45, 0.08, 16), chromeMat);
        head.position.set(0, 8.2, d / 2 - 1.5); bt.add(head);
        // WC
        const wcTank = new THREE.Mesh(new THREE.BoxGeometry(1.3, 1.6, 0.65), ceramicMat);
        wcTank.position.set(w / 2 - 1.5, 1.5, d / 2 - 1.0); bt.add(wcTank);
        const wcBowl = new THREE.Mesh(new THREE.CylinderGeometry(0.6, 0.45, 1.2, 16), ceramicMat);
        wcBowl.position.set(w / 2 - 1.5, 0.65, d / 2 - 1.6); bt.add(wcBowl);
        addDownlights(bt, [[0, -2.0], [0, 2.0]], true);
        furnitureGroup.add(bt);
      }
      buildBath(20.4, 6.0, 6.4, 11.0);
      buildBath(27.2, 6.0, 6.4, 11.0);
      buildBath(21.2, 71.1, 6.8, 4.8);

      // ── 3. MASTER DRESS (Dress 1) & GUEST DRESS 2 (Dress 2) ──
      function buildDress(cx, cz) {
        const dr = new THREE.Group();
        dr.position.set(cx, 0, cz);
        const wrd = new THREE.Mesh(new THREE.BoxGeometry(5.5, 9.0, 2.0), walnutMat);
        wrd.position.set(0, 4.5, 3.8); wrd.castShadow = true; dr.add(wrd);
        for (let wx = -2.0; wx <= 2.0; wx += 1.33) {
          const handle = new THREE.Mesh(new THREE.BoxGeometry(0.05, 1.4, 0.06), brassMat);
          handle.position.set(wx, 4.5, 2.75); dr.add(handle);
        }
        const ottoman = new THREE.Mesh(new THREE.CylinderGeometry(1.1, 1.1, 1.3, 24), sageFabric);
        ottoman.position.set(0, 0.65, -0.5); ottoman.castShadow = true; dr.add(ottoman);
        const mir = new THREE.Mesh(new THREE.BoxGeometry(2.2, 6.2, 0.1), chromeMat);
        mir.position.set(-2.9, 3.5, -1.0); mir.rotation.y = Math.PI / 2; dr.add(mir);
        addDownlights(dr, [[0, -1.5], [0, 1.5]], false);
        furnitureGroup.add(dr);
      }
      buildDress(20.4, 17.5);
      buildDress(27.2, 17.5);

      // ── 4. BEDROOM 2 (Guest / Study Suite) ──
      const b2 = new THREE.Group();
      b2.position.set(39.2, 0, 7.5);
      const hb2 = new THREE.Mesh(new THREE.BoxGeometry(6.8, 4.0, 0.45), greyFabric);
      hb2.position.set(0, 2.0, -3.3); hb2.castShadow = true; b2.add(hb2);
      const mat2 = new THREE.Mesh(new THREE.BoxGeometry(6.2, 1.25, 6.8), creamFabric);
      mat2.position.set(0, 0.85, 0.2); mat2.castShadow = true; b2.add(mat2);
      const duvet2 = new THREE.Mesh(new THREE.BoxGeometry(6.3, 0.28, 4.2), ochreFabric);
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
      });
      const r2 = new THREE.Mesh(new THREE.PlaneGeometry(11, 12), rugMat);
      r2.rotation.x = -Math.PI / 2; r2.position.set(-0.5, 0.03, 1.5); r2.receiveShadow = true; b2.add(r2);
      // Study Desk, Chair, Monitor & Bookshelf
      const deskTop = new THREE.Mesh(new THREE.BoxGeometry(2.2, 0.16, 5.2), oakMat);
      deskTop.position.set(6.8, 2.45, 3.5); deskTop.castShadow = true; b2.add(deskTop);
      [[5.9, 1.2], [5.9, 5.8], [7.7, 1.2], [7.7, 5.8]].forEach(([lx, lz]) => {
        const dLeg = new THREE.Mesh(new THREE.CylinderGeometry(0.06, 0.05, 2.4, 10), metalMat);
        dLeg.position.set(lx, 1.2, lz); b2.add(dLeg);
      });
      const monitor = new THREE.Mesh(new THREE.BoxGeometry(0.12, 1.25, 2.2), metalMat);
      monitor.position.set(7.2, 3.4, 3.5); b2.add(monitor);
      const chair2 = new THREE.Mesh(new THREE.BoxGeometry(1.6, 1.8, 1.6), darkFabric);
      chair2.position.set(4.8, 1.5, 3.5); chair2.castShadow = true; b2.add(chair2);
      // Bookshelf with books
      const bk = new THREE.Mesh(new THREE.BoxGeometry(1.4, 8.2, 4.8), walnutMat);
      bk.position.set(7.0, 4.1, 9.8); bk.castShadow = true; b2.add(bk);
      const bkColors = ['#991b1b', '#1e40af', '#065f46', '#b45309', '#475569'];
      for (let sy = 1.6; sy <= 6.8; sy += 1.3) {
        const sh = new THREE.Mesh(new THREE.BoxGeometry(1.45, 0.1, 4.6), oakMat);
        sh.position.set(6.95, sy, 9.8); b2.add(sh);
        for (let b = 0; b < 6; b++) {
          const book = new THREE.Mesh(new THREE.BoxGeometry(0.7, 0.75 + (b % 3) * 0.1, 0.25), new THREE.MeshStandardMaterial({ color: bkColors[(b + Math.round(sy)) % bkColors.length], roughness: 0.7 }));
          book.position.set(6.7, sy + 0.42, 8.0 + b * 0.55); b2.add(book);
        }
      }
      addFramedArt(b2, 0, 5.8, -6.5, 3.6, 2.4, 0, '#c48b3b');
      addPlant(b2, -5.8, 11.5, 0.85);
      addTrayCeiling(b2, 14.5, 21.0);
      addCeilingFan(b2, 0, 1.5, oakMat);
      addDownlights(b2, [[-4, -3], [4, -3], [-4, 6], [4, 6]]);
      furnitureGroup.add(b2);

      // ── 5. POOJA SANCTUM ──
      const pj = new THREE.Group();
      pj.position.set(6.9, 0, 28.5);
      const mBase = new THREE.Mesh(new THREE.BoxGeometry(5.4, 2.6, 2.8), walnutMat);
      mBase.position.set(0, 1.3, -4.0); mBase.castShadow = true; pj.add(mBase);
      const mAlt = new THREE.Mesh(new THREE.BoxGeometry(5.6, 0.25, 3.0), calaMat);
      mAlt.position.set(0, 2.7, -4.0); pj.add(mAlt);
      // 4 Carved Pillars
      [[-2.2, -5.0], [2.2, -5.0], [-2.2, -3.0], [2.2, -3.0]].forEach(([px, pz]) => {
        const pil = new THREE.Mesh(new THREE.CylinderGeometry(0.14, 0.18, 4.2, 12), oakMat);
        pil.position.set(px, 4.8, pz); pj.add(pil);
      });
      const mRoof = new THREE.Mesh(new THREE.BoxGeometry(5.6, 0.35, 3.0), walnutMat);
      mRoof.position.set(0, 7.0, -4.0); pj.add(mRoof);
      const mDome = new THREE.Mesh(new THREE.ConeGeometry(1.4, 2.2, 8), brassMat);
      mDome.position.set(0, 8.2, -4.0); pj.add(mDome);
      // Glowing Diyas & Warm Sanctum Light
      [-1.5, 1.5].forEach(dx => {
        const diya = new THREE.Mesh(new THREE.CylinderGeometry(0.24, 0.12, 0.45, 14), brassMat);
        diya.position.set(dx, 3.05, -3.3); pj.add(diya);
        const flame = new THREE.Mesh(new THREE.SphereGeometry(0.1, 8, 8), glowWarmMat);
        flame.position.set(dx, 3.35, -3.3); pj.add(flame);
      });
      const pjLight = new THREE.PointLight('#ffaa44', 0.85, 12, 1.6);
      pjLight.position.set(0, 4.2, -3.2); pj.add(pjLight);
      const prayerRug = new THREE.Mesh(new THREE.PlaneGeometry(5.0, 4.5), terraFabric);
      prayerRug.rotation.x = -Math.PI / 2; prayerRug.position.set(0, 0.03, 0.5); pj.add(prayerRug);
      addDownlights(pj, [[-2.8, -1.5], [2.8, -1.5], [-2.8, 2.5], [2.8, 2.5]]);
      furnitureGroup.add(pj);

      // ── 6. DINING ROOM ──
      const dn = new THREE.Group();
      dn.position.set(6.9, 0, 41.2);
      const dt = new THREE.Mesh(new THREE.BoxGeometry(4.4, 0.25, 8.4), oakMat);
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
          const seat = new THREE.Mesh(new THREE.BoxGeometry(1.5, 0.22, 1.5), creamFabric);
          seat.position.set(0, 1.55, 0); seat.castShadow = true; ch.add(seat);
          const back = new THREE.Mesh(new THREE.BoxGeometry(1.5, 1.6, 0.22), creamFabric);
          back.position.set(0, 2.4, -0.65); back.rotation.x = -0.1; back.castShadow = true; ch.add(back);
          [[-0.6, -0.6], [0.6, -0.6], [-0.6, 0.6], [0.6, 0.6]].forEach(([lx, lz]) => {
            const leg = new THREE.Mesh(new THREE.CylinderGeometry(0.06, 0.04, 1.5, 8), walnutMat);
            leg.position.set(lx, 0.75, lz); ch.add(leg);
          });
          dn.add(ch);
        });
      });
      // Sideboard / Crockery Unit on West Wall
      const sideb = new THREE.Mesh(new THREE.BoxGeometry(1.6, 2.8, 6.2), walnutMat);
      sideb.position.set(-5.2, 1.4, 0); sideb.castShadow = true; dn.add(sideb);
      addFramedArt(dn, -5.9, 5.5, 0, 4.0, 2.5, Math.PI / 2, '#d4af37');
      // Linear Brass & Opal Globe Chandelier
      const chBar = new THREE.Mesh(new THREE.CylinderGeometry(0.05, 0.05, 6.2, 10), brassMat);
      chBar.rotation.x = Math.PI / 2; chBar.position.set(0, 7.6, 0); dn.add(chBar);
      [-2.4, 2.4].forEach(sz => {
        const sRod = new THREE.Mesh(new THREE.CylinderGeometry(0.03, 0.03, 2.4, 8), brassMat);
        sRod.position.set(0, 8.8, sz); dn.add(sRod);
      });
      [-2.5, -0.8, 0.8, 2.5].forEach(gz => {
        const globe = new THREE.Mesh(new THREE.SphereGeometry(0.26, 14, 14), glowWarmMat);
        globe.position.set(0, 7.35, gz); dn.add(globe);
      });
      const dnLight = new THREE.PointLight('#ffdca8', 0.8, 16, 1.6);
      dnLight.position.set(0, 7.2, 0); dn.add(dnLight);
      addTrayCeiling(dn, 11.2, 10.2);
      addDownlights(dn, [[-3.5, -3.5], [3.5, -3.5], [-3.5, 3.5], [3.5, 3.5]]);
      furnitureGroup.add(dn);

      // ── 7. LIVING HALL (Grand Pavilion, Chandelier, Fireplace, Sectional, Spiral Staircase) ──
      const lv = new THREE.Group();
      lv.position.set(30.5, 0, 36.0);
      // Monumental Hand-Hewn Limestone Fireplace Wall (North)
      const fpWall = new THREE.Mesh(new THREE.BoxGeometry(13.5, 9.8, 1.6), stoneMat);
      fpWall.position.set(0, 4.9, -12.0); fpWall.castShadow = true; fpWall.receiveShadow = true; lv.add(fpWall);
      // Recessed Fireplace Box & Glowing Ribbon Flame
      const fpCav = new THREE.Mesh(new THREE.BoxGeometry(6.2, 1.6, 0.45), metalMat);
      fpCav.position.set(0, 2.1, -11.08); lv.add(fpCav);
      const fpFlame = new THREE.Mesh(new THREE.BoxGeometry(5.2, 0.35, 0.2), new THREE.MeshStandardMaterial({ color: '#ff9e2c', emissive: '#ff6b00', emissiveIntensity: 2.2 }));
      fpFlame.position.set(0, 1.6, -10.95); lv.add(fpFlame);
      const fpLight = new THREE.PointLight('#ff8822', 0.9, 14, 1.7);
      fpLight.position.set(0, 2.2, -10.2); lv.add(fpLight);
      // Walnut Mantel & Art above Fireplace
      const mantel = new THREE.Mesh(new THREE.BoxGeometry(7.5, 0.25, 0.9), walnutMat);
      mantel.position.set(0, 3.6, -10.9); lv.add(mantel);
      addFramedArt(lv, 0, 6.2, -11.1, 5.0, 3.2, 0, '#a85a44');
      // Hearth Bench
      const hearth = new THREE.Mesh(new THREE.BoxGeometry(15.5, 0.85, 2.4), calaMat);
      hearth.position.set(0, 0.42, -10.6); hearth.receiveShadow = true; lv.add(hearth);

      // Plush Area Rug
      const lvRug = new THREE.Mesh(new THREE.PlaneGeometry(18.5, 17.5), rugMat);
      lvRug.rotation.x = -Math.PI / 2; lvRug.position.set(-0.5, 0.03, -0.5); lvRug.receiveShadow = true; lv.add(lvRug);

      // Sculpted L-Shaped Sectional Sofa (main run + chaise return + cushions + throw pillows)
      addSofa(lv, 0.5, 4.2, 14.0, 3.6, Math.PI, creamFabric, [sageFabric, terraFabric, ochreFabric]);
      addSofa(lv, -5.2, -1.8, 8.2, 3.4, Math.PI / 2, creamFabric, [ochreFabric, sageFabric]);

      // 2 Accent Lounge Armchairs & Side Table
      addArmchair(lv, 6.8, -3.0, -Math.PI * 0.65, sageFabric);
      addArmchair(lv, 6.8, 1.5, -Math.PI * 0.45, greyFabric);
      const sideTbl = new THREE.Mesh(new THREE.CylinderGeometry(0.95, 0.95, 1.65, 20), marbleMat);
      sideTbl.position.set(7.5, 0.82, -0.8); sideTbl.castShadow = true; lv.add(sideTbl);

      // Twin Nesting Coffee Tables (Calacatta Marble + Brass Base + Decor)
      const ctBase1 = new THREE.Mesh(new THREE.CylinderGeometry(1.9, 1.9, 1.0, 28), walnutMat);
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
      lvVase.position.set(0.4, 1.58, -1.9); lv.add(lvVase);

      // Flos Arco Arched Brass & Black Marble Floor Lamp
      addFloorLamp(lv, -7.8, 5.2, -0.6);

      // Potted 7' Fiddle-Leaf Fig & Corner Palm
      addPlant(lv, -9.8, -8.5, 1.35);
      addPlant(lv, 11.2, 7.2, 1.15);

      // Window Curtains on East Wall
      addCurtains(lv, 16.5, 5.2, -1.5, 9.5, 6.5, -Math.PI / 2);

      // East Corner Spiral Staircase (with handrail & vertical balusters)
      const stairGroup = new THREE.Group();
      stairGroup.position.set(13.2, 0, -8.5);
      const pole = new THREE.Mesh(new THREE.CylinderGeometry(0.32, 0.32, 10.0, 18), metalMat);
      pole.position.y = 5.0; stairGroup.add(pole);
      const numSteps = 16;
      const railPts = [];
      for (let s = 0; s < numSteps; s++) {
        const ang = (s / numSteps) * Math.PI * 1.8;
        const sy = (s / numSteps) * 9.5;
        const tread = new THREE.Mesh(new THREE.BoxGeometry(3.2, 0.18, 0.85), oakMat);
        tread.position.set(Math.cos(ang) * 1.6, sy + 0.2, Math.sin(ang) * 1.6);
        tread.rotation.y = -ang;
        tread.castShadow = true;
        stairGroup.add(tread);
        const bal = new THREE.Mesh(new THREE.CylinderGeometry(0.035, 0.035, 2.8, 8), metalMat);
        const bx = Math.cos(ang) * 3.0, bz = Math.sin(ang) * 3.0;
        bal.position.set(bx, sy + 1.6, bz);
        stairGroup.add(bal);
        railPts.push(new THREE.Vector3(bx, sy + 3.0, bz));
      }
      const railCurve = new THREE.CatmullRomCurve3(railPts);
      const railMesh = new THREE.Mesh(new THREE.TubeGeometry(railCurve, 32, 0.07, 8, false), brassMat);
      stairGroup.add(railMesh);
      lv.add(stairGroup);

      // Living Hall Tray Ceiling, 2-Tier Brass Chandelier & 6 Recessed Downlights
      addTrayCeiling(lv, 31.0, 23.0);
      addChandelier(lv, 0, -1.5, 2.8, 10);
      addDownlights(lv, [[-10, -8], [0, -8], [10, -8], [-10, 6], [0, 6], [10, 6]]);
      furnitureGroup.add(lv);

''' + kitchen_block + '''

      // ── 9. DRAWING HALL (Formal Lounge with Chandelier, Sofa, Media Unit & Marble Wall) ──
      const dw = new THREE.Group();
      dw.position.set(36.3, 0, 62.5);
      // Nero Marquina Dark Marble Focal Accent Wall
      const dwWall = new THREE.Mesh(new THREE.BoxGeometry(20.0, 9.8, 0.4), marbleMat);
      dwWall.position.set(0, 4.9, -10.8); dwWall.castShadow = true; dwWall.receiveShadow = true; dw.add(dwWall);
      // Center 3-Pane Window with Venetian Blinds & Curtains
      const dWin = new THREE.Mesh(new THREE.BoxGeometry(7.5, 3.8, 0.2), ceramicMat);
      dWin.position.set(0, 5.5, -10.5); dw.add(dWin);
      const dBlinds = new THREE.Mesh(new THREE.BoxGeometry(7.4, 2.2, 0.1), metalMat);
      dBlinds.position.set(0, 6.2, -10.3); dw.add(dBlinds);
      addCurtains(dw, 0, 5.5, -10.2, 8.2, 5.8, 0);
      // Plush Area Rug
      const dwRug = new THREE.Mesh(new THREE.PlaneGeometry(14.5, 12.5), rugMat);
      dwRug.rotation.x = -Math.PI / 2; dwRug.position.set(0, 0.03, -2.5); dwRug.receiveShadow = true; dw.add(dwRug);
      // Sculpted Cream 3-Seater Sofa
      addSofa(dw, 0, -6.0, 9.2, 3.4, 0, creamFabric, [terraFabric, ochreFabric]);
      // Low Walnut Coffee Table with Books & Vase
      const dwTable = new THREE.Mesh(new THREE.BoxGeometry(4.4, 0.25, 2.6), oakMat);
      dwTable.position.set(0, 1.25, -1.8); dwTable.castShadow = true; dw.add(dwTable);
      [[-1.8, -1.0], [1.8, -1.0], [-1.8, 1.0], [1.8, 1.0]].forEach(([lx, lz]) => {
        const leg = new THREE.Mesh(new THREE.CylinderGeometry(0.05, 0.04, 1.2, 8), metalMat);
        leg.position.set(lx, 0.6, -1.8 + lz); dw.add(leg);
      });
      const dwVase = new THREE.Mesh(new THREE.CylinderGeometry(0.2, 0.3, 0.75, 14), ceramicMat);
      dwVase.position.set(-0.6, 1.75, -1.8); dw.add(dwVase);
      // Left Armchair & Right Chaise
      addArmchair(dw, -6.2, -2.2, 0.55, greyFabric);
      addSofa(dw, 6.2, -2.2, 4.8, 3.0, -0.55, darkFabric, [ochreFabric]);
      // Fluted Oak TV Media Console on South/Side Wall
      const dwConsole = new THREE.Mesh(new THREE.BoxGeometry(8.0, 1.4, 1.5), oakMat);
      dwConsole.position.set(0, 0.7, 8.8); dwConsole.castShadow = true; dw.add(dwConsole);
      const dwTV = new THREE.Mesh(new THREE.BoxGeometry(6.2, 3.4, 0.12), metalMat);
      dwTV.position.set(0, 4.3, 9.5); dw.add(dwTV);
      addFloorLamp(dw, -6.5, -6.8, 0.4);
      addPlant(dw, 7.8, -8.2, 1.15);
      addTrayCeiling(dw, 20.0, 20.0);
      addChandelier(dw, 0, -2.5, 2.2, 8);
      addDownlights(dw, [[-6.5, -7.5], [6.5, -7.5], [-6.5, 4.5], [6.5, 4.5]]);
      furnitureGroup.add(dw);

      // ── 10. WET KITCHEN & STORE ROOM ──
      const wk = new THREE.Group();
      wk.position.set(8.8, 0, 78.8);
      const wkCounter = new THREE.Mesh(new THREE.BoxGeometry(13.5, 2.7, 2.2), greyFabric);
      wkCounter.position.set(0, 1.35, -3.2); wkCounter.castShadow = true; wk.add(wkCounter);
      const wkTop = new THREE.Mesh(new THREE.BoxGeometry(13.7, 0.18, 2.4), marbleMat);
      wkTop.position.set(0, 2.79, -3.2); wk.add(wkTop);
      const wkWash = new THREE.Mesh(new THREE.BoxGeometry(2.2, 2.7, 2.2), ceramicMat);
      wkWash.position.set(4.5, 1.35, -3.2); wk.add(wkWash);
      const wkUp = new THREE.Mesh(new THREE.BoxGeometry(9.0, 2.2, 1.2), oakMat);
      wkUp.position.set(-2.0, 5.5, -3.7); wk.add(wkUp);
      addDownlights(wk, [[-4.0, 0], [0, 0], [4.0, 0]], true);
      furnitureGroup.add(wk);

      const st_rm = new THREE.Group();
      st_rm.position.set(4.9, 0, 49.3);
      for (let s = 1; s <= 4; s++) {
        const sh = new THREE.Mesh(new THREE.BoxGeometry(6.8, 0.1, 1.4), oakMat);
        sh.position.set(0, s * 1.6, -1.2); st_rm.add(sh);
      }
      addDownlights(st_rm, [[0, 0]], true);
      furnitureGroup.add(st_rm);

      // ── 11. SITOUT (Covered Veranda with Cane Lounge, Tea Table, Palms & Ceiling Fan) ──
      const st = new THREE.Group();
      st.position.set(32.3, 0, 78.0);
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
        st.add(cGroup);
      });
      const rTab = new THREE.Mesh(new THREE.CylinderGeometry(1.5, 1.5, 0.14, 24), oakMat);
      rTab.position.set(0, 1.45, 0); rTab.castShadow = true; st.add(rTab);
      const rLeg = new THREE.Mesh(new THREE.CylinderGeometry(0.45, 0.65, 1.4, 16), metalMat);
      rLeg.position.set(0, 0.7, 0); st.add(rLeg);
      addPlant(st, -11.5, -1.5, 1.1);
      addPlant(st, 11.5, -1.5, 1.1);
      addCeilingFan(st, 0, 0, oakMat);
      addDownlights(st, [[-7, 0], [7, 0]]);
      furnitureGroup.add(st);
    }

'''

code = code[:furn_start] + new_furniture_code + code[furn_end:]

with open(index_path, 'w', encoding='utf-8') as f:
    f.write(code)

print("Successfully upgraded lighting, materials, ceiling fixtures, and furniture across all rooms!")

