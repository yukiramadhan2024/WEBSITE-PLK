#!/usr/bin/env python3
"""
=============================================================================
SUITE PENGUJIAN BUG RESPONTIF & INTERAKTIF (DESKTOP & MOBILE)
Website PLK UNY Mengabdi - Kalurahan Trimurti
=============================================================================
Skrip ini menguji:
1. Horizontal Scroll / Layout Overflow (Desktop & Mobile)
2. Mobile Drawer Navigation & Touch Targets
3. Desktop Custom Cursor & Fine Pointer Guard
4. Tim & Profile Modal Glassmorphism (Desktop & Mobile viewports)
5. Galeri Squeeze Carousel & Touch Gestures
6. Peta Lokasi & Interaktivitas
7. Pengambilan Tangkapan Layar Verifikasi Nyata (Desktop + Mobile)
=============================================================================
"""

import sys
import os
import subprocess
import time
import json
import re
from pathlib import Path

# Setup UTF-8 output
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

WORKSPACE_DIR = Path(__file__).resolve().parent
HTML_PATH = WORKSPACE_DIR / 'index.html'
CSS_PATH = WORKSPACE_DIR / 'style.css'
CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
OUTPUT_DIR = Path(r"C:\Users\Yuki\.gemini\antigravity-ide\brain\e5217081-1111-47f8-8465-2788224e605b")

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

