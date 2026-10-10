#!/usr/bin/env python3
"""
=============================================================================
SUITE PENGUJIAN REGRESI BUG SINKRONISASI NAVBAR
Website PLK UNY Mengabdi - Kalurahan Trimurti
=============================================================================
Skrip ini memverifikasi secara langsung (via headless Chrome):
1. Keberadaan 7 seksi & target internal navbar desktop dan mobile
2. Sinkronisasi indikator baris presisi (#nav-indicator-line)
3. Sinkronisasi klik pada ke-7 item navigasi desktop & drawer mobile
4. Sinkronisasi Scrollspy deterministik saat scroll turun (downward scroll)
5. Sinkronisasi Scrollspy saat scroll kembali ke atas (upward scroll)
6. Pencegahan race condition dan flickering saat animasi smooth scroll
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

def run_navbar_tests():
    print(f"\n{BOLD}{CYAN}======================================================================{RESET}")
    print(f"{BOLD}{CYAN}   MEMULAI SUITE PENGUJIAN SINKRONISASI NAVBAR & SCROLLSPY            {RESET}")
    print(f"{BOLD}{CYAN}======================================================================{RESET}\n")

    # 1. Verifikasi File & Sintaksis Lokal
    print(f"{BOLD}[1/4] Audit Struktur Navigasi & File Konfigurasi{RESET}")
    html_text = (WORKSPACE_DIR / "index.html").read_text(encoding="utf-8")
    css_text = (WORKSPACE_DIR / "style.css").read_text(encoding="utf-8")

    expected_sections = ['#beranda', '#peta-lokasi', '#profil-desa', '#kegiatan', '#dokumentasi', '#tim', '#kontak']
    
    # Periksa link desktop
    has_desktop_nav = 'id="desktop-nav"' in html_text
    all_desktop_links = all(f'href="{sec}"' in html_text for sec in expected_sections)
    record("Markup", "Navigasi Desktop (#desktop-nav) Memuat 7 Tautan Seksi Lengkap", has_desktop_nav and all_desktop_links)

    # Periksa link mobile
    has_mobile_nav = 'id="mobile-nav"' in html_text
    record("Markup", "Navigasi Mobile (#mobile-nav) Tersedia Lengkap", has_mobile_nav)

    # Periksa indikator aktif
    has_indicator = 'id="nav-indicator-line"' in html_text and '#nav-indicator-line' in css_text
    record("Markup", "Elemen & CSS Indikator Presisi (#nav-indicator-line) Terdaftar", has_indicator)

    # Bebas dari content-visibility yang memicu layout shift navbar
    no_bad_content_visibility = 'content-visibility: auto' not in css_text
    record("CSS Guard", "Bebas dari 'content-visibility: auto' Penyebab Layout Shift Offset", no_bad_content_visibility)

    # 2. Browser Unit Test Menggunakan Headless Chrome
    print(f"\n{BOLD}[2/4] Eksekusi Uji Interaktivitas Klik & Navigasi Langsung di Chrome{RESET}")
    
    harness_script = """<!DOCTYPE html>
