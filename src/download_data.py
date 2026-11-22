from pathlib import Path
import requests, time, json, csv, datetime
BASE=Path(__file__).resolve().parents[1]
D=BASE/'data'; D.mkdir(exist_ok=True,parents=True)
session=requests.Session()
session.headers['User-Agent']='SemarangTourABC-UniversityCoursework/1.0 (public academic route-planning research)'
places=['Lawang Sewu','Sam Poo Kong','Gereja Blenduk','Pantai Marina','Museum Ranggawarsita','Grand Maerakaca','Masjid Agung Jawa Tengah','Kampung Pelangi','Tugu Muda','Pagoda Avalokitesvara','Taman Indonesia Kaya']
rows=[]
for i,name in enumerate(places):
    cache=D/f'geocode_{i:02d}.json'
    if cache.exists(): data=json.loads(cache.read_text(encoding='utf-8'))
    else:
        r=session.get('https://nominatim.openstreetmap.org/search',params={'q':name+', Semarang','format':'jsonv2','limit':5,'viewbox':'110.25,-6.85,110.55,-7.15','bounded':1},timeout=25)
        r.raise_for_status();data=r.json()
        cache.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8');time.sleep(1.1)
    if not data:
        alternatives={'Gereja Blenduk':'Blenduk','Grand Maerakaca':'Maerokoco','Pagoda Avalokitesvara':'Watugong'}
        r=session.get('https://nominatim.openstreetmap.org/search',params={'q':alternatives.get(name,name)+', Semarang','format':'jsonv2','limit':5,'viewbox':'110.25,-6.85,110.55,-7.15','bounded':1},timeout=25)
        r.raise_for_status();data=r.json();time.sleep(1.1)
        cache.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
    if not data: print('MISSING',name,flush=True); continue
    eligible=[x for x in data if x.get('category',x.get('class')) not in ('highway','boundary')]
    assert eligible, f'No POI candidate: {name}'
    p=eligible[0]
    if name=='Pagoda Avalokitesvara': name='Vihara Buddhagaya Watugong'
    rows.append({'id':len(rows),'name':name,'latitude':float(p['lat']),'longitude':float(p['lon']),'osm_url':f"https://www.openstreetmap.org/{p['osm_type']}/{p['osm_id']}",'display_name':p['display_name'],'query':name+', Semarang','retrieved_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()})
    print(name,p['lat'],p['lon'],p['display_name'],flush=True)
with (D/'locations.csv').open('w',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f,fieldnames=rows[0].keys());w.writeheader();w.writerows(rows)
assert rows[0]['name']=='Lawang Sewu' and len(rows)>=8
coords=';'.join(f"{x['longitude']},{x['latitude']}" for x in rows)
url=f'https://router.project-osrm.org/table/v1/driving/{coords}'
r=session.get(url,params={'annotations':'duration,distance'},timeout=40);r.raise_for_status()
data=r.json();assert data['code']=='Ok'
(D/'osrm_table_raw.json').write_text(json.dumps(data,indent=2),encoding='utf-8')
for key in ['durations','distances']:
    assert all(v is not None for row in data[key] for v in row)
    with (D/f'{key}.csv').open('w',newline='') as f:
        w=csv.writer(f);w.writerow(range(len(rows)));w.writerows(data[key])
(D/'provenance.json').write_text(json.dumps({'retrieved_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'locations_source':'Nominatim / OpenStreetMap','osm_attribution':'© OpenStreetMap contributors, ODbL 1.0','osm_license':'https://www.openstreetmap.org/copyright','matrix_url':r.url,'matrix_source':'OSRM driving table','objective_unit':'seconds','distance_unit':'meters','live_traffic':False,'location_selection':'Name-matched POI in Semarang bounding box, excluding highway/boundary; raw candidates saved. Watugong is Vihara Buddhagaya POI, not the residential road returned first.','note':'Locations are mapped POI reference points, not verified visitor entrances. OSRM snaps each point to road network; inspect sources/destinations in raw response.'},indent=2,ensure_ascii=False),encoding='utf-8')
print('DATA READY',len(rows),flush=True)
