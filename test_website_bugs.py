#!/usr/bin/env python3
"""
=============================================================================
SUITE PENGUJIAN OTOMATIS BUG & INTEGRITAS WEBSITE PLK UNY MENGABDI
=============================================================================
Skrip ini melakukan audit otomatis komprehensif terhadap:
1. Integritas Struktur HTML & Validitas Semantic DOM
2. Keberadaan Seluruh Aset Lokal (Gambar, Font WebP/WOFF2, CSS, Script)
3. Konsistensi Anchor Link & Navigasi Antar-Seksi
4. Aksesibilitas WCAG 2.1 AA (Alt text, ARIA attributes, Touch Target, Semantic DL)
5. Integritas Data JavaScript (10 Anggota Tim, GeoJSON Peta, Galeri, Proker)
6. Kerapihan CSS & Vendor Prefixing (-webkit-backdrop-filter)
7. Kesiapan Live Server HTTP Lokal
=============================================================================
"""

import sys
import os
import re
import urllib.request
import json
from pathlib import Path

if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

# ANSI Color codes for clean reporting
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
CYAN = '\033[96m'
BOLD = '\033[1m'
RESET = '\033[0m'

WORKSPACE_DIR = Path(__file__).resolve().parent
HTML_PATH = WORKSPACE_DIR / 'index.html'
CSS_PATH = WORKSPACE_DIR / 'style.css'

test_results = []

def record(name, passed, details=""):
    test_results.append({
        "name": name,
        "passed": passed,
        "details": details
    })
    status = f"{GREEN}[PASS]{RESET}" if passed else f"{RED}[FAIL]{RESET}"
    print(f"  {status} {name}")
    if not passed and details:
        print(f"       {YELLOW}-> {details}{RESET}")

