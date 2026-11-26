index_path = '/Users/puspharaj/Documents/Projects/ai-interior-designer/index.html'

with open(index_path, 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Replace .action-select CSS with Customize Panel + Corner Pill Group CSS
old_select_css = '''    .action-select {
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
      max-width: 185px;
      text-overflow: ellipsis;
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

new_panel_css = '''    .customize-btn {
      background: linear-gradient(135deg, rgba(56, 189, 248, 0.22), rgba(37, 99, 235, 0.22));
      border: 1px solid rgba(56, 189, 248, 0.5);
      color: #e0f2fe;
      font-weight: 700;
    }
    .customize-btn:hover, .customize-btn.active {
      background: #38bdf8;
      color: #090d16;
      border-color: #38bdf8;
      box-shadow: 0 0 14px rgba(56, 189, 248, 0.45);
    }

    /* 4-Corner Viewpoint Group */
    .corner-group {
      display: flex;
      align-items: center;
      gap: 3px;
      background: rgba(255, 255, 255, 0.04);
      border: 1px solid rgba(255, 255, 255, 0.1);
      border-radius: 12px;
      padding: 2px 6px;
    }
    .corner-label {
      font-size: 9.5px;
      font-weight: 800;
      letter-spacing: 0.06em;
      color: #64748b;
      padding: 0 4px;
    }
    .corner-btn {
      background: transparent;
      border: 1px solid transparent;
      color: #cbd5e1;
      font-size: 11px;
      font-weight: 600;
      padding: 3px 7px;
      border-radius: 8px;
      cursor: pointer;
      transition: all 0.15s ease;
    }
    .corner-btn:hover {
      background: rgba(255, 255, 255, 0.1);
      color: #ffffff;
    }
    .corner-btn.active {
      background: #38bdf8;
      color: #090d16;
      font-weight: 700;
    }

    /* Floating Customize Studio Panel */
    .customize-panel {
      position: absolute;
      top: 58px;
      right: 18px;
      width: 356px;
      max-width: calc(100vw - 36px);
      max-height: calc(100vh - 155px);
      background: rgba(13, 20, 36, 0.94);
      backdrop-filter: blur(22px);
      -webkit-backdrop-filter: blur(22px);
      border: 1px solid rgba(255, 255, 255, 0.14);
      border-radius: 16px;
      padding: 14px 16px;
      color: #f1f5f9;
      z-index: 30;
      box-shadow: 0 20px 44px rgba(0, 0, 0, 0.72);
      display: none;
      flex-direction: column;
      gap: 12px;
      animation: cardFadeIn 0.22s cubic-bezier(0.16, 1, 0.3, 1);
    }
    .customize-panel.visible {
      display: flex;
    }
    .customize-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    .customize-title {
      font-size: 15px;
      font-weight: 700;
      font-family: 'Space Grotesk', sans-serif;
      color: #ffffff;
      display: flex;
      align-items: center;
      gap: 7px;
    }
    .customize-tabs {
      display: flex;
      gap: 6px;
      background: rgba(255, 255, 255, 0.04);
      padding: 4px;
      border-radius: 10px;
      border: 1px solid rgba(255, 255, 255, 0.08);
    }
    .cust-tab {
      flex: 1;
      background: transparent;
      border: none;
      color: #94a3b8;
      font-size: 11.5px;
      font-weight: 600;
      padding: 6px 8px;
      border-radius: 7px;
      cursor: pointer;
      transition: all 0.18s ease;
    }
    .cust-tab:hover {
      color: #ffffff;
    }
    .cust-tab.active {
      background: #38bdf8;
      color: #090d16;
      font-weight: 700;
    }
    .customize-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 10px;
      overflow-y: auto;
      padding-right: 2px;
    }
    .customize-grid::-webkit-scrollbar {
      width: 4px;
    }
    .customize-grid::-webkit-scrollbar-thumb {
      background: rgba(56, 189, 248, 0.35);
      border-radius: 4px;
    }
    .option-card {
      background: rgba(255, 255, 255, 0.04);
      border: 1px solid rgba(255, 255, 255, 0.1);
      border-radius: 11px;
      padding: 8px;
      cursor: pointer;
      display: flex;
      flex-direction: column;
      gap: 6px;
      transition: all 0.18s ease;
      position: relative;
      text-align: left;
    }
    .option-card:hover {
      background: rgba(255, 255, 255, 0.08);
      border-color: rgba(56, 189, 248, 0.45);
      transform: translateY(-1px);
    }
    .option-card.active {
      background: rgba(56, 189, 248, 0.14);
      border-color: #38bdf8;
      box-shadow: 0 0 14px rgba(56, 189, 248, 0.25);
    }
    .option-thumb {
      width: 100%;
      height: 66px;
      border-radius: 7px;
      background: #080d18;
      border: 1px solid rgba(255, 255, 255, 0.07);
      display: flex;
      align-items: center;
      justify-content: center;
      overflow: hidden;
    }
    .option-ai-badge {
      position: absolute;
      top: 12px;
      right: 12px;
      background: rgba(245, 158, 11, 0.92);
      color: #090d16;
      font-size: 9px;
      font-weight: 800;
      padding: 2px 6px;
      border-radius: 6px;
      letter-spacing: 0.03em;
    }
    .option-name {
      font-size: 11.5px;
      font-weight: 600;
      color: #e2e8f0;
      line-height: 1.28;
    }
    .option-card.active .option-name {
      color: #ffffff;
    }'''

assert old_select_css in code, "old_select_css not found"
code = code.replace(old_select_css, new_panel_css, 1)

# 2. Replace the 3 <select> elements in #room-actions-row with 4-Corner Group + Customize Button + Panel HTML
old_actions_selects = '''      <select id="ceiling-light-select" class="action-select" onchange="changeCeilingLight(this.value)" title="AI-Recommended Ceiling Lights"></select>
      <select id="focus-light-select" class="action-select" onchange="changeFocusLight(this.value)" title="AI-Recommended Focus Lights"></select>
      <select id="furniture-style-select" class="action-select" onchange="changeFurnitureStyle(this.value)" title="AI-Recommended Furniture Styles"></select>'''

new_actions_html = '''      <div class="corner-group" title="Stand at any of the 4 corners of the room">
        <span class="corner-label">CORNERS</span>
        <button class="corner-btn" id="corner-nw" onclick="goToCorner('nw')">NW</button>
        <button class="corner-btn" id="corner-ne" onclick="goToCorner('ne')">NE</button>
        <button class="corner-btn" id="corner-sw" onclick="goToCorner('sw')">SW</button>
        <button class="corner-btn" id="corner-se" onclick="goToCorner('se')">SE</button>
      </div>
      <button class="action-pill customize-btn" id="btn-customize" onclick="toggleCustomizePanel()">✦ Customize</button>'''

assert old_actions_selects in code, "old_actions_selects not found"
code = code.replace(old_actions_selects, new_actions_html, 1)

panel_html_anchor = '  <div id="labels-container"'
customize_panel_html = '''  <!-- FLOATING CUSTOMIZE STUDIO PANEL (Visual Cards with Preview Thumbnails) -->
  <div class="customize-panel" id="customize-panel">
    <div class="customize-header">
      <div class="customize-title">
        <span style="color:#38bdf8;">✦</span>
        <span id="customize-room-title">Customize Room</span>
      </div>
      <button class="card-icon-btn" onclick="toggleCustomizePanel()" title="Close Customize Panel">
        <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><path d="M18 6L6 18M6 6l12 12"/></svg>
      </button>
    </div>
    <div class="customize-tabs">
      <button class="cust-tab active" id="tab-ceiling" onclick="switchCustomizeTab('ceiling')">Ceiling Lights</button>
      <button class="cust-tab" id="tab-focus" onclick="switchCustomizeTab('focus')">Focus Lights</button>
      <button class="cust-tab" id="tab-furniture" onclick="switchCustomizeTab('furniture')">Furniture</button>
    </div>
    <div class="customize-grid" id="customize-grid"></div>
  </div>

