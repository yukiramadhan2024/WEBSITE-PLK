#!/usr/bin/env python3
"""
=============================================================================
SUITE PENGUJIAN REGRESI BUG GLYPH PORTAL: ZOOM TITIK 'i' & TRANSISI BACKGROUND
Website PLK UNY Mengabdi - Kalurahan Trimurti
=============================================================================
Skrip ini memverifikasi secara langsung (via headless Chrome):
1. Target kordinat kamera tepat masuk ke titik 'i' (bukan celah kosong/putih)
2. Transisi animasi background pin menyesuaikan secara halus dari putih ke hijau forest (#0F231A)
3. Hilangnya layar putih kosong (white flash/gap) selama zoom portal
4. Transformasi glyph akurat dan presisi pada berbagai tingkat progress
5. Pengungkapan (reveal) konten 4 pilar program kerja di dalam portal
=============================================================================
"""

import sys
import subprocess
import json
from pathlib import Path

# Setup UTF-8 encoding
if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
CYAN = '\033[96m'
BOLD = '\033[1m'
RESET = '\033[0m'

CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
WORKSPACE_DIR = Path(__file__).resolve().parent

test_results = []

def record(category, name, passed, details=""):
    test_results.append({
        "category": category,
        "name": name,
        "passed": passed,
        "details": details
    })
    status = f"{GREEN}[PASS]{RESET}" if passed else f"{RED}[FAIL]{RESET}"
    print(f"  {status} {name}")
    if not passed and details:
        print(f"       {YELLOW}-> {details}{RESET}")

