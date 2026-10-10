# Guardrails: Desain Web Editorial & Ergonomi Antarmuka Pengguna

## 1. Full-Bleed Hero Section dengan Navbar Floating Overlay
- Jika bilah navigasi (navbar/header) menggunakan layout overlay mengambang (`fixed top-0` atau `absolute top-0` yang tidak mengambil ruang dalam alur dokumen/flow layout normal), seksi hero **DILARANG** mengurangi tinggi navbar dengan rumus pengurangan seperti `calc(100vh - navHeight)`.
- Rumus `calc(100vh - navHeight)` akan menyebabkan tinggi hero lebih pendek dari tinggi viewport fisik pengguna, sehingga bagian atas seksi berikutnya (yang seringkali berwarna putih atau berbeda latar belakang) akan mengintip dan terlihat sebagai celah putih di bawah hero saat halaman dimuat pada `scrollY = 0`.
- **Wajib**: Gunakan `min-height: 100vh; min-height: 100svh;` secara konsisten pada CSS container dan utility class agar viewport awal selalu tertutup penuh 100% tanpa celah latar belakang seksi berikutnya.

## 2. Hierarki Informasi: Kartu Grid vs. Thumbnail Foto di Dalam Modal
- **Kartu Miniatur di Grid Halaman Utama**:
  - WAJIB menyajikan identitas visual esensial: foto potret, nama panggilan (`m.panggilan`), peran/titel tim (`m.peran`), dan indikator aksi (`Profil ↗`).
  - Ini memungkinkan pengguna melakukan pemindaian cepat (*quick scanning*) terhadap seluruh anggota tim secara langsung di halaman utama tanpa harus membuka modal satu per satu.
- **Thumbnail Foto di Dalam Dialog Modal**:
  - DILARANG menumpuk overlay teks nama dan peran di atas thumbnail foto di dalam modal.
  - Seluruh atribut tekstual (nama lengkap, peran, nama panggilan, NIM, divisi, prodi, fakultas, ringkasan peran, dan daftar tugas) dipusatkan secara eksklusif pada kolom detail di samping foto.
  - Pola ini membuat foto thumbnail di dalam modal tampil bersih, proporsional, dan bebas dari duplikasi teks yang mengganggu.

## 3. Afordansi Aksi Peta Langsung (Direct Intent Marker)
- Ketika peta interaktif berfokus pada titik tujuan tunggal (seperti posko utama atau lokasi kegiatan resmi), interaksi pengguna pada pin marker harus langsung mengeksekusi tujuan utama (*direct intent*), yaitu membuka navigasi rute Google Maps di tab baru.
- **DILARANG** menampilkan *popup information bar* atau balun teks perantara jika tidak ada opsi tambahan yang perlu dipilih pengguna. Menghilangkan lapisan perantara ini menghemat langkah interaksi dan memberikan respons seketika yang identik dengan tombol tindakan utama seperti "Petunjuk Arah".

## 4. Reduksi Beban Kognitif pada Galeri Interaktif Dinamis
- Pada galeri kegiatan yang telah mengadopsi format presentasi interaktif canggih (seperti *adaptive squeezed slats* / *squeeze carousel* yang responsif terhadap hover dan autoplay), hindari penumpukan tombol filter kategori jika seluruh item galeri telah terkurasi dengan ringkas dan mudah dijelajahi langsung.
- Penumpukan tombol filter kategori pada galeri yang sudah memiliki sistem navigasi slide atau slat akan memecah perhatian pengguna dan menambah beban kognitif (*cognitive load*). Pertahankan judul editorial dan pengantar cerita yang jelas, lalu biarkan pengguna berinteraksi langsung dengan visual foto.

## 5. Konsistensi Tipografi & Komponen Modal Editorial
- **Format Label Kategori / Prodi**:
  - DILARANG menggunakan tag badge berbentuk pil (`rounded-full`, background warna pastel, border) di dalam dialog modal.
  - WAJIB menggunakan teks murni berbobot semibold (`text-xs font-semibold text-brand-forest`) dengan pemisah titik (`•`) untuk metadata pendukung.
- **Keseragaman Ikon Centang**:
  - Seluruh poin capaian dan fitur kegiatan wajib menggunakan ikon seragam `data-lucide="check"` (bukan variasi `check-circle`).
- **Keluarga Font & Angka Tabular**:
  - Seluruh teks antarmuka diatur secara eksklusif menggunakan `Outfit` (heading/display) dan `Plus Jakarta Sans` (body/UI).
  - Hindari penggunaan kelas `font-mono` yang memanggil fallback sistem; gunakan `tabular-nums` untuk perataan angka pada counter dan NIM.
