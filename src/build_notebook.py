from pathlib import Path
import nbformat as n
BASE=Path(__file__).resolve().parents[1]
cells=[]
def md(s):cells.append(n.v4.new_markdown_cell(s))
def code(s):cells.append(n.v4.new_code_cell(s))
md('''# Optimasi Rute Wisata Semarang Menggunakan ABC dan Random Keys

**Swarm Intelligence, Pertemuan 10: Representasi Solusi dan Adaptasi Algoritma Swarm**

Purna Siswantomo, C2C023160. Dua anggota lain dan pembagian pekerjaan aktual perlu dilengkapi kelompok.

Kasus: perencanaan urutan kunjungan terhadap lokasi nyata di Semarang. Ini eksperimen
komputasional dengan data publik, bukan catatan perjalanan wisatawan atau penerapan operasional.
Lawang Sewu menjadi titik awal dan akhir, sepuluh destinasi lain dikunjungi tepat sekali.
Tujuan minimisasi total estimasi waktu berkendara. Jam buka, lama kunjungan, kemacetan
aktual, biaya tiket dan kelayakan selesai dalam sehari belum dimodelkan.

Lokasi: Nominatim/OpenStreetMap; matriks jalan: OSRM driving. Semua respons mentah
dan sumber per lokasi ada dalam folder data. © OpenStreetMap contributors, ODbL 1.0.
Lihat https://www.openstreetmap.org/copyright dan https://project-osrm.org/docs/v26.4.0/http.
Titik POI belum diverifikasi sebagai pintu masuk pengunjung; snapping ke jalan adalah pendekatan.

Jalankan notebook dari folder project. Data sudah disimpan sehingga eksperimen tidak
memerlukan internet. Pengunduhan ulang opsional memakai src/download_data.py.
''')
code('''from pathlib import Path
import json, time, itertools, hashlib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
BASE=Path.cwd()
assert (BASE/'data'/'locations.csv').exists(), 'Jalankan dari folder Project ABC Wisata Semarang'
OUT=BASE/'hasil';OUT.mkdir(exist_ok=True)
locations=pd.read_csv(BASE/'data'/'locations.csv')
T=pd.read_csv(BASE/'data'/'durations.csv').to_numpy(float)
DIST=pd.read_csv(BASE/'data'/'distances.csv').to_numpy(float)
assert T.shape==(len(locations),len(locations))
assert np.isfinite(T).all() and (T>=0).all() and np.allclose(np.diag(T),0)
display(locations[['id','name','latitude','longitude','osm_url']])
display(pd.DataFrame(T/60,index=locations.name,columns=locations.name).round(2))
print('Matriks asimetris:',not np.allclose(T,T.T))
print('Data provenance:',json.loads((BASE/'data'/'provenance.json').read_text(encoding='utf-8')))
''')
md('''## Representasi solusi, search space dan objective

Satu food source adalah vektor 10 random keys dalam [0,1], bukan satu objek wisata.
Stable argsort menghasilkan urutan ID destinasi 1..10; ID 0 ditempatkan tetap di awal
dan akhir. Search space vektor kontinu [0,1]^10 dipetakan ke 10! = 3.628.800 permutasi.
Banyak vektor berbeda dapat menghasilkan rute yang sama, sehingga ada plateau representasi.

Contoh empat tujuan: keys [0,72; 0,18; 0,91; 0,43] menghasilkan urutan [2,4,1,3].
Angka key bukan koordinat atau biaya perjalanan. Tie diselesaikan stabil menurut ID.
Constraint tepat satu kunjungan dijamin decoder, bukan penalti. Keys di luar rentang
di-clip. Sisi yang tidak dapat dirutekan akan ditolak saat validasi data, bukan diberi
nilai nol atau diganti jarak garis lurus.

Objective f(pi) = T[0,pi1] + sum T[pi_i,pi_(i+1)] + T[pi_n,0], dalam detik.
Karena matriks jalan bisa asimetris, rute terbalik belum tentu mempunyai biaya sama.
Fitness untuk seleksi probabilistik adalah 1/(1+f), lalu dinormalisasi menjadi peluang.
Ini bukan perbandingan jarak lurus maupun optimasi durasi berwisata keseluruhan.
''')
code((BASE/'src'/'abc_routing.py').read_text(encoding='utf-8'))
code('''demo=np.array([.72,.18,.91,.43])
print('Keys:',demo,'Rute:',decode(demo))
assert decode(demo).tolist()==[0,2,4,1,3,0]
assert decode(np.ones(4)).tolist()==[0,1,2,3,4,0]
# Uji oracle eksak terhadap enumerasi pada matriks kecil yang asimetris.
check=np.random.default_rng(91).integers(1,200,size=(6,6)).astype(float)
np.fill_diagonal(check,0)
small_route,small_value=held_karp(check)
brute=min(tour_cost(np.array((0,)+p+(0,)),check) for p in itertools.permutations(range(1,6)))
assert np.isclose(small_value,brute)
print('Decoder, tie handling, dan Held-Karp lulus pemeriksaan.')
''')
md('''## Adaptasi fase ABC

Employed bee memilih peer k berbeda dari i dan satu dimensi j, lalu menghitung
v_ij = x_ij + phi_ij(x_ij - x_kj), phi uniform [-1,1]. Kandidat di-clip dan di-decode,
kemudian diterima hanya bila objective membaik ketat. Trial bertambah bila gagal,
termasuk ketika keys berubah tetapi rutenya sama.

Onlooker memilih sumber makanan menurut peluang fitness, lalu memakai operator yang
sama. Probabilitas dibekukan per fase onlooker. Scout mengganti satu sumber dengan
trial tertinggi jika mencapai limit; arsip best-so-far tetap disimpan.

Gerak kontinu tetap dipertahankan. Adaptasi utamanya berada pada decoder dan evaluasi
permutasi. Ini tidak diklaim sebagai algoritma baru atau varian improved.
''')
md('''## Desain eksperimen

ABC: 20 food sources, 20 percobaan onlooker per siklus, limit 50.
Berhenti tepat pada 5.000 evaluasi, termasuk 20 evaluasi populasi awal dan evaluasi scout.
Seed 11,22,...,220 (20 run). Random search memakai 20 kandidat awal yang sama per seed,
lalu kandidat independen hingga anggaran yang sama. Setiap panggilan objective tetap
dihitung meskipun menghasilkan rute duplikat; tidak ada cache tersembunyi.

Nearest neighbor memakai depot yang sama. Held-Karp menjadi referensi eksak bagi
instance kecil ini, bukan baseline dengan anggaran sama. Keduanya deterministik,
sehingga tidak dibuat 20 hasil semu atau standard deviation antar-run palsu.
Konfigurasi ini pilihan awal yang transparan, bukan hasil tuning optimal.
''')
code('''SEEDS=list(range(11,221,11)); BUDGET=5000
start=time.perf_counter();exact_route,exact_value=held_karp(T);exact_time=time.perf_counter()-start
start=time.perf_counter();nn_route,nn_value=nearest_neighbor(T);nn_time=time.perf_counter()-start
runs=[]
for seed in SEEDS:
    # Rotate order to reduce systematic runtime ordering effects.
    for method in (['ABC','Random'] if seed//11%2 else ['Random','ABC']):
        r=solve(T,seed=seed,method=method,budget=BUDGET,sources=20,limit=50)
        assert r['cost_seconds']>=exact_value-1e-7
        runs.append(r)
df=pd.DataFrame([{k:v for k,v in r.items() if k not in ('history_fe','history_best','unique_population','keys')} for r in runs])
df['minutes']=df.cost_seconds/60
df['gap_percent']=100*(df.cost_seconds-exact_value)/exact_value
summary=df.groupby('method').agg(best_minutes=('minutes','min'),mean_minutes=('minutes','mean'),
    std_minutes=('minutes','std'),worst_minutes=('minutes','max'),mean_gap_percent=('gap_percent','mean'),
    mean_runtime_s=('runtime_seconds','mean'),mean_unique_routes=('unique_routes','mean'),
    optimum_hits=('gap_percent',lambda x:int(np.isclose(x,0,atol=1e-7).sum()))).reset_index()
display(summary)
print('Nearest neighbor:',nn_value/60,'menit; exact:',exact_value/60,'menit')
print('NN gap:',100*(nn_value-exact_value)/exact_value,'%')
df.to_csv(OUT/'runs_20_seed.csv',index=False);summary.to_csv(OUT/'summary.csv',index=False)
with (OUT/'histories.json').open('w') as f:json.dump(runs,f,indent=2,allow_nan=True)
best=min((r for r in runs if r['method']=='ABC'),key=lambda r:r['cost_seconds'])
route=best['route'];validate_route(route,len(T))
legs=pd.DataFrame([{'from':locations.name.iloc[a],'to':locations.name.iloc[b],
    'minutes':T[a,b]/60,'km':DIST[a,b]/1000} for a,b in zip(route[:-1],route[1:])])
display(legs);legs.to_csv(OUT/'best_route_legs.csv',index=False)
print('Rute terbaik:', ' -> '.join(locations.name.iloc[i] for i in route))
assert np.isclose(legs.minutes.sum()*60,best['cost_seconds'])
report={'exact_seconds':exact_value,'exact_route':exact_route,'exact_runtime_s':exact_time,
        'nn_seconds':nn_value,'nn_route':nn_route,'nn_runtime_s':nn_time,
        'best_abc_seconds':best['cost_seconds'],'best_abc_route':route,'best_abc_seed':best['seed'],
        'nodes':len(T),'destinations':len(T)-1,'budget':BUDGET,'seeds':SEEDS,
        'data_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (BASE/'data').glob('*.csv')}}
(OUT/'report.json').write_text(json.dumps(report,indent=2))
''')
code('''grid=np.arange(20,BUDGET+1,20)
fig,ax=plt.subplots(figsize=(9,4.5))
for method in ['ABC','Random']:
    curves=[]
    for r in runs:
        if r['method']!=method:continue
        idx=np.searchsorted(r['history_fe'],grid,side='right')-1
        curves.append(np.array(r['history_best'])[idx]/60)
    curves=np.array(curves)
    ax.plot(grid,curves.mean(axis=0),label=method)
    ax.fill_between(grid,np.quantile(curves,.25,axis=0),np.quantile(curves,.75,axis=0),alpha=.15)
ax.axhline(exact_value/60,color='black',ls='--',label='Optimum eksak')
ax.set(xlabel='Evaluasi objective (FE)',ylabel='Best-so-far (menit)',title='Mean convergence, 20 seed; pita = kuartil 25-75%')
ax.legend();ax.grid(alpha=.2);fig.tight_layout();fig.savefig(OUT/'convergence.png',dpi=160);plt.show()
fig,axes=plt.subplots(1,2,figsize=(11,4.2))
axes[0].boxplot([df[df.method==m].minutes for m in ['ABC','Random']],tick_labels=['ABC','Random'])
axes[0].axhline(exact_value/60,c='black',ls='--');axes[0].set(ylabel='Waktu perjalanan (menit)',title='Variasi hasil antar-run')
abcrows=df[df.method=='ABC']
axes[1].scatter(abcrows.seed,abcrows.same_route_fraction*100)
axes[1].set(xlabel='Seed',ylabel='Kandidat dengan rute tetap (%)',title='Plateau pada representasi random keys')
fig.tight_layout();fig.savefig(OUT/'stability_encoding.png',dpi=160);plt.show()
''')
code('''fig,ax=plt.subplots(figsize=(8,7))
xy=locations[['longitude','latitude']].to_numpy()
ax.plot(xy[route,0],xy[route,1],'-o',alpha=.7)
for i,(x,y) in enumerate(xy):ax.annotate(str(i),(x,y),xytext=(5,5),textcoords='offset points')
ax.scatter(xy[0,0],xy[0,1],c='red',s=120,marker='*',label='0: Lawang Sewu')
ax.set(xlabel='Longitude',ylabel='Latitude',title='Skema urutan rute ABC pada lokasi nyata')
ax.set_aspect(1/np.cos(np.deg2rad(locations.latitude.mean())))
ax.grid(alpha=.2);ax.legend()
fig.text(.12,.015,'Garis hanya penghubung antartitik, bukan geometri jalan. Objective memakai matriks OSRM.',fontsize=9)
fig.tight_layout(rect=(0,.04,1,1));fig.savefig(OUT/'route_schematic.png',dpi=160);plt.show()
display(locations[['id','name']])
''')
md('''## Interpretasi dan keterbatasan

Lihat tabel dan grafik hasil di atas. Analisis harus membedakan best satu run, mean,
std, gap terhadap optimum dan runtime komputasi dari waktu perjalanan rute.
Random keys menghindari tujuan hilang/ganda, tetapi perubahan satu key sering
tidak menyeberangi key lain, sehingga rute tidak berubah. Persentase kandidat dengan
rute tetap mengukur masalah ini langsung, bukan hanya menduga dari kurva datar.

Scout mendukung exploration, sedangkan seleksi onlooker dan greedy acceptance
mendukung exploitation. Mencapai optimum pada salah satu seed tidak menjamin semua
run mencapainya. Solusi eksak layak untuk 10 destinasi dan menjadi pemeriksa mutu;
ABC ditunjukkan sebagai metode adaptasi dan dapat diuji lagi pada instance lebih besar.

Hasil hanya optimal terhadap matriks statis yang disimpan. Jam buka, durasi kunjungan,
akses kendaraan ke pintu masuk dan lalu lintas aktual belum diverifikasi.
Peta garis antartitik adalah skema urutan, bukan petunjuk navigasi.

Pembagian peran yang diusulkan: anggota 1 memeriksa sumber lokasi dan formulasi,
anggota 2 menjelaskan implementasi ABC/decoder, anggota 3 memeriksa evaluasi dan visualisasi.
Nama dan kontribusi aktual diisi sesuai pekerjaan kelompok; semua anggota perlu menguasai seluruh alur.
''')
nb=n.v4.new_notebook(cells=cells,metadata={'kernelspec':{'display_name':'Python 3','language':'python','name':'python3'}})
n.write(nb,BASE/'Project_ABC_Wisata_Semarang.ipynb')
print('Notebook built')
