index_path = '/Users/puspharaj/Documents/Projects/ai-interior-designer/index.html'

with open(index_path, 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Update body and #canvas-container CSS to flex layout so sidebars never overlap the 3D canvas
old_layout_css = '''    html, body {
      width: 100%;
      height: 100%;
      overflow: hidden;
      background: #090d16;
      font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
      color: #f1f5f9;
    }
    #canvas-container {
      width: 100%;
      height: 100%;
      position: absolute;
      top: 0;
      left: 0;
      z-index: 1;
    }'''

new_layout_css = '''    html, body {
      width: 100%;
      height: 100%;
      overflow: hidden;
      background: #090d16;
      font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
      color: #f1f5f9;
      display: flex;
      flex-direction: row;
    }
    #canvas-container {
      flex: 1;
      height: 100%;
      position: relative;
      min-width: 0;
      z-index: 1;
    }
    /* Dedicated Non-Overlapping Left Sidebar */
    .left-sidebar {
      width: 288px;
      min-width: 288px;
      height: 100%;
      background: #0b1120;
      border-right: 1px solid rgba(255, 255, 255, 0.09);
      display: flex;
      flex-direction: column;
      gap: 12px;
      padding: 14px;
      overflow-y: auto;
      z-index: 25;
      scrollbar-width: thin;
    }
    .left-sidebar::-webkit-scrollbar { width: 4px; }
    .left-sidebar::-webkit-scrollbar-thumb { background: rgba(56, 189, 248, 0.3); border-radius: 4px; }
    .sidebar-section {
      background: rgba(255, 255, 255, 0.03);
      border: 1px solid rgba(255, 255, 255, 0.08);
      border-radius: 12px;
      padding: 10px 12px;
      display: flex;
      flex-direction: column;
      gap: 8px;
    }
    .sidebar-section-title {
      font-size: 10px;
      font-weight: 800;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      color: #64748b;
    }
    .sidebar-grid {
      display: flex;
      flex-wrap: wrap;
      gap: 5px;
    }'''

assert old_layout_css in code, "old_layout_css not found"
code = code.replace(old_layout_css, new_layout_css, 1)

# 2. Update .customize-panel CSS to be a dedicated Right Sidebar column (not floating over 3D)
old_cust_panel_css = '''    /* Floating Customize Studio Panel */
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
    }'''

new_cust_panel_css = '''    /* Dedicated Non-Overlapping Right Customize Sidebar */
    .customize-panel {
      position: relative;
      width: 344px;
      min-width: 344px;
      height: 100%;
      background: #0b1120;
      border-left: 1px solid rgba(255, 255, 255, 0.09);
      padding: 14px 16px;
      color: #f1f5f9;
      z-index: 25;
      display: none;
      flex-direction: column;
      gap: 12px;
    }'''

assert old_cust_panel_css in code, "old_cust_panel_css not found"
code = code.replace(old_cust_panel_css, new_cust_panel_css, 1)

# Adjust .room-info-card, .top-right-hud, .bottom-nav-container so they live cleanly inside .left-sidebar (no floating overlay)
old_card_css = '''    .room-info-card {
      position: absolute;
      top: 18px;
      left: 18px;
      width: 340px;
      max-width: calc(100vw - 36px);
      background: rgba(13, 20, 36, 0.90);
      backdrop-filter: blur(20px);
      -webkit-backdrop-filter: blur(20px);
      border: 1px solid rgba(255, 255, 255, 0.12);
      border-radius: 14px;
      padding: 16px 18px;
      color: #f1f5f9;
      z-index: 25;
      box-shadow: 0 16px 36px rgba(0, 0, 0, 0.65);
      display: none;
      flex-direction: column;
      gap: 10px;
      transition: opacity 0.25s ease, transform 0.25s ease;
      animation: cardFadeIn 0.3s cubic-bezier(0.16, 1, 0.3, 1);
    }'''

new_card_css = '''    .room-info-card {
      width: 100%;
      background: rgba(255, 255, 255, 0.03);
      border: 1px solid rgba(255, 255, 255, 0.08);
      border-radius: 12px;
      padding: 12px;
      color: #f1f5f9;
      display: none;
      flex-direction: column;
      gap: 8px;
    }'''

assert old_card_css in code, "old_card_css not found"
code = code.replace(old_card_css, new_card_css, 1)

# Hide floating top-bar / left-floating-bar / top-right-hud overlays, and make .bottom-nav-container flow inside .left-sidebar
old_bottom_css = '''    /* Bottom Dual-Row Navigation (Right-Anchored Pill Container) */
    .bottom-nav-container {
      position: absolute;
      bottom: 16px;
      right: 18px;
      left: auto;
      width: fit-content;
      max-width: calc(100vw - 36px);
      display: flex;
      flex-direction: column;
      align-items: flex-end;
      gap: 6px;
      z-index: 20;
      pointer-events: none;
    }
    .bottom-nav-row {
      display: flex;
      align-items: center;
      gap: 6px;
      background: rgba(13, 20, 36, 0.92);
      backdrop-filter: blur(16px);
      -webkit-backdrop-filter: blur(16px);
      border: 1px solid rgba(255, 255, 255, 0.1);
      border-radius: 12px;
      padding: 6px 12px;
      pointer-events: auto;
      overflow-x: auto;
      box-shadow: 0 10px 28px rgba(0, 0, 0, 0.5);
      scrollbar-width: none;
    }'''

new_bottom_css = '''    /* Sidebar-Docked Room & Action Navigation (Zero Overlap on 3D Viewer) */
    .bottom-nav-container {
      width: 100%;
      display: flex;
      flex-direction: column;
      gap: 10px;
    }
    .bottom-nav-row {
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      gap: 5px;
      background: rgba(255, 255, 255, 0.03);
      border: 1px solid rgba(255, 255, 255, 0.08);
      border-radius: 12px;
      padding: 10px;
    }'''

assert old_bottom_css in code, "old_bottom_css not found"
code = code.replace(old_bottom_css, new_bottom_css, 1)

# 3. Reorganize <body> HTML into:
#    <aside class="left-sidebar"> (Overview controls + Room Brief + Room Actions + Rooms Grid)
#    <div id="canvas-container"> (pure 3D viewport + labels + reticle)
#    <aside class="customize-panel" id="customize-panel"> (Right Customize Sidebar)
body_start = code.find('<body>')
script_start = code.find('  <!-- THREE.JS & ORBITCONTROLS CDN -->')
assert body_start != -1 and script_start != -1

new_body_html = '''<body>
  <!-- DEDICATED LEFT SIDEBAR (Zero Overlap on 3D Viewport) -->
  <aside class="left-sidebar" id="left-sidebar">
    <div class="brand-badge" style="padding: 8px 10px;">
      <div class="brand-dot"></div>
      <div>
        <div class="brand-title" style="font-size:12px;">3D Walkthrough</div>
        <div class="brand-sub" style="font-size:10px;">4,537 Sq. Ft • Plot 74'×135'</div>
      </div>
    </div>

    <!-- Overview Controls (Shown in Dollhouse Mode) -->
    <div id="overview-sidebar-controls" style="display:flex; flex-direction:column; gap:10px;">
      <div class="sidebar-section">
        <span class="sidebar-section-title">Camera Views</span>
        <div class="sidebar-grid">
          <button class="btn active" id="btn-view-overview" onclick="setViewMode('overview')">Overview</button>
          <button class="btn" id="btn-view-topplan" onclick="setViewMode('topplan')">Top Plan</button>
          <button class="btn" id="btn-view-front" onclick="setViewMode('front')">Front</button>
        </div>
      </div>
      <div class="sidebar-section">
        <span class="sidebar-section-title">Architecture Toggles</span>
        <div class="sidebar-grid">
          <button class="btn active" id="btn-toggle-roof" onclick="toggleRoof()">Roof Off</button>
          <button class="btn" id="btn-toggle-cutaway" onclick="toggleCutaway()">Cutaway</button>
          <button class="btn active" id="btn-toggle-labels" onclick="toggleLabels()">Labels</button>
          <button class="btn active" id="btn-toggle-furniture" onclick="toggleFurniture()">Furniture</button>
          <button class="btn active" id="btn-toggle-daylight" onclick="toggleDaylight()">Daylight</button>
        </div>
      </div>
    </div>

    <!-- Room Brief Card (Shown when inside a room) -->
    <div class="room-info-card" id="room-info-card">
      <div class="card-header-row">
        <div>
          <div class="card-room-title" id="card-room-title" style="font-size:17px;">Kitchen</div>
          <div class="card-room-subtitle" id="card-room-dims">Plan size 24'0" × 22'3"</div>
        </div>
        <div class="card-header-actions">
          <button class="card-icon-btn" id="btn-toggle-minimap" onclick="toggleMinimap()" title="Toggle 2D Floor Plan Radar (M)">
            <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><rect x="3" y="3" width="18" height="18" rx="2"/><path d="M3 9h18M9 21V9"/></svg>
          </button>
          <button class="card-icon-btn" onclick="toggleCardCollapse()" title="Minimize Details (H)">
            <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><line x1="5" y1="12" x2="19" y2="12"/></svg>
          </button>
        </div>
      </div>
      <div class="card-section">
        <div class="card-label">CONCEPT</div>
        <div class="card-text" id="card-concept" style="font-size:11px;"></div>
      </div>
      <div class="card-section">
        <div class="card-label">FURNITURE</div>
        <div class="card-text" id="card-furniture" style="font-size:11px;"></div>
      </div>
      <div class="card-section">
        <div class="card-label">LIGHTING</div>
        <div class="card-text" id="card-lighting" style="font-size:11px;"></div>
      </div>
      <div class="card-minimap-box" id="card-minimap-box">
        <div class="card-minimap-header">
          <span>2D Floor Plan Radar</span>
          <span style="color:#94a3b8; font-weight:500;">Click room</span>
        </div>
        <canvas id="minimap-canvas" width="600" height="360"></canvas>
      </div>
    </div>

    <!-- Collapsed Room Chip -->
    <div class="room-chip-collapsed" id="room-chip-collapsed" onclick="toggleCardCollapse()" style="position:static; width:100%; justify-content:space-between;">
      <div style="display:flex; align-items:center; gap:8px;">
        <div class="chip-dot"></div>
        <span class="chip-title" id="collapsed-room-title">Kitchen</span>
        <span class="chip-dims" id="collapsed-room-dims">24'0" × 22'3"</span>
      </div>
      <span class="chip-badge">Details ▾</span>
    </div>

    <!-- Room Controls & Rooms List (Zero Overlap on 3D Viewer) -->
    <div class="bottom-nav-container" id="bottom-nav-container">
      <div class="bottom-nav-row" id="room-actions-row" style="display:none;">
        <span class="nav-label" style="width:100%; margin-bottom:2px;">ROOM CONTROLS</span>
        <button class="action-pill" onclick="exitRoom()">
          <svg width="11" height="11" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><path d="M18 6L6 18M6 6l12 12"></path></svg>
          Exit
        </button>
        <button class="action-pill" onclick="prevRoom()">Prev</button>
        <button class="action-pill" onclick="nextRoom()">Next</button>
        <button class="action-pill" id="action-lights" onclick="toggleLights()">Lights</button>
        <button class="action-pill active" id="action-daylight" onclick="toggleDaylight()">Daylight</button>
        <button class="action-pill" id="action-lookaround" onclick="toggleLookAround()">360°</button>
        <button class="action-pill customize-btn" id="btn-customize" onclick="toggleCustomizePanel()" style="width:100%; justify-content:center; margin-top:2px;">✦ Customize Room</button>
        <div class="corner-group" style="width:100%; justify-content:space-between; margin-top:2px;" title="Stand at any of the 4 corners of the room">
          <span class="corner-label">CORNERS</span>
          <div style="display:flex; gap:2px;">
            <button class="corner-btn" id="corner-nw" onclick="goToCorner('nw')">NW</button>
            <button class="corner-btn" id="corner-ne" onclick="goToCorner('ne')">NE</button>
            <button class="corner-btn" id="corner-sw" onclick="goToCorner('sw')">SW</button>
            <button class="corner-btn" id="corner-se" onclick="goToCorner('se')">SE</button>
          </div>
        </div>
      </div>

      <div class="bottom-nav-row" id="rooms-pill-row">
        <span class="nav-label" style="width:100%; margin-bottom:2px;">ROOMS (15)</span>
        <div id="room-pills-list" style="display:flex; flex-wrap:wrap; gap:4px; align-items:center;"></div>
      </div>
    </div>

    <div style="font-size:10px; color:#64748b; text-align:center; margin-top:auto; padding-top:4px;">
      Drag to look · Scroll zoom · WASD/Arrows walk · Esc exit
    </div>
  </aside>

  <!-- PURE UNOBSTRUCTED 3D VIEWPORT -->
  <div id="canvas-container">
    <div class="reticle" id="reticle"></div>
    <div id="labels-container" class="ui-layer" style="width:100%; height:100%; top:0; left:0;"></div>
  </div>

  <!-- DEDICATED RIGHT CUSTOMIZE SIDEBAR (Zero Overlap on 3D Viewer) -->
  <aside class="customize-panel" id="customize-panel">
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
  </aside>

'''

code = code[:body_start] + new_body_html + code[script_start:]

# 4. Update init(), onWindowResize(), updateRoomLabels(), onPointerDown() to use container dimensions instead of window.innerWidth
code = code.replace(
    'camera = new THREE.PerspectiveCamera(50, window.innerWidth / window.innerHeight, 0.2, 500);',
    'const cw = container.clientWidth || window.innerWidth, ch = container.clientHeight || window.innerHeight;\n      camera = new THREE.PerspectiveCamera(50, cw / ch, 0.2, 500);'
)
code = code.replace(
    'renderer.setSize(window.innerWidth, window.innerHeight);',
    'const cont = document.getElementById(\'canvas-container\');\n      renderer.setSize(cont.clientWidth || window.innerWidth, cont.clientHeight || window.innerHeight);'
)
code = code.replace(
    '''    function onWindowResize() {
      camera.aspect = window.innerWidth / window.innerHeight;
      camera.updateProjectionMatrix();
      renderer.setSize(window.innerWidth, window.innerHeight);
    }''',
    '''    function onWindowResize() {
      const cont = document.getElementById('canvas-container');
      const w = cont ? cont.clientWidth : window.innerWidth;
      const h = cont ? cont.clientHeight : window.innerHeight;
      if (w <= 0 || h <= 0) return;
      camera.aspect = w / h;
      camera.updateProjectionMatrix();
      renderer.setSize(w, h);
    }'''
)
code = code.replace(
    'const x = (proj.x * 0.5 + 0.5) * window.innerWidth;\n        const y = (-(proj.y * 0.5) + 0.5) * window.innerHeight;',
    '''const cont = document.getElementById('canvas-container');
        const cw = cont ? cont.clientWidth : window.innerWidth;
        const ch = cont ? cont.clientHeight : window.innerHeight;
        const x = (proj.x * 0.5 + 0.5) * cw;
        const y = (-(proj.y * 0.5) + 0.5) * ch;'''
)
code = code.replace(
    'mouse.x = (e.clientX / window.innerWidth) * 2 - 1;\n        mouse.y = -(e.clientY / window.innerHeight) * 2 + 1;',
    '''const rect = renderer.domElement.getBoundingClientRect();
        mouse.x = ((e.clientX - rect.left) / rect.width) * 2 - 1;
        mouse.y = -((e.clientY - rect.top) / rect.height) * 2 + 1;'''
)

# 5. Update toggleCustomizePanel, enterRoom, exitRoom to toggle #overview-sidebar-controls and call onWindowResize()
code = code.replace(
    '''      if (panel) panel.classList.toggle('visible', isCustomizeOpen);
      if (btn) btn.classList.toggle('active', isCustomizeOpen);
      if (isCustomizeOpen) renderCustomizeGrid();''',
    '''      if (panel) panel.classList.toggle('visible', isCustomizeOpen);
      if (btn) btn.classList.toggle('active', isCustomizeOpen);
      if (isCustomizeOpen) renderCustomizeGrid();
      onWindowResize();'''
)

code = code.replace(
    '''      // Hide Overview Top Bar & Left Floating Toolbar (Ultra Clean View)
      const topBar = document.querySelector('.top-bar');
      if (topBar) topBar.style.display = 'none';
      const leftBar = document.querySelector('.left-floating-bar');
      if (leftBar) leftBar.style.display = 'none';''',
    '''      const ovCtrl = document.getElementById('overview-sidebar-controls');
      if (ovCtrl) ovCtrl.style.display = 'none';'''
)
code = code.replace(
    '''      // Restore Overview Top Bar & Left Floating Toolbar
      const topBar = document.querySelector('.top-bar');
      if (topBar) topBar.style.display = 'flex';
      const leftBar = document.querySelector('.left-floating-bar');
      if (leftBar) leftBar.style.display = 'flex';''',
    '''      const ovCtrl = document.getElementById('overview-sidebar-controls');
      if (ovCtrl) ovCtrl.style.display = 'flex';'''
)
code = code.replace(
    '''      const cb = document.getElementById('btn-customize');
      if (cb) cb.classList.remove('active');''',
    '''      const cb = document.getElementById('btn-customize');
      if (cb) cb.classList.remove('active');
      onWindowResize();'''
)

# Also call onWindowResize() when ?customize=... opens on initial load
code = code.replace(
    '          switchCustomizeTab(custTab);',
    '          switchCustomizeTab(custTab);\n          onWindowResize();'
)

with open(index_path, 'w', encoding='utf-8') as f:
    f.write(code)

print("Converted UI to non-overlapping Left Sidebar + 3D Viewport + Right Customize Sidebar!")

