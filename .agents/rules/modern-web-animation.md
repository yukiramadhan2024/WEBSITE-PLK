# Guardrails: SVG Clip-Path & Scroll-Driven Animation Engines

## 1. Invarian SVG `<clipPath>` untuk CSS `clip-path: url(#...)`
- **DILARANG** membungkus elemen grafis/teks di dalam tag `<g transform="...">` di dalam `<clipPath>` jika clip-path tersebut direferensikan oleh elemen HTML via CSS `clip-path: url(#...)`.
- Chromium/Blink memiliki bug rendering di mana matriks transformasi `<g>` di dalam `<clipPath>` HTML diabaikan atau memicu kalkulasi kliping kosong (elemen menghilang atau layar menjadi putih/transparan).
- **Wajib**: Terapkan atribut `transform` secara langsung pada elemen anak grafis (misal `<text transform="...">`, `<path transform="...">`, `<circle transform="...">`).

## 2. Larangan Timer Stall Palsu Berbasis Wall-Clock Mount Time
- Pada komponen scroll-driven / camera zoom, **DILARANG** menggunakan timer absolut sejak script load (`performance.now() - mountedAt > X`) untuk menentukan apakah animasi 'stalled' atau gagal.
- Pengguna membaca konten di bagian atas halaman dengan durasi tidak terduga sebelum melakukan scroll. Menggunakan timer absolut akan mematikan animasi secara prematur.
- Status statis/fallback HANYA boleh dipicu oleh `prefers-reduced-motion` atau ketiadaan dukungan API penting (misal `IntersectionObserver`).

## 3. Sinkronisasi Lenis / Smooth-Scroll dengan Custom RAF Engines
- Jika halaman menggunakan Lenis Momentum Scroll dan komponen interaktif mandiri yang memiliki loop RAF sendiri, komponen harus mengekspos fungsi callback scroll global (misal `window.componentScroll`) dan didaftarkan pada `lenis.on('scroll', ...)`.

## 4. Presisi Koordinat Kamera pada Karakter Majemuk (Compound Glyphs)
- Untuk karakter dengan lebih dari satu komponen tinta (misalnya huruf 'i' yang memiliki titik dan batang terpisah oleh celah spasi putih), kalkulasi target kamera HARUS mengisolasi klaster komponen secara spesifik.
- DILARANG membidik titik tengah bounding box karakter secara naif jika target yang diinginkan adalah bagian kecil tertentu (seperti titik 'i'), karena titik tengah akan jatuh pada celah kosong (*whitespace gap*) dan menyebabkan layar menjadi putih kosong (*blank white void*) saat diperbesar dengan skala tinggi.
- Gunakan pemindaian raster klaster tinta teratas atau metrik font deterministik untuk membidik tepat ke tengah komponen target.

## 5. Interpolasi Warna Latar Belakang Scroll-Driven & Pencegahan Lag Transisi
- Hindari percabangan warna biner diskrit (`if (progress >= 0.95) bg = green else bg = white`) yang menyebabkan efek kedip/lompat mendadak atau tampilan putih kosong sebelum batas akhir.
- Gunakan interpolasi warna berbasis matematika mulus (`smooth(min, max, t)`) yang dihitung langsung pada fungsi `paint(progress)` per frame render scroll.
- Nonaktifkan CSS `transition` pada container pin saat digerakkan oleh scroll aktif (`.glyph-portal[data-gp-motion="on"] [data-gp-pin] { transition: none; }`) untuk mencegah desinkronisasi atau lag frame 200ms terhadap gerakan roda mouse pengguna.

## 6. Pengukuran Geometri Teks SVG (SVG DOM Geometry First vs Canvas 2D)
- **DILARANG** mengandalkan Canvas 2D (`context.measureText()`) sebagai acuan koordinat tunggal untuk elemen teks SVG `<text>` di dalam `<clipPath>`.
- Canvas 2D tidak secara otomatis mewarisi atau mencerminkan aturan layout per-karakter SVG browser, terutama properti seperti `letter-spacing` (misalnya `-0.02em`), kerning SVG, dan layout glyph mesin rendering SVG.
- **Wajib**: Gunakan metode bawaan standar SVG DOM (`SVGTextContentElement`):
  - `glyph.getStartPositionOfChar(index)`
  - `glyph.getExtentOfChar(index)`
  - `glyph.getEndPositionOfChar(index)`
  pada elemen `<text>` aktual untuk memperoleh koordinat ruang pengguna (*SVG user coordinate system*) yang 100% sinkron dengan aturan CSS dan layout fisik glyph di layar.
- **Penting**: Selalu lepaskan sementara atribut `transform` (`glyph.removeAttribute("transform")`) sebelum memanggil metode pengukuran SVG agar koordinat yang diperoleh adalah koordinat murni tanpa offset transformasi aktif, lalu kembalikan atribut `transform` setelah pengukuran.

## 7. Amplifikasi Galat (Error Amplification) pada Zoom Skala Tinggi (>50x)
- Pada animasi kamera tipe zoom skala tinggi (skala 50x–150x), galat koordinat sekecil 5px–8px pada font dasar (100px) akan teramplifikasi menjadi 500px–1.200px di layar, mendorong target keluar dari viewport ke arah berlawanan.
- Setiap target kamera titik mikro WAJIB diverifikasi simetri posisinya di layar (`screenCenter = W/2, H/2`) melalui audit visual headless browser pada progress zoom menengah (`p = 0.50`) dan tingkat lanjut (`p = 0.75`).