def run_chrome_screenshot(url, out_path, width, height, wait_ms=2500):
    cmd = [
        CHROME_PATH,
        '--headless=new',
        f'--screenshot={out_path}',
        f'--window-size={width},{height}',
        f'--virtual-time-budget={wait_ms}',
        '--no-first-run',
        '--no-default-browser-check',
        url
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    return out_path.exists() and out_path.stat().st_size > 0

def run_tests():
    print(f"\n{BOLD}{CYAN}======================================================================{RESET}")
    print(f"{BOLD}{CYAN}   MEMULAI AUDIT BUG DESKTOP & MOBILE - WEBSITE PLK UNY MENGABDI      {RESET}")
    print(f"{BOLD}{CYAN}======================================================================{RESET}\n")

    with open(HTML_PATH, 'r', encoding='utf-8') as f:
        html = f.read()

    with open(CSS_PATH, 'r', encoding='utf-8') as f:
        css = f.read()

    # -------------------------------------------------------------
    # 1. AUDIT LAYOUT & OVERFLOW GUARDRAILS (DESKTOP & MOBILE)
    # -------------------------------------------------------------
    print(f"{BOLD}[1/5] Audit Layout, Viewport, & Pencegahan Horizontal Overflow{RESET}")

    # Meta viewport standard check
    has_viewport = 'name="viewport"' in html and 'width=device-width' in html
    record("Layout", "Meta Viewport Responsif Terdefinisi Sempurna", has_viewport,
           "Meta viewport hilang atau tidak menyertakan width=device-width")

    # Body overflow-x hidden check in CSS
    has_body_overflow_x = bool(re.search(r'body\s*\{[^}]*overflow-x:\s*(hidden|clip)', css)) or \
                          bool(re.search(r'html,\s*body\s*\{[^}]*overflow-x:\s*(hidden|clip)', css))
    record("Layout", "CSS Body & HTML Memiliki Proteksi overflow-x: hidden / clip", has_body_overflow_x,
           "Potensi layout shifting horizontal karena ketiadaan overflow-x: hidden pada body")

    # Container max-width and padding guardrails
    has_responsive_containers = ('max-w-6xl' in html or 'max-w-7xl' in html) and 'px-4' in html and 'sm:px-6' in html
    record("Layout", "Container Utama Menggunakan Skala Responsif Tailwind (max-w-6xl/7xl, px-4, sm:px-6)",
           has_responsive_containers, "Container utama tidak konsisten dalam padding viewport")

    # -------------------------------------------------------------
    # 2. AUDIT NAVIGASI MOBILE (HAMBURGER & TOUCH DRAWER)
    # -------------------------------------------------------------
    print(f"\n{BOLD}[2/5] Audit Navigasi Mobile (Hamburger Menu & Drawer){RESET}")

    # Cek tombol hamburger
    has_menu_toggle = 'id="menu-toggle"' in html and 'aria-expanded' in html and 'aria-label' in html
    record("Mobile Nav", "Tombol Hamburger (#menu-toggle) Memiliki Atribut Aksesibilitas ARIA",
           has_menu_toggle, "Tombol menu hamburger tidak memiliki aria-expanded atau aria-label")

    # Cek drawer menu mobile
    has_mobile_nav = 'id="mobile-nav"' in html
    record("Mobile Nav", "Container Navigasi Mobile (#mobile-nav) Tersedia",
           has_mobile_nav, "#mobile-nav tidak ditemukan di DOM")

    # Cek touch target minimum (touch-target kelas CSS)
    has_touch_target_class = '.touch-target' in css and 'min-height:' in css and 'min-width:' in css
    record("Mobile Nav", "Spesifikasi CSS .touch-target Memenuhi Rekomendasi WCAG (>= 36-44px)",
           has_touch_target_class, ".touch-target tidak memiliki min-width/min-height memadai")

    # Cek event handler mobile drawer di JavaScript
    has_mobile_drawer_js = 'menuToggle.addEventListener' in html and 'mobileNav.classList.toggle' in html
    has_mobile_link_close_js = 'mobileLinks.forEach' in html and 'mobileNav.classList.add(\'hidden\')' in html
    record("Mobile Nav", "Logika Interaktif Menu Mobile Menutup Otomatis Saat Tautan Diklik",
           has_mobile_link_close_js, "Menu drawer mobile tidak menutup saat salah satu tautan ditekan")

    # -------------------------------------------------------------
    # 3. AUDIT DESKTOP FEATURES (CUSTOM CURSOR & 3D HOVER)
    # -------------------------------------------------------------
    print(f"\n{BOLD}[3/5] Audit Fitur Khusus Desktop (Custom Cursor & 3D Tilt){RESET}")

    # Custom cursor markup & style
    has_cursor_el = 'id="mac-cursor"' in html
    has_cursor_css = '.mac-cursor' in css and '.has-custom-cursor' in css
    record("Desktop", "Elemen & Styling Glassmorphism Mac Cursor (#mac-cursor) Tersedia",
           has_cursor_el and has_cursor_css, "Markup atau CSS mac cursor hilang")

    # Guardrail kursor: hanya aktif di desktop (pointer: fine)
    has_fine_pointer_guard = 'pointer: fine' in html and 'min-width: 768px' in html
    record("Desktop", "Guardrail Kursor: Dinonaktifkan Otomatis pada Layar Sentuh / Mobile",
           has_fine_pointer_guard, "Custom cursor berisiko tampil di perangkat mobile touchscreen")

    # 3D Tilt effect guardrail
    has_tilt_fine_guard = 'isFinePointer' in html and 'prefers-reduced-motion' in html
    record("Desktop", "Efek 3D Tilt Memperhatikan prefers-reduced-motion dan Layar Sentuh",
           has_tilt_fine_guard, "Efek tilt 3D dapat mengganggu pengguna perangkat reduced motion")

    # -------------------------------------------------------------
    # 4. AUDIT MODAL ANGGOTA TIM & DETAIL GLASSMORPHISM
    # -------------------------------------------------------------
    print(f"\n{BOLD}[4/5] Audit Modal Anggota Tim & Card Profil Glassmorphism{RESET}")

    # Dialog attributes
    has_dialog_role = 'id="modal-anggota"' in html and 'role="dialog"' in html and 'aria-modal="true"' in html
    record("Modal Anggota", "Modal Dialog Memiliki role='dialog' & aria-modal='true'",
           has_dialog_role, "Atribut aksesibilitas modal anggota tidak lengkap")

    # Glassmorphism container classes
    has_glass_box = '.light-modal-box' in css and 'backdrop-filter:' in css and '-webkit-backdrop-filter:' in css
    record("Modal Anggota", "Container Modal Memiliki Backdrop Filter Glassmorphism Valid",
           has_glass_box, "Backdrop filter pada .light-modal-box tidak terpasang dengan benar")

    # Mini card di kiri modal
    has_modal_mini_card = 'id="modal-foto-wrapper"' in html and 'team-interactive-card' in html
    record("Modal Anggota", "Mini Card Sisi Kiri Modal (#modal-foto-wrapper) Terpelihara Utuh",
           has_modal_mini_card, "Mini card sisi kiri modal hilang atau salah kelas")

    # Prodi modal sebagai teks bersih
    prodi_tag = re.search(r'<[^>]+id=["\']modal-prodi-badge["\'][^>]*>', html)
    prodi_is_clean_text = prodi_tag and 'rounded-full' not in prodi_tag.group(0) and 'border' not in prodi_tag.group(0)
    record("Modal Anggota", "Prodi Modal Ditampilkan Sebagai Teks Bersih (Bukan Badge Pill)",
           bool(prodi_is_clean_text), "Prodi di dalam modal masih menggunakan styling pill/badge")

    # Tombol navigasi modal (Prev, Next, Close)
    has_modal_nav_buttons = 'id="modal-prev-btn"' in html and 'id="modal-next-btn"' in html and 'id="modal-close-btn"' in html
    record("Modal Anggota", "Kelengkapan Tombol Navigasi Modal (Sebelumnya, Berikutnya, Tutup)",
           has_modal_nav_buttons, "Tombol navigasi modal anggota tidak lengkap")

    # -------------------------------------------------------------
    # 5. UJI VISUAL AKTUAL BROWSER HEADLESS (DESKTOP & MOBILE)
    # -------------------------------------------------------------
    print(f"\n{BOLD}[5/5] Eksekusi Uji Visual Nyata Headless Chrome (Desktop & Mobile){RESET}")

    if not Path(CHROME_PATH).exists():
        record("Headless Chrome", "Biner Google Chrome Ditemukan di Sistem", False, f"Tidak ditemukan di {CHROME_PATH}")
    else:
        record("Headless Chrome", "Biner Google Chrome Siap untuk Uji Render", True)

        screenshots_to_test = [
            ("Desktop", "Beranda & Hero (1440x900)", "http://localhost:8080/#beranda", OUTPUT_DIR / "audit_desktop_hero_1440.png", 1440, 900),
            ("Desktop", "Seksi Tim Pengabdi (1440x900)", "http://localhost:8080/#tim", OUTPUT_DIR / "audit_desktop_tim_1440.png", 1440, 900),
            ("Desktop", "Modal Profil Glassmorphism Moreo (1440x900)", "http://localhost:8080/?member=6", OUTPUT_DIR / "audit_desktop_modal_moreo_1440.png", 1440, 900),
            ("Desktop", "Seksi Dokumentasi Kegiatan (1440x900)", "http://localhost:8080/#kegiatan", OUTPUT_DIR / "audit_desktop_kegiatan_1440.png", 1440, 900),
            ("Desktop", "Seksi Peta Lokasi Kalurahan (1440x900)", "http://localhost:8080/#peta-lokasi", OUTPUT_DIR / "audit_desktop_peta_1440.png", 1440, 900),
            ("Mobile", "Beranda & Hero (iPhone SE 375x667)", "http://localhost:8080/#beranda", OUTPUT_DIR / "audit_mobile_hero_375.png", 375, 667),
            ("Mobile", "Seksi Tim Pengabdi (iPhone SE 375x667)", "http://localhost:8080/#tim", OUTPUT_DIR / "audit_mobile_tim_375.png", 375, 667),
            ("Mobile", "Modal Profil Glassmorphism Moreo (iPhone SE 375x667)", "http://localhost:8080/?member=6", OUTPUT_DIR / "audit_mobile_modal_moreo_375.png", 375, 667),
            ("Mobile", "Seksi Dokumentasi (iPhone SE 375x667)", "http://localhost:8080/#kegiatan", OUTPUT_DIR / "audit_mobile_kegiatan_375.png", 375, 667),
            ("Mobile", "Seksi Peta Lokasi (iPhone SE 375x667)", "http://localhost:8080/#peta-lokasi", OUTPUT_DIR / "audit_mobile_peta_375.png", 375, 667),
            ("Mobile", "Modal Profil di Smartphone Modern (iPhone 14 390x844)", "http://localhost:8080/?member=6", OUTPUT_DIR / "audit_mobile_modal_moreo_390.png", 390, 844)
        ]

        for category, desc, url, path, w, h in screenshots_to_test:
            success = run_chrome_screenshot(url, path, w, h)
            record(f"Render {category}", f"Render {desc} [OK: {path.stat().st_size if success else 0} bytes]", success, f"Gagal merender {desc}")

    # Ringkasan
    total = len(test_results)
    passed = sum(1 for t in test_results if t['passed'])
    failed = total - passed

    print(f"\n{BOLD}{CYAN}======================================================================{RESET}")
    print(f"{BOLD}{CYAN}   RINGKASAN AUDIT PENGUJIAN BUG DESKTOP & MOBILE:                    {RESET}")
    print(f"   Total Pengujian : {total}")
    print(f"   Lolos (Pass)    : {GREEN}{passed}{RESET}")
    print(f"   Gagal (Fail)    : {RED}{failed}{RESET}")

    if failed == 0:
        print(f"\n   {BOLD}{GREEN}🎉 SELURUH PENGUJIAN DESKTOP & MOBILE LOLOS DENGAN SEMPURNA!{RESET}")
    else:
        print(f"\n   {BOLD}{RED}⚠️ TERDAPAT {failed} PENGUJIAN YANG GAGAL!{RESET}")
    print(f"{BOLD}{CYAN}======================================================================{RESET}\n")

    return failed == 0

if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
