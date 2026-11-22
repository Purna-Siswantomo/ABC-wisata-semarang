from pathlib import Path
import nbformat as n, json, pandas as pd
BASE=Path(__file__).resolve().parents[1]
p=BASE/'Project_ABC_Wisata_Semarang.ipynb';nb=n.read(p,as_version=4)
summary=pd.read_csv(BASE/'hasil/summary.csv').set_index('method')
df=pd.read_csv(BASE/'hasil/runs_20_seed.csv');r=json.loads((BASE/'hasil/report.json').read_text())
abc=summary.loc['ABC'];random=summary.loc['Random'];plateau=df[df.method=='ABC'].same_route_fraction.mean()*100
analysis=f'''## Hasil dan kesimpulan dari eksekusi

ABC menghasilkan mean **{abc.mean_minutes:.4f} menit**, std sampel **{abc.std_minutes:.4f} menit**,
best **{abc.best_minutes:.4f} menit** dan worst **{abc.worst_minutes:.4f} menit**.
Random search: mean **{random.mean_minutes:.4f} menit** dan std **{random.std_minutes:.4f} menit**.
Pada anggaran 5.000 evaluasi yang sama, mean ABC lebih rendah
**{100*(random.mean_minutes-abc.mean_minutes)/random.mean_minutes:.2f}%** dari random search.
Nearest neighbor menghasilkan **{r['nn_seconds']/60:.4f} menit**.

Optimum Held-Karp untuk matriks ini **{r['exact_seconds']/60:.4f} menit**.
ABC mencapai nilai tersebut pada **{int(abc.optimum_hits)}/20 run**, random search pada
**{int(random.optimum_hits)}/20 run**. Mean optimality gap ABC **{abc.mean_gap_percent:.3f}%**.
Mencapai optimum pada run terbaik tidak sama dengan selalu mencapai optimum.

Rata-rata **{plateau:.2f}%** kandidat tetangga ABC memiliki urutan yang sama dengan
sumbernya meskipun nilai key berubah atau terpotong di batas. Ini bukti langsung plateau
decoder. Random search menjelajah lebih banyak rute unik, tetapi tidak menggunakan
seleksi terarah sehingga mean kualitasnya lebih buruk pada anggaran ini.

Runtime mean ABC **{abc.mean_runtime_s:.4f} detik** dan random **{random.mean_runtime_s:.4f} detik**.
Held-Karp selesai dalam **{r['exact_runtime_s']:.4f} detik** pada perangkat pengujian ini.
Jadi untuk hanya 10 destinasi, metode eksak justru praktis dan memberi kepastian optimum.
ABC digunakan untuk mempelajari adaptasi kontinu-ke-permutasi; keunggulan pada instance
lebih besar perlu diuji lagi dan tidak boleh diklaim dari eksperimen ini.

Tidak dilakukan uji signifikansi, sehingga perbedaan yang dilaporkan adalah deskriptif.
Data jaringan jalan statis dan aturan berhenti di tiap POI, tanpa kemacetan aktual.
Geometri rute diambil dengan continue_straight=false agar perhentian dapat berbalik
sesuai matriks antartitik. Durasi route service cocok dengan penjumlahan matriks.
'''
roadcode='''
# Geometri jalan sebenarnya dari OSRM; tetap bukan observasi lalu lintas aktual.
road=json.loads((BASE/'data'/'best_route_osrm.json').read_text())['routes'][0]
assert np.isclose(road['duration'],best['cost_seconds'],atol=.11)
roadxy=np.array(road['geometry']['coordinates'])
fig,ax=plt.subplots(figsize=(7,7))
ax.plot(roadxy[:,0],roadxy[:,1],lw=1.7,c='#167b70')
ax.scatter(locations.longitude,locations.latitude,c='#172f4a',s=35)
for i,row in locations.iterrows():ax.annotate(str(i),(row.longitude,row.latitude),xytext=(5,4),textcoords='offset points')
ax.scatter(locations.longitude.iloc[0],locations.latitude.iloc[0],c='#c04f25',s=130,marker='*',label='0: Lawang Sewu')
ax.set(xlabel='Longitude',ylabel='Latitude',title='Rute jalan terbaik ABC, OSRM driving')
ax.set_aspect(1/np.cos(np.deg2rad(locations.latitude.mean())));ax.grid(alpha=.2);ax.legend()
fig.text(.12,.015,'Sumber: OpenStreetMap contributors / OSRM. POI di-snap ke jaringan jalan.',fontsize=8)
fig.tight_layout(rect=(0,.04,1,1));fig.savefig(OUT/'route_roads.png',dpi=170);plt.show()
'''
if not any(c.cell_type=='code' and 'roadxy=' in c.source for c in nb.cells):
    nb.cells.insert(-1,n.v4.new_code_cell(roadcode));nb.cells.append(n.v4.new_markdown_cell(analysis))
