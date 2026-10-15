# TSP Metaheuristic: Simulated Annealing, Tabu Search, and VNS

Aplikasi berbasis **Streamlit** untuk menyelesaikan permasalahan *Traveling Salesman Problem* (TSP) dan membandingkan tiga algoritma metaheuristik: **Simulated Annealing (SA)**, **Tabu Search (TS)**, dan **Variable Neighborhood Search (VNS)**.

Aplikasi menyediakan input data kota, pembentukan solusi awal, optimasi rute, visualisasi, analisis hasil, serta eksperimen multi-run untuk mengevaluasi kualitas solusi dan waktu komputasi setiap algoritma.

## Fitur Utama

- **Data Input:** menambahkan kota melalui klik kanvas X-Y, generate koordinat acak, input manual, upload Excel/CSV, dan menggunakan dataset contoh.
- **Distance Setting:** memilih Euclidean atau Manhattan distance.
- **Initial Solution:** membentuk rute awal menggunakan Nearest Neighbor (NN), Nearest Insertion (NI), Cheapest Insertion (CI), Farthest Insertion (FI), Arbitrary Insertion (AI), atau rute manual.
- **Local Search:** menerapkan 2-opt pada solusi awal atau sebagai perbaikan setelah algoritma optimasi.
- **Simulated Annealing (SA):** optimasi menggunakan probabilitas penerimaan solusi dan mekanisme penurunan suhu.
- **Tabu Search (TS):** optimasi menggunakan neighborhood, tabu list FIFO, dan aspiration criterion.
- **Variable Neighborhood Search (VNS):** optimasi dengan pergantian struktur neighborhood untuk mengeksplorasi solusi yang berbeda.
- **Perbandingan Algoritma:** membandingkan jarak terbaik, runtime, jumlah iterasi, dan struktur rute SA, TS, serta VNS.
- **Convergence Analysis:** memvisualisasikan perubahan best distance berdasarkan riwayat optimasi aktual.
- **Iteration Log:** menampilkan detail iterasi dan menyediakan ekspor CSV.
- **Automatic Analysis:** menyajikan analisis solusi awal, kualitas hasil, runtime, perbaikan solusi, dan kesamaan edge dalam bentuk enam kartu informasi serta panel catatan.
- **Multi-run:** menjalankan eksperimen berulang untuk membandingkan rata-rata, standar deviasi, dan konsistensi hasil.
- **Visualization & Export:** menampilkan rute, grafik konvergensi, perbandingan edge, serta ekspor PNG dan CSV.
- **Tabu Search Explorer:** mengeksplorasi riwayat Tabu Search untuk dataset berukuran kecil.

## Struktur Project

```text
TSP-Metaheuristic/
├── app/
│   └── app.py                 # Antarmuka utama Streamlit
├── src/
│   └── tsp_core.py            # Implementasi algoritma TSP
├── data/
│   └── data1.xlsx             # Dataset contoh
├── docs/                      # Dokumentasi project (opsional)
├── .streamlit/
│   └── config.toml            # Konfigurasi tema aplikasi
├── requirements.txt           # Daftar dependency
└── README.md                  # Dokumentasi utama
```

### Komponen Utama

- `app/app.py`: mengatur antarmuka Streamlit, sidebar, input data, parameter algoritma, eksekusi optimasi, visualisasi, tabel hasil, dan analisis.
- `src/tsp_core.py`: berisi fungsi perhitungan jarak, construction heuristic, local search, serta implementasi SA, TS, ILS, dan VNS.
- `data/data1.xlsx`: dataset contoh dengan sheet `Sheet7`, berisi Case I (25 kota), Case II (40 kota), dan Case III (68 kota).

## Teknologi

- Python
- Streamlit
- NumPy
- Pandas
- Matplotlib
- Plotly
- openpyxl

## Instalasi dan Menjalankan Aplikasi

Pastikan Python telah terpasang di komputer.

### 1. Buka terminal pada folder project

```powershell
cd "path\ke\TSP-Metaheuristic"
```

### 2. Buat dan aktifkan virtual environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Jika virtual environment sudah tersedia, cukup aktifkan tanpa membuatnya kembali.

### 3. Instal dependency

```powershell
python -m pip install -r requirements.txt
```

### 4. Jalankan aplikasi

```powershell
python -m streamlit run app/app.py
```

Buka alamat lokal yang ditampilkan di terminal, biasanya:

```text
http://localhost:8501
```

## Cara Penggunaan

### 1. Data Kota

Pilih metode input melalui sidebar:

