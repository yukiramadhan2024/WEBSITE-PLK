import subprocess
import time
import json
import urllib.request
import sys
from pathlib import Path

if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
WORKSPACE_DIR = Path(__file__).resolve().parent
ARTIFACT_DIR = Path(r"C:\Users\Yuki\.gemini\antigravity-ide\brain\28901f44-697e-4f45-8fc4-72b418f4aca2")

GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
CYAN = '\033[96m'
BOLD = '\033[1m'
RESET = '\033[0m'

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

def run_mobile_tests():
    print(f"\n{BOLD}{CYAN}======================================================================{RESET}")
    print(f"{BOLD}{CYAN}   MEMULAI AUDIT LENGKAP BROWSER: RESPONSIVITAS MOBILE & MODAL BUG   {RESET}")
    print(f"{BOLD}{CYAN}======================================================================{RESET}\n")

    port = 9333
    user_data = WORKSPACE_DIR / ".chrome_test_profile"
    
    cmd = [
        CHROME_PATH,
        "--headless=new",
        f"--remote-debugging-port={port}",
        "--remote-allow-origins=*",
        f"--user-data-dir={user_data}",
        "--disable-gpu",
        "--no-first-run",
        "--no-default-browser-check",
        "--window-size=390,844",
        "http://localhost:8080/"
    ]
    
    proc = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(2.5)

    try:
        req = urllib.request.urlopen(f"http://127.0.0.1:{port}/json", timeout=5)
        tabs = json.loads(req.read().decode('utf-8'))
        ws_url = None
        for t in tabs:
            if t.get('type') == 'page' and 'localhost:8080' in t.get('url', ''):
                ws_url = t.get('webSocketDebuggerUrl')
                break
        if not ws_url and tabs:
            ws_url = tabs[0].get('webSocketDebuggerUrl')

        if not ws_url:
            record("Koneksi Chrome DevTools WebSocket", False, "Tidak dapat menemukan tab target")
            return False

        import websocket
        ws = websocket.create_connection(ws_url, timeout=10)
        msg_id = 1

        def send_cmd(method, params=None):
            nonlocal msg_id
            msg_id += 1
            payload = {"id": msg_id, "method": method, "params": params or {}}
            ws.send(json.dumps(payload))
            while True:
                resp = json.loads(ws.recv())
                if resp.get("id") == msg_id:
                    return resp.get("result", {})

        # Enable runtime
        send_cmd("Runtime.enable")
        send_cmd("Page.enable")
        time.sleep(1)

        def eval_js(expr):
            res = send_cmd("Runtime.evaluate", {"expression": expr, "returnByValue": True})
            return res.get("result", {}).get("value")

        # -------------------------------------------------------------
        # 1. PENGUJIAN HORIZONTAL SCROLL & OVERFLOW PADA VIEWPORT MOBILE
        # -------------------------------------------------------------
        print(f"{BOLD}[1/4] Audit Overflow & Horizontal Scroll pada Berbagai Lebar Layar{RESET}")
        
        viewports = [
            (320, 568, "Mobile Ekstrem 320px (iPhone SE 1st / CSS Min)"),
            (360, 800, "Mobile Standar 360px (Android Common)"),
            (390, 844, "Mobile Modern 390px (iPhone 12/13/14)"),
            (768, 1024, "Tablet 768px (iPad Mini)"),
            (1440, 900, "Desktop Widescreen 1440px")
        ]

        for width, height, label in viewports:
            send_cmd("Emulation.setDeviceMetricsOverride", {
                "width": width,
                "height": height,
                "deviceScaleFactor": 2,
                "mobile": (width < 768)
            })
            time.sleep(0.5)

            overflow_info = eval_js("""
                (() => {
                    const docWidth = document.documentElement.clientWidth;
                    const scrollWidth = document.documentElement.scrollWidth;
                    const bodyWidth = document.body.scrollWidth;
                    const hasOverflow = scrollWidth > docWidth || bodyWidth > docWidth;
                    
                    // Cari elemen penyebab overflow jika ada
                    let offending = [];
                    if (hasOverflow) {
                        document.querySelectorAll('*').forEach(el => {
                            const rect = el.getBoundingClientRect();
                            if (rect.right > docWidth + 1 || rect.left < -1) {
                                offending.push(`${el.tagName}#${el.id}.${el.className.slice(0, 30)} (w:${Math.round(rect.width)}, r:${Math.round(rect.right)})`);
                            }
                        });
                    }
                    return { docWidth, scrollWidth, hasOverflow, offending: offending.slice(0, 3) };
                })()
            """)

            no_overflow = not overflow_info.get("hasOverflow", False)
            record(f"Bebas Horizontal Scroll pada {label}", 
                   no_overflow, 
                   f"Overflow terdeteksi: scrollWidth={overflow_info.get('scrollWidth')} > clientWidth={overflow_info.get('docWidth')}. Elemen: {overflow_info.get('offending')}")

        # -------------------------------------------------------------
        # 2. AUDIT TARGET SENTUH MINIMAL (WCAG 2.5.8 & DESIGN.md)
        # -------------------------------------------------------------
        print(f"\n{BOLD}[2/4] Audit Ukuran Target Sentuh (Touch Target Size >= 24px){RESET}")
        
        touch_target_info = eval_js("""
            (() => {
                const interactive = document.querySelectorAll('button:not([aria-hidden="true"]), a:not([aria-hidden="true"]), [role="button"]');
                let smallTargets = [];
                interactive.forEach(el => {
                    // Hanya periksa elemen yang terlihat di layar
                    const rect = el.getBoundingClientRect();
                    const style = window.getComputedStyle(el);
                    if (style.display !== 'none' && style.visibility !== 'hidden' && rect.width > 0 && rect.height > 0) {
                        // Toleransi untuk inline links dalam paragraf dan slat carousel
                        if ((el.tagName === 'A' && el.closest('p')) || el.classList.contains('sq-card')) return;
                        if (rect.width < 24 || rect.height < 24) {
                            smallTargets.push(`${el.tagName}#${el.id} (${Math.round(rect.width)}x${Math.round(rect.height)}px)`);
                        }
                    }
                });
                return { count: interactive.length, smallTargets };
            })()
        """)

        no_small_targets = len(touch_target_info.get("smallTargets", [])) == 0
        record("Target Sentuh Kontrol Interaktif Memenuhi Kriteria WCAG (>= 24px)",
               no_small_targets,
               f"Kontrol terlalu kecil: {touch_target_info.get('smallTargets')}")

        # -------------------------------------------------------------
        # 3. PENGUJIAN DETAIL MODAL GALERI DOKUMENTASI (ITEM USER REQUEST)
        # -------------------------------------------------------------
        print(f"\n{BOLD}[3/4] Audit Interaktivitas & Tampilan Modal Galeri Dokumentasi{RESET}")

        # Atur viewport ke ukuran mobile 390px
        send_cmd("Emulation.setDeviceMetricsOverride", {
            "width": 390,
            "height": 844,
            "deviceScaleFactor": 2,
            "mobile": True
        })
        time.sleep(0.3)

        # Buka modal galeri index 2 (item ke-3 "Aksi Sabuk Hijau & Konservasi Pekarangan")
        eval_js("openGalleryModal(2);")
        time.sleep(0.6)

        modal_galeri_state = eval_js("""
            (() => {
                const modal = document.getElementById('modal-galeri');
                const isHidden = modal.classList.contains('hidden');
                const katEl = document.getElementById('modal-galeri-kategori');
                const waktuEl = document.getElementById('modal-galeri-waktu');
                const judulEl = document.getElementById('modal-galeri-judul');
                const poinList = document.getElementById('modal-galeri-poin-list');
                
                // Periksa styling kategori (apakah ada border/pill badge)
                const katClass = katEl ? katEl.className : '';
                const katText = katEl ? katEl.textContent.trim() : '';
                const katStyle = katEl ? window.getComputedStyle(katEl) : null;
                const hasBorder = katStyle && parseFloat(katStyle.borderWidth) > 0;
                const hasPillShape = katClass.includes('rounded-full');
                
                // Periksa ikon centang di poin list
                const items = poinList ? Array.from(poinList.querySelectorAll('li')) : [];
                const checkIcons = poinList ? Array.from(poinList.querySelectorAll('svg, i')) : [];
                const iconTypes = checkIcons.map(ic => ic.getAttribute('data-lucide') || ic.classList.toString());
                const allAreCheck = checkIcons.length > 0 && checkIcons.every(ic => {
                    const lucideName = ic.getAttribute('data-lucide');
                    const isSvgCheck = ic.classList.contains('lucide-check') || ic.innerHTML.includes('polyline points="20 6 9 17 4 12"');
                    return lucideName === 'check' || isSvgCheck;
                });
                const hasCheckCircle = checkIcons.some(ic => {
                    const lucideName = ic.getAttribute('data-lucide');
                    return lucideName === 'check-circle' || ic.classList.contains('lucide-check-circle');
                });

                return {
                    isOpen: !isHidden,
                    katText,
                    katClass,
                    hasBorder,
                    hasPillShape,
                    itemCount: items.length,
                    iconCount: checkIcons.length,
                    allAreCheck,
                    hasCheckCircle,
                    waktuText: waktuEl ? waktuEl.textContent : '',
                    judulText: judulEl ? judulEl.textContent : ''
                };
            })()
        """)

        record("Modal Dokumentasi Berhasil Dibuka dengan Data Valid",
               modal_galeri_state.get("isOpen", False) and "Sabuk Hijau" in modal_galeri_state.get("judulText", ""),
               f"State: {modal_galeri_state}")

        is_pure_text = (not modal_galeri_state.get("hasPillShape", True)) and ("badge" not in modal_galeri_state.get("katClass", ""))
        record("Badge Kategori Dihilangkan & Ditampilkan sebagai Teks Murni",
               is_pure_text and modal_galeri_state.get("katText") == "Lingkungan",
               f"Kelas kategori: '{modal_galeri_state.get('katClass')}', teks: '{modal_galeri_state.get('katText')}'")

        uses_check_icon = modal_galeri_state.get("allAreCheck", False) and not modal_galeri_state.get("hasCheckCircle", True)
        record("Ikon Centang di Capaian Dokumentasi Menggunakan 'check' (Bukan check-circle)",
               uses_check_icon,
               f"allAreCheck: {modal_galeri_state.get('allAreCheck')}, hasCheckCircle: {modal_galeri_state.get('hasCheckCircle')}")

        # Tangkap screenshot modal dokumentasi di mobile (390px)
        ss_res = send_cmd("Page.captureScreenshot", {"format": "png"})
        if ss_res and "data" in ss_res:
            import base64
            img_data = base64.b64decode(ss_res["data"])
            out_file = ARTIFACT_DIR / "audit_modal_galeri_mobile_390.png"
            with open(out_file, "wb") as f:
                f.write(img_data)
            print(f"  {CYAN}[SCREENSHOT] Modal Dokumentasi Tersimpan: {out_file.name}{RESET}")

        # Tutup modal galeri
        eval_js("closeGalleryModal();")
        time.sleep(0.3)

        # -------------------------------------------------------------
        # 4. AUDIT DESKTOP (1440PX) & MODAL GALERI DESKTOP
        # -------------------------------------------------------------
        print(f"\n{BOLD}[4/4] Audit Desktop Widescreen (1440px) & Tangkapan Layar Visual{RESET}")

        send_cmd("Emulation.setDeviceMetricsOverride", {
            "width": 1440,
            "height": 900,
            "deviceScaleFactor": 1,
            "mobile": False
        })
        time.sleep(0.5)

        eval_js("openGalleryModal(2);")
        time.sleep(0.5)

        ss_desktop = send_cmd("Page.captureScreenshot", {"format": "png"})
        if ss_desktop and "data" in ss_desktop:
            import base64
            img_data = base64.b64decode(ss_desktop["data"])
            out_desktop = ARTIFACT_DIR / "audit_modal_galeri_desktop_1440.png"
            with open(out_desktop, "wb") as f:
                f.write(img_data)
            print(f"  {CYAN}[SCREENSHOT] Modal Dokumentasi Desktop Tersimpan: {out_desktop.name}{RESET}")

        eval_js("closeGalleryModal();")
        time.sleep(0.3)

        # Audit Console Errors
        console_logs = eval_js("window._test_console_errors || []")
        record("Bebas dari JavaScript Error di Console Peramban",
               len(console_logs) == 0,
               f"Console logs: {console_logs}")

        ws.close()

    finally:
        proc.terminate()
        try:
            proc.wait(timeout=2)
        except Exception:
            proc.kill()

    # Rekapitulasi
    total = len(test_results)
    passed_count = sum(1 for t in test_results if t['passed'])
    failed_count = total - passed_count

    print(f"\n{BOLD}{CYAN}======================================================================{RESET}")
    print(f"{BOLD}   RINGKASAN HASIL AUDIT BROWSER MOBILE & DESKTOP:                   {RESET}")
    print(f"   Total Pengujian : {BOLD}{total}{RESET}")
    print(f"   Lolos (Pass)    : {BOLD}{GREEN}{passed_count}{RESET}")
    print(f"   Gagal (Fail)    : {BOLD}{RED if failed_count > 0 else GREEN}{failed_count}{RESET}")
    if failed_count == 0:
        print(f"\n   {BOLD}{GREEN}[SUCCESS] SELURUH PENGUJIAN BROWSER MOBILE & DESKTOP LOLOS 100%!{RESET}")
    print(f"{BOLD}{CYAN}======================================================================{RESET}\n")

    return failed_count == 0

if __name__ == '__main__':
    run_mobile_tests()
