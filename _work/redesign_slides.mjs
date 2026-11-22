const ROOT='C:/Users/Purna Siswantomo/Documents/Semester 7/Swarm Intelligence/Project ABC Wisata Semarang';
const C={navy:'#142D50',teal:'#007F82',coral:'#F06D49',gold:'#E6A822',purple:'#7851BA',ink:'#19344C',muted:'#5B6C7B',paper:'#F8F7F3',white:'#FFFFFF'};
function tx(s,t,x,y,w,h,size=28,bold=false,color=C.ink){
 const z=s.shapes.add({geometry:'textbox',position:{left:x,top:y,width:w,height:h},fill:'none',line:{fill:'none',width:0}});
 z.text=t;z.text.style={fontFamily:'Arial',fontSize:size,bold,color};return z;
}
function im(s,name,x,y,w,h,fit='contain'){return s.images.add({path:ROOT+'/'+name,fit,position:{left:x,top:y,width:w,height:h}});}
function reset(p,i,title,section,color=C.teal,bg=C.white){
 const s=p.slides.getItem(i);for(const x of [...s.shapes.items,...s.images.items,...s.tables.items])x.delete();
 s.background.fill=bg;
 tx(s,section.toUpperCase(),64,35,1090,30,19,true,color);
 tx(s,title,64,88,1150,105,43,true,C.navy);
 tx(s,String(i+1).padStart(2,'0')+' / 10',1120,670,100,28,18,false,C.muted);
 return s;
}
function note(s,t){s.speakerNotes.text=t;}
export async function revise({presentation,input}){
 const start=input.start,end=input.end;
 for(let i=start;i<end;i++){
  let s;
  if(i===0){
   s=reset(presentation,0,'','PROJECT SWARM INTELLIGENCE',C.gold,C.navy);
   // Minimal cover, strong title contrast, original illustration on the right.
   for(const z of [...s.shapes.items])z.delete();
   tx(s,'PERTEMUAN 10',64,60,500,35,21,true,'#77DED4');
   tx(s,'Optimasi Rute\nWisata Semarang',64,150,660,190,58,true,C.white);
   tx(s,'Artificial Bee Colony\ndengan representasi random keys',66,390,570,110,29,false,'#C8EDE8');
   tx(s,'Purna Siswantomo  ·  C2C023160',66,590,620,40,23,false,C.white);
   tx(s,'Lengkapi dua anggota lain sebelum pengumpulan',66,640,620,40,19,false,'#B9C8D9');
   im(s,'presentasi/assets/hero_route_illustration.png',740,110,500,500,'cover');
   note(s,'40 detik. Fokus presentasi adalah adaptasi vektor kontinu menjadi rute wisata yang valid. Ilustrasi AI pada cover bersifat konseptual, bukan peta nyata atau foto lokasi. Identitas dua anggota lain belum diberikan.');
  }
  if(i===1){
   s=reset(presentation,1,'Outline: dari kasus ke hasil yang terukur','ALUR PRESENTASI');
   const titles=['Kasus & data','Mekanisme ABC','Representasi & adaptasi','Hasil & evaluasi'];
   const subtitles=['Lokasi nyata dan kebutuhan optimasi','Employed, onlooker dan scout','Random keys menjadi urutan kunjungan','Baseline, optimum dan keterbatasan'];
   [C.teal,C.coral,C.purple,C.navy].forEach((color,j)=>{
    tx(s,'0'+(j+1),66,205+j*103,100,70,49,true,color);
    tx(s,titles[j],180,210+j*103,530,40,31,true);
    tx(s,subtitles[j],180,255+j*103,560,40,24,false,C.muted);
   });
   tx(s,'Masalahnya',805,220,370,45,27,true,C.coral);
   tx(s,'Tempatnya sama.\nUrutannya berbeda.\nWaktu tempuh\nbisa berubah.',805,288,370,220,35,true,C.navy);
   tx(s,'Kita mencari urutan kunjungan\ndengan estimasi perjalanan terendah.',805,560,370,85,24);
   note(s,'50 detik. Outline empat bagian menjaga arah pembahasan. Latar masalah: daftar destinasi sudah ditentukan, keputusan optimasinya urutan kunjungan, bukan mencari tempat baru. Ini skenario perencanaan berbasis lokasi publik, bukan catatan perjalanan operasional.');
  }
  if(i===2){
   s=reset(presentation,2,'Lokasi nyata, biaya dari jaringan jalan','01  KASUS & DATA');
   tx(s,'10',64,215,170,120,86,true,C.teal);tx(s,'destinasi wisata',220,245,430,55,34,true);
   tx(s,'Lawang Sewu menjadi titik awal dan akhir.\nSemua tujuan dikunjungi tepat sekali.',66,365,605,100,30);
   tx(s,'Lokasi: OpenStreetMap / Nominatim\nWaktu jalan: OSRM driving\nObjective: jumlah waktu semua ruas',66,505,605,140,27,false,C.muted);
   im(s,'hasil/route_roads.png',715,185,500,460);
   tx(s,'Durasi statis; belum memasukkan jam buka dan lama kunjungan.',66,670,960,30,18,false,C.muted);
   note(s,'60 detik. Sepuluh destinasi plus depot berarti sebelas POI. Peta benar-benar geometri OSRM dari hasil ABC; bukan ilustrasi AI. Matriks asimetris, satuan detik lalu ditampilkan menit. Titik POI belum disurvei sebagai pintu masuk, dan OSRM melakukan snapping ke jaringan jalan. Dataset raw dan provenance disimpan. Sumber: https://www.openstreetmap.org/copyright ; https://project-osrm.org/docs/v26.4.0/http .');
  }
  if(i===3){
   s=reset(presentation,3,'Tiga peran lebah menggerakkan pencarian','02  MEKANISME ABC');
   im(s,'presentasi/assets/abc_bee_phases.png',64,190,1150,300);
   const names=['Employed','Onlooker','Scout'];
   const descriptions=['Mencoba perubahan\npada sumber saat ini','Memilih sumber bagus\nberdasarkan fitness','Mengganti sumber stagnan\ndengan kandidat baru'];
   [C.teal,C.coral,C.purple].forEach((color,j)=>{
    tx(s,names[j],75+j*395,495,355,48,33,true,color);
    tx(s,descriptions[j],75+j*395,555,355,90,26);
   });
   note(s,'60 detik. Satu sumber makanan adalah satu rute lengkap. Ilustrasi lebah merupakan metafora AI, bukan model biologis. Employed dan onlooker memakai operator tetangga yang sama; scout melakukan restart. Peluang pemilihan sumber proporsional terhadap fitness=1/(1+objective), lalu dinormalisasi. Best-so-far disimpan terpisah. ABC: Karaboga2005TR06ErciyesUniversity. Bagian ini mengenalkan mekanisme, fokus representasi ada sesudahnya.');
  }
  if(i===4){
   s=reset(presentation,4,'Satu vektor angka menjadi satu rute','03  REPRESENTASI SOLUSI',C.coral);
   im(s,'presentasi/assets/random_keys_example.png',64,190,765,430);
   tx(s,'Cara membaca',875,230,330,50,29,true,C.teal);
   tx(s,'1  Setiap key milik satu tujuan\n\n2  Urutkan key terkecil\n\n3  Pasang depot di dua ujung',875,300,340,220,25);
   tx(s,'Depot – B – D – A – C – Depot',66,640,1000,43,29,true,C.navy);
   note(s,'90 detik. Ilustrasi empat tujuan hanya contoh pengajaran: A=.72 B=.18 C=.91 D=.43, decoder menghasilkan B,D,A,C. Warna tiap tujuan konsisten pada dua baris, sehingga arah baca terlihat. Angka key bukan koordinat, jarak atau waktu. Implementasi actual memakai10keys dalam[0,1], 10! permutasi. Stable argsort mengatasi tie menurut ID dan menjamin setiap tujuan muncul sekali.');
  }
  if(i===5){
   s=reset(presentation,5,'Ubah key, decode ulang, lalu evaluasi rute','03  ADAPTASI ABC',C.purple);
   tx(s,'vᵢⱼ = xᵢⱼ + φᵢⱼ(xᵢⱼ − xₖⱼ)',66,200,1120,65,43,true,C.teal);
   tx(s,'Contoh key D',66,320,510,40,25,true,C.muted);
   tx(s,'0,43  →  0,79',66,380,590,85,59,true,C.coral);
   tx(s,'0,43 + 0,9 × (0,43 − 0,03) = 0,79',66,495,590,60,25);
   tx(s,'Urutan awal',750,315,450,40,25,false,C.muted);
   tx(s,'B  D  A  C',750,370,450,60,43,true,C.navy);
   tx(s,'Urutan kandidat',750,470,450,40,25,false,C.muted);
   tx(s,'B  A  D  C',750,520,450,60,43,true,C.teal);
   tx(s,'Terima hanya jika waktu turun. Jika gagal, trial bertambah; limit memicu scout.',66,635,1100,50,24);
   note(s,'80 detik. Contoh dihitung dengan phi=.9 dan key peerD=.03, valid pada[0,1]. Tujuan lain tetapA=.72B=.18C=.91, jadi D=.79 menyeberangi A. Ini contoh representasi, tidak diasumsikan objective membaik. Kandidat selalu dievaluasi pada matriks perjalanan. Clipping menjaga key[0,1]; decoder menjaga permutasi; trial mencatat kegagalan, termasuk key berubah tanpa perubahan urutan. Ini adaptasi, tidak diklaim algoritma improved baru.');
  }
  if(i===6){
   s=reset(presentation,6,'Eksperimen memakai anggaran evaluasi setara','04  DESAIN EKSPERIMEN');
   const xs=[65,370,675,980],nums=['20','5.000','20','50'],labels=['seed pengujian','evaluasi per run','food sources','limit stagnasi'];
   nums.forEach((v,j)=>{tx(s,v,xs[j],220,260,100,64,true,[C.teal,C.coral,C.purple,C.navy][j]);tx(s,labels[j],xs[j],335,250,60,25);});
   tx(s,'Perbandingan utama',66,470,510,50,30,true,C.teal);
   tx(s,'ABC vs random search\nPopulasi awal dan jumlah evaluasi sama',66,540,550,100,28);
   tx(s,'Pembanding tambahan',700,470,510,50,30,true,C.coral);
   tx(s,'Nearest neighbor sebagai baseline\nHeld–Karp sebagai referensi optimum',700,540,510,100,28);
   note(s,'50 detik. Seed11,22,...220. Dua puluhfoodsources dan20percobaanonlookerpersiklus.5.000FE termasukpopulasi awal dan scout. Kandidatduplikat tetap dihitung,tanpacache tersembunyi. NN daneksak deterministik, tidak dibuat20runsemu atau stdnolpalsu. Perbandingan setaraFE berlakuABC/random, bukanNN/exact.');
  }
  if(i===7){
   s=reset(presentation,7,'ABC memberi mean perjalanan lebih rendah','04  HASIL EKSPERIMEN');
   const values=[['Metode','Durasi (menit)'],['ABC, mean','71,53'],['Random, mean','74,09'],['Nearest neighbor','81,22'],['Optimum eksak','70,51']];
   const table=s.tables.add({rows:5,columns:2,left:64,top:205,width:465,height:280,columnWidths:[285,180],values});
   for(let r=0;r<5;r++)for(let c=0;c<2;c++){
    const cell=table.getCell(r,c);cell.fill=r===0?C.navy:(r===1?'#E4F4EF':C.white);
    cell.text.style={fontFamily:'Arial',fontSize:24,bold:r<=1,color:r===0?C.white:C.ink};
   }
   im(s,'hasil/convergence.png',560,200,655,370);
   tx(s,'3,45%',66,530,300,85,61,true,C.teal);
   tx(s,'mean lebih rendah daripada random\npada 5.000 evaluasi yang sama',66,620,510,65,24);
   tx(s,'Kurva: mean 20 seed; pita menunjukkan kuartil 25–75%.',570,595,640,70,22,false,C.muted);
   note(s,'70 detik. TabelNN danexact adalahhasil deterministik tunggal, ABC/randommean20seed. StdABC .6646min,random .9666min. BestABC70.51min,worst72.60167min. MeanABC71.52875,random74.08533. Penguranganmean3.45086%,dibulatkan3.45%. Kurva atasFE, bukaniterasi. Ini deskriptif,tanpauji signifikansi. Sumber hasil/summary.csv danreport.json.');
  }
  if(i===8){
   s=reset(presentation,8,'Perubahan angka belum tentu mengubah rute','04  ANALISIS REPRESENTASI',C.coral);
   tx(s,'4 / 20',66,205,330,100,72,true,C.teal);
   tx(s,'run ABC mencapai\noptimum matriks',66,320,370,95,31,true);
   tx(s,'Mean gap 1,44%\nStd hasil 0,66 menit',66,460,380,100,29);
   im(s,'hasil/stability_encoding.png',455,205,760,350);
   tx(s,'Plateau decoder: key berubah, urutan bisa tetap sama.',455,590,740,60,26,true,C.coral);
   tx(s,'Scout membantu exploration; seleksi greedy menjaga exploitation.',66,665,1040,30,21,false,C.muted);
   note(s,'60 detik. Diagram kanan menunjukkan persentase kandidat tetangga yang rutenya sama dengan parent. Denominator adalah percobaan neighbor, bukan scout. Angkaunikrute ABC rata1981.9,random4996.2: lebih banyakruteunik tidak otomatis meanlebihbaik. Empatrun mencapaioptimum,16lainbelum. Solusiarsipterbaik bisa berhentimembaik meski populasimasihberubah. Jangan menyamakan diversitaskeydanrute.');
  }
  if(i===9){
   s=reset(presentation,9,'Representasi valid, hasilnya bisa diperiksa','KESIMPULAN',C.gold,C.navy);
   for(const z of [...s.shapes.items])z.delete();
   tx(s,'KESIMPULAN',64,48,1100,35,21,true,'#77DED4');
   tx(s,'Representasi valid.\nHasilnya bisa diperiksa.',64,135,1140,140,54,true,C.white);
   tx(s,'Random keys menjamin setiap tujuan muncul sekali.\nABC memperbaiki mean terhadap baseline pengujian.\nUntuk 10 tujuan, metode eksak justru lebih cepat.',66,340,1140,165,30,false,'#D6ECEB');
   tx(s,'DATA & FORMULASI',66,565,355,35,23,true,'#77DED4');
   tx(s,'IMPLEMENTASI ABC',455,565,355,35,23,true,'#FFB398');
   tx(s,'EVALUASI & VISUAL',845,565,355,35,23,true,'#D7C1FF');
   tx(s,'Lengkapi nama/NIM dua anggota lain dan pembagian kontribusi aktual.',66,650,1120,35,21,false,'#C2D0E0');
   note(s,'40 detik. Peran tigaanggota adalahusulan, bukanrekamkontribusiaktual. Ketiganya harusmenguasaiseluruhalur. UntukinstancekecilHeldKarplebihcepatdanpastioptimum; ABCbukanjaminantercepat. Nilairuteoptimumhanyauntukmatriksstatis, bukanwaktuaktualmacet. Jam buka,durasikunjungan,tiketdanentrancebelummasukmodel. Sumber OSM/OSRM dan notebook project; ilustrasiAIhanya penjelas. Akhiri10menit, lanjut5menitQA.');
  }
 }
 return {revised:[start+1,end],total:presentation.slides.items.length};
}
