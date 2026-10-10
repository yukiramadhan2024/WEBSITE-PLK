# DESIGN.md: Kontrak Desain dan Rekayasa 

Kontrak untuk engineer dan agen AI. Mengatur arah kreatif, integritas konten, tipografi, warna, komposisi, mobile, copywriting, gerak, kode, UX, performa, dan aksesibilitas. Agen WAJIB memenuhi seluruh isinya sebelum menyerahkan hasil.

# 0. CARA PAKAI DAN URUTAN PRIORITAS

Jika dua aturan bertabrakan, menangkan yang lebih atas:
1. Keamanan dan aksesibilitas.
2. Integritas konten (bagian 3).
3. Arah Kreatif Proyek (bagian 2).
4. Dokumen ini.
5. Kebiasaan atau preferensi bawaan agen.

Dokumen turunan proyek (misalnya ANIMASI_SCROLL.md atau catatan desain proyek) boleh mengganti nilai tertentu di dokumen ini, selama tidak melanggar prioritas 1 dan 2. Agen mencatat penggantian itu di laporan akhir. Daftar contoh (font, pola, warna) di dokumen ini adalah contoh, BUKAN pilihan bawaan.

# 1. PRINSIP

1. Fungsi lebih dulu, keindahan menyusul. Estetika tidak boleh mengorbankan keterbacaan, aksesibilitas, atau kecepatan.
2. Setiap elemen punya alasan. Jika dihapus tidak mengubah makna atau fungsi, hapus.
3. Keputusan spesifik, bukan bawaan. Slop lahir dari tidak adanya keputusan. Setiap pilihan visual harus bisa dijelaskan lewat ide proyek.
4. Hasil lengkap dan berjalan. Tidak ada kode tanggung, tidak ada komentar "TODO implement". Data yang memang belum ada ditandai placeholder yang jelas (bagian 3), bukan dikarang.
5. Jujur pada konten. Tampilan tidak boleh mengesankan fakta, kegiatan, angka, atau bukti yang belum ada.

# 2. ARAH KREATIF PROYEK (WAJIB TERISI SEBELUM AGEN MULAI)

Agen menolak memulai desain visual jika bagian ini kosong, kecuali pemilik meminta agen mengusulkan isinya. Isi:
1. Pengguna dan perangkat utama.
2. Satu ide visual dalam dua kalimat.
3. Tiga kata sifat brand dan satu hal yang tidak boleh terjadi.
4. Dua sampai tiga referensi di luar dunia web (cetak, papan, kemasan, arsip, peta, buku).
5. Aset asli yang tersedia (foto, logo, data, teks).
6. Keputusan bentuk: radius, kepadatan, tingkat dekorasi.

Terisi sementara untuk proyek PLK UNY Mengabdi (ganti jika proyek lain atau jika pemilik ingin arah berbeda):
1. Pengguna: pengunjung dari bio Instagram lewat ponsel (webview), serta dosen penilai dan pamong kalurahan.
2. Ide visual: "buku catatan lapangan yang dirapikan". Tenang, faktual, editorial, dibangun dari tipografi, garis tipis, dan ritme jarak, bukan efek.
3. Sifat: tenang, faktual, hangat. Tidak boleh: terlihat seperti template startup, atau memajang foto buatan generator sebagai dokumentasi kegiatan nyata.
4. Referensi: laporan kegiatan cetak, papan informasi balai kalurahan, arsip lapangan.
5. Aset: foto asli, data anggota, dan nomor kontak belum tersedia (pakai placeholder).
6. Bentuk: sudut kecil, garis 1 px, satu nada warna hijau, dekorasi minimal.

Kewajiban agen: tulis berkas docs/keputusan_desain.md sebelum membangun, berisi (a) pilihan font, palet, dan tata letak beserta alasan yang terhubung ke ide visual, (b) tiga hal yang SENGAJA tidak dilakukan, (c) rujukan referensi yang dipakai.

# 3. INTEGRITAS KONTEN DAN DATA

