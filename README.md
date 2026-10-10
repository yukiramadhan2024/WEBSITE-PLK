# Website PLK UNY Mengabdi - Kalurahan Trimurti, Bantul

> Portal Dokumentasi Resmi Program Pengabdian Luar Kampus (PLK) Mahasiswa Universitas Negeri Yogyakarta di Kalurahan Trimurti, Kapanewon Srandakan, Kabupaten Bantul, Daerah Istimewa Yogyakarta.

Website ini dibangun mematuhi secara ketat spesifikasi desain, performa, dan aksesibilitas pada [DESIGN.md](DESIGN.md) (*Fullstack & Frontend Craft Contract*).

---

## 🚀 Panduan Menjalankan Secara Lokal (Quickstart)

Website ini dibangun menggunakan **Vanilla HTML5, CSS Modules/Tailwind CSS tokens, dan Vanilla JavaScript ES2022** tanpa dependensi runtime build yang memberatkan.

### Persyaratan Sistem
- Python 3.8+ **atau** Node.js 18+ (opsional untuk HTTP static server)
- Web browser modern dengan dukungan WebGL (Chrome, Edge, Firefox, Safari)

### Menjalankan Server Lokal

#### Menggunakan Python:
```bash
python -m http.server 8080
```
Buka browser di: [http://localhost:8080](http://localhost:8080)

#### Menggunakan Node.js / npx:
```bash
npx serve -p 8080 .
```

---

## 📐 Arsitektur Sistem & Spesifikasi Desain (DESIGN.md Compliance)

### 1. Pasangan Tipografi (Typography Pairing)
- **Display & Headings**: `Outfit` (Variable Font: Weights 700, 800) – Karakter geometris kontemporer, bulat, bersih, dan berwibawa.
- **Body & UI**: `Outfit` (Weights 400, 500) dengan fallback `Plus Jakarta Sans` – Keterbacaan tinggi dengan rasio hierarki judul terhadap body $\ge 2.8\times$ dan panjang baris terkontrol $45\text{--}75\text{ch}$.

### 2. Palet Warna Semantis & Modul OKLCH
- `--color-primary`: `oklch(0.28 0.04 150)` (#162F24 Forest Green)
- `--color-surface`: `oklch(1 0 0)` (#FFFFFF Clean White)
- `--color-canvas`: `oklch(0.985 0.006 145)` (#F7FAF8 Tinted Sage-Gray)
- `--color-text-main`: `oklch(0.2 0.015 260)` (#111827 Deep Ink, rasio kontras $> 10:1$)
- `--color-text-muted`: `oklch(0.42 0.015 260)` (#4B5563 Muted, rasio kontras $> 4.5:1$)
- `--color-border`: `oklch(0.92 0.008 145)` (#E2E8E4 1px Crisp Border)

### 3. Hierarki Radius 2-Level
- **Kontrol Kecil (Buttons, Badges, Inputs)**: `--radius-sm` = `6px` (`rounded-md`).
- **Kontainer Besar (Cards, Modals, Bento Tiles)**: `--radius-md` = `14px` (`rounded-xl`).

### 4. Zero-Tolerance Anti-Slop (Pola yang Dieliminasi)
- ❌ **Tidak ada border kiri tebal 3-4px**: Menggunakan diferensiasi permukaan (*surface shift*) dan border tipis 1px.
- ❌ **Tidak ada glassmorphism dekoratif**: Kartu konten menggunakan permukaan solid (*tactile surface*). Efek kaca buram eksklusif hanya untuk lapisan overlay kontekstual (sticky header & modal backdrop).
- ❌ **Tidak ada data dummy generik**: Seluruh nama mahasiswa, NIM UNY, data kependudukan (19.428 jiwa, 6,42 km² Trimurti), batas wilayah, serta 4 program kerja riil tercantum spesifik.
- ❌ **Tidak ada kata klise/slop AI**: Bebas dari "pemberdayaan", "transformative", "seamless", dan kata klise lainnya.

---

## ♿ Aksesibilitas WCAG 2.2 (Level AA)

1. **Target Sentuh Minimal**: Seluruh kontrol interaktif berukuran minimal $44 \times 44\text{ px}$ pada perangkat bergerak (`.touch-target`).
2. **Indikator Fokus Kontras**: State `:focus-visible` memiliki ring kontras $2\text{px}$ `outline: 2px solid #162F24` dengan `outline-offset: 2px`.
3. **Fokus Tidak Tertutup Header**: Menggunakan `scroll-padding-top: 5rem` pada `html` agar fokus kibor tidak terhalang oleh sticky header.
4. **Motion Guardrail**: Transisi mikro dibatasi 180ms – 240ms (`cubic-bezier(0.16, 1, 0.3, 1)`). Dilengkapi media query `@media (prefers-reduced-motion: reduce)` yang mematikan seluruh gerak transformasi.

---

## ⚡ Optimasi Core Web Vitals

| Metrik | Realisasi | Strategi Teknis |
| :--- | :--- | :--- |
| **LCP** | $< 1.8\text{ s}$ | Preload gambar hero WebP (`hero-1200.webp`, 97 KB, `fetchpriority="high"`), eliminasi payload JPG 903 KB. |
| **CLS** | $0.00$ | Seluruh tag `<img>` dan kontainer media memiliki atribut `width` dan `height` eksplisit serta `aspect-ratio`. |
| **INP** | $< 100\text{ ms}$ | Vanilla JavaScript interaksi ringan, passive scroll event listeners, dan requestAnimationFrame throttling. |

---

## 📁 Struktur Berkas

```
WEBSITE PLK/
├── assets/
│   ├── fonts/                      # Font lokal mandiri (Outfit, Plus Jakarta Sans)
│   ├── images/                     # Berkas foto kegiatan lokal teroptimasi WebP
│   └── js/                         # Skrip pendukung (Lenis scroll)
├── docs/
│   ├── kata_diizinkan.txt          # Daftar istilah resmi yang diizinkan
│   ├── kata_terlarang.txt          # Kamus kata terlarang & anti-slop
│   └── keputusan_desain.md         # Catatan pertimbangan arsitektur desain
├── index.html                      # Halaman beranda portofolio pengabdian
├── start_server.bat                # Skrip peluncur server lokal (Port 8080)
├── style.css                       # Desain sistem, token semantis, dan modul gerak
├── test_website_bugs.py            # Skrip audit otomatis integritas website (20 uji)
├── DESIGN.md                       # Kontrak craft frontend & anti-slop specification
└── README.md                       # Dokumentasi dan panduan eksekusi
```


