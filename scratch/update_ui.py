import re

index_path = '/Users/puspharaj/Documents/Projects/ai-interior-designer/index.html'

with open(index_path, 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Update HTML Markup
old_markup_start = '<!-- TOP-LEFT ROOM INFO CARD'
old_markup_end = '<div id="labels-container"'

new_markup = '''<!-- TOP-LEFT ROOM INFO CARD (Matching Claude Image 2 with Minimap & Minimize Toggle) -->
  <div class="room-info-card" id="room-info-card">
    <div class="card-header-row">
      <div>
        <div class="card-room-title" id="card-room-title">Kitchen</div>
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
      <div class="card-text" id="card-concept">A working kitchen with an island for quick meals and the fridge on the dining side.</div>
    </div>
    <div class="card-section">
      <div class="card-label">FURNITURE</div>
      <div class="card-text" id="card-furniture">Sage cabinets with stone counters, sink under the west window, gas hob with chimney, island with three stools, tall pantry, fridge, wall cabinets, subway-tile backsplash.</div>
    </div>
    <div class="card-section">
      <div class="card-label">LIGHTING</div>
      <div class="card-text" id="card-lighting">Cool white downlights for work, pendants over the island, and under-cabinet LED strips.</div>
    </div>
    <div class="card-minimap-box" id="card-minimap-box">
      <div class="card-minimap-header">
        <span>2D Floor Plan Radar</span>
        <span style="color:#94a3b8; font-weight:500;">Click room to fly</span>
      </div>
      <canvas id="minimap-canvas" width="600" height="360"></canvas>
    </div>
  </div>

  <!-- COLLAPSED ROOM CHIP (When user minimizes card) -->
  <div class="room-chip-collapsed" id="room-chip-collapsed" onclick="toggleCardCollapse()" title="Click to show room design details (H)">
    <div class="chip-dot"></div>
    <span class="chip-title" id="collapsed-room-title">Kitchen</span>
    <span class="chip-dims" id="collapsed-room-dims">24'0" × 22'3"</span>
    <span class="chip-badge">Details ▾</span>
  </div>

  <!-- TOP-RIGHT MINIMAL HUD -->
  <div class="top-right-hud" id="top-right-hud">
    Drag to look around · scroll to zoom · arrow keys walk · Esc to leave
  </div>

  <!-- BOTTOM DUAL-ROW NAVIGATION (Matching Claude Image 2) -->
  <div class="bottom-nav-container" id="bottom-nav-container">
    <div class="bottom-nav-row" id="rooms-pill-row">
      <span class="nav-label">ROOMS</span>
      <div id="room-pills-list" style="display:flex; gap:6px; align-items:center;"></div>
    </div>
    <div class="bottom-nav-row" id="room-actions-row" style="display:none;">
      <span class="nav-label">ROOM</span>
      <button class="action-pill" onclick="exitRoom()">
        <svg width="12" height="12" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><path d="M18 6L6 18M6 6l12 12"></path></svg>
        Exit room
      </button>
      <button class="action-pill" onclick="prevRoom()">Previous</button>
      <button class="action-pill" onclick="nextRoom()">Next</button>
      <button class="action-pill" id="action-lights" onclick="toggleLights()">Lights</button>
      <button class="action-pill active" id="action-daylight" onclick="toggleDaylight()">Daylight</button>
      <button class="action-pill" id="action-lookaround" onclick="toggleLookAround()">Look around</button>
    </div>
  </div>

  '''

s_idx = code.find(old_markup_start)
e_idx = code.find(old_markup_end)
if s_idx != -1 and e_idx != -1:
    code = code[:s_idx] + new_markup + code[e_idx:]
    print("Updated Markup successfully!")
else:
    print("Markup markers not found!")

# 2. Update JavaScript Functions: enterRoom, exitRoom, toggleCardCollapse, toggleMinimap, drawMinimap, etc.
old_enter_start = 'function enterRoom(roomId, immediate = false) {'
old_enter_end = 'function nextRoom() {'

new_enter_js = '''let isCardCollapsed = false;
    let isMinimapOpen = false;

    function toggleCardCollapse() {
      if (!isInsideRoom) return;
      isCardCollapsed = !isCardCollapsed;
      const card = document.getElementById('room-info-card');
      const chip = document.getElementById('room-chip-collapsed');
      if (isCardCollapsed) {
        if (card) card.classList.remove('visible');
        if (chip) chip.style.display = 'flex';
      } else {
        if (card) card.classList.add('visible');
        if (chip) chip.style.display = 'none';
        if (isMinimapOpen) drawMinimap();
      }
    }

    function toggleMinimap() {
      isMinimapOpen = !isMinimapOpen;
      const box = document.getElementById('card-minimap-box');
      const btn = document.getElementById('btn-toggle-minimap');
      if (box) box.style.display = isMinimapOpen ? 'flex' : 'none';
      if (btn) btn.classList.toggle('active', isMinimapOpen);
      if (isMinimapOpen) {
        setupMinimapEvents();
        drawMinimap();
      }
    }

    let minimapEventsSetup = false;
    function setupMinimapEvents() {
      if (minimapEventsSetup) return;
      const canvas = document.getElementById('minimap-canvas');
      if (!canvas) return;
      minimapEventsSetup = true;

      canvas.addEventListener('click', (e) => {
        const rect = canvas.getBoundingClientRect();
        const clickX = ((e.clientX - rect.left) / rect.width) * canvas.width;
        const clickY = ((e.clientY - rect.top) / rect.height) * canvas.height;

        const pad = 16;
        const scaleX = (canvas.width - 2 * pad) / 48.25;
        const scaleZ = (canvas.height - 2 * pad) / 83.5;
        const scale = Math.min(scaleX, scaleZ);
        const offsetX = pad + (canvas.width - 2 * pad - 48.25 * scale) / 2;
        const offsetZ = pad + (canvas.height - 2 * pad - 83.5 * scale) / 2;

        const wx = (clickX - offsetX) / scale;
        const wz = (clickY - offsetZ) / scale;

        const clickedRoom = ROOMS.find(r => 
          wx >= r.bounds.x1 && wx <= r.bounds.x2 && wz >= r.bounds.z1 && wz <= r.bounds.z2
        );
        if (clickedRoom) {
          enterRoom(clickedRoom.id);
        }
      });
    }

    function drawMinimap() {
      const canvas = document.getElementById('minimap-canvas');
      if (!canvas) return;
      const ctx = canvas.getContext('2d');
      if (!ctx) return;

      const pad = 16;
      const scaleX = (canvas.width - 2 * pad) / 48.25;
      const scaleZ = (canvas.height - 2 * pad) / 83.5;
      const scale = Math.min(scaleX, scaleZ);
      const offsetX = pad + (canvas.width - 2 * pad - 48.25 * scale) / 2;
      const offsetZ = pad + (canvas.height - 2 * pad - 83.5 * scale) / 2;

      // Clear Canvas
      ctx.fillStyle = '#080c14';
      ctx.fillRect(0, 0, canvas.width, canvas.height);

      // Draw Grid Lines
      ctx.strokeStyle = 'rgba(255, 255, 255, 0.04)';
      ctx.lineWidth = 1;
      for (let x = 0; x <= 48.25; x += 10) {
        const px = offsetX + x * scale;
        ctx.beginPath(); ctx.moveTo(px, offsetZ); ctx.lineTo(px, offsetZ + 83.5 * scale); ctx.stroke();
      }
      for (let z = 0; z <= 83.5; z += 10) {
        const pz = offsetZ + z * scale;
        ctx.beginPath(); ctx.moveTo(offsetX, pz); ctx.lineTo(offsetX + 48.25 * scale, pz); ctx.stroke();
      }

      // Draw Plot Boundary
      ctx.strokeStyle = 'rgba(56, 189, 248, 0.2)';
      ctx.lineWidth = 1.5;
      ctx.strokeRect(offsetX, offsetZ, 48.25 * scale, 83.5 * scale);

      // Draw Rooms
      ROOMS.forEach(r => {
        const rx = offsetX + r.bounds.x1 * scale;
        const rz = offsetZ + r.bounds.z1 * scale;
        const rw = (r.bounds.x2 - r.bounds.x1) * scale;
        const rh = (r.bounds.z2 - r.bounds.z1) * scale;
        const isActive = (r.id === currentRoomId);

        if (isActive) {
          ctx.fillStyle = 'rgba(56, 189, 248, 0.25)';
          ctx.fillRect(rx, rz, rw, rh);
          ctx.strokeStyle = '#38bdf8';
          ctx.lineWidth = 2.5;
          ctx.strokeRect(rx, rz, rw, rh);
        } else {
          ctx.fillStyle = 'rgba(255, 255, 255, 0.03)';
          ctx.fillRect(rx, rz, rw, rh);
          ctx.strokeStyle = 'rgba(255, 255, 255, 0.15)';
          ctx.lineWidth = 1;
          ctx.strokeRect(rx, rz, rw, rh);
        }

        // Room Name
        ctx.fillStyle = isActive ? '#ffffff' : '#94a3b8';
        ctx.font = isActive ? '700 13px Plus Jakarta Sans, sans-serif' : '500 11px Plus Jakarta Sans, sans-serif';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText(r.short || r.name, rx + rw / 2, rz + rh / 2);
      });

      // Draw Camera Position & FOV Sight Cone
      if (isInsideRoom && currentRoomId) {
        const cx = offsetX + camera.position.x * scale;
        const cz = offsetZ + camera.position.z * scale;

        // FOV Sight Cone
        ctx.save();
        ctx.translate(cx, cz);
        ctx.rotate(-camYaw + Math.PI);

        const coneGrad = ctx.createRadialGradient(0, 0, 2, 0, 0, 50);
        coneGrad.addColorStop(0, 'rgba(56, 189, 248, 0.65)');
        coneGrad.addColorStop(1, 'rgba(56, 189, 248, 0)');
        ctx.fillStyle = coneGrad;
        ctx.beginPath();
        ctx.moveTo(0, 0);
        ctx.arc(0, 0, 50, -0.45, 0.45);
        ctx.closePath();
        ctx.fill();
        ctx.restore();

        // Camera Point
        ctx.fillStyle = '#38bdf8';
        ctx.beginPath();
        ctx.arc(cx, cz, 5, 0, Math.PI * 2);
        ctx.fill();
        ctx.strokeStyle = '#ffffff';
        ctx.lineWidth = 1.8;
        ctx.stroke();
      }
    }

    function enterRoom(roomId, immediate = false) {
      const room = ROOMS.find(r => r.id === roomId);
      if (!room) return;

      currentRoomId = roomId;
      isInsideRoom = true;
      controls.enabled = false;

      // Hide Overview Top Bar & Left Floating Toolbar (Ultra Clean View)
      const topBar = document.querySelector('.top-bar');
      if (topBar) topBar.style.display = 'none';
      const leftBar = document.querySelector('.left-floating-bar');
      if (leftBar) leftBar.style.display = 'none';

      // Update Bottom Room Pills
      document.querySelectorAll('.room-pill').forEach(c => c.classList.remove('active'));
      const activePill = document.getElementById(`pill-${roomId}`);
      if (activePill) activePill.classList.add('active');

      // Hide all 3D floating labels
      labelElements.forEach(l => l.el.style.opacity = '0');

      // Populate Top-Left Room Card
      const titleEl = document.getElementById('card-room-title');
      if (titleEl) titleEl.textContent = room.short || room.name;
      const dimsEl = document.getElementById('card-room-dims');
      if (dimsEl) dimsEl.textContent = `Plan size ${room.dims}`;
      const conceptEl = document.getElementById('card-concept');
      if (conceptEl) conceptEl.textContent = room.concept;
      const furnEl = document.getElementById('card-furniture');
      if (furnEl) furnEl.textContent = room.furnitureText || room.furniture.map(f => f.name).join(', ');
      const lightEl = document.getElementById('card-lighting');
      if (lightEl) lightEl.textContent = room.lighting;

      // Update Collapsed Chip
      const chipTitle = document.getElementById('collapsed-room-title');
      if (chipTitle) chipTitle.textContent = room.short || room.name;
      const chipDims = document.getElementById('collapsed-room-dims');
      if (chipDims) chipDims.textContent = room.dims;

      const card = document.getElementById('room-info-card');
      const chip = document.getElementById('room-chip-collapsed');
      if (isCardCollapsed) {
        if (card) card.classList.remove('visible');
        if (chip) chip.style.display = 'flex';
      } else {
        if (card) card.classList.add('visible');
        if (chip) chip.style.display = 'none';
      }

      const topHud = document.getElementById('top-right-hud');
      if (topHud) topHud.classList.add('visible');
      const actRow = document.getElementById('room-actions-row');
      if (actRow) actRow.style.display = 'flex';

      // Update minimap if open
      if (isMinimapOpen) drawMinimap();

      // Enable active room lighting
      setupRoomLighting(room);

      // Calculate initial yaw & pitch from look direction
      const dx = room.camTarget[0] - room.camPos[0];
      const dy = room.camTarget[1] - room.camPos[1];
      const dz = room.camTarget[2] - room.camPos[2];
      camYaw = Math.atan2(dx, dz);
      camPitch = Math.asin(dy / Math.hypot(dx, dy, dz));

      if (immediate) {
        camera.position.set(room.camPos[0], room.camPos[1], room.camPos[2]);
        const lookTgt = new THREE.Vector3(
          camera.position.x + Math.sin(camYaw) * Math.cos(camPitch) * 10,
          camera.position.y + Math.sin(camPitch) * 10,
          camera.position.z + Math.cos(camYaw) * Math.cos(camPitch) * 10
        );
        camera.lookAt(lookTgt);
        isAnimating = false;
        animProgress = 1.0;
        roofGroup.visible = true;
      } else {
        // Start Camera Flying Animation
        animStartPos.copy(camera.position);
        animTargetPos.set(room.camPos[0], room.camPos[1], room.camPos[2]);

        animStartLook.copy(controls.target);
        animTargetLook.set(room.camTarget[0], room.camTarget[1], room.camTarget[2]);

        animStartTime = performance.now();
        animProgress = 0;
        isAnimating = true;
      }
    }

    function exitRoom() {
      if (!isInsideRoom) return;
      isInsideRoom = false;
      controls.enabled = true;

      // Restore Overview Top Bar & Left Floating Toolbar
      const topBar = document.querySelector('.top-bar');
      if (topBar) topBar.style.display = 'flex';
      const leftBar = document.querySelector('.left-floating-bar');
      if (leftBar) leftBar.style.display = 'flex';

      document.querySelectorAll('.room-pill').forEach(c => c.classList.remove('active'));
      const card = document.getElementById('room-info-card');
      if (card) card.classList.remove('visible');
      const chip = document.getElementById('room-chip-collapsed');
      if (chip) chip.style.display = 'none';
      const topHud = document.getElementById('top-right-hud');
      if (topHud) topHud.classList.remove('visible');
      const actRow = document.getElementById('room-actions-row');
      if (actRow) actRow.style.display = 'none';

      // Restore roof according to user preference
      roofGroup.visible = roofVisible;

      // Clear local lights
      while (lightsGroup.children.length > 0) {
        lightsGroup.remove(lightsGroup.children[0]);
      }

      setViewMode('overview');
    }

    function setupRoomLighting(room) {
      while (lightsGroup.children.length > 0) {
        lightsGroup.remove(lightsGroup.children[0]);
      }
      if (!lightsEnabled) return;

      const b = room.bounds;
      const cx = (b.x1 + b.x2) / 2;
      const cz = (b.z1 + b.z2) / 2;

      // Dedicated recessed ceiling spotlight
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
      lightsGroup.add(pt);
    }

    '''

s_enter = code.find(old_enter_start)
e_enter = code.find(old_enter_end)
if s_enter != -1 and e_enter != -1:
    code = code[:s_enter] + new_enter_js + code[e_enter:]
    print("Updated enterRoom/exitRoom successfully!")
else:
    print("Enter room markers not found!")

# 3. Update onKeyDown to include 'h', 'i', 'm', 'l', 'd', ' '
old_key = '''function onKeyDown(e) {
      keys[e.key.toLowerCase()] = true;
      if (e.key === 'Escape') exitRoom();
      if (e.key === 'ArrowRight' && isInsideRoom) nextRoom();
      if (e.key === 'ArrowLeft' && isInsideRoom) prevRoom();
    }'''

new_key = '''function onKeyDown(e) {
      const k = e.key.toLowerCase();
      keys[k] = true;
      if (e.key === 'Escape') exitRoom();
      if (e.key === 'ArrowRight' && isInsideRoom) nextRoom();
      if (e.key === 'ArrowLeft' && isInsideRoom) prevRoom();
      if (k === 'h' || k === 'i') toggleCardCollapse();
      if (k === 'm') toggleMinimap();
      if (k === 'l') toggleLights();
      if (k === 'd') toggleDaylight();
      if (e.key === ' ') { e.preventDefault(); toggleLookAround(); }
    }'''

if old_key in code:
    code = code.replace(old_key, new_key, 1)
    print("Updated onKeyDown successfully!")
else:
    print("onKeyDown marker not found!")

# 4. In animate() loop, update minimap cone continuously if minimap is open
old_anim = '''      // Auto-turntable in 360 mode
      if (autoRotateActive && isInsideRoom && !isDragging) {
        camYaw += 0.003;
      }'''

new_anim = '''      // Auto-turntable in 360 mode
      if (autoRotateActive && isInsideRoom && !isDragging) {
        camYaw += 0.003;
      }

      // Update live 2D Minimap FOV radar cone if open
      if (isInsideRoom && isMinimapOpen) {
        drawMinimap();
      }'''

if old_anim in code:
    code = code.replace(old_anim, new_anim, 1)
    print("Updated animate loop successfully!")
else:
    print("animate marker not found!")

with open(index_path, 'w', encoding='utf-8') as f:
    f.write(code)

print("Finished updating index.html!")

