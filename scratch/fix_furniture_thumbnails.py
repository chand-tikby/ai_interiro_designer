index_path = '/Users/puspharaj/Documents/Projects/ai-interior-designer/index.html'

with open(index_path, 'r', encoding='utf-8') as f:
    code = f.read()

old_furn_svg_start = '      // Furniture / Sofas preview SVG'
old_furn_svg_end = '    function renderCustomizeGrid() {'
s = code.find(old_furn_svg_start)
e = code.find(old_furn_svg_end)
assert s != -1 and e != -1, "Furniture SVG block not found"

new_furn_svg_js = '''      // Detailed 3D-Perspective Furniture Illustrations (unique per room & preset)
      function sofaSVG(bodyCol, cushCol, legCol, pilCol, style = '3seat', tblCol = '#f1f5f9') {
        if (style === 'lshape') {
          return `<svg viewBox="0 0 120 66" width="100%" height="100%">
            <rect x="0" y="52" width="120" height="14" fill="rgba(255,255,255,0.03)"/>
            <!-- Sofa Legs -->
            <line x1="18" y1="48" x2="18" y2="55" stroke="${legCol}" stroke-width="2.5"/>
            <line x1="94" y1="48" x2="94" y2="55" stroke="${legCol}" stroke-width="2.5"/>
            <!-- Backrest -->
            <rect x="14" y="18" width="84" height="18" rx="4" fill="${bodyCol}"/>
            <!-- Chaise Return -->
            <rect x="14" y="24" width="26" height="26" rx="4" fill="${cushCol}" stroke="${bodyCol}" stroke-width="1.5"/>
            <!-- Seat Cushions -->
            <rect x="41" y="30" width="26" height="18" rx="3" fill="${cushCol}" stroke="${bodyCol}" stroke-width="1"/>
            <rect x="68" y="30" width="26" height="18" rx="3" fill="${cushCol}" stroke="${bodyCol}" stroke-width="1"/>
            <!-- Armrest -->
            <rect x="92" y="26" width="8" height="22" rx="3" fill="${bodyCol}"/>
            <!-- Throw Pillows -->
            <rect x="20" y="22" width="10" height="10" rx="2" fill="${pilCol}" transform="rotate(-8 25 27)"/>
            <rect x="80" y="22" width="10" height="10" rx="2" fill="${pilCol}" transform="rotate(8 85 27)"/>
            <!-- Coffee Table in front -->
            <ellipse cx="66" cy="51" rx="18" ry="5" fill="${tblCol}"/>
            <line x1="54" y1="53" x2="54" y2="61" stroke="#d4af37" stroke-width="1.8"/>
            <line x1="78" y1="53" x2="78" y2="61" stroke="#d4af37" stroke-width="1.8"/>
          </svg>`;
        }
        if (style === 'twin') {
          return `<svg viewBox="0 0 120 66" width="100%" height="100%">
            <!-- Left Sofa -->
            <rect x="8" y="22" width="12" height="28" rx="3" fill="${bodyCol}"/>
            <rect x="16" y="28" width="16" height="20" rx="3" fill="${cushCol}"/>
            <rect x="14" y="26" width="7" height="9" rx="2" fill="${pilCol}"/>
            <line x1="12" y1="50" x2="12" y2="56" stroke="${legCol}" stroke-width="2"/>
            <line x1="28" y1="48" x2="28" y2="54" stroke="${legCol}" stroke-width="2"/>
            <!-- Right Sofa -->
            <rect x="100" y="22" width="12" height="28" rx="3" fill="${bodyCol}"/>
            <rect x="88" y="28" width="16" height="20" rx="3" fill="${cushCol}"/>
            <rect x="99" y="26" width="7" height="9" rx="2" fill="${pilCol}"/>
            <line x1="108" y1="50" x2="108" y2="56" stroke="${legCol}" stroke-width="2"/>
            <line x1="92" y1="48" x2="92" y2="54" stroke="${legCol}" stroke-width="2"/>
            <!-- Center Coffee Table -->
            <rect x="44" y="38" width="32" height="6" rx="2" fill="${tblCol}"/>
            <line x1="48" y1="44" x2="48" y2="54" stroke="#d4af37" stroke-width="2"/>
            <line x1="72" y1="44" x2="72" y2="54" stroke="#d4af37" stroke-width="2"/>
            <rect x="55" y="33" width="10" height="5" rx="1" fill="#d4af37"/>
          </svg>`;
        }
        if (style === 'ushape') {
          return `<svg viewBox="0 0 120 66" width="100%" height="100%">
            <rect x="16" y="18" width="88" height="16" rx="4" fill="${bodyCol}"/>
            <rect x="16" y="26" width="22" height="24" rx="3" fill="${cushCol}"/>
            <rect x="82" y="26" width="22" height="24" rx="3" fill="${cushCol}"/>
            <rect x="39" y="28" width="42" height="14" rx="3" fill="${cushCol}" stroke="${bodyCol}" stroke-width="1"/>
            <ellipse cx="60" cy="49" rx="15" ry="6" fill="${tblCol}"/>
            <rect x="52" y="51" width="16" height="7" rx="2" fill="${tblCol}"/>
            <rect x="24" y="22" width="9" height="8" rx="2" fill="${pilCol}"/>
            <rect x="87" y="22" width="9" height="8" rx="2" fill="${pilCol}"/>
          </svg>`;
        }
        if (style === 'club4') {
          return `<svg viewBox="0 0 120 66" width="100%" height="100%">
            <!-- 2 Back Armchairs -->
            <rect x="18" y="16" width="24" height="20" rx="4" fill="${bodyCol}"/>
            <rect x="22" y="24" width="16" height="10" rx="2" fill="${cushCol}"/>
            <rect x="78" y="16" width="24" height="20" rx="4" fill="${bodyCol}"/>
            <rect x="82" y="24" width="16" height="10" rx="2" fill="${cushCol}"/>
            <!-- Center Round Marble Table -->
            <ellipse cx="60" cy="42" rx="18" ry="6" fill="${tblCol}"/>
            <rect x="54" y="46" width="12" height="10" fill="${legCol}"/>
            <!-- 2 Foreground Armchairs -->
            <rect x="14" y="38" width="24" height="18" rx="4" fill="${cushCol}" stroke="${bodyCol}" stroke-width="1.5"/>
            <rect x="82" y="38" width="24" height="18" rx="4" fill="${cushCol}" stroke="${bodyCol}" stroke-width="1.5"/>
          </svg>`;
        }
        // Standard 3-Seater Sofa + Coffee Table
        return `<svg viewBox="0 0 120 66" width="100%" height="100%">
          <line x1="20" y1="44" x2="18" y2="53" stroke="${legCol}" stroke-width="2.5"/>
          <line x1="100" y1="44" x2="102" y2="53" stroke="${legCol}" stroke-width="2.5"/>
          <rect x="16" y="16" width="88" height="20" rx="5" fill="${bodyCol}"/>
          <rect x="14" y="25" width="10" height="20" rx="4" fill="${bodyCol}"/>
          <rect x="96" y="25" width="10" height="20" rx="4" fill="${bodyCol}"/>
          <rect x="24" y="29" width="23" height="14" rx="3" fill="${cushCol}" stroke="${bodyCol}" stroke-width="1"/>
          <rect x="48" y="29" width="24" height="14" rx="3" fill="${cushCol}" stroke="${bodyCol}" stroke-width="1"/>
          <rect x="73" y="29" width="23" height="14" rx="3" fill="${cushCol}" stroke="${bodyCol}" stroke-width="1"/>
          <rect x="26" y="20" width="10" height="10" rx="2" fill="${pilCol}" transform="rotate(-10 31 25)"/>
          <rect x="84" y="20" width="10" height="10" rx="2" fill="${pilCol}" transform="rotate(10 89 25)"/>
          <rect x="42" y="49" width="36" height="5" rx="2" fill="${tblCol}"/>
          <line x1="46" y1="54" x2="46" y2="61" stroke="${legCol}" stroke-width="2"/>
          <line x1="74" y1="54" x2="74" y2="61" stroke="${legCol}" stroke-width="2"/>
        </svg>`;
      }

      // Living Hall & Drawing Hall Sofas
      if (id === 'lv_warmth' || id === 'dw_sectional') return sofaSVG('#cfc8bc', '#e6dfd3', '#6e4726', '#a85a44', 'lshape', '#ffffff');
      if (id === 'lv_modular') return sofaSVG('#52657a', '#70869e', '#334155', '#d97706', 'lshape', '#e5e0d8');
      if (id === 'lv_nordic') return sofaSVG('#4a6655', '#648571', '#4a2e1b', '#dfd9ce', 'lshape', '#6e4726');
      if (id === 'lv_symmetrical' || id === 'dw_twin') return sofaSVG('#2a4d3c', '#3d6b54', '#d4af37', '#d97706', 'twin', '#6e4726');
      if (id === 'lv_curved' || id === 'dw_boucle') return sofaSVG('#374151', '#e5e7eb', '#1f2937', '#a85a44', 'ushape', '#f1f5f9');
      if (id === 'lv_chesterfield' || id === 'dw_cognac') return sofaSVG('#6e3318', '#8b4523', '#d4af37', '#e5dfd3', '3seat', '#93c5fd');
      if (id === 'lv_japandi') return sofaSVG('#8c6445', '#dfd9ce', '#6e4726', '#5d7a68', '3seat', '#8c6445');
      if (id === 'lv_conversation' || id === 'dw_club') return sofaSVG('#64748b', '#e2e8f0', '#4a2e1b', '#c48b3b', 'club4', '#f8fafc');
      if (id === 'dw_formal') return sofaSVG('#cfc8bc', '#eae5dc', '#6e4726', '#a85a44', '3seat', '#8c6445');

      // Beds (Bedroom 1 & Bedroom 2)
      if (id === 'b1_canopy') {
        return `<svg viewBox="0 0 120 66" width="100%" height="100%">
          <line x1="30" y1="8" x2="30" y2="56" stroke="#6e4726" stroke-width="3"/>
          <line x1="90" y1="8" x2="90" y2="56" stroke="#6e4726" stroke-width="3"/>
          <line x1="30" y1="10" x2="90" y2="10" stroke="#6e4726" stroke-width="3"/>
          <rect x="33" y="22" width="54" height="18" rx="2" fill="#475569"/>
          <rect x="33" y="34" width="54" height="20" rx="2" fill="#5d7a68"/>
          <rect x="38" y="26" width="18" height="9" rx="2" fill="#f1f5f9"/>
          <rect x="64" y="26" width="18" height="9" rx="2" fill="#f1f5f9"/>
          <rect x="14" y="38" width="12" height="14" rx="2" fill="#6e4726"/>
          <rect x="94" y="38" width="12" height="14" rx="2" fill="#6e4726"/>
        </svg>`;
      }
      if (id === 'b2_twin') {
        return `<svg viewBox="0 0 120 66" width="100%" height="100%">
          <rect x="14" y="18" width="34" height="36" rx="3" fill="#5c6672"/>
          <rect x="16" y="28" width="30" height="24" rx="2" fill="#c48b3b"/>
          <rect x="21" y="22" width="20" height="8" rx="2" fill="#f1f5f9"/>
          <rect x="53" y="32" width="14" height="18" rx="2" fill="#6e4726"/>
          <rect x="72" y="18" width="34" height="36" rx="3" fill="#5c6672"/>
          <rect x="74" y="28" width="30" height="24" rx="2" fill="#c48b3b"/>
          <rect x="79" y="22" width="20" height="8" rx="2" fill="#f1f5f9"/>
        </svg>`;
      }
      if (id.startsWith('b1_') || id.startsWith('b2_')) {
        const huv = id.includes('walnut') ? '#6e4726' : id.includes('charcoal') ? '#1e293b' : id.includes('sage') ? '#3d6352' : '#475569';
        const duv = id.includes('walnut') ? '#c48b3b' : id.includes('charcoal') ? '#64748b' : id.includes('study') ? '#c48b3b' : '#5d7a68';
        return `<svg viewBox="0 0 120 66" width="100%" height="100%">
          <rect x="28" y="14" width="64" height="22" rx="3" fill="${huv}"/>
          <rect x="30" y="30" width="60" height="24" rx="3" fill="${duv}"/>
          <rect x="36" y="22" width="20" height="10" rx="2" fill="#f1f5f9"/>
          <rect x="64" y="22" width="20" height="10" rx="2" fill="#f1f5f9"/>
          <rect x="12" y="36" width="13" height="16" rx="2" fill="#6e4726"/>
          <circle cx="18.5" cy="31" r="4" fill="#fff3c4"/>
          <rect x="95" y="36" width="13" height="16" rx="2" fill="#6e4726"/>
          <circle cx="101.5" cy="31" r="4" fill="#fff3c4"/>
        </svg>`;
      }

      // Dining Sets
      if (id === 'dn_round') {
        return `<svg viewBox="0 0 120 66" width="100%" height="100%">
          <ellipse cx="60" cy="30" rx="26" ry="8" fill="#f1f5f9"/>
          <rect x="55" y="36" width="10" height="18" fill="#6e4726"/>
          <rect x="46" y="52" width="28" height="4" rx="1" fill="#6e4726"/>
          <rect x="24" y="26" width="12" height="18" rx="2" fill="#5d7a68"/>
          <rect x="84" y="26" width="12" height="18" rx="2" fill="#5d7a68"/>
          <rect x="40" y="38" width="12" height="16" rx="2" fill="#5d7a68"/>
          <rect x="68" y="38" width="12" height="16" rx="2" fill="#5d7a68"/>
        </svg>`;
      }
      if (id.startsWith('dn_')) {
        const tbl = id === 'dn_glass' ? '#93c5fd' : id.includes('walnut') || id.includes('banquet') ? '#4a2e1b' : '#a67b5b';
        const chr = id === 'dn_glass' ? '#334155' : id.includes('banquet') ? '#475569' : '#e5dfd3';
        return `<svg viewBox="0 0 120 66" width="100%" height="100%">
          <rect x="26" y="28" width="68" height="6" rx="2" fill="${tbl}"/>
          <line x1="36" y1="34" x2="36" y2="54" stroke="#4a2e1b" stroke-width="3"/>
          <line x1="84" y1="34" x2="84" y2="54" stroke="#4a2e1b" stroke-width="3"/>
          <rect x="14" y="22" width="10" height="22" rx="2" fill="${chr}"/>
          <rect x="96" y="22" width="10" height="22" rx="2" fill="${chr}"/>
          <rect x="38" y="36" width="12" height="18" rx="2" fill="${chr}"/>
          <rect x="54" y="36" width="12" height="18" rx="2" fill="${chr}"/>
          <rect x="70" y="36" width="12" height="18" rx="2" fill="${chr}"/>
        </svg>`;
      }

      // Kitchen Islands
      if (id.startsWith('kt_') || id.startsWith('wk_')) {
        const isl = id.includes('walnut') || id.includes('oak') ? '#6e4726' : id.includes('charcoal') || id.includes('slate') ? '#27272a' : '#182c44';
        return `<svg viewBox="0 0 120 66" width="100%" height="100%">
          <rect x="18" y="24" width="84" height="5" rx="1" fill="#f8fafc"/>
          <rect x="22" y="29" width="76" height="24" rx="1" fill="${isl}"/>
          <rect x="22" y="51" width="76" height="4" fill="#d4af37"/>
          <ellipse cx="36" cy="40" rx="6" ry="2.5" fill="#8b5a2b"/>
          <line x1="36" y1="42" x2="36" y2="57" stroke="#0f172a" stroke-width="2"/>
          <ellipse cx="60" cy="40" rx="6" ry="2.5" fill="#8b5a2b"/>
          <line x1="60" y1="42" x2="60" y2="57" stroke="#0f172a" stroke-width="2"/>
          <ellipse cx="84" cy="40" rx="6" ry="2.5" fill="#8b5a2b"/>
          <line x1="84" y1="42" x2="84" y2="57" stroke="#0f172a" stroke-width="2"/>
        </svg>`;
      }

      // Sitout Cane / Loveseat
      if (id === 'st_loveseat') return sofaSVG('#5d7a68', '#dfd9ce', '#6e4726', '#c48b3b', '3seat', '#8c6445');
      if (id === 'st_cane') return sofaSVG('#a67b5b', '#dfd9ce', '#6e4726', '#5d7a68', 'twin', '#a67b5b');

      // Pooja / Bath / Dress
      if (id.startsWith('pj_')) {
        const mc = id === 'pj_marble' ? '#ebe6de' : '#6e4726';
        return `<svg viewBox="0 0 120 66" width="100%" height="100%">
          <polygon points="60,8 44,24 76,24" fill="#d4af37"/>
          <rect x="34" y="24" width="52" height="5" fill="${mc}"/>
          <line x1="38" y1="29" x2="38" y2="48" stroke="${mc}" stroke-width="3"/>
          <line x1="82" y1="29" x2="82" y2="48" stroke="${mc}" stroke-width="3"/>
          <rect x="32" y="48" width="56" height="10" rx="2" fill="${mc}"/>
          <circle cx="48" cy="44" r="2.5" fill="#ffcf87"/>
          <circle cx="72" cy="44" r="2.5" fill="#ffcf87"/>
        </svg>`;
      }
      return sofaSVG('#cfc8bc', '#e6dfd3', '#6e4726', '#5d7a68', '3seat', '#f1f5f9');
    }

'''

code = code[:s] + new_furn_svg_js + code[e:]

# Add optional ?customize=tab URL param support in init() for instant inspection/testing
code = code.replace(
    "      if (roomParam) {\n        enterRoom(roomParam, true);\n      }",
    '''      if (roomParam) {
        enterRoom(roomParam, true);
        const custTab = urlParams.get('customize');
        if (custTab) {
          activeCustomizeTab = custTab;
          isCustomizeOpen = true;
          const panel = document.getElementById('customize-panel');
          const btn = document.getElementById('btn-customize');
          if (panel) panel.classList.add('visible');
          if (btn) btn.classList.add('active');
          switchCustomizeTab(custTab);
        }
      }'''
)

with open(index_path, 'w', encoding='utf-8') as f:
    f.write(code)

print("Replaced abstract blobs with 3D-perspective furniture illustrations!")