- **Klik kanvas X-Y:** klik area kanvas untuk menambah kota; gunakan Undo, Hapus kota, dan Reset sesuai kebutuhan.
- **Generate acak:** tentukan jumlah kota, rentang koordinat, dan random seed.
- **Input manual:** tambah, ubah, atau hapus data kota melalui editor tabel.
- **Upload Excel/CSV:** pilih file, sheet jika menggunakan Excel, serta kolom City, X, dan Y.
- **Dataset contoh:** gunakan `data1.xlsx`, pilih Case I, Case II, atau Case III, dan tentukan jumlah kota yang digunakan.

Jumlah kota yang didukung aplikasi dibatasi maksimal 200 kota.

### 2. Pengaturan Algoritma

Buka expander **Pengaturan lanjutan** untuk mengatur metric, solusi awal, local search, algoritma, dan eksperimen.

#### Distance & Initial Solution

Pilih Euclidean atau Manhattan distance, construction heuristic, kota awal, atau rute manual.

Contoh format rute manual:

```text
1,4,2,5,3,6
```

Rute manual harus memuat setiap kota tepat satu kali.

#### Local Search

- **2-opt pada solusi awal:** memperbaiki rute awal sebelum algoritma dijalankan.
- **2-opt setelah SA/TS/VNS (polish):** melakukan perbaikan rute setelah algoritma selesai.
- **Improvement strategy:** memilih Best Improvement atau First Improvement.

#### Simulated Annealing (SA)

Parameter yang tersedia:

- Initial temperature (\(T_0\))
- Alpha atau cooling rate (\(\alpha\))
- Minimum temperature (\(T_{\min}\))
- Iterasi per temperatur
- Maximum iteration
- Neighborhood: 2-opt, Swap, atau 3-opt

SA menerima solusi yang memperbaiki jarak. Solusi yang lebih buruk dapat diterima berdasarkan probabilitas Metropolis:

\[
P(\text{accept})=
\begin{cases}
1, & \Delta E \leq 0\\
e^{-\Delta E/T}, & \Delta E>0
\end{cases}
\]

Suhu diturunkan menggunakan:

\[
T_{k+1}=\alpha T_k
\]

Algoritma berhenti ketika suhu berada di bawah batas minimum atau jumlah iterasi maksimum tercapai.

#### Tabu Search (TS)

Parameter yang tersedia:

- Maximum iteration
- Tabu size
- Neighborhood size
- Neighborhood: 2-opt, Swap, atau 3-opt
- Aspiration criterion

TS menggunakan tabu list berukuran terbatas dengan mekanisme FIFO untuk mencegah pengulangan move tertentu. Aspiration criterion memungkinkan move tabu diterima apabila menghasilkan solusi yang lebih baik daripada best solution yang telah ditemukan.

#### Variable Neighborhood Search (VNS)

VNS menggunakan beberapa struktur neighborhood secara bergantian untuk mencari solusi TSP yang lebih baik.

Parameter yang tersedia:

- **Maximum iteration VNS:** batas iterasi pencarian.
- **Jumlah maksimum neighborhood (`k_max`):** jumlah struktur neighborhood yang digunakan, maksimal tiga pada implementasi ini.
- **Struktur neighborhood:** Swap, Insertion, dan 2-opt.
- **Metode shaking:** satu move acak atau beberapa move berdasarkan \(k+1\).
- **Local search:** pilihan penerapan 2-opt setelah shaking.
- **Random seed:** mengatur proses acak agar eksperimen dapat direproduksi.

Alur VNS:

1. Menggunakan solusi awal yang telah dibentuk.
2. Melakukan shaking berdasarkan neighborhood aktif.
3. Menerapkan local search jika diaktifkan.
4. Mengevaluasi jarak kandidat.
5. Jika kandidat lebih baik, memperbarui solusi dan kembali ke neighborhood pertama.
6. Jika tidak lebih baik, melanjutkan ke neighborhood berikutnya.
7. Menyimpan best distance, runtime, jumlah iterasi, dan riwayat konvergensi aktual.

VNS mendukung Euclidean dan Manhattan distance melalui matriks jarak yang digunakan oleh aplikasi.

#### Iterated Local Search (ILS)

ILS tersedia sebagai metode opsional. Implementasinya menggunakan 2-opt dan perturbasi double-bridge, serta menerima solusi baru jika tidak lebih buruk berdasarkan aturan penerimaan yang diterapkan.

#### Multi-run & Random Seed

Multi-run menjalankan SA, TS, dan VNS berulang kali dengan variasi seed yang terkontrol.

Hasilnya dapat digunakan untuk mengevaluasi:

- Best distance
- Average distance
- Standard deviation
- Konsistensi hasil antar-run

