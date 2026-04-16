import pandas as pd
import json
import re

def parse_wkt_line(wkt_string):
    coords = []
    if pd.isna(wkt_string): return coords
    matches = re.findall(r'(-?\d+\.\d+)\s(-?\d+\.\d+)', str(wkt_string))
    for m in matches:
        coords.append([float(m[1]), float(m[0])]) # [lat, lon]
    return coords

def parse_wkt_polygon(wkt_string):
    polys = []
    if not wkt_string or pd.isna(wkt_string): return polys
    
    # Split multipolygon into individual polygons
    splits = re.split(r'\)\)\s*,\s*\(\(', str(wkt_string))
    for s in splits:
        coords = []
        matches = re.findall(r'(-?\d+\.\d+)\s(-?\d+\.\d+)', s)
        for m in matches:
            coords.append([float(m[1]), float(m[0])])
        if coords:
            polys.append(coords)
    return polys

def fix_coord(val):
    if pd.isna(val): return None
    s = str(val).replace('.', '')
    if s.startswith('-22'):
        return -22.0 - float(s[3:])/ (10**(len(s)-3)) if len(s)>3 else -22.0
    if s.startswith('-49'):
        return -49.0 - float(s[3:])/ (10**(len(s)-3)) if len(s)>3 else -49.0
    if s.startswith('-4'):
        return -49.0 - float(s[3:])/ (10**(len(s)-3)) if len(s)>3 else -49.0
    return None

def point_in_polygon(x, y, poly):
    n = len(poly)
    inside = False
    p1x, p1y = poly[0]
    for i in range(1, n + 1):
        p2x, p2y = poly[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xints = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xints:
                        inside = not inside
        p1x, p1y = p2x, p2y
    return inside

def main():
    print("Loading talhoes...")
    with open('input/talhoes.geojson', 'r', encoding='utf-8') as f:
        talhoes_data = json.load(f)
        
    # Extrair todos os poligonos para filtrar os rastros
    all_polygons = []
    
    html = """<!DOCTYPE html>
<html>
<head>
    <title>FarmLab - Mapa de Pulverização Real vs Armadilhas</title>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
    <style>
        body { margin: 0; padding: 0; font-family: 'Inter', sans-serif; background: #0f172a; color: #fff; }
        #map { width: 100vw; height: 100vh; }
        /* custom marker */
        .trap-conv { background: #f97316; border: 3px solid white; border-radius: 50%; box-shadow: 0 0 12px rgba(249,115,22,1.0); }
        .trap-elec { background: #10b981; border: 3px solid white; border-radius: 50%; box-shadow: 0 0 12px rgba(16,185,129,1.0); }
    </style>
</head>
<body>
    <div id="map"></div>
    <script>
        var map = L.map('map').setView([-22.245, -49.977], 15);
        L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
            attribution: 'Tiles &copy; Esri &mdash; Source: Esri',
            maxZoom: 19
        }).addTo(map);

        // Talhões
"""
    
    for item in talhoes_data.get('content', []):
        name = item.get('fieldName', 'Desconhecido')
        wkt = item.get('fieldGeom', '')
        polys = parse_wkt_polygon(wkt)
        
        is_4_0 = '4.0' in name
        color = '#10b981' if is_4_0 else '#ef4444' # Verde forte (4.0), Vermelho forte (Conv)
        
        for poly in polys:
            if len(poly) > 2:
                all_polygons.append(poly)
                html += f"""
        L.polygon({json.dumps(poly)}, {{
            color: '{color}',
            fillColor: '{color}',
            fillOpacity: 0.15,
            weight: 4,
            dashArray: '6, 6'
        }}).bindPopup("<b>Talhão:</b><br>{name}").addTo(map);
"""

    print("Loading traps...")
    traps = pd.read_csv('input/traps_list.csv', sep=';', on_bad_lines='skip')
    traps['lat'] = traps['latitude'].apply(fix_coord)
    traps['lon'] = traps['longitude'].apply(fix_coord)
    traps = traps.dropna(subset=['lat', 'lon'])

    print("Loading state data...")
    spray = pd.read_csv('input/LAYER_MAP_STATE.csv', sep=';', on_bad_lines='skip', low_memory=False)
    spray = spray.dropna(subset=['geometry'])
    
    spray['StateLower'] = spray['MachineState'].astype(str).str.strip().str.lower()
    spray_ops = spray[spray['StateLower'].isin(['operação', 'operacao', 'trabalhando'])]
    
    html += """
        // Pulverização linhas filtradas estritamente dentro dos talhões
        var linhasPulverizadas = [];
"""
    
    pulverizadas = 0
    fora_area = 0

    for idx, row in spray_ops.iterrows():
        coords = parse_wkt_line(row['geometry'])
        if len(coords) > 1:
            # Pegamos o primeiro ponto da linha [lat, lon]
            pt_lat, pt_lon = coords[0]
            inside_any = False
            for poly in all_polygons:
                # nosso poly tem [lat, lon]
                # point_in_polygon trata x e y. vamos passar (lat, lon)
                if point_in_polygon(pt_lat, pt_lon, poly):
                    inside_any = True
                    break
            
            if inside_any:
                html += f"            linhasPulverizadas.push({json.dumps(coords)});\n"
                pulverizadas += 1
            else:
                fora_area += 1
            
    html += """        
        linhasPulverizadas.forEach(function(line) {
            L.polyline(line, {color: '#3b82f6', weight: 3, opacity: 0.55}).addTo(map);
        });

        // Armadilhas points
"""
    for idx, row in traps.iterrows():
        name = str(row['code'])
        tipo = str(row.get('type', 'CONVENTIONAL')).upper()
        css_class = 'trap-elec' if tipo == 'ELECTRONIC' else 'trap-conv'
        legenda = 'Armadilha Eletrônica' if tipo == 'ELECTRONIC' else 'Armadilha Convencional'
        
        html += f"""
        var icon_{idx} = L.divIcon({{className: '{css_class}', iconSize: [16, 16]}});
        L.marker([{row['lat']}, {row['lon']}], {{icon: icon_{idx}}}).bindPopup("<b>{name}</b><br>{legenda}").addTo(map);
"""
    html += """
    </script>
</body>
</html>
"""
    with open('mapa_pragas.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"Map gen! Dentro: {pulverizadas} | Fora/Erros: {fora_area}")
    
if __name__ == "__main__":
    main()
