index_path = '/Users/puspharaj/Documents/Projects/ai-interior-designer/index.html'

with open(index_path, 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Add CSS for .action-select
css_anchor = '''    .action-pill.active {
      background: #38bdf8;
      color: #090d16;
      font-weight: 700;
      border-color: #38bdf8;
      box-shadow: 0 0 12px rgba(56, 189, 248, 0.35);
    }'''

new_select_css = css_anchor + '''
    .action-select {
      background: rgba(56, 189, 248, 0.12);
      border: 1px solid rgba(56, 189, 248, 0.45);
      color: #e0f2fe;
      font-family: inherit;
      font-size: 11.5px;
      font-weight: 600;
      padding: 4px 10px;
      border-radius: 12px;
      cursor: pointer;
      outline: none;
      transition: all 0.18s ease;
    }
    .action-select:hover, .action-select:focus {
      background: rgba(56, 189, 248, 0.22);
      border-color: #38bdf8;
      color: #ffffff;
    }
    .action-select option {
      background: #0f172a;
      color: #f1f5f9;
    }'''

assert css_anchor in code, "css_anchor not found"
code = code.replace(css_anchor, new_select_css, 1)

# 2. Add <select id="ceiling-light-select"> inside #room-actions-row
html_anchor = '''      <button class="action-pill" id="action-lookaround" onclick="toggleLookAround()">Look around</button>
    </div>'''

new_select_html = '''      <button class="action-pill" id="action-lookaround" onclick="toggleLookAround()">Look around</button>
      <select id="ceiling-light-select" class="action-select" onchange="changeCeilingLight(this.value)" title="Choose Ceiling Light Fixture">
        <option value="chandelier">Ceiling: Brass Ring Chandelier</option>
        <option value="linear">Ceiling: Linear Globe Pendant</option>
        <option value="sputnik">Ceiling: Sputnik Starburst</option>
        <option value="pendant">Ceiling: Trio Dome Pendants</option>
        <option value="fan">Ceiling: Walnut Ceiling Fan</option>
        <option value="flush">Ceiling: Flush LED Halo</option>
      </select>
    </div>'''

assert html_anchor in code, "html_anchor not found"
code = code.replace(html_anchor, new_select_html, 1)

# 3. Add global roomCeilingFixtures map, factory, and switcher before buildDetailedFurniture
factory_anchor = '    // ── HIGH-REALISM SHAPED PROCEDURAL FURNITURE & CEILING LIGHTS ─────────────────'

ceiling_system_js = '''    const roomCeilingFixtures = {};
    const CEILING_LIGHT_LABELS = {
      chandelier: 'Brass Ring Chandelier',
      linear: 'Linear Opal Globe Pendant',
      sputnik: 'Modern Sputnik Starburst',
      pendant: 'Trio Brushed Brass Dome Pendants',
      fan: 'Walnut & Brass Ceiling Fan with Light',
      flush: 'Minimalist Flush LED Halo Panel'
    };

    function createCeilingFixtureMesh(style) {
      const g = new THREE.Group();
      const brass = new THREE.MeshStandardMaterial({ color: '#d4af37', metalness: 0.85, roughness: 0.24 });
      const walnut = new THREE.MeshStandardMaterial({ color: '#4a2e1b', roughness: 0.42 });
      const darkMetal = new THREE.MeshStandardMaterial({ color: '#18181b', metalness: 0.8, roughness: 0.3 });
      const ceramic = new THREE.MeshStandardMaterial({ color: '#f1efe9', roughness: 0.25 });
      const glowWarm = new THREE.MeshStandardMaterial({ color: '#fff8e7', emissive: '#ffcf87', emissiveIntensity: 1.5, roughness: 0.3 });

      if (style === 'chandelier') {
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
      } else if (style === 'linear') {
        const bar = new THREE.Mesh(new THREE.CylinderGeometry(0.05, 0.05, 6.2, 10), brass);
        bar.rotation.z = Math.PI / 2; bar.position.set(0, 7.6, 0); g.add(bar);
        [-2.4, 2.4].forEach(sx => {
          const rod = new THREE.Mesh(new THREE.CylinderGeometry(0.03, 0.03, 2.4, 8), brass);
          rod.position.set(sx, 8.8, 0); g.add(rod);
        });
        [-2.5, -0.8, 0.8, 2.5].forEach(gx => {
          const gl = new THREE.Mesh(new THREE.SphereGeometry(0.28, 14, 14), glowWarm);
          gl.position.set(gx, 7.35, 0); g.add(gl);
        });
        const pt = new THREE.PointLight('#ffdca8', 0.85, 18, 1.6);
        pt.position.set(0, 7.2, 0); g.add(pt);
      } else if (style === 'sputnik') {
        const rod = new THREE.Mesh(new THREE.CylinderGeometry(0.04, 0.04, 2.1, 10), brass);
        rod.position.set(0, 8.95, 0); g.add(rod);
        const hub = new THREE.Mesh(new THREE.SphereGeometry(0.28, 16, 16), brass);
        hub.position.set(0, 7.9, 0); g.add(hub);
        const dirs = [
          [1, 0.2, 0], [-1, 0.2, 0], [0, 0.2, 1], [0, 0.2, -1],
          [0.7, -0.35, 0.7], [-0.7, -0.35, 0.7], [0.7, -0.35, -0.7], [-0.7, -0.35, -0.7],
          [0.5, 0.5, 0.5], [-0.5, 0.5, -0.5]
        ];
        dirs.forEach(([dx, dy, dz]) => {
          const len = 1.7;
          const v = new THREE.Vector3(dx, dy, dz).normalize();
          const arm = new THREE.Mesh(new THREE.CylinderGeometry(0.025, 0.025, len, 8), brass);
          arm.position.set(v.x * len / 2, 7.9 + v.y * len / 2, v.z * len / 2);
          arm.quaternion.setFromUnitVectors(new THREE.Vector3(0, 1, 0), v);
          g.add(arm);
          const bulb = new THREE.Mesh(new THREE.SphereGeometry(0.18, 12, 12), glowWarm);
          bulb.position.set(v.x * len, 7.9 + v.y * len, v.z * len);
          g.add(bulb);
        });
        const pt = new THREE.PointLight('#ffdca8', 0.9, 18, 1.6);
        pt.position.set(0, 7.6, 0); g.add(pt);
      } else if (style === 'pendant') {
        [-2.4, 0, 2.4].forEach(px => {
          const pCan = new THREE.Mesh(new THREE.CylinderGeometry(0.22, 0.22, 0.08, 16), brass);
          pCan.position.set(px, 9.96, 0); g.add(pCan);
          const rod = new THREE.Mesh(new THREE.CylinderGeometry(0.03, 0.03, 2.6, 10), brass);
          rod.position.set(px, 8.7, 0); g.add(rod);
          const dome = new THREE.Mesh(new THREE.SphereGeometry(0.75, 22, 14, 0, Math.PI * 2, 0, Math.PI / 2), brass);
          dome.rotation.x = Math.PI; dome.position.set(px, 7.4, 0); dome.castShadow = true; g.add(dome);
          const bulb = new THREE.Mesh(new THREE.SphereGeometry(0.2, 12, 12), glowWarm);
          bulb.position.set(px, 7.45, 0); g.add(bulb);
        });
        const pt = new THREE.PointLight('#ffeedb', 0.9, 16, 1.6);
        pt.position.set(0, 7.2, 0); g.add(pt);
      } else if (style === 'fan') {
        const rod = new THREE.Mesh(new THREE.CylinderGeometry(0.06, 0.06, 1.1, 12), darkMetal);
        rod.position.set(0, 9.45, 0); g.add(rod);
        const hub = new THREE.Mesh(new THREE.CylinderGeometry(0.35, 0.35, 0.25, 20), brass);
        hub.position.set(0, 8.85, 0); g.add(hub);
        const dome = new THREE.Mesh(new THREE.SphereGeometry(0.28, 16, 12, 0, Math.PI * 2, 0, Math.PI / 2), glowWarm);
        dome.rotation.x = Math.PI; dome.position.set(0, 8.75, 0); g.add(dome);
        for (let i = 0; i < 3; i++) {
          const blade = new THREE.Mesh(new THREE.BoxGeometry(2.1, 0.04, 0.42), walnut);
          const a = (i / 3) * Math.PI * 2;
          blade.position.set(Math.cos(a) * 1.15, 8.88, Math.sin(a) * 1.15);
          blade.rotation.y = -a;
          g.add(blade);
        }
        const pt = new THREE.PointLight('#ffe8cc', 0.65, 16, 1.6);
        pt.position.set(0, 8.4, 0); g.add(pt);
      } else {
        // flush LED halo
        const ring = new THREE.Mesh(new THREE.CylinderGeometry(1.35, 1.35, 0.14, 32), ceramic);
        ring.position.set(0, 9.92, 0); g.add(ring);
        const halo = new THREE.Mesh(new THREE.CylinderGeometry(1.2, 1.2, 0.16, 32), glowWarm);
        halo.position.set(0, 9.9, 0); g.add(halo);
        const pt = new THREE.PointLight('#fff4e0', 0.75, 16, 1.6);
        pt.position.set(0, 9.4, 0); g.add(pt);
      }
      return g;
    }

    function registerRoomCeilingLight(roomId, parentGroup, x, z, defaultStyle) {
      const slot = new THREE.Group();
      slot.position.set(x, 0, z);
      parentGroup.add(slot);
      roomCeilingFixtures[roomId] = { slot, currentStyle: defaultStyle };
      setRoomCeilingLight(roomId, defaultStyle);
    }

    function setRoomCeilingLight(roomId, style) {
      const entry = roomCeilingFixtures[roomId];
      if (!entry) return;
      while (entry.slot.children.length > 0) {
        entry.slot.remove(entry.slot.children[0]);
      }
      entry.currentStyle = style;
      entry.slot.add(createCeilingFixtureMesh(style));
    }

    function changeCeilingLight(style) {
      if (!currentRoomId) return;
      setRoomCeilingLight(currentRoomId, style);
      const room = ROOMS.find(r => r.id === currentRoomId);
      if (room) {
        const lightEl = document.getElementById('card-lighting');
        const label = CEILING_LIGHT_LABELS[style] || style;
        if (lightEl) lightEl.textContent = `${label} • ${room.lighting}`;
      }
    }

'''

assert factory_anchor in code, "factory_anchor not found"
code = code.replace(factory_anchor, ceiling_system_js + factory_anchor, 1)

# 4. Replace per-room static ceiling fixtures with registerRoomCeilingLight(...)
replacements = [
    # Bed 1
    ('      addCeilingFan(b1, 0, 1.0, walnutMat);',
     "      registerRoomCeilingLight('bed1', b1, 0, 1.0, 'fan');"),
    # Bath 1, Bath 2, Bath 3 via buildBath
    ('      function buildBath(cx, cz, w, d) {',
     '      function buildBath(roomId, cx, cz, w, d) {'),
    ('        addDownlights(bt, [[0, -2.0], [0, 2.0]], true);\n        furnitureGroup.add(bt);\n      }\n      buildBath(20.4, 6.0, 6.4, 11.0);\n      buildBath(27.2, 6.0, 6.4, 11.0);\n      buildBath(21.2, 71.1, 6.8, 4.8);',
     "        registerRoomCeilingLight(roomId, bt, 0, 0, 'flush');\n        addDownlights(bt, [[0, -2.0], [0, 2.0]], true);\n        furnitureGroup.add(bt);\n      }\n      buildBath('bath1', 20.4, 6.0, 6.4, 11.0);\n      buildBath('bath2', 27.2, 6.0, 6.4, 11.0);\n      buildBath('bath3', 21.2, 71.1, 6.8, 4.8);"),
    # Dress 1 & Dress 2 via buildDress
    ('      function buildDress(cx, cz) {',
     '      function buildDress(roomId, cx, cz) {'),
    ('        addDownlights(dr, [[0, -1.5], [0, 1.5]], false);\n        furnitureGroup.add(dr);\n      }\n      buildDress(20.4, 17.5);\n      buildDress(27.2, 17.5);',
     "        registerRoomCeilingLight(roomId, dr, 0, -0.5, 'flush');\n        addDownlights(dr, [[0, -1.5], [0, 1.5]], false);\n        furnitureGroup.add(dr);\n      }\n      buildDress('dress1', 20.4, 17.5);\n      buildDress('dress2', 27.2, 17.5);"),
    # Bed 2
    ('      addCeilingFan(b2, 0, 1.5, oakMat);',
     "      registerRoomCeilingLight('bed2', b2, 0, 1.5, 'fan');"),
    # Pooja
    ('      addDownlights(pj, [[-2.8, -1.5], [2.8, -1.5], [-2.8, 2.5], [2.8, 2.5]]);',
     "      registerRoomCeilingLight('pooja', pj, 0, 0.5, 'pendant');\n      addDownlights(pj, [[-2.8, -1.5], [2.8, -1.5], [-2.8, 2.5], [2.8, 2.5]]);"),
    # Dining: replace static Linear Brass & Opal Globe Chandelier with registerRoomCeilingLight('dining', dn, 0, 0, 'linear')
    ('''      // Linear Brass & Opal Globe Chandelier
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
      dnLight.position.set(0, 7.2, 0); dn.add(dnLight);''',
     "      registerRoomCeilingLight('dining', dn, 0, 0, 'linear');"),
    # Living Hall
    ('      addChandelier(lv, 0, -1.5, 2.8, 10);',
     "      registerRoomCeilingLight('living', lv, 0, -1.5, 'chandelier');"),
    # Kitchen: replace static 3 brass dome pendants over island with registerRoomCeilingLight('kitchen', islGroup, 0, 0, 'pendant')
    ('''      // --- 4. 3 BRASS DOME PENDANT LIGHTS OVER ISLAND ---
      const pendantXs = [-2.8, 0, 2.8];
      pendantXs.forEach(px => {
        const pend = new THREE.Group();
        pend.position.set(px, 0, 0);

        // Vertical suspension rod from ceiling
        const rod = new THREE.Mesh(new THREE.CylinderGeometry(0.03, 0.03, 3.2, 12), goldBrassMat);
        rod.position.set(0, 8.4, 0);
        pend.add(rod);

        // Ceiling canopy
        const pCanopy = new THREE.Mesh(new THREE.CylinderGeometry(0.25, 0.25, 0.08, 16), goldBrassMat);
        pCanopy.position.set(0, 9.96, 0);
        pend.add(pCanopy);

        // Brass dome shade (semi-sphere)
        const dome = new THREE.Mesh(new THREE.SphereGeometry(0.85, 24, 16, 0, Math.PI * 2, 0, Math.PI / 2), goldBrassMat);
        dome.rotation.x = Math.PI;
        dome.position.set(0, 6.8, 0);
        dome.castShadow = true;
        pend.add(dome);

        // Diffuser ring rim
        const rim = new THREE.Mesh(new THREE.TorusGeometry(0.85, 0.04, 8, 24), goldBrassMat);
        rim.rotation.x = Math.PI / 2;
        rim.position.set(0, 6.8, 0);
        pend.add(rim);

        // Inside glowing bulb
        const bulb = new THREE.Mesh(new THREE.SphereGeometry(0.22, 12, 12), new THREE.MeshStandardMaterial({ color: 0xffffff, emissive: 0xffe4b5, emissiveIntensity: 1.5 }));
        bulb.position.set(0, 6.9, 0);
        pend.add(bulb);

        // Real warm pointlight casting down onto island
        const pLight = new THREE.PointLight(0xffeedb, 1.2, 14, 1.8);
        pLight.position.set(0, 6.7, 0);
        pLight.castShadow = true;
        pLight.shadow.bias = -0.002;
        pend.add(pLight);

        islGroup.add(pend);
      });''',
     "      registerRoomCeilingLight('kitchen', islGroup, 0, 0, 'pendant');"),
    # Drawing Hall
    ('      addChandelier(dw, 0, -2.5, 2.2, 8);',
     "      registerRoomCeilingLight('drawing', dw, 0, -2.5, 'sputnik');"),
    # Wet Kitchen
    ('      addDownlights(wk, [[-3.5, 0], [0, 0], [3.5, 0]], true);',
     "      registerRoomCeilingLight('wetkitchen', wk, 0, 0, 'flush');\n      addDownlights(wk, [[-3.5, 0], [0, 0], [3.5, 0]], true);"),
    # Store
    ('      addDownlights(st_rm, [[0, 0]], true);',
     "      registerRoomCeilingLight('store', st_rm, 0, 0, 'flush');\n      addDownlights(st_rm, [[0, 0]], true);"),
    # Sitout
    ('      addCeilingFan(st, 0, 0, oakMat);',
     "      registerRoomCeilingLight('sitout', st, 0, 0, 'fan');")
]

for old, new in replacements:
    assert old in code, f"Replacement target not found: {old[:60]}"
    code = code.replace(old, new, 1)

# 5. Sync #ceiling-light-select in enterRoom()
enter_anchor = "      const lightEl = document.getElementById('card-lighting');\n      if (lightEl) lightEl.textContent = room.lighting;"
enter_new = '''      const clSelect = document.getElementById('ceiling-light-select');
      const activeStyle = roomCeilingFixtures[roomId]?.currentStyle || 'chandelier';
      if (clSelect) clSelect.value = activeStyle;
      const lightEl = document.getElementById('card-lighting');
      if (lightEl) lightEl.textContent = `${CEILING_LIGHT_LABELS[activeStyle] || activeStyle} • ${room.lighting}`;'''

assert enter_anchor in code, "enter_anchor not found"
code = code.replace(enter_anchor, enter_new, 1)

with open(index_path, 'w', encoding='utf-8') as f:
    f.write(code)

print("Ceiling light selector and dynamic 3D fixture switcher added successfully!")