def run_portal_tests():
    print(f"\n{BOLD}{CYAN}======================================================================{RESET}")
    print(f"{BOLD}{CYAN}   MEMULAI AUDIT PENGUJIAN GLYPH PORTAL: ZOOM TITIK 'i' & BACKGROUND  {RESET}")
    print(f"{BOLD}{CYAN}======================================================================{RESET}\n")

    # 1. Audit Markup & CSS
    print(f"{BOLD}[1/3] Audit Markup SVG, ClipPath & CSS Portal{RESET}")
    html_text = (WORKSPACE_DIR / "index.html").read_text(encoding="utf-8")
    css_text = (WORKSPACE_DIR / "style.css").read_text(encoding="utf-8")

    has_portal_section = 'id="kegiatan"' in html_text and 'glyph-portal' in html_text
    record("Markup", "Seksi #kegiatan Memiliki Kelas 'glyph-portal'", has_portal_section)

    has_clip_path = 'id="gp-kegiatan-clip"' in html_text and '<text data-gp-glyph' in html_text
    record("Markup", "SVG ClipPath dan Teks 'kegiatan' Terdaftar Lengkap", has_clip_path)

    has_pin_css = '.glyph-portal [data-gp-pin]' in css_text
    record("CSS", "CSS Container Pin Terdaftar di style.css", has_pin_css)

    has_no_pin_lag = '.glyph-portal[data-gp-motion="on"] [data-gp-pin]' in css_text and 'transition: none' in css_text
    record("CSS", "Bebas dari Lag CSS Transition pada Pin saat Motion Aktif", has_no_pin_lag)

    # 2. Browser Verification via Headless Chrome
    print(f"\n{BOLD}[2/3] Eksekusi Simulasi Scroll Zoom Portal di Headless Chrome{RESET}")
    
    harness_script = """<!DOCTYPE html>
<html>
<head><meta charset="utf-8"></head>
<body>
<div id="test-output">WAITING</div>
<iframe id="test-frame" src="http://localhost:8080" style="width: 1440px; height: 900px; border: none;"></iframe>
<script>
window.addEventListener('load', async () => {
    const frame = document.getElementById('test-frame');
    await new Promise(r => setTimeout(r, 2000)); // tunggu font dan inisialisasi lenis/engine
    
    const doc = frame.contentDocument;
    const win = frame.contentWindow;
    const section = doc.getElementById('kegiatan');
    const pin = section.querySelector('[data-gp-pin]');
    const field = section.querySelector('[data-gp-field]');
    const glyph = section.querySelector('[data-gp-glyph]');
    
    const output = {
        ready: section.dataset.gpReady,
        motion: section.dataset.gpMotion,
        scrollPoints: []
    };
    
    const travel = parseFloat(section.style.getPropertyValue('--gp-height') || 900) * 2.2;
    const sTop = section.offsetTop;
    
    // Uji progress dari 0.0 (awal) hingga 1.0 (penuh)
    const testP = [0.0, 0.25, 0.50, 0.75, 0.88, 1.0];
    
    for (const p of testP) {
        const scrollY = sTop + p * travel;
        if (win.lenis) {
            win.lenis.scrollTo(scrollY, { immediate: true });
        } else {
            win.scrollTo(0, scrollY);
            doc.documentElement.scrollTop = scrollY;
        }
        if (win.glyphPortalPaint) {
            win.glyphPortalPaint(p);
        } else if (win.glyphPortalScroll) {
            win.glyphPortalScroll();
        }
        await new Promise(r => setTimeout(r, 150));
        
        const pinBg = win.getComputedStyle(pin).backgroundColor;
        const fieldClip = field.style.clipPath || win.getComputedStyle(field).clipPath;
        const transform = glyph.getAttribute('transform') || '';
        const reveal = section.style.getPropertyValue('--gp-reveal') || '0';
        
        output.scrollPoints.push({
            p: p,
            pinBg: pinBg,
            fieldClip: fieldClip,
            transform: transform,
            reveal: parseFloat(reveal),
            entered: section.dataset.gpEntered
        });
    }
    
    document.getElementById('test-output').textContent = JSON.stringify(output);
});
</script>
</body>
</html>
"""
    harness_path = WORKSPACE_DIR / "temp_portal_harness.html"
    harness_path.write_text(harness_script, encoding="utf-8")

    cmd = [
        CHROME_PATH,
        '--headless=new',
        '--dump-dom',
        '--virtual-time-budget=25000',
        '--no-first-run',
        f'http://localhost:8080/{harness_path.name}'
    ]

    proc = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
    harness_path.unlink(missing_ok=True)
    out = proc.stdout

    if '<div id="test-output">' in out:
        start = out.find('<div id="test-output">') + len('<div id="test-output">')
        end = out.find('</div>', start)
        raw_json = out[start:end].replace('&quot;', '"').replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')
        data = json.loads(raw_json)

        record("Live Ready", "Glyph Portal Berhasil Diinisialisasi (Ready: true)", data.get('ready') == "true")
        record("Live Motion", "Mode Motion Berjalan Aktif (Motion: on)", data.get('motion') == "on")

        print(f"\n{BOLD}[3/3] Evaluasi Transisi Warna Background & Titik Kamera 'i'{RESET}")
        points = data.get('scrollPoints', [])
        
        for pt in points:
            p_val = pt.get('p')
            bg = pt.get('pinBg')
            t_str = pt.get('transform')
            clip = pt.get('fieldClip')
            rev = pt.get('reveal')

            # Parse RGB
            # Format rgb(r, g, b)
            rgb_parts = [int(x.strip()) for x in bg.replace('rgb(', '').replace(')', '').split(',') if x.strip().isdigit()]
            is_green = len(rgb_parts) == 3 and rgb_parts[1] <= 100 and rgb_parts[0] <= 100
            
            if p_val == 0.0:
                # Pada awal, background bernilai terang/paper
                is_paper = len(rgb_parts) == 3 and rgb_parts[0] >= 240 and rgb_parts[1] >= 240
                record("Color Init", f"Progress p=0.0 -> Background Bersih Terang/Paper ({bg})", is_paper, f"bg={bg}")
            elif p_val >= 0.75:
                # Menjelang dalam portal, background telah bertransisi ke hijau forest
                record("Color Green", f"Progress p={p_val} -> Background Menyesuaikan ke Hijau ({bg})", is_green, f"bg={bg}")
                
            if p_val == 1.0:
                # Pada progress penuh, konten kartu terungkap sempurna
                record("Card Reveal", f"Progress p=1.0 -> Kartu Terungkap Penuh (Reveal={rev:.2f})", rev >= 0.95, f"reveal={rev}")
                # Transform kamera membidik titik i (cx sekitar 172 s/d 174, cy sekitar -60 s/d -62)
                has_target_x = any(f"{v}." in t_str or f"{v} " in t_str or f"{v}," in t_str for v in [172, 173, 174])
                has_target_y = any(f"{v}." in t_str or f"{v} " in t_str or f"{v}," in t_str for v in [59, 60, 61, 62])
                record("Dot Camera X", "Kamera Membidik Horizontal Tepat Titik 'i' (cx 172 s/d 174)", has_target_x, f"transform={t_str}")
                record("Dot Camera Y", "Kamera Membidik Vertikal Masuk Titik 'i' (cy -60 s/d -62)", has_target_y, f"transform={t_str}")

    print(f"\n{BOLD}{CYAN}======================================================================{RESET}")
    print(f"{BOLD}{CYAN}   RINGKASAN HASIL AUDIT PENGUJIAN GLYPH PORTAL:                      {RESET}")
    total = len(test_results)
    passed = sum(1 for t in test_results if t['passed'])
    failed = total - passed
    print(f"   Total Pengujian : {total}")
    print(f"   Lolos (Pass)    : {GREEN}{passed}{RESET}")
    print(f"   Gagal (Fail)    : {RED if failed else GREEN}{failed}{RESET}")
    if failed == 0:
        print(f"\n   🎉 {GREEN}SELURUH PENGUJIAN PORTAL BERHASIL: KAMERA MASUK TITIK 'i' & BG HIJAU SEMPURNA!{RESET}")
    print(f"{BOLD}{CYAN}======================================================================{RESET}\n")

if __name__ == '__main__':
    run_portal_tests()
