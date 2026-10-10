# Dokumen Keputusan Desain (Design Decision Record)
**Proyek:** PLK UNY Mengabdi - Kalurahan Trimurti, Kapanewon Srandakan, Bantul  
**Kepatuhan:** Kontrak Rekayasa & Desain [DESIGN.md](../DESIGN.md)

---

## 1. Arah Kreatif & Ide Visual
- **Ide Visual:** *"Buku catatan lapangan yang dirapikan"*. Tenang, faktual, editorial, dan hangat. Desain dibangun dari kekuatan tipografi, garis tipis 1px presisi, dan ritme jarak (spasi terukur), bukan efek visual murahan (*AI-slop*).
- **Target Pengguna:** Pengunjung bio Instagram melalui peramban ponsel (*in-app webview*), dosen pembimbing lapangan, pamong Kalurahan Trimurti, dan masyarakat mitra.
- **Tiga Sifat Identitas:** Tenang, Faktual, Hangat.
- **Satu Hal yang Tidak Boleh Terjadi:** Terlihat seperti template SaaS/startup generik, atau menampilkan kartu gelap terisolasi di halaman bertema terang.

---

## 2. Tipografi & Skala Hierarki
- **Keluarga Font Utama Modern:** `Outfit` (Variable Font: bobot 100–900). Karakter sans-serif geometrik kontemporer, bulat, bersih, dan segar (seperti tipografi Airbnb, Spotify, dan Notion). Bebas dari kesan kaku maupun kesan kuno (*jadul*).
- **Fallback Font:** `Plus Jakarta Sans`, sans-serif.
- **Display & Headings:** `Outfit` dengan bobot `font-extrabold` (800) dan `font-bold` (700), *letter-spacing* rapat `-0.02em` untuk hierarki visual modern dan dinamis.
- **Body & UI Text:** `Outfit` bobot regular (400) dan medium (500) dengan *line-height* 1.5–1.7 untuk kenyamanan baca optimal.
- **Pemuatan Aset:** Self-hosted WOFF2 lokal (`assets/fonts/Outfit-Variable.woff2`), `font-display: swap`, preload font kritis di `<head>`, zero CDN eksternal.

---

## 3. Sistem Palet Warna (Semantic Brand Tokens)
- `--color-primary` / `--color-forest` (`#162F24`): Hijau botol dalam yang merepresentasikan kesuburan pertanian Trimurti dan identitas akademis UNY.
- `--color-canvas` (`#F8FAFC`): Latar belakang netral hangat bersih (bukan `#FFFFFF` silau murni).
- `--color-surface` (`#FFFFFF`): Permukaan kartu bertekstur taktil dengan batas tipis 1px (`#E2E8E4`).
- `--color-sage` (`#EBF1EC`): Aksen lembut permukaan interaktif.
- `--color-ink` (`#0F172A`): Teks utama berbobot tinggi (bukan `#000000` pekat).
- `--color-muted` (`#64748B`): Teks pendukung dengan rasio kontras $\ge 4.5:1$ (memenuhi WCAG 2.2 AA).

---

## 4. Tiga Hal yang Sengaja Tidak Dilakukan (Deliberate Non-Goals)
1. **Tidak Menggunakan Elemen AI-Slop (Garis Dekoratif & Eyebrow Kapital Mengambang):** Garis 24px (`.gerakGarisLabel`) dan badge kapital lebar telah dihapus seluruhnya dan digantikan dengan penanda bab editorial bernomor (`01 / Wilayah`, `02 / Pengantar`, `03 / Pilar`, `04 / Dokumentasi`, `05 / Tim`).
2. **Tidak Menggunakan Komponen Pura-Pura Interaktif (Fake Video Player):** Blok video fiktif dengan cap waktu "12:45 Durasi" dan tombol putar palsu di seksi dokumentasi telah dibersihkan sepenuhnya.
3. **Tidak Menampilkan Placeholder Kotak Abu-Abu ("Foto Anggota"):** Ke-10 mahasiswa pengabdi kini memiliki foto potret dokumenter beresolusi tinggi nyata dengan rasio 3:4.
4. **Tidak Menggunakan Istilah "KKN" atau "Kuliah Kerja Nyata":** Mengikuti instruksi eksplisit pengguna dan arahan akademik resmi, seluruh istilah dan foto diselaraskan menjadi "PLK" (*Pengabdian Luar Kampus*).

---

## 5. Rujukan Referensi Non-Web
1. Laporan Pengabdian Lapangan Cetak LPPM UNY (layout laporan kertas bersih, tipografi tenang, nomor urut tegas).
2. Papan Pengumuman & Monografi Kalurahan Trimurti di Balai Desa Srandakan (peta terarah, data demografi riil, kejelasan kontak pamong).
3. Lembar Arsip Dokumentasi Kegiatan Balai RW (foto lanskap proporsional dengan takarir waktu, lokasi, dan ringkasan aksi konkret).