1. Dilarang mengarang nama, angka, kutipan, testimoni, tanggal, lokasi, atau prestasi. Data yang belum ada ditulis sebagai placeholder dalam kurung siku, misalnya [Nama Lengkap], [Tanggal kegiatan].
2. Dilarang "Lorem ipsum", "John Doe", "Company Name", dan angka bulat sempurna yang dikarang (10+, 100%, 500K). Angka hanya boleh jika fakta nyata yang diberikan pemilik.
3. Data contoh yang dibutuhkan sistem saat pengembangan harus berlabel jelas CONTOH dan tidak boleh tampil di versi produksi.
4. Foto atau ilustrasi contoh tidak boleh diberi keterangan yang mengklaim kejadian nyata (minggu ke berapa, lokasi, kode dokumentasi). Foto yang tampak buatan generator tidak boleh dipresentasikan sebagai dokumentasi nyata di halaman publik.
5. Tidak ada catatan pengembang, instruksi internal, atau teks placeholder teknis yang terlihat publik. Blok yang belum siap (video, galeri) disembunyikan atau diberi penanda netral.
6. Istilah resmi konsisten di seluruh halaman (misalnya satu nama program, bukan dua).
7. Data dinamis diisolasi dalam satu konfigurasi atau skema data agar bisa diganti tanpa merusak markup.

# 4. LARANGAN SLOP (BERLAKU JUGA UNTUK PADANAN TERDEKATNYA)

Menghapus satu pola lalu memakai kembarannya (misalnya mengganti gradien ungu dengan gradien oranye, atau kartu kembar dengan bento seragam) tetap melanggar. Larangan kata dan frasa ada di bagian 8.

Tipografi dan teks:
1. Font tunggal bawaan tanpa pasangan berkontras (Inter, Roboto, Arial).
2. Satu kata miring serif di tengah judul sans serif.
3. Label mono kecil kapital ber titik atau garis tanpa informasi nyata. Label cetak (eyebrow) hanya boleh jika membawa informasi (nomor bagian, kategori nyata).
4. Judul bergradien, teks berpendar.

Visual dan warna:
1. Gradien ungu ke biru atau lavender ke cyan, neon, glow, tanpa dasar identitas merek.
2. Glassmorphism dan blur dekoratif. Blur hanya untuk lapisan overlay yang benar benar fungsional.
3. Hitam #000000 dan putih #FFFFFF murni. Beri tint pada netral.
4. Border kiri tebal berwarna pada kartu.
5. Bayangan tebal merata di semua kartu. Pembeda kedalaman memakai pergeseran warna permukaan dan garis 1 px. Bayangan hanya untuk lapisan yang benar benar melayang (menu, dialog), satu tingkat saja.
6. Radius besar di semua elemen, tombol dan tag berbentuk pil di mana mana, ikon dalam kotak berwarna, tekstur butiran atau noise dekoratif, blob melayang.

Tata letak dan komponen:
1. Tiga kartu identik berjajar (ikon, judul tebal, dua baris teks).
2. Hero rata tengah berisi judul besar, subjudul abu abu, dua tombol sama besar. Badge pil di atas judul ("Baru", "Didukung AI").
3. Logo cloud, testimoni berputar dengan nama palsu, tabel harga tiga paket, bagian statistik berisi angka bulat, FAQ akordeon tanpa pertanyaan nyata.
4. Footer empat kolom tautan padahal situs satu halaman.
5. Kartu yang naik dan bersinar saat hover sebagai satu satunya interaksi.
6. Komponen pura pura interaktif (tombol, tab, filter, toggle tanpa penanganan event nyata).
7. Emoji sebagai ikon antarmuka.

Aset:
1. Foto stok berjabat tangan, orang tertawa di depan laptop, ilustrasi 3D tokoh gelembung, avatar stok.
2. Foto buatan generator yang berisi teks atau logo tidak konsisten.
3. Ikon dekoratif tanpa makna, satu set ikon yang diulang di setiap kartu.

Gerak:
1. Fade in naik dari bawah yang identik di semua elemen.
2. Bounce, overshoot, putaran, flip 3D, animasi huruf demi huruf, pengulangan tak berujung, pembajakan scroll.

# 5. SISTEM DESAIN