Random seed yang sama, bersama dengan data dan parameter yang sama, membantu menghasilkan proses eksperimen yang dapat direproduksi. Runtime tetap dapat berubah antar-eksekusi karena kondisi komputer.

### 3. Optimization Summary

Sebelum menjalankan optimasi, aplikasi menampilkan ringkasan konfigurasi yang mencakup data kota, distance metric, solusi awal, local search, parameter SA, TS, VNS, ILS, multi-run, dan random seed.

Ringkasan konfigurasi berbeda dari hasil optimasi. Hasil aktual baru tersedia setelah tombol **RUN OPTIMIZATION** dijalankan.

### 4. Hasil Optimasi

Setelah optimasi selesai, hasil ditampilkan pada tab berikut:

| Tab | Isi |
|---|---|
| Ringkasan | Jarak awal, jarak terbaik, improvement, runtime, dan jumlah iterasi. |
| Rute | Visualisasi rute awal dan hasil algoritma. |
| Perbandingan | Perbandingan edge dan perbedaan jarak SA, TS, dan VNS. |
| Konvergensi | Grafik best distance berdasarkan riwayat iterasi aktual. |
| Detail & Log | Detail setiap sisi rute, iteration log, dan distance matrix. |
| Analisis | Enam kartu analisis dan catatan tentang random seed serta multi-run. |
| Kompetisi | Membandingkan rute manual pengguna dengan hasil algoritma. |
| Tabu Explorer | Menelusuri detail Tabu Search untuk dataset kecil. |
| Multi-run | Statistik hasil eksperimen berulang jika multi-run diaktifkan. |

Tab Tabu Explorer tersedia untuk dataset dengan maksimal 12 kota. Tab Multi-run ditampilkan ketika jumlah run lebih dari satu.

## Visualisasi dan Export

Aplikasi menyediakan visualisasi rute, perbandingan struktur edge, serta grafik konvergensi.

Data dapat diekspor dalam format berikut:

- **PNG:** gambar rute, perbandingan rute, dan grafik konvergensi.
- **CSV:** detail rute, iteration log masing-masing algoritma, dan distance matrix.

Data yang ditampilkan pada hasil optimasi dan grafik konvergensi berasal dari riwayat algoritma yang dijalankan, bukan nilai hasil yang di-hardcode.

## Catatan Implementasi

- Rute TSP merupakan tur tertutup; perjalanan dari kota terakhir kembali ke kota awal ikut dihitung.
- Setiap kota harus dikunjungi tepat satu kali.
- Batas maksimum kota adalah 200.
- Euclidean distance dihitung berdasarkan jarak garis lurus koordinat X-Y.
- Manhattan distance dihitung berdasarkan jumlah selisih absolut koordinat X dan Y.
- Neighborhood Swap, 2-opt, dan 3-opt tersedia untuk metode yang mendukungnya; VNS menggunakan Swap, Insertion, dan 2-opt.
- SA, TS, dan VNS menggunakan solusi awal serta matriks jarak yang sama dalam satu eksekusi agar perbandingan lebih sebanding.
- Jika fitur 2-opt polish diaktifkan, jarak hasil akhir turut memperhitungkan perbaikan setelah algoritma.
- Hasil terbaik tidak dijamin selalu diperoleh algoritma yang sama. Kualitas solusi dipengaruhi dataset, konfigurasi parameter, seed, dan proses pencarian.
- Perbandingan runtime mengukur waktu eksekusi aktual dan dapat berubah karena kondisi komputer.
- Nilai improvement, best distance, jumlah iterasi, dan kesamaan edge dihitung dari hasil eksperimen yang sedang ditampilkan.

## Troubleshooting

**Streamlit tidak dikenali**

Gunakan:

```powershell
python -m streamlit run app/app.py
```

**Dependency belum terpasang**

Pastikan virtual environment aktif, kemudian jalankan:

```powershell
python -m pip install -r requirements.txt
```

**Dataset contoh tidak ditemukan**

Pastikan file tersedia di:

```text
data/data1.xlsx
```

**Hasil belum muncul atau konfigurasi berubah**

Periksa validitas input dan jalankan kembali **RUN OPTIMIZATION** setelah mengubah parameter atau dataset.

## Tujuan Project

Project ini dikembangkan sebagai sarana pembelajaran dan eksperimen optimasi kombinatorial, khususnya untuk memahami perilaku **Simulated Annealing, Tabu Search, dan Variable Neighborhood Search** pada permasalahan Traveling Salesman Problem.

Fokus evaluasi adalah kualitas rute, waktu komputasi, konvergensi, dan konsistensi solusi, bukan mengasumsikan satu algoritma selalu lebih unggul daripada algoritma lainnya.