# Project ABC: rute wisata Semarang

Fokus Pertemuan 10: representasi solusi dan adaptasi algoritma swarm.

## Mulai
1. Ekstrak paket dan buka folder ini.
2. Pasang dependensi: `python -m pip install -r requirements.txt`.
3. Jalankan Jupyter dari folder ini, buka `Project_ABC_Wisata_Semarang.ipynb`, pilih Run All.
4. Data tersedia lokal. Internet hanya diperlukan untuk pengunduhan ulang opsional.

## Berkas
- Notebook memuat kode ABC lengkap, decoder, uji oracle, 20 seed, hasil, grafik, dan interpretasi.
- src/abc_routing.py: implementasi mandiri ABC, random search, nearest neighbor, Held-Karp.
- src/download_data.py: pengambilan Nominatim/OSRM; cache mencegah pengulangan permintaan geocoding.
- data/: POI nyata, CSV matriks durasi/jarak, respons mentah, provenance dan geometri jalan.
- hasil/: tabel 20 run, ringkasan, rute terbaik, riwayat pencarian dan grafik.
- Panduan_Presentasi.txt: alur 10 slide dan pembagian peran yang diusulkan.

Data © OpenStreetMap contributors, ODbL 1.0. https://www.openstreetmap.org/copyright
OSRM docs: https://project-osrm.org/docs/v26.4.0/http
ABC: D. Karaboga, 2005, An Idea Based on Honey Bee Swarm for Numerical Optimization, Technical Report TR06, Erciyes University.
Sumber ketentuan: Pengumuman_Project_Presentation_Swarm_Intelligence_P10-P13_FINAL.pdf milik dosen.

## Batas klaim
Ini skenario perencanaan rute pada lokasi nyata, bukan bukti implementasi pada operator wisata.
POI belum diverifikasi sebagai pintu masuk. Durasi adalah estimasi statis OSRM, tidak mencakup
kemacetan aktual, jam buka, durasi kunjungan, tiket atau jaminan selesai sehari.
Random/ABC dibandingkan pada anggaran 5.000 evaluasi; NN dan metode eksak bukan pembanding budget setara.
Held-Karp lebih cepat dan pasti optimum pada instance kecil ini; ABC tidak diklaim lebih unggul.
Nama dua anggota lain, NIM, dan pembagian kerja aktual wajib dilengkapi kelompok sebelum pengumpulan.