Tipografi:
1. Maksimal dua keluarga font: satu untuk judul (karakter tegas), satu untuk isi dan UI (keterbacaan tinggi), dengan kontras karakter yang jelas.
2. Pilih font berdasarkan ide visual dan uji pada teks nyata proyek (termasuk teks Bahasa Indonesia yang panjang), bukan dari daftar populer. Font yang sering menjadi pilihan bawaan agen (Inter, Roboto, Arial, Poppins, Montserrat, Space Grotesk, DM Sans, Playfair Display, Bricolage Grotesque, Syne, Plus Jakarta Sans) boleh dipakai hanya jika alasannya tertulis di keputusan desain.
3. Rasio ukuran H1 terhadap teks isi minimal 2,5 sampai 3 kali. Panjang baris 45 sampai 75 karakter dengan line height 1,5 sampai 1,7.
4. Self host dalam woff2 subset, preload font utama, font display swap, fallback yang metriknya mirip untuk menekan CLS.

Warna (OKLCH, dipetakan ke variabel CSS dengan nama bermakna):
1. Token: warnaUtama (aksen dan aksi utama), permukaan, kanvas, teksUtama, teksRedup, garis, sukses, peringatan, bahaya.
2. Palet diturunkan dari identitas atau aset proyek, bukan dari preset. Satu aksen dominan, warna lain hanya untuk membedakan makna.
3. Kontras teks terhadap latar minimal 4,5 banding 1 (teks besar 3 banding 1, komponen UI 3 banding 1). Warna tidak menjadi satu satunya pembeda makna.
4. Gradien dilarang untuk dekorasi. Satu scrim datar di atas foto boleh jika perlu keterbacaan.

Spasi dan bentuk:
1. Grid 8 poin: padding dan margin kelipatan 4 atau 8 px (4, 8, 12, 16, 24, 32, 48, 64, 96). Dilarang nilai arbitrer acak.
2. Radius maksimal dua tingkat. Kontrol kecil (tombol, input, badge) 4 sampai 6 px. Kontainer (kartu, modal, ubin) 6 sampai 12 px, kecuali Arah Kreatif menetapkan lain.
3. Pemisah dengan garis 1 px atau pergeseran warna permukaan.

Ikon dan gambar:
1. Ikon SVG inline, satu keluarga, hanya yang dipakai, hanya jika menambah makna, tanpa kotak latar. Tidak ada emoji sebagai ikon.
2. Foto asli diprioritaskan. Rasio konsisten, atribut width dan height (atau rasio aspek) wajib, keterangan di bawah foto bila relevan, alt bermakna (dekoratif dikosongkan).
3. Jika foto belum ada, pakai blok netral berlabel (misalnya "Foto menyusul") dengan rasio yang sama agar tata letak tetap teruji.

# 6. KOMPOSISI

1. Satu hal dibaca pertama di setiap layar. Satu aksi utama per layar.
2. Tata letak asimetris atau bervariasi bila isi mendukung, tetapi tetap di atas satu grid dan satu skala jarak. Tinggi dan padding section tidak harus seragam, tetapi mengikuti ritme yang disengaja.
3. Whitespace adalah alat hierarki, bukan sisa ruang.
4. Elemen interaktif tidak boleh tertutup header sticky atau bilah melayang.

# 7. MOBILE DAN RESPONSIF

Mobile first. Agen WAJIB menguji tampilan dan interaksi di ukuran ponsel (320, 360, 390 px) di browser sebelum menyerahkan hasil, bukan hanya membaca kode. Untuk webview Instagram: tinggi dengan dvh (bukan vh), perhitungkan safe area, tanpa interaksi yang hanya bisa lewat hover.
1. Tanpa scroll horizontal pada lebar 320 px. Perbaiki penyebabnya di sumber: lebar tetap piksel besar, gambar tanpa batas lebar, teks atau URL panjang tanpa pemotongan kata, tabel lebar. Jangan menutupi masalah dengan overflow tersembunyi pada body atau kontainer utama. Overflow tersembunyi hanya untuk komponen yang memang memotong isinya (bingkai foto, carousel, peta).
2. Target sentuh: semua kontrol minimal 24 x 24 CSS px (WCAG 2.5.8). Aksi utama (CTA), ikon navigasi, input, dan checkbox yang disentuh jari berukuran 44 x 44 px.
3. Teks dan label: judul tidak melimpah keluar layar. Label tombol dan menu cukup singkat untuk satu baris di 320 px. Jika tetap panjang, izinkan pembungkusan yang rapi dan jaga tinggi tombol, jangan memaksa satu baris yang melimpah. Tidak ada teks terpotong canggung.
4. Elemen yang menerima fokus atau hasil lompatan anchor tidak boleh tertutup sticky header, banner melayang, atau widget obrolan. Atur scroll padding top pada dokumen dan scroll margin pada target anchor (WCAG 2.4.11).
5. Susun ulang, bukan mengecilkan. Komponen disusun ulang vertikal dengan hierarki jelas, bukan tata letak desktop yang diperkecil. Media responsif, gambar LCP versi ponsel maksimum 150 KB.
6. Uji juga: orientasi lanskap, zoom teks 200 persen, dan area aman layar berlekuk.

