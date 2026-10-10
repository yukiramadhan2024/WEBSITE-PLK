import { spawn } from 'child_process';
import fs from 'fs';
import path from 'path';

const CHROME_PATH = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
const ARTIFACT_DIR = 'C:\\Users\\Yuki\\.gemini\\antigravity-ide\\brain\\28901f44-697e-4f45-8fc4-72b418f4aca2';
const PORT = 9266;

const GREEN = '\x1b[92m';
const RED = '\x1b[91m';
const YELLOW = '\x1b[93m';
const CYAN = '\x1b[96m';
const BOLD = '\x1b[1m';
const RESET = '\x1b[0m';

const results = [];

function record(name, passed, details = "") {
  results.push({ name, passed, details });
  const status = passed ? `${GREEN}[PASS]${RESET}` : `${RED}[FAIL]${RESET}`;
  console.log(`  ${status} ${name}`);
  if (!passed && details) {
    console.log(`       ${YELLOW}-> ${details}${RESET}`);
  }
}

async function main() {
  console.log(`\n${BOLD}${CYAN}======================================================================${RESET}`);
  console.log(`${BOLD}${CYAN}   MEMULAI AUDIT LENGKAP BROWSER: RESPONSIVITAS MOBILE & MODAL BUG   ${RESET}`);
  console.log(`${BOLD}${CYAN}======================================================================${RESET}\n`);

  const chrome = spawn(CHROME_PATH, [
    '--headless=new',
    `--remote-debugging-port=${PORT}`,
    '--window-size=390,844',
    '--disable-gpu',
    'http://localhost:8080/index.html'
  ]);

  await new Promise(r => setTimeout(r, 1800));

  try {
    const tabsRes = await fetch(`http://localhost:${PORT}/json`);
    const tabs = await tabsRes.json();
    const tab = tabs.find(t => t.type === 'page');

    if (!tab) {
      console.error("Tab tidak ditemukan!");
      process.exit(1);
    }

    const ws = new WebSocket(tab.webSocketDebuggerUrl);
    await new Promise(r => ws.onopen = r);

    let msgId = 1;
    function send(method, params = {}) {
      return new Promise(resolve => {
        const id = msgId++;
        const handler = e => {
          const d = JSON.parse(e.data);
          if (d.id === id) {
            ws.removeEventListener('message', handler);
            resolve(d.result);
          }
        };
        ws.addEventListener('message', handler);
        ws.send(JSON.stringify({ id, method, params }));
      });
    }

    async function evalJS(expr) {
      const res = await send('Runtime.evaluate', { expression: expr, returnByValue: true, awaitPromise: true });
      return res?.result?.value;
    }

    await evalJS('document.fonts.ready');

    // -------------------------------------------------------------
    // 1. AUDIT HORIZONTAL OVERFLOW PADA VIEWPORT MOBILE & DESKTOP
    // -------------------------------------------------------------
    console.log(`${BOLD}[1/4] Audit Overflow & Horizontal Scroll pada Berbagai Lebar Layar${RESET}`);

    const viewports = [
      { w: 320, h: 568, label: 'Mobile Ekstrem 320px (iPhone SE 1st / CSS Min)' },
      { w: 360, h: 800, label: 'Mobile Standar 360px (Android Common)' },
      { w: 390, h: 844, label: 'Mobile Modern 390px (iPhone 12/13/14)' },
      { w: 768, h: 1024, label: 'Tablet 768px (iPad Mini)' },
      { w: 1440, h: 900, label: 'Desktop Widescreen 1440px' }
    ];

    for (const vp of viewports) {
      await send('Emulation.setDeviceMetricsOverride', {
        width: vp.w,
        height: vp.h,
        deviceScaleFactor: 2,
        mobile: vp.w < 768
      });
      await new Promise(r => setTimeout(r, 400));

      const overflow = await evalJS(`
        (() => {
          const docWidth = document.documentElement.clientWidth;
          const scrollWidth = document.documentElement.scrollWidth;
          const bodyWidth = document.body.scrollWidth;
          const hasOverflow = scrollWidth > docWidth + 0.5 || bodyWidth > docWidth + 0.5;
          return { docWidth, scrollWidth, bodyWidth, hasOverflow };
        })()
      `);

      const noOverflow = !overflow?.hasOverflow;
      record(
        `Bebas Horizontal Scroll pada ${vp.label}`,
        noOverflow,
        `scrollWidth=${overflow?.scrollWidth} > clientWidth=${overflow?.docWidth}`
      );
    }

    // -------------------------------------------------------------
    // 2. AUDIT TARGET SENTUH MINIMAL (WCAG 2.5.8 & DESIGN.md)
    // -------------------------------------------------------------
    console.log(`\n${BOLD}[2/4] Audit Ukuran Target Sentuh (Touch Target Size >= 24px)${RESET}`);

    const touchTargetInfo = await evalJS(`
      (() => {
        const interactive = document.querySelectorAll('button:not([aria-hidden="true"]), a:not([aria-hidden="true"]), [role="button"]');
        let smallTargets = [];
        interactive.forEach(el => {
          const rect = el.getBoundingClientRect();
          const style = window.getComputedStyle(el);
          if (style.display !== 'none' && style.visibility !== 'hidden' && rect.width > 0 && rect.height > 0) {
            if ((el.tagName === 'A' && el.closest('p')) || el.classList.contains('sq-card')) return;
            if (rect.width < 24 || rect.height < 24) {
              smallTargets.push(\`\${el.tagName}#\${el.id || el.className.slice(0, 20)} (\${Math.round(rect.width)}x\${Math.round(rect.height)}px)\`);
            }
          }
        });
        return { count: interactive.length, smallTargets };
      })()
    `);

    record(
      "Target Sentuh Kontrol Interaktif Memenuhi Kriteria WCAG (>= 24px)",
      (touchTargetInfo?.smallTargets || []).length === 0,
      `Kontrol terlalu kecil: ${touchTargetInfo?.smallTargets?.join(', ')}`
    );

    // -------------------------------------------------------------
    // 3. PENGUJIAN MODAL GALERI DOKUMENTASI (ITEM USER REQUEST)
    // -------------------------------------------------------------
    console.log(`\n${BOLD}[3/4] Audit Interaktivitas & Tampilan Modal Galeri Dokumentasi${RESET}`);

    // Set viewport ke 390px mobile
    await send('Emulation.setDeviceMetricsOverride', {
      width: 390,
      height: 844,
      deviceScaleFactor: 2,
      mobile: true
    });
    await new Promise(r => setTimeout(r, 300));

    // Buka modal galeri index 2 ("Aksi Sabuk Hijau & Konservasi Pekarangan")
    await evalJS('openGalleryModal(2);');
    await new Promise(r => setTimeout(r, 600));

    const modalState = await evalJS(`
      (() => {
        const modal = document.getElementById('modal-galeri');
        const isHidden = modal.classList.contains('hidden');
        const katEl = document.getElementById('modal-galeri-kategori');
        const waktuEl = document.getElementById('modal-galeri-waktu');
        const judulEl = document.getElementById('modal-galeri-judul');
        const poinList = document.getElementById('modal-galeri-poin-list');
        
        const katClass = katEl ? katEl.className : '';
        const katText = katEl ? katEl.textContent.trim() : '';
        const katStyle = katEl ? window.getComputedStyle(katEl) : null;
        const hasBorder = katStyle && parseFloat(katStyle.borderWidth) > 0;
        const hasPillShape = katClass.includes('rounded-full');
        const hasBadgeClass = katClass.includes('badge');

        const items = poinList ? Array.from(poinList.querySelectorAll('li')) : [];
        const checkIcons = poinList ? Array.from(poinList.querySelectorAll('svg, i')) : [];
        
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
          hasBadgeClass,
          itemCount: items.length,
          iconCount: checkIcons.length,
          allAreCheck,
          hasCheckCircle,
          waktuText: waktuEl ? waktuEl.textContent : '',
          judulText: judulEl ? judulEl.textContent : ''
        };
      })()
    `);

    record(
      "Modal Dokumentasi Berhasil Dibuka dengan Data Valid",
      modalState?.isOpen && (modalState?.judulText || '').includes("Sabuk Hijau"),
      `State: ${JSON.stringify(modalState)}`
    );

    const isPureText = !modalState?.hasPillShape && !modalState?.hasBadgeClass && !modalState?.hasBorder;
    record(
      "Badge Kategori Dihilangkan & Ditampilkan sebagai Teks Murni Tanpa Pill/Border",
      isPureText && modalState?.katText === "Lingkungan",
      `Kelas kategori: '${modalState?.katClass}', teks: '${modalState?.katText}', hasBorder: ${modalState?.hasBorder}`
    );

    record(
      "Ikon Centang di Capaian Dokumentasi Menggunakan 'check' (Sinkron dengan #kegiatan)",
      modalState?.allAreCheck && !modalState?.hasCheckCircle,
      `allAreCheck: ${modalState?.allAreCheck}, hasCheckCircle: ${modalState?.hasCheckCircle}, count: ${modalState?.iconCount}`
    );

    // Screenshot modal mobile 390px
    const ssResMobile = await send('Page.captureScreenshot', { format: 'png' });
    if (ssResMobile?.data) {
      const buf = Buffer.from(ssResMobile.data, 'base64');
      const outPath = path.join(ARTIFACT_DIR, 'audit_modal_galeri_mobile_390.png');
      fs.writeFileSync(outPath, buf);
      console.log(`  ${CYAN}📸 Screenshot Modal Dokumentasi Mobile (390px) Tersimpan: ${outPath}${RESET}`);
    }

    // Tutup modal
    await evalJS('closeGalleryModal();');
    await new Promise(r => setTimeout(r, 400));

    // -------------------------------------------------------------
    // 4. AUDIT DESKTOP (1440PX) & MODAL DOKUMENTASI DESKTOP
    // -------------------------------------------------------------
    console.log(`\n${BOLD}[4/4] Audit Desktop Widescreen (1440px) & Tangkapan Layar Visual${RESET}`);

    await send('Emulation.setDeviceMetricsOverride', {
      width: 1440,
      height: 900,
      deviceScaleFactor: 1,
      mobile: false
    });
    await new Promise(r => setTimeout(r, 500));

    await evalJS('openGalleryModal(2);');
    await new Promise(r => setTimeout(r, 600));

    const ssResDesktop = await send('Page.captureScreenshot', { format: 'png' });
    if (ssResDesktop?.data) {
      const buf = Buffer.from(ssResDesktop.data, 'base64');
      const outPath = path.join(ARTIFACT_DIR, 'audit_modal_galeri_desktop_1440.png');
      fs.writeFileSync(outPath, buf);
      console.log(`  ${CYAN}📸 Screenshot Modal Dokumentasi Desktop (1440px) Tersimpan: ${outPath}${RESET}`);
    }

    await evalJS('closeGalleryModal();');
    await new Promise(r => setTimeout(r, 300));

    // -------------------------------------------------------------
    // REKAPITULASI HASIL AUDIT
    // -------------------------------------------------------------
    const total = results.length;
    const passedCount = results.filter(r => r.passed).length;
    const failedCount = total - passedCount;

    console.log(`\n${BOLD}${CYAN}======================================================================${RESET}`);
    console.log(`${BOLD}   RINGKASAN HASIL AUDIT BROWSER MOBILE & DESKTOP:                   ${RESET}`);
    console.log(`   Total Pengujian : ${BOLD}${total}${RESET}`);
    console.log(`   Lolos (Pass)    : ${BOLD}${GREEN}${passedCount}{RESET}`);
    console.log(`   Gagal (Fail)    : ${BOLD}${failedCount > 0 ? RED : GREEN}${failedCount}${RESET}`);
    if (failedCount === 0) {
      console.log(`\n   ${BOLD}${GREEN}🎉 SELURUH PENGUJIAN BROWSER MOBILE & DESKTOP LOLOS 100%!${RESET}`);
    }
    console.log(`${BOLD}${CYAN}======================================================================${RESET}\n`);

    ws.close();
  } finally {
    chrome.kill();
  }
}

main().catch(err => {
  console.error("Error eksekusi:", err);
  process.exit(1);
});