else:
    nb.cells[-1].source=analysis
n.write(nb,p)
(BASE/'requirements.txt').write_text('numpy>=1.26\npandas>=2.0\nmatplotlib>=3.9\njupyter>=1.0\nrequests>=2.31\n',encoding='utf-8')
(BASE/'README.md').write_text('''# Project ABC: rute wisata Semarang

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
''',encoding='utf-8')
notes='''PANDUAN PRESENTASI 10 MENIT, 10 SLIDE

1 (40 dtk): Judul, anggota, kasus dan fokus representasi. Dua anggota lain belum diisi.
2 (50 dtk): Tunjukkan lokasi nyata dan kebutuhan memilih urutan. Sebutkan skenario, bukan data perjalanan operasional.
3 (60 dtk): 11 POI termasuk depot; OSM/Nominatim dan OSRM; matriks asimetris, objective detik. Batas jam buka belum dimodelkan.
4 (60 dtk): Employed, onlooker, scout dan arsip best. Jelaskan alasan ABC: seleksi sumber yang bagus dan restart saat stagnasi.
5 (90 dtk): Contoh [0.72,0.18,0.91,0.43] menjadi [2,4,1,3]. Depot tetap. Keys bukan koordinat.
6 (80 dtk): Gerakan satu dimensi, clipping, decoding dan greedy acceptance. Trial bertambah pada kegagalan termasuk rute tetap.
7 (50 dtk): 20 seed, 20 food sources, limit50, 5000FE termasuk init/scout. Random memakai kondisi awal sama. NN dan exact tambahan.
8 (70 dtk): Mean, std, gap optimum dan kurva convergence terhadap FE. Sebut hasil aktual, bukan angka simulasi ilustratif.
9 (60 dtk): Banyak perubahan key tidak mengubah urutan. Scout memulihkan exploration. Exact lebih cepat untuk instance kecil.
10 (40 dtk): Kesimpulan dan pembagian peran. Lengkapi nama aktual. Waktu total 600 detik, tambah tanya jawab5menit.

USUL PEMBAGIAN PERAN, BUKAN CATATAN KONTRIBUSI AKTUAL
Anggota1: formulasi, validasi sumber POI dan matriks.
Anggota2: ABC, decoder dan desain eksperimen.
Anggota3: validasi hasil, visualisasi dan analisis.
Semua anggota memahami seluruh alur. Isi nama/NIM sesuai kelompok.

LATIHAN TANYA JAWAB
Mengapa ABC untuk routing? Mekanisme ABC tetap dipakai di ruang key kontinu, decoder menjamin permutasi valid.
Mengapa bukan ACO? ACO juga relevan; tujuan project ini menguji adaptasi ABC, bukan membuktikan algoritma lain tidak cocok.
Mengapa tidak pakai penjumlahan jarak Euclidean? Matriks waktu jalan lebih dekat pada kebutuhan perjalanan, tetap hanya estimasi.
Mengapa exact lebih cepat? Instance hanya10destinasi; dynamic programming masih kecil. Jangan mengklaim ABC selalu tercepat.
Apakah rute optimum global? Best ABC cocok dengan Held-Karp untuk matriks statis ini; tidak berarti optimum kondisi jalan aktual.
Mengapa random tidak selalu kalah? Metode stokastik dan anggaran terbatas; gunakan mean/std20seed, jangan satu run.
Apakah keys berbeda pasti rute berbeda? Tidak, inilah plateau representasi yang diukur pada kandidat tetangga.
Apakah berhenti sehari? Belum diuji; perlu durasi kunjungan dan time windows untuk perluasan model.
'''
(BASE/'Panduan_Presentasi.txt').write_text(notes,encoding='utf-8')
print('Final analysis and road geometry cell added')