# 8. COPYWRITING

Aturan:
1. Suara yang jelas dan hangat, ditulis seperti orang yang benar benar mengerjakan hal ini berbicara kepada pembaca. Spesifik dan faktual. Uji obrolan: baca keras, jika tidak akan diucapkan kepada teman atau rekan kerja, tulis ulang.
2. Judul menyebut isi, bukan slogan. Gunakan kalimat aktif dan lugas, variasikan panjang kalimat, hindari pola tiga poin yang selalu sejajar dan kalimat penutup yang terlalu rapi.
3. Tombol memakai kata kerja konkret yang menjelaskan hasilnya ("Lihat kegiatan", "Hubungi tim", "Buka peta", "Hitung estimasi biaya"). Bukan "Mulai Sekarang" atau "Jelajahi Solusi".
4. Microcopy keadaan (kosong, memuat, gagal, berhasil) ditulis manusiawi dan spesifik pada konteksnya.
5. Ganti klaim abstrak dengan fakta konkret yang berasal dari data nyata (bagian 3). Contoh pola: tulis apa yang dikerjakan, untuk siapa, di mana, dan berapa lama, memakai placeholder bila datanya belum ada. Contoh: "Kami melatih [kelompok sasaran] memakai [alat atau materi] di [lokasi]." Jangan menulis angka perbandingan atau hasil yang tidak punya sumber.
6. Daftar di bawah berlaku. Simpan juga sebagai docs/kata_terlarang.txt agar bisa dicek otomatis. Pengecualian: kata dalam daftar boleh dipakai bila merupakan istilah resmi atau fakta bidang (misalnya "pemberdayaan masyarakat" sebagai nama resmi program) dan diikuti detail konkret. Yang dilarang adalah memakainya sebagai pengisi klaim kosong. Catat pengecualian di docs/kata_diizinkan.txt.

Bahasa Indonesia, kata kerja terlarang: mewujudkan, menghadirkan, memfasilitasi, memberdayakan, mengoptimalkan, menjangkau, menjelajahi, menjembatani, mengakselerasi, menemukan (sebagai ajakan tombol).
Bahasa Indonesia, kata sifat dan bunga bahasa terlarang: terpadu, sinergi, inovatif, solusi, unggul, berkelanjutan, komprehensif, mutakhir, dinamis.
Bahasa Indonesia, frasa pembuka dan transisi terlarang: "Dalam era digital yang terus berkembang", "Di tengah pesatnya perkembangan teknologi", "Dalam dunia yang serba cepat ini", "Perlu diingat bahwa", "Penting untuk dicatat".
Bahasa Indonesia, slogan dan klaim abstrak terlarang: "Hadir untuk Anda", "Hadir sebagai solusi terpadu", "Tidak hanya X, tetapi juga Y", "Bukan sekadar X, melainkan Y", "Lebih dari sekadar X", "Membangun masa depan yang lebih baik", "Perubahan nyata", "Semangat kolaborasi, inovasi, dan kreativitas", "Mulai sekarang".
Tanda baca: tanda seru beruntun, em dash sebagai pengganti tanda baca alami.
Bahasa Inggris (jika konten berbahasa Inggris): delve, harness, leverage, utilize, empower, unlock, unleash, revolutionize, seamless, robust, transformative, cutting edge, game changing, vibrant, "in today's digital age", "not X, but Y", "No X. No Y. Just Z."

# 9. GERAK