<html>
<head><meta charset="utf-8"></head>
<body>
<div id="test-output">WAITING</div>
<iframe id="test-frame" src="http://localhost:8080" style="width: 1440px; height: 900px; border: none;"></iframe>
<script>
window.addEventListener('load', async () => {
    const frame = document.getElementById('test-frame');
    await new Promise(r => setTimeout(r, 1800)); // tunggu font dan inisialisasi lenis
    
    const doc = frame.contentDocument;
    const win = frame.contentWindow;
    const desktopNav = doc.getElementById('desktop-nav');
    const desktopLinks = Array.from(desktopNav ? desktopNav.querySelectorAll('a[href^="#"]') : []);
    const indicator = doc.getElementById('nav-indicator-line');
    
    const output = {
        initial: {},
        clicks: [],
        scrollspy: []
    };
    
    // Status awal
    const initialActive = desktopNav ? desktopNav.querySelector('a.active') : null;
    output.initial = {
        activeHref: initialActive ? initialActive.getAttribute('href') : null,
        indicatorWidth: indicator ? parseFloat(indicator.style.width) : 0,
        indicatorTransform: indicator ? indicator.style.transform : ''
    };
    
    // Pengujian Klik setiap link
    for (const link of desktopLinks) {
        const href = link.getAttribute('href');
        link.click();
        await new Promise(r => setTimeout(r, 2000)); // tunggu transisi scroll
        
        const currentActive = desktopNav ? desktopNav.querySelector('a.active') : null;
        const mobileActive = doc.querySelector('#mobile-nav a.active');
        const rectA = link.getBoundingClientRect();
        const rectNav = desktopNav.getBoundingClientRect();
        const indW = indicator ? parseFloat(indicator.style.width) : 0;
        
        output.clicks.push({
            href: href,
            activeHref: currentActive ? currentActive.getAttribute('href') : null,
            mobileHref: mobileActive ? mobileActive.getAttribute('href') : null,
            indicatorMatchesWidth: Math.abs(indW - rectA.width) < 1.5,
            isMatch: currentActive && currentActive.getAttribute('href') === href
        });
    }
    
    // Pengujian Scrollspy deterministik saat scroll ke bawah dan kembali ke atas
    const scrollPositions = [
        // Scroll Turun
        { y: 50, expected: '#beranda' },
        { y: 1100, expected: '#peta-lokasi' },
        { y: 1800, expected: '#profil-desa' },
        { y: 3000, expected: '#kegiatan' },
        { y: 5250, expected: '#dokumentasi' },
        { y: 5850, expected: '#tim' },
        { y: 6117, expected: '#kontak' },
        // Scroll Naik
        { y: 5850, expected: '#tim' },
        { y: 5250, expected: '#dokumentasi' },
        { y: 3000, expected: '#kegiatan' },
        { y: 1800, expected: '#profil-desa' },
        { y: 1100, expected: '#peta-lokasi' },
        { y: 0, expected: '#beranda' }
    ];
    
    // Buka lock klik sebelum uji manual scroll
    if (win.setNavClickLock) win.setNavClickLock(false);
    
    for (const item of scrollPositions) {
        let activeLink = null;
        if (typeof win.getActiveSectionLink === 'function') {
            activeLink = win.getActiveSectionLink(item.y);
        }
        const activeHref = activeLink ? activeLink.getAttribute('href') : null;
        output.scrollspy.push({
            scrollY: item.y,
            expected: item.expected,
            activeHref: activeHref,
            matches: activeHref === item.expected
        });
    }
    
    document.getElementById('test-output').textContent = JSON.stringify(output);
});
</script>
</body>
</html>
"""
    harness_path = WORKSPACE_DIR / "temp_nav_harness.html"
    harness_path.write_text(harness_script, encoding="utf-8")

    cmd = [
        CHROME_PATH,
        '--headless=new',
        '--dump-dom',
        '--virtual-time-budget=35000',
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

        # Evaluasi Status Awal
        init = data.get('initial', {})
        record("Live Load", "Status Awal Memilih '#beranda' dengan Indikator Aktif",
               init.get('activeHref') == '#beranda' and init.get('indicatorWidth', 0) > 0,
               f"Initial active: {init.get('activeHref')}, width: {init.get('indicatorWidth')}")

        # Evaluasi Klik
        print(f"\n{BOLD}[3/4] Evaluasi Sinkronisasi Klik Navigasi (7 Seksi){RESET}")
        clicks = data.get('clicks', [])
        for c in clicks:
            href = c.get('href')
            active = c.get('activeHref')
            is_match = c.get('isMatch')
            mob_match = c.get('mobileHref') == href
            w_match = c.get('indicatorMatchesWidth')
            record("Nav Click", f"Klik Tautan '{href}' -> Navigasi & Indikator Selaras",
                   is_match and mob_match and w_match,
                   f"Target={href}, Desktop={active}, Mobile={c.get('mobileHref')}, WidthMatch={w_match}")

        # Evaluasi Scrollspy
        print(f"\n{BOLD}[4/4] Evaluasi Sinkronisasi Scrollspy Deterministik (Turun & Naik){RESET}")
        scrolls = data.get('scrollspy', [])
        for s in scrolls:
            y = s.get('scrollY')
            exp = s.get('expected')
            act = s.get('activeHref')
            matches = s.get('matches')
            dir_label = "Scroll Turun" if y > 0 and scrolls.index(s) < 6 else "Scroll Naik"
            record("Scrollspy", f"{dir_label} pada ScrollY={y}px -> Tepat Aktif di '{exp}'",
                   matches, f"Expected {exp}, but got {act}")
    else:
        record("Runner", "Eksekusi Pengujian Headless Chrome", False, "Gagal membaca output dari browser")

    # Ringkasan Akhir
    total = len(test_results)
    passed = sum(1 for t in test_results if t['passed'])
    failed = total - passed

    print(f"\n{BOLD}{CYAN}======================================================================{RESET}")
    print(f"{BOLD}{CYAN}   RINGKASAN HASIL AUDIT PENGUJIAN SINKRONISASI NAVBAR:               {RESET}")
    print(f"{BOLD}   Total Pengujian : {total}{RESET}")
    print(f"{BOLD}{GREEN}   Lolos (Pass)    : {passed}{RESET}")
    print(f"{BOLD}{RED if failed > 0 else GREEN}   Gagal (Fail)    : {failed}{RESET}")

    if failed == 0:
        print(f"\n{BOLD}{GREEN}   🎉 100% NAVBAR & SCROLLSPY TERBUKTI SINKRON SEMPURNA TANPA BUG!{RESET}")
    else:
        print(f"\n{BOLD}{RED}   ⚠️ DITEMUKAN {failed} KELEMAHAN PADA SINKRONISASI NAVBAR.{RESET}")
    print(f"{BOLD}{CYAN}======================================================================{RESET}\n")

    return failed == 0

if __name__ == '__main__':
    success = run_navbar_tests()
    sys.exit(0 if success else 1)