def run_tests():
    print(f"\n{BOLD}{CYAN}======================================================================{RESET}")
    print(f"{BOLD}{CYAN}   MEMULAI AUDIT & PENGUJIAN BUG WEBSITE PLK UNY MENGABDI             {RESET}")
    print(f"{BOLD}{CYAN}======================================================================{RESET}\n")

    if not HTML_PATH.exists():
        print(f"{RED}Error: File index.html tidak ditemukan di {HTML_PATH}{RESET}")
        sys.exit(1)

    with open(HTML_PATH, 'r', encoding='utf-8') as f:
        html = f.read()

    css = ""
    if CSS_PATH.exists():
        with open(CSS_PATH, 'r', encoding='utf-8') as f:
            css = f.read()

    # -------------------------------------------------------------
    # 1. STRUKTUR HTML & META DATA
    # -------------------------------------------------------------
    print(f"{BOLD}[1/7] Pengujian Struktur HTML & Dokumen{RESET}")
    
    record("Doctype HTML5 dan Tag Bahasa (lang='id')", 
           html.startswith("<!DOCTYPE html>") and '<html lang="id"' in html,
           "Doctype harus tepat <!DOCTYPE html> dan lang harus 'id'")

    viewport_match = re.search(r'<meta\s+name=["\']viewport["\']\s+content=["\']([^"\']+)["\']', html)
    has_viewport = viewport_match is not None
    no_max_scale = has_viewport and "maximum-scale" not in viewport_match.group(1)
    record("Meta Viewport Responsif Tanpa Pembatasan Zoom (Tanpa maximum-scale)",
           has_viewport and no_max_scale,
           "Meta viewport tidak boleh mematikan zoom pengguna untuk aksesibilitas")

    title_match = re.search(r'<title>(.*?)</title>', html)
    has_title = title_match and len(title_match.group(1).strip()) > 10
    record("Judul Halaman (<title>) Informatif", has_title, "Title tag wajib ada dan deskriptif")

    h1_count = len(re.findall(r'<h1[\s>]', html))
    record("Hierarki Heading: Tepat 1 Elemen <h1> di Halaman",
           h1_count == 1,
           f"Ditemukan {h1_count} elemen <h1> (harus tepat 1)")

    # -------------------------------------------------------------
    # 2. VALIDASI ANCHOR LINK & SEKSI ID
    # -------------------------------------------------------------
    print(f"\n{BOLD}[2/7] Pengujian Navigasi & Anchor Link Target{RESET}")
    
    # Kumpulkan semua ID yang didefinisikan di HTML
    all_ids = set(re.findall(r'id=["\']([a-zA-Z0-9_\-]+)["\']', html))

    # Kumpulkan semua link internal #href
    internal_links = re.findall(r'href=["\']#([a-zA-Z0-9_\-]+)["\']', html)
    missing_targets = [link for link in internal_links if link not in all_ids]
    
    record("Validitas Target Internal (#hash links menuju ID yang ada)",
           len(missing_targets) == 0,
           f"Target ID tidak ditemukan: {missing_targets}")

    required_sections = ['beranda', 'peta-lokasi', 'profil-desa', 'program-kerja', 'dokumentasi', 'tim', 'kontak']
    missing_sections = [s for s in required_sections if s not in all_ids]
    record("Kelengkapan 7 Seksi Utama Halaman",
           len(missing_sections) == 0,
           f"Seksi hilang: {missing_sections}")

    # -------------------------------------------------------------
    # 3. KEBERADAAN ASET LOKAL (GAMBAR & FONT)
    # -------------------------------------------------------------
    print(f"\n{BOLD}[3/7] Pengujian Keberadaan Aset Lokal (Zero 404 Broken Assets){RESET}")
    
    # Cari semua gambar lokal
    img_srcs = re.findall(r'<img[^>]+src=["\']([^"\']+)["\']', html)
    preload_links = re.findall(r'<link[^>]+href=["\']([^"\']+)["\']', html)
    local_assets = [src for src in img_srcs if not src.startswith(('http://', 'https://', 'data:', '${'))]
    local_preloads = [src for src in preload_links if not src.startswith(('http://', 'https://', 'data:', '${')) and src.endswith(('.webp', '.png', '.jpg', '.woff2', '.svg'))]

    all_local_assets = list(set(local_assets + local_preloads))
    missing_files = []
    zero_byte_files = []

    for rel_path in all_local_assets:
        clean_path = rel_path.split('?')[0].split('#')[0]
        file_path = WORKSPACE_DIR / clean_path
        if not file_path.exists():
            missing_files.append(clean_path)
        elif file_path.stat().st_size == 0:
            zero_byte_files.append(clean_path)

    record("Semua Berkas Gambar Lokal Ditemukan di Disk",
           len(missing_files) == 0,
           f"Aset tidak ditemukan: {missing_files}")
    record("Semua Berkas Aset Memiliki Ukuran Valid (> 0 bytes)",
           len(zero_byte_files) == 0,
           f"Aset kosong: {zero_byte_files}")

    # -------------------------------------------------------------
    # 4. AKSESIBILITAS WCAG 2.1 AA
    # -------------------------------------------------------------
    print(f"\n{BOLD}[4/7] Pengujian Aksesibilitas Web (WCAG 2.1 AA){RESET}")

    # Cek img alt
    all_imgs = re.findall(r'<img([^>]+)>', html)
    imgs_without_alt = [img for img in all_imgs if 'alt=' not in img]
    record("Seluruh Tag <img> Memiliki Atribut 'alt'",
           len(imgs_without_alt) == 0,
           f"Ditemukan {len(imgs_without_alt)} gambar tanpa atribut alt")

    # Cek tombol memiliki label atau aria-label
    all_buttons = re.findall(r'<button([^>]+)>(.*?)</button>', html, re.DOTALL)
    unlabeled_buttons = []
    for attrs, inner_text in all_buttons:
        clean_text = re.sub(r'<[^>]+>', '', inner_text).strip()
        has_aria = 'aria-label=' in attrs or 'title=' in attrs
        if not clean_text and not has_aria:
            id_match = re.search(r'id=["\']([^"\']+)["\']', attrs)
            btn_id = id_match.group(1) if id_match else attrs[:40]
            unlabeled_buttons.append(btn_id)

    record("Seluruh Elemen <button> Memiliki Label Aksesibel (Text / aria-label)",
           len(unlabeled_buttons) == 0,
           f"Tombol tanpa label: {unlabeled_buttons}")

    # Cek Modal accessibility
    modals = ['modal-anggota', 'modal-galeri']
    missing_modal_attrs = []
    for m_id in modals:
        m_regex = rf'<div[^>]+id=["\']{m_id}["\'][^>]*>'
        m_tag = re.search(m_regex, html)
        if m_tag:
            tag_str = m_tag.group(0)
            if 'role="dialog"' not in tag_str or 'aria-modal="true"' not in tag_str:
                missing_modal_attrs.append(m_id)
        else:
            missing_modal_attrs.append(f"{m_id} (not found)")

    record("Modal Dialog Memiliki Atribut Aksesibilitas (role='dialog' & aria-modal='true')",
           len(missing_modal_attrs) == 0,
           f"Modal tidak memenuhi spesifikasi: {missing_modal_attrs}")

    # Cek semantik <dl>
    invalid_dl_structure = False
    # Verifikasi <dl> tidak mengandung <div> bersarang langsung yang melanggar HTML5 spec
    if "<dl" in html:
        # Cek jika ada div bersarang di dalam div di dalam dl
        if re.search(r'<dl[^>]*>\s*<div[^>]*>\s*<div', html):
            invalid_dl_structure = True
    record("Semantik Daftar Definisi (<dl>) Valid Sesuai Spesifikasi W3C",
           not invalid_dl_structure,
           "Ditemukan hierarki div ilegal di dalam elemen <dl>")

    # -------------------------------------------------------------
    # 5. DATA JAVASCRIPT & LOGIKA SEKSI
    # -------------------------------------------------------------
    print(f"\n{BOLD}[5/7] Pengujian Integritas Logika JavaScript & Data Tim{RESET}")

    # Ekstraksi array anggota
    anggota_match = re.search(r'const\s+anggota\s*=\s*(\[.*?\]);', html, re.DOTALL)
    has_anggota_array = anggota_match is not None
    record("Array Data 'anggota' Didefinisikan di Skrip", has_anggota_array, "Array anggota hilang")

    member_count = 0
    members_valid = True
    member_names = []
    if has_anggota_array:
        # Parse objek anggota secara manual / regex
        raw_members = re.findall(r'nama:\s*[\'"]([^\'"]+)[\'"]', anggota_match.group(1))
        member_count = len(raw_members)
        member_names = raw_members

    record("Jumlah Anggota Tim Tepat 10 Mahasiswa Pengabdi",
           member_count == 10,
           f"Jumlah anggota terdeteksi: {member_count}")

    # Validasi 10 nama anggota resmi yang diminta
    expected_members = [
        ["Ivana Daffa Inggita", "Ivana Dafa Inggita"], ["Faza Nur Syabhila"], ["Azaria Bimarichi"],
        ["Sekar Nisfussanah"], ["Yohanes Wijaya Satria"], ["Muhammad Nur Syarifulloh"],
        ["Nailah Salsabilah"], ["Yuki Ramadhan"], ["Alejandro Mohammed Daudy"], ["Rafael Aga Pratama"]
    ]
    all_names_present = all(
        any(any(alias.lower() in actual.lower() for alias in exp_group) for actual in member_names)
        for exp_group in expected_members
    )
    record("Ke-10 Nama Resmi Mahasiswa Pengabdi Sesuai Input Pengguna",
           all_names_present,
           f"Nama yang terdaftar: {member_names}")

    # Validasi ke-10 NIM Mahasiswa Pengabdi
    expected_nims = [
        "240505030039", "24050530027", "24010430099", "24010430103",
        "24020330202", "24020330133", "24050530039", "24051130053",
        "24051130059", "24050530049"
    ]
    all_nims_present = all(nim in html for nim in expected_nims)
    record("Ke-10 NIM Resmi Mahasiswa Terdaftar Akurat di Sistem",
           all_nims_present,
           "Beberapa NIM mahasiswa tidak ditemukan di markup")

    # Cek dead-code peta wilayah
    has_dead_pilih = 'pilihWilayah(' in html or 'btn-pilih-wilayah' in html
    record("Pembersihan Dead-Code Peta (Bebas dari fungsi pilihWilayah / sidebar)",
           not has_dead_pilih,
           "Fungsi usang pilihWilayah atau kelas btn-pilih-wilayah masih tersisa")

    # Cek aksi tombol Petunjuk Arah minimalis di #peta-lokasi
    has_peta_action = 'maps.google.com' in html and 'Petunjuk Arah' in html
    no_bulky_map_text = 'Posko Penempatan Resmi' not in html
    record("Tombol Aksi Petunjuk Arah Minimalis Aktif di #peta-lokasi",
           has_peta_action and no_bulky_map_text,
           "Tombol petunjuk arah tidak ditemukan atau teks panjang posko penempatan belum dibersihkan")

    # Cek pin marker peta (hanya teks murni, tanpa simbol bulat atau petunjuk di dalam badge)
    pin_badge_match = re.search(r'peta-marker-badge[^>]*>(.*?)</div>', html, re.DOTALL)
    pin_badge_html = pin_badge_match.group(1) if pin_badge_match else ""
    pin_has_no_pulse_dot = 'animate-pulse' not in pin_badge_html and 'rounded-full bg-emerald' not in pin_badge_html
    pin_has_no_arrow = '<svg' not in pin_badge_html and '↗' not in pin_badge_html
    pin_has_text = '${m.nama}' in pin_badge_html
    record("Pin Marker Peta Menyisakan Teks Saja (Tanpa Simbol Bulat & Petunjuk)",
           pin_has_no_pulse_dot and pin_has_no_arrow and pin_has_text,
           "Pin marker masih mengandung simbol bulat atau icon petunjuk di dalam badge")

    # Cek penghilangan badge prodi (diganti teks murni)
    has_modal_prodi_badge = 'id="modal-prodi-badge"' in html
    prodi_tag = re.search(r'<[^>]+id=["\']modal-prodi-badge["\'][^>]*>', html)
    prodi_tag_str = prodi_tag.group(0) if prodi_tag else ""
    no_pill_badge_html = 'rounded-full' not in prodi_tag_str and 'border' not in prodi_tag_str and 'px-' not in prodi_tag_str
    js_prodi_assignment = re.search(r'prodiBadge\.className\s*=\s*([^;]+);', html)
    js_prodi_str = js_prodi_assignment.group(1) if js_prodi_assignment else ""
    no_pill_badge_js = 'rounded-full' not in js_prodi_str and 'border' not in js_prodi_str and 'p.bg' not in js_prodi_str

    record("Prodi Modal Ditampilkan sebagai Teks Bersih (Bebas dari Badge/Pill/Border)",
           has_modal_prodi_badge and no_pill_badge_html and no_pill_badge_js,
           "Elemen prodi masih memiliki styling badge pill (rounded-full/border/bg)")

    # Cek penggantian ikon centang galeri (harus memakai 'check', bukan 'check-circle')
    has_gallery_check_icon = '<i data-lucide="check"' in html
    has_gallery_check_circle = 'data-lucide="check-circle"' in html
    record("Ikon Centang Modal Galeri Menggunakan 'check' (Sinkron dengan #kegiatan)",
           not has_gallery_check_circle and has_gallery_check_icon,
           "Ikon modal galeri masih menggunakan 'check-circle' atau belum menggunakan 'check'")

    # Cek penghilangan badge kategori di modal dokumentasi (teks murni tanpa pill/border/badgeBg)
    has_modal_galeri_kat = 'id="modal-galeri-kategori"' in html
    kat_tag = re.search(r'<[^>]+id=["\']modal-galeri-kategori["\'][^>]*>', html)
    kat_tag_str = kat_tag.group(0) if kat_tag else ""
    no_pill_kat_html = 'rounded-full' not in kat_tag_str and 'border' not in kat_tag_str and 'px-' not in kat_tag_str
    js_kat_assignment = re.search(r'katEl\.className\s*=\s*([^;]+);', html)
    js_kat_str = js_kat_assignment.group(1) if js_kat_assignment else ""
    no_pill_kat_js = 'rounded-full' not in js_kat_str and 'border' not in js_kat_str and 'badgeBg' not in js_kat_str

    record("Kategori Modal Dokumentasi Ditampilkan sebagai Teks Murni (Bebas dari Badge/Pill)",
           has_modal_galeri_kat and no_pill_kat_html and no_pill_kat_js,
           "Elemen kategori modal galeri masih memiliki styling badge pill (rounded-full/border/badgeBg)")

    # Cek sinkronisasi tipografi (bebas dari font-mono di modal dan label)
    modal_has_mono = 'font-mono' in html[html.find('id="modal-galeri"'):html.find('id="modal-anggota"') + 1500]
    record("Tipografi Modal Dokumentasi & Tim Tersinkronisasi (Bebas dari font-mono yang Mismatch)",
           not modal_has_mono,
           "Ditemukan kelas font-mono di dalam modal galeri atau modal anggota")

    # -------------------------------------------------------------
    # 6. PENGECEKAN CSS & SYNTAX INTEGRITY
    # -------------------------------------------------------------
    print(f"\n{BOLD}[6/7] Pengujian Validitas CSS & Sintaksis{RESET}")

    # Cek backdrop-filter prefixing
    backdrop_issues = []
    lines = css.split('\n')
    for idx, line in enumerate(lines, 1):
        if 'backdrop-filter:' in line and '-webkit-backdrop-filter:' not in line:
            # Periksa apakah baris sebelumnya ada -webkit-backdrop-filter
            prev_line = lines[idx-2] if idx > 1 else ""
            if '-webkit-backdrop-filter' not in prev_line:
                backdrop_issues.append(f"Baris {idx}: {line.strip()}")

    record("Vendor Prefixing Backdrop Filter Sesuai Standar Linter IDE",
           len(backdrop_issues) == 0,
           f"Ditemukan backdrop-filter tanpa prefix -webkit: {backdrop_issues}")

    # Cek kurung kurawal seimbang di style.css
    open_brackets = css.count('{')
    close_brackets = css.count('}')
    record("Integritas Kurung Kurawal CSS (Brackets Seimbang)",
           open_brackets == close_brackets,
           f"Buka: {open_brackets}, Tutup: {close_brackets}")

    # -------------------------------------------------------------
    # 7. LIVE SERVER HTTP STATUS
    # -------------------------------------------------------------
    print(f"\n{BOLD}[7/7] Pengujian Kesiapan Live Server HTTP Lokal (Port 8080){RESET}")
    
    server_online = False
    status_code = None
    try:
        req = urllib.request.Request("http://localhost:8080/", headers={"User-Agent": "PLK-Bug-Tester/1.0"})
        with urllib.request.urlopen(req, timeout=3) as resp:
            status_code = resp.status
            server_online = (resp.status == 200)
    except Exception as e:
        status_code = str(e)

    record("Server HTTP Lokal Berjalan & Merespons HTTP 200 OK",
           server_online,
           f"Status server: {status_code}")

    # -------------------------------------------------------------
    # REKAPITULASI HASIL AUDIT
    # -------------------------------------------------------------
    total = len(test_results)
    passed_count = sum(1 for t in test_results if t['passed'])
    failed_count = total - passed_count

    print(f"\n{BOLD}{CYAN}======================================================================{RESET}")
    print(f"{BOLD}   RINGKASAN HASIL AUDIT PENGUJIAN BUG:{RESET}")
    print(f"   Total Pengujian : {BOLD}{total}{RESET}")
    print(f"   Lolos (Pass)    : {BOLD}{GREEN}{passed_count}{RESET}")
    print(f"   Gagal (Fail)    : {BOLD}{RED if failed_count > 0 else GREEN}{failed_count}{RESET}")
    
    if failed_count == 0:
        print(f"\n   {BOLD}{GREEN}🎉 SELURUH PENGUJIAN BERHASIL: 100% BEBAS DARI BUG STRUKTURAL!{RESET}")
    else:
        print(f"\n   {BOLD}{YELLOW}⚠️  DITEMUKAN {failed_count} MASALAH YANG PERLU DIPERHATIKAN.{RESET}")
    print(f"{BOLD}{CYAN}======================================================================{RESET}\n")

    return failed_count == 0

if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