1. Interaksi mikro 150 sampai 250 ms dengan easing keluar (easeOutExpo, nilai 0,16 1 0,3 1).
2. Animasi masuk saat scroll dan hero mengikuti dokumen animasi proyek jika ada (maksimum 900 ms, hanya transform dan opasitas, sekali per elemen, konten terlihat penuh tanpa JavaScript). Jika tidak ada dokumen animasi, gunakan gerak minimal.
3. Wajib menghormati prefers reduced motion: matikan animasi transform dan pergeseran, tampilkan keadaan akhir.
4. Gerak harus bisa dihentikan bila berlangsung lebih dari 5 detik (carousel otomatis punya tombol jeda).

# 10. KEADAAN UX (CAKUPAN PENUH)

Setiap komponen yang menyentuh data atau sumber daya luar mengimplementasikan:
1. Kosong: informatif, mengarahkan ke aksi awal.
2. Memuat: skeleton proporsional dengan atribut aria busy. Tombol memuat tidak berubah dimensi.
3. Gagal: pesan spesifik dan manusiawi di samping komponen bermasalah, plus fallback (misalnya peta gagal, gambar gagal, font gagal).
4. Berhasil: konfirmasi visual yang jelas.
5. Nonaktif: tetap terbaca, atribut disabled atau aria disabled.
6. Khusus web publik: mode hemat data, koneksi lambat, JavaScript mati, dan keadaan setelah navigasi anchor atau tombol kembali.

# 11. REKAYASA

1. Ikuti stack yang sudah ada di repositori. Jangan migrasi framework tanpa diminta. Jika proyek baru: situs statis memakai HTML, CSS, dan JavaScript sederhana atau build ringan; aplikasi dinamis memakai stack modular (misalnya Next.js atau React dengan TypeScript, backend Node.js, Hono, atau Laravel, database PostgreSQL atau MySQL dengan ORM) sesuai kebutuhan nyata.
2. Pisahkan lapisan: antarmuka, hooks atau logika tampilan, layanan data, dan skema validasi. Jangan satu berkas raksasa.
3. Dependensi minimal dan dikunci versinya. Dilarang runtime compiler di browser untuk produksi (misalnya Tailwind via CDN). Aset kritis (font, ikon, pustaka peta) disalin dan dilayani sendiri, bukan dari CDN publik.
4. Validasi ganda (klien dan server) dengan pustaka skema bila ada formulir atau API. Lindungi dari XSS, CSRF, SQL injection, dan sanitasi payload. Kredensial dan kunci API hanya lewat environment variables, tidak boleh di hardcode.
5. Sertakan README berisi cara menjalankan dan membangun. Kode harus langsung berjalan secara lokal.

# 12. AKSESIBILITAS (WCAG 2.2 AA)

1. Ukuran target minimal 24 x 24 CSS px (kriteria 2.5.8, AA) dan 44 x 44 px untuk sentuhan (bagian 7).
2. Fokus terlihat (focus visible) pada semua kontrol. Ring minimal 2 px dengan kontras 3 banding 1 (praktik baik sesuai 2.4.13, yang secara resmi level AAA). Fokus tidak boleh tertutup elemen sticky (2.4.11, AA).
3. Operasi penuh dengan keyboard, urutan fokus logis, dialog mengurung fokus dan bisa ditutup dengan Escape, fokus kembali ke pemicu.
4. Semantik benar: landmark, satu H1, urutan heading, label formulir, tautan lompat ke konten, atribut lang, alt gambar, aria live untuk perubahan dinamis.
5. Konten tetap utuh pada zoom 200 persen dan lebar 320 px (reflow). Tidak ada scroll horizontal.
6. Kontras sesuai bagian 5. Warna bukan satu satunya penanda.

# 13. PERFORMA

Target (diukur di Lighthouse mobile dari server lokal, throttling bawaan):
1. LCP maksimum 2,5 detik. INP maksimum 200 ms. CLS maksimum 0,1 (proyek boleh lebih ketat).
2. Lighthouse minimal: Performance 90, Accessibility 95, Best Practices 95, SEO 95 (untuk halaman publik).
3. Anggaran awal untuk situs statis: transfer awal tanpa gambar di bawah lipatan dan tanpa pustaka malas maksimum 350 KB, font 60 KB, JavaScript halaman 30 KB, gambar LCP ponsel 150 KB.