'''
assert panel_html_anchor in code, "panel_html_anchor not found"
code = code.replace(panel_html_anchor, customize_panel_html + panel_html_anchor, 1)

# 3. Add drum_trio & crystal_ring to createCeilingFixtureMesh + expanded AI_ROOM_RECOMMENDATIONS + SVG Thumbnails + Customize Panel & Corner logic
old_ceil_labels = '''    const CEILING_LIGHT_LABELS = {
      chandelier: 'Brass Ring Chandelier',
      linear: 'Linear Opal Globe Pendant',
      sputnik: 'Modern Sputnik Starburst',
      pendant: 'Trio Brushed Brass Dome Pendants',
      fan: 'Walnut & Brass Ceiling Fan with Light',
      flush: 'Minimalist Flush LED Halo Panel'
    };'''

new_ceil_labels = '''    const CEILING_LIGHT_LABELS = {
      chandelier: '3-Tier Brass Halo Chandelier',
      drum_trio: 'Trio Cream Drum Pendants',
      crystal_ring: 'Crystal & Gold Ring Chandelier',
      linear: 'Linear Opal Globe Pendant',
      sputnik: 'Modern Sputnik Starburst',
      pendant: 'Trio Brass Dome Pendants',
      fan: 'Walnut & Brass Ceiling Fan',
      flush: 'Minimalist Flush LED Halo'
    };'''

assert old_ceil_labels in code, "old_ceil_labels not found"
code = code.replace(old_ceil_labels, new_ceil_labels, 1)

# Add drum_trio and crystal_ring 3D geometry in createCeilingFixtureMesh
old_flush_branch = '''      } else {
        // flush LED halo'''

new_extra_ceil_branches = '''      } else if (style === 'drum_trio') {
        const drumMat = new THREE.MeshStandardMaterial({ color: '#f3efe6', roughness: 0.75, side: THREE.DoubleSide });
        [-2.4, 0, 2.4].forEach(px => {
          const rod = new THREE.Mesh(new THREE.CylinderGeometry(0.025, 0.025, 2.4, 8), darkMetal);
          rod.position.set(px, 8.8, 0); g.add(rod);
          const shade = new THREE.Mesh(new THREE.CylinderGeometry(0.75, 0.75, 0.72, 24, 1, true), drumMat);
          shade.position.set(px, 7.3, 0); g.add(shade);
          const diff = new THREE.Mesh(new THREE.CircleGeometry(0.72, 24), glowWarm);
          diff.rotation.x = Math.PI / 2; diff.position.set(px, 7.05, 0); g.add(diff);
        });
        const pt = new THREE.PointLight('#ffe8c8', 0.9, 18, 1.6);
        pt.position.set(0, 7.0, 0); g.add(pt);
      } else if (style === 'crystal_ring') {
        const canopy = new THREE.Mesh(new THREE.CylinderGeometry(0.4, 0.4, 0.1, 20), brass);
        canopy.position.set(0, 9.95, 0); g.add(canopy);
        [0, 2.1, 4.2].forEach(a => {
          const cable = new THREE.Mesh(new THREE.CylinderGeometry(0.015, 0.015, 2.2, 6), darkMetal);
          cable.position.set(Math.cos(a) * 1.9, 8.85, Math.sin(a) * 1.9); g.add(cable);
        });
        const ring = new THREE.Mesh(new THREE.TorusGeometry(1.9, 0.08, 12, 40), brass);
        ring.rotation.x = Math.PI / 2; ring.position.set(0, 7.75, 0); g.add(ring);
        const crysMat = new THREE.MeshStandardMaterial({ color: '#ffffff', emissive: '#fff0d4', emissiveIntensity: 1.2, roughness: 0.1 });
        for (let i = 0; i < 16; i++) {
          const a = (i / 16) * Math.PI * 2;
          const prism = new THREE.Mesh(new THREE.OctahedronGeometry(0.16, 0), crysMat);
          prism.scale.set(0.7, 1.6, 0.7);
          prism.position.set(Math.cos(a) * 1.9, 7.52, Math.sin(a) * 1.9); g.add(prism);
        }
        const pt = new THREE.PointLight('#fff0d4', 1.0, 22, 1.5);
        pt.position.set(0, 7.4, 0); g.add(pt);
      } else {
        // flush LED halo'''

assert old_flush_branch in code, "old_flush_branch not found"
code = code.replace(old_flush_branch, new_extra_ceil_branches, 1)

# Add extra options in AI_ROOM_RECOMMENDATIONS for Living Hall, Drawing Hall, Dining, Kitchen
code = code.replace(
    "          { id: 'fan', label: 'Ceiling: Walnut Ceiling Fan' }\n        ],\n        focus: [",
    "          { id: 'crystal_ring', label: 'Ceiling: Crystal & Gold Ring' },\n          { id: 'drum_trio', label: 'Ceiling: Trio Cream Drum Pendants' },\n          { id: 'fan', label: 'Ceiling: Walnut Ceiling Fan' }\n        ],\n        focus: ["
)
code = code.replace(
    "          { id: 'pendant', label: 'Ceiling: Trio Dome Pendants' }\n        ],\n        focus: [\n          { id: 'warm_recessed', label: '★ AI Focus: 2700K Dining Wash Spots' }",
    "          { id: 'drum_trio', label: 'Ceiling: Trio Cream Drum Pendants' },\n          { id: 'pendant', label: 'Ceiling: Trio Dome Pendants' },\n          { id: 'crystal_ring', label: 'Ceiling: Crystal & Gold Ring' }\n        ],\n        focus: [\n          { id: 'warm_recessed', label: '★ AI Focus: 2700K Dining Wash Spots' }"
)
code = code.replace(
    "          { id: 'lv_curved', label: 'Sofa: U-Shape Bouclé Lounge + Ottomans' }\n        ]",
    "          { id: 'lv_curved', label: 'Sofa: U-Shape Bouclé Lounge + Ottomans' },\n          { id: 'lv_modular', label: 'Sofa: Modular Pit Sofa + Travertine Plinth' }\n        ]"
)
code = code.replace(
    "          { id: 'dw_sectional', label: 'Sofa: Executive Charcoal L-Sectional' }\n        ]",
    "          { id: 'dw_sectional', label: 'Sofa: Executive Charcoal L-Sectional' },\n          { id: 'dw_boucle', label: 'Sofa: Curved Bouclé + Twin Chairs' }\n        ]"
)

# Add lv_modular & dw_boucle builders
code = code.replace(
    "        } else if (presetId === 'lv_curved') {",
    '''        } else if (presetId === 'lv_modular') {
          const modMat = new THREE.MeshStandardMaterial({ color: '#6b8299', roughness: 0.85 });
          addSofa(slot, 0, 4.5, 14.5, 4.2, Math.PI, modMat, [terraFabric, creamFabric]);
          addSofa(slot, -5.8, -1.5, 8.8, 3.8, Math.PI / 2, modMat, [ochreFabric]);
          addArmchair(slot, 6.8, -1.5, -Math.PI * 0.55, creamFabric);
          const plinth = new THREE.Mesh(new THREE.BoxGeometry(5.2, 0.85, 3.4), calaMat);
          plinth.position.set(0, 0.42, -1.2); plinth.castShadow = true; slot.add(plinth);
        } else if (presetId === 'lv_curved') {'''
)
code = code.replace(
    "        } else if (presetId === 'dw_sectional') {",
    '''        } else if (presetId === 'dw_boucle') {
          addSofa(slot, 0, -5.8, 10.0, 3.5, 0, creamFabric, [sageFabric, terraFabric]);
          addArmchair(slot, -5.8, -1.8, 0.6, sageFabric);
          addArmchair(slot, 5.8, -1.8, -0.6, sageFabric);
          const rTbl = new THREE.Mesh(new THREE.CylinderGeometry(1.9, 1.9, 0.16, 28), ceramicMat);
          rTbl.position.set(0, 1.25, -2.0); rTbl.castShadow = true; slot.add(rTbl);
          const rLeg = new THREE.Mesh(new THREE.CylinderGeometry(0.7, 0.9, 1.15, 20), brassMat);
          rLeg.position.set(0, 0.58, -2.0); slot.add(rLeg);
        } else if (presetId === 'dw_sectional') {'''
)

# 4. Add SVG Thumbnail Preview generator, Customize Panel controller, and goToCorner()
old_enter_sync = '''      const recs = getRecommendationsForRoom(roomId);
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

new_enter_sync = '''      document.querySelectorAll('.corner-btn').forEach(b => b.classList.remove('active'));
      const custTitle = document.getElementById('customize-room-title');
      if (custTitle) custTitle.textContent = `Customize ${room.short || room.name}`;
      if (isCustomizeOpen) renderCustomizeGrid();
      updateRoomInfoCardLighting();'''

assert old_enter_sync in code, "old_enter_sync not found"
code = code.replace(old_enter_sync, new_enter_sync, 1)

# Hide customize panel on exitRoom
old_exit = "      const actRow = document.getElementById('room-actions-row');\n      if (actRow) actRow.style.display = 'none';"
new_exit = '''      const actRow = document.getElementById('room-actions-row');
      if (actRow) actRow.style.display = 'none';
      isCustomizeOpen = false;
      const cp = document.getElementById('customize-panel');
      if (cp) cp.classList.remove('visible');
      const cb = document.getElementById('btn-customize');
      if (cb) cb.classList.remove('active');'''
assert old_exit in code, "old_exit not found"
code = code.replace(old_exit, new_exit, 1)

# Add Customize panel & 4-corner logic right before function enterRoom
cust_logic_anchor = '    function enterRoom(roomId, immediate = false) {'
cust_logic_js = '''    let isCustomizeOpen = false;
    let activeCustomizeTab = 'ceiling';

    function toggleCustomizePanel() {
      isCustomizeOpen = !isCustomizeOpen;
      const panel = document.getElementById('customize-panel');
      const btn = document.getElementById('btn-customize');
      if (panel) panel.classList.toggle('visible', isCustomizeOpen);
      if (btn) btn.classList.toggle('active', isCustomizeOpen);
      if (isCustomizeOpen) renderCustomizeGrid();
    }

    function switchCustomizeTab(tab) {
      activeCustomizeTab = tab;
      ['ceiling', 'focus', 'furniture'].forEach(t => {
        const el = document.getElementById(`tab-${t}`);
        if (el) el.classList.toggle('active', t === tab);
      });
      renderCustomizeGrid();
    }

    function getOptionThumbnailSVG(tab, id) {
      if (tab === 'ceiling') {
        if (id === 'chandelier') return `<svg viewBox="0 0 120 66" width="100%" height="100%"><line x1="60" y1="0" x2="60" y2="12" stroke="#d4af37" stroke-width="2"/><ellipse cx="60" cy="24" rx="34" ry="8" fill="none" stroke="#d4af37" stroke-width="3"/><ellipse cx="60" cy="26" rx="33" ry="7" fill="none" stroke="#fff3c4" stroke-width="1.5"/><ellipse cx="63" cy="37" rx="23" ry="6" fill="none" stroke="#d4af37" stroke-width="2.5"/><ellipse cx="57" cy="48" rx="14" ry="4" fill="none" stroke="#d4af37" stroke-width="2"/></svg>`;
        if (id === 'crystal_ring') return `<svg viewBox="0 0 120 66" width="100%" height="100%"><line x1="35" y1="0" x2="35" y2="26" stroke="#94a3b8" stroke-width="1"/><line x1="85" y1="0" x2="85" y2="26" stroke="#94a3b8" stroke-width="1"/><ellipse cx="60" cy="26" rx="30" ry="7" fill="none" stroke="#d4af37" stroke-width="3"/><path d="M34 32 L38 44 L42 32 M48 34 L52 46 L56 34 M62 34 L66 46 L70 34 M76 32 L80 44 L84 32" stroke="#fef08a" stroke-width="2" fill="none"/></svg>`;
        if (id === 'drum_trio') return `<svg viewBox="0 0 120 66" width="100%" height="100%"><line x1="30" y1="0" x2="30" y2="24" stroke="#94a3b8" stroke-width="1.5"/><line x1="60" y1="0" x2="60" y2="24" stroke="#94a3b8" stroke-width="1.5"/><line x1="90" y1="0" x2="90" y2="24" stroke="#94a3b8" stroke-width="1.5"/><rect x="20" y="24" width="20" height="16" rx="2" fill="#f3efe6"/><rect x="50" y="24" width="20" height="16" rx="2" fill="#f3efe6"/><rect x="80" y="24" width="20" height="16" rx="2" fill="#f3efe6"/></svg>`;
        if (id === 'sputnik') return `<svg viewBox="0 0 120 66" width="100%" height="100%"><line x1="60" y1="0" x2="60" y2="33" stroke="#d4af37" stroke-width="2"/><line x1="30" y1="20" x2="90" y2="46" stroke="#d4af37" stroke-width="1.5"/><line x1="30" y1="46" x2="90" y2="20" stroke="#d4af37" stroke-width="1.5"/><line x1="60" y1="12" x2="60" y2="54" stroke="#d4af37" stroke-width="1.5"/><circle cx="60" cy="33" r="5" fill="#d4af37"/><circle cx="30" cy="20" r="4" fill="#fff3c4"/><circle cx="90" cy="46" r="4" fill="#fff3c4"/><circle cx="30" cy="46" r="4" fill="#fff3c4"/><circle cx="90" cy="20" r="4" fill="#fff3c4"/><circle cx="60" cy="54" r="4" fill="#fff3c4"/></svg>`;
        if (id === 'linear') return `<svg viewBox="0 0 120 66" width="100%" height="100%"><line x1="32" y1="0" x2="32" y2="30" stroke="#d4af37" stroke-width="1.5"/><line x1="88" y1="0" x2="88" y2="30" stroke="#d4af37" stroke-width="1.5"/><line x1="20" y1="30" x2="100" y2="30" stroke="#d4af37" stroke-width="3"/><circle cx="28" cy="36" r="5" fill="#fff3c4"/><circle cx="49" cy="36" r="5" fill="#fff3c4"/><circle cx="71" cy="36" r="5" fill="#fff3c4"/><circle cx="92" cy="36" r="5" fill="#fff3c4"/></svg>`;
        if (id === 'pendant') return `<svg viewBox="0 0 120 66" width="100%" height="100%"><line x1="30" y1="0" x2="30" y2="26" stroke="#d4af37" stroke-width="1.5"/><line x1="60" y1="0" x2="60" y2="26" stroke="#d4af37" stroke-width="1.5"/><line x1="90" y1="0" x2="90" y2="26" stroke="#d4af37" stroke-width="1.5"/><path d="M18 38 A12 12 0 0 1 42 38 Z" fill="#d4af37"/><path d="M48 38 A12 12 0 0 1 72 38 Z" fill="#d4af37"/><path d="M78 38 A12 12 0 0 1 102 38 Z" fill="#d4af37"/></svg>`;
        if (id === 'fan') return `<svg viewBox="0 0 120 66" width="100%" height="100%"><line x1="60" y1="0" x2="60" y2="24" stroke="#94a3b8" stroke-width="2"/><path d="M22 28 L54 30 L54 35 L22 33 Z" fill="#8b5a2b"/><path d="M66 30 L98 28 L98 33 L66 35 Z" fill="#8b5a2b"/><circle cx="60" cy="33" r="7" fill="#d4af37"/><circle cx="60" cy="39" r="5" fill="#fff3c4"/></svg>`;
        return `<svg viewBox="0 0 120 66" width="100%" height="100%"><ellipse cx="60" cy="24" rx="28" ry="8" fill="#f1f5f9"/><ellipse cx="60" cy="26" rx="24" ry="6" fill="#fff3c4"/></svg>`;
      }
      if (tab === 'focus') {
        if (id === 'brass_track') return `<svg viewBox="0 0 120 66" width="100%" height="100%"><circle cx="35" cy="24" r="6" fill="#d4af37"/><rect x="31" y="24" width="8" height="14" rx="2" fill="#d4af37"/><polygon points="28,38 42,38 50,62 20,62" fill="rgba(255,224,150,0.22)"/><circle cx="85" cy="24" r="6" fill="#d4af37"/><rect x="81" y="24" width="8" height="14" rx="2" fill="#d4af37"/><polygon points="78,38 92,38 100,62 70,62" fill="rgba(255,224,150,0.22)"/></svg>`;
        if (id === 'gallery_pin') return `<svg viewBox="0 0 120 66" width="100%" height="100%"><ellipse cx="60" cy="18" rx="14" ry="5" fill="#334155"/><ellipse cx="60" cy="19" rx="8" ry="3" fill="#ffe4b5"/><polygon points="52,20 68,20 82,62 38,62" fill="rgba(255,216,155,0.25)"/></svg>`;
        if (id === 'task_cool') return `<svg viewBox="0 0 120 66" width="100%" height="100%"><ellipse cx="38" cy="18" rx="12" ry="4" fill="#e0f2fe"/><ellipse cx="82" cy="18" rx="12" ry="4" fill="#e0f2fe"/><polygon points="28,20 48,20 56,62 20,62" fill="rgba(224,242,254,0.2)"/><polygon points="72,20 92,20 100,62 64,62" fill="rgba(224,242,254,0.2)"/></svg>`;
        return `<svg viewBox="0 0 120 66" width="100%" height="100%"><ellipse cx="38" cy="18" rx="12" ry="4" fill="#fff3c4"/><ellipse cx="82" cy="18" rx="12" ry="4" fill="#fff3c4"/><polygon points="26,20 50,20 58,62 18,62" fill="rgba(255,232,180,0.22)"/><polygon points="70,20 94,20 102,62 62,62" fill="rgba(255,232,180,0.22)"/></svg>`;
      }
      // Furniture / Sofas preview SVG
      if (id.includes('symmetrical') || id.includes('twin')) {
        return `<svg viewBox="0 0 120 66" width="100%" height="100%"><rect x="14" y="16" width="16" height="34" rx="4" fill="#3d6352"/><rect x="90" y="16" width="16" height="34" rx="4" fill="#3d6352"/><rect x="46" y="24" width="28" height="18" rx="3" fill="#8b5a2b"/></svg>`;
      }
      if (id.includes('curved') || id.includes('boucle')) {
        return `<svg viewBox="0 0 120 66" width="100%" height="100%"><rect x="20" y="42" width="80" height="14" rx="5" fill="#475569"/><rect x="18" y="16" width="14" height="30" rx="4" fill="#e2e8f0"/><rect x="88" y="16" width="14" height="30" rx="4" fill="#e2e8f0"/><circle cx="60" cy="28" r="10" fill="#f1f5f9"/></svg>`;
      }
      if (id.includes('modular') || id.includes('sectional')) {
        return `<svg viewBox="0 0 120 66" width="100%" height="100%"><rect x="22" y="38" width="76" height="16" rx="4" fill="#6b8299"/><rect x="22" y="16" width="18" height="34" rx="4" fill="#6b8299"/><rect x="52" y="20" width="26" height="12" rx="3" fill="#e2e8f0"/></svg>`;
      }
      if (id.includes('round')) {
        return `<svg viewBox="0 0 120 66" width="100%" height="100%"><circle cx="60" cy="33" r="15" fill="#f1f5f9"/><circle cx="60" cy="12" r="4" fill="#5d7a68"/><circle cx="60" cy="54" r="4" fill="#5d7a68"/><circle cx="38" cy="22" r="4" fill="#5d7a68"/><circle cx="82" cy="22" r="4" fill="#5d7a68"/><circle cx="38" cy="44" r="4" fill="#5d7a68"/><circle cx="82" cy="44" r="4" fill="#5d7a68"/></svg>`;
      }
      if (id.includes('canopy') || id.includes('tufted') || id.includes('japandi') || id.includes('bed') || id.includes('study')) {
        return `<svg viewBox="0 0 120 66" width="100%" height="100%"><rect x="34" y="12" width="52" height="42" rx="3" fill="#5d7a68"/><rect x="34" y="12" width="52" height="10" rx="2" fill="#334155"/><rect x="40" y="18" width="18" height="8" rx="2" fill="#f1f5f9"/><rect x="62" y="18" width="18" height="8" rx="2" fill="#f1f5f9"/><rect x="18" y="14" width="12" height="12" rx="2" fill="#8b5a2b"/><rect x="90" y="14" width="12" height="12" rx="2" fill="#8b5a2b"/></svg>`;
      }
      return `<svg viewBox="0 0 120 66" width="100%" height="100%"><rect x="20" y="38" width="62" height="15" rx="4" fill="#dfd9ce"/><rect x="20" y="16" width="16" height="34" rx="4" fill="#dfd9ce"/><ellipse cx="62" cy="24" rx="14" ry="8" fill="#ffffff"/><rect x="86" y="16" width="16" height="16" rx="4" fill="#5d7a68"/></svg>`;
    }

    function renderCustomizeGrid() {
      if (!currentRoomId) return;
      const grid = document.getElementById('customize-grid');
      if (!grid) return;
      const recs = getRecommendationsForRoom(currentRoomId);
      const list = recs[activeCustomizeTab] || [];
      const currentVal = activeCustomizeTab === 'ceiling'
        ? roomCeilingFixtures[currentRoomId]?.currentStyle
        : activeCustomizeTab === 'focus'
          ? roomFocusFixtures[currentRoomId]?.currentStyle
          : roomFurnitureState[currentRoomId];

      grid.innerHTML = list.map(opt => {
        const isAI = opt.label.startsWith('★');
        const cleanTitle = opt.label.replace(/^★ AI [^:]+: /, '').replace(/^[^:]+: /, '');
        const activeCls = (opt.id === currentVal) ? 'active' : '';
        return `
          <button class="option-card ${activeCls}" onclick="selectCustomizeOption('${activeCustomizeTab}', '${opt.id}')">
            ${isAI ? '<span class="option-ai-badge">★ AI</span>' : ''}
            <div class="option-thumb">${getOptionThumbnailSVG(activeCustomizeTab, opt.id)}</div>
            <div class="option-name">${cleanTitle}</div>
          </button>
        `;
      }).join('');
    }

    function selectCustomizeOption(tab, id) {
      if (tab === 'ceiling') changeCeilingLight(id);
      else if (tab === 'focus') changeFocusLight(id);
      else changeFurnitureStyle(id);
      renderCustomizeGrid();
    }

    function goToCorner(corner) {
      if (!currentRoomId) return;
      const room = ROOMS.find(r => r.id === currentRoomId);
      if (!room) return;
      const b = room.bounds;
      const w = b.x2 - b.x1, d = b.z2 - b.z1;
      const px = Math.min(2.2, w * 0.22);
      const pz = Math.min(2.2, d * 0.22);
      const cx = (b.x1 + b.x2) / 2;
      const cz = (b.z1 + b.z2) / 2;

      let tx = cx, tz = cz;
      if (corner === 'nw') { tx = b.x1 + px; tz = b.z1 + pz; }
      else if (corner === 'ne') { tx = b.x2 - px; tz = b.z1 + pz; }
      else if (corner === 'sw') { tx = b.x1 + px; tz = b.z2 - pz; }
      else if (corner === 'se') { tx = b.x2 - px; tz = b.z2 - pz; }

      document.querySelectorAll('.corner-btn').forEach(btn => btn.classList.remove('active'));
      const activeBtn = document.getElementById(`corner-${corner}`);
      if (activeBtn) activeBtn.classList.add('active');

      // Compute current look vector so tween is seamless
      const currDir = new THREE.Vector3(
        Math.sin(camYaw) * Math.cos(camPitch),
        Math.sin(camPitch),
        Math.cos(camYaw) * Math.cos(camPitch)
      );
      animStartPos.copy(camera.position);
      animTargetPos.set(tx, 5.3, tz);
      animStartLook.copy(camera.position).add(currDir.multiplyScalar(10));
      animTargetLook.set(cx, 4.3, cz);

      const dx = cx - tx, dy = 4.3 - 5.3, dz = cz - tz;
      camYaw = Math.atan2(dx, dz);
      camPitch = Math.asin(dy / Math.hypot(dx, dy, dz));

      animStartTime = performance.now();
      animProgress = 0;
      isAnimating = true;
    }

'''

assert cust_logic_anchor in code, "cust_logic_anchor not found"
code = code.replace(cust_logic_anchor, cust_logic_js + cust_logic_anchor, 1)

with open(index_path, 'w', encoding='utf-8') as f:
    f.write(code)

print("Customize panel with visual thumbnails + 4-corner viewpoints added successfully!")