Strategi: preload gambar LCP dengan fetchpriority high, gambar WebP atau AVIF responsif dengan srcset dan sizes, lazy load selain hero, atribut dimensi pada semua media, CSS esensial yang ringan, pecah tugas JavaScript panjang (lebih dari 50 ms), tanpa listener scroll atau resize tanpa throttle (utamakan IntersectionObserver), pustaka berat (peta, video) dimuat malas dan hanya saat diperlukan, facade untuk embed pihak ketiga.

# 14. VERIFIKASI OTOMATIS (PASANG, JANGAN HANYA PERCAYA MATA)

Pasang atau jalankan sesuai toolchain proyek, dan catat hasilnya di laporan:
1. Audit aksesibilitas otomatis dengan axe.
2. Lighthouse atau Lighthouse CI untuk skor dan metrik.
3. stylelint (atau skrip setara) yang menolak #000000, #FFFFFF, warna di luar token, dan nilai spasi di luar skala.
4. Lint yang menolak nilai arbitrer di utilitas Tailwind bila Tailwind dipakai.
5. Skrip grep atas docs/kata_terlarang.txt (dengan pengecualian dari docs/kata_diizinkan.txt), em dash, dan teks placeholder teknis di berkas yang tampil publik.
6. Pengecekan atribut width dan height (atau rasio aspek) pada gambar, iframe, dan video.
7. Pengecekan scroll horizontal di lebar 320 px, bahwa tidak ada permintaan ke CDN yang dilarang, dan tidak ada eror di console.

# 15. PROSES KERJA AGEN

1. Baca dokumen ini dan Arah Kreatif Proyek. Jika kosong, usulkan isinya dulu atau minta pemilik mengisi.
2. Tulis docs/keputusan_desain.md (bagian 2).
3. Bangun.
4. Kritik diri: jalankan di browser, ambil tangkapan layar 320, 390, dan 1440 px, periksa satu per satu terhadap bagian 4 dan bagian 8, uji dengan teks nyata yang panjang, lalu lakukan uji tutup logo: jika logo ditutup, apakah halaman masih terasa milik proyek ini? Jika tidak, ubah arah komposisi dan tipografi, bukan hanya warna.
5. Perbaiki, jalankan verifikasi otomatis (bagian 14), ulangi sampai lolos.
6. Laporan akhir (maksimum 15 baris): keputusan desain utama dan alasannya, hasil pengukuran (Lighthouse, axe), penggantian aturan dokumen turunan, asumsi, dan daftar hal yang perlu diputuskan pemilik.

# 16. GERBANG SEBELUM SERAH (CEKLIS BINER)

1. [ ] Arah Kreatif terisi dan docs/keputusan_desain.md ada, dengan alasan yang terhubung ke ide visual.
2. [ ] Tidak ada pola dari bagian 4 maupun padanan terdekatnya, dan tidak ada kata atau frasa terlarang dari bagian 8 (selain pengecualian yang tercatat).
3. [ ] Tidak ada data, nama, angka, kutipan, atau keterangan yang dikarang. Semua placeholder bertanda jelas dan tidak ada catatan pengembang yang terlihat publik.
4. [ ] Maksimal dua font berkarakter, panjang baris 45 sampai 75 karakter, tanpa hitam dan putih murni.
5. [ ] Spasi dan radius sesuai skala dan token, tidak ada nilai liar.
6. [ ] Target sentuh, fokus terlihat, kontras 4,5 banding 1, dan keyboard memenuhi bagian 12.
7. [ ] Tampilan ponsel diuji di 320, 360, dan 390 px: tanpa scroll horizontal (masalah diperbaiki di sumbernya), label tidak terpotong, fokus dan anchor tidak tertutup elemen sticky (bagian 7).
8. [ ] Semua media punya dimensi eksplisit dan alt yang benar.
9. [ ] Semua komponen interaktif punya penanganan event nyata dan keadaan lengkap (bagian 10).
10. [ ] Gerak mengikuti bagian 9 dan menghormati prefers reduced motion.
11. [ ] Tidak ada eror di console, tidak ada runtime compiler atau CDN terlarang.
12. [ ] Lighthouse dan axe memenuhi target, hasilnya dilampirkan.
13. [ ] README ada dan kode berjalan lokal.

Klausul wajib: jika satu butir saja belum terpenuhi, perbaiki dulu sebelum mengirim hasil akhir.