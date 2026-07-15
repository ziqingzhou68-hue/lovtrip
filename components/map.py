"""地图组件模块

Leaflet 交互式地图渲染与标记构建。
"""

import json
from config import BAIDU_AK


def render_map(center_lng, center_lat, markers=None, height=500):
    """生成 Leaflet 交互式地图 HTML

    Args:
        center_lng: 中心经度
        center_lat: 中心纬度
        markers: 标记列表 [{"lng", "lat", "name", "addr", "icon", "color", "isDest"}, ...]
        height: 地图高度（像素）

    Returns:
        HTML 字符串
    """
    if markers is None:
        markers = []

    markers_json = json.dumps(markers, ensure_ascii=False)

    html = f"""<!DOCTYPE html>
<html lang="zh">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1.0"/>
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/>
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<style>
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ font-family: 'Inter', -apple-system, sans-serif; }}
#map {{ width:100%; height:{height}px; border-radius:20px; }}
.leaflet-popup-content-wrapper {{
    border-radius: 16px !important; padding: 0 !important;
    box-shadow: 0 8px 32px rgba(0,0,0,0.15) !important;
}}
.leaflet-popup-content {{
    margin: 12px 16px !important; font-family: 'Inter', sans-serif !important;
    font-size: 14px !important; line-height: 1.5 !important;
}}
.leaflet-popup-content h4 {{ margin:0 0 4px; color:#7c3aed; font-size:15px; }}
.leaflet-popup-content p {{ margin:0; color:#666; font-size:12px; }}
.custom-marker {{
    width: 32px; height: 32px; border-radius: 50%; border: 3px solid #fff;
    box-shadow: 0 3px 10px rgba(0,0,0,0.25); text-align: center; line-height: 26px;
    font-size: 16px; font-weight: bold; color: #fff;
}}
.marker-spot {{ background: #ef4444; }}
.marker-hotel {{ background: #f59e0b; }}
.marker-food {{ background: #10b981; }}
.marker-dest {{ background: #7c3aed; width:40px; height:40px; line-height:34px; font-size:20px; }}
</style>
</head>
<body>
<div id="map"></div>
<script>
var MapLayer = {{
    // Try CartoDB Positron (clean, modern)
    url: 'https://{{s}}.basemaps.cartocdn.com/light_all/{{z}}/{{x}}/{{y}}{{r}}.png',
    attr: '&copy; <a href="https://www.openstreetmap.org/copyright">OSM</a> &copy; <a href="https://carto.com/">CARTO</a>'
}};

var map = L.map('map', {{
    center: [{center_lat}, {center_lng}],
    zoom: 12,
    zoomControl: true,
    scrollWheelZoom: true
}});

L.tileLayer(MapLayer.url, {{
    attribution: MapLayer.attr,
    subdomains: 'abcd',
    maxZoom: 19
}}).addTo(map);

// Add scale control
L.control.scale({{position:'bottomleft', imperial:false}}).addTo(map);

// Markers
var markers = {markers_json};

markers.forEach(function(m) {{
    var color = m.color || '#7c3aed';
    var icon = L.divIcon({{
        className: '',
        iconSize: m.isDest ? [40,40] : [32,32],
        iconAnchor: m.isDest ? [20,20] : [16,16],
        popupAnchor: [0, m.isDest ? -20 : -16],
        html: '<div style="background:' + color + ';width:' + (m.isDest?40:32) + 'px;height:' + (m.isDest?40:32) + 'px;'
            + 'border-radius:50%;border:3px solid #fff;box-shadow:0 3px 10px rgba(0,0,0,0.25);'
            + 'text-align:center;line-height:' + (m.isDest?34:26) + 'px;font-size:' + (m.isDest?20:14) + 'px;'
            + 'color:#fff;font-weight:bold;">' + (m.icon || '📍') + '</div>'
    }});

    var popup = '<h4>' + m.name + '</h4>';
    if (m.addr) popup += '<p>' + m.addr + '</p>';
    if (m.score) popup += '<p style="color:#e85d9e;">⭐ ' + m.score + '</p>';

    L.marker([m.lat, m.lng], {{icon: icon}})
        .bindPopup(popup)
        .addTo(map);
}});

// Fit all markers
if (markers.length > 1) {{
    var group = new L.featureGroup(markers.map(function(m) {{
        return L.marker([m.lat, m.lng]);
    }}));
    map.fitBounds(group.getBounds().pad(0.15));
}}
</script>
</body>
</html>"""
    return html


def build_map_markers(dest_coords, dest_name, pois_by_cat):
    """从目的地和 POI 分类构建地图标记列表

    Args:
        dest_coords: {"lng": float, "lat": float}
        dest_name: 目的地名称
        pois_by_cat: {"景点": [...], "酒店": [...], "美食": [...]}

    Returns:
        标记列表
    """
    markers = [{
        "lng": dest_coords["lng"], "lat": dest_coords["lat"],
        "name": dest_name, "addr": "目的地", "icon": "📍",
        "color": "#7c3aed", "isDest": True
    }]
    cat_config = {"景点": ("🎯", "#ef4444"), "酒店": ("🏨", "#f59e0b"), "美食": ("🍜", "#10b981")}
    for cat, pois in pois_by_cat.items():
        emoji, color = cat_config.get(cat, ("📍", "#6366f1"))
        for p in pois[:6]:
            if p.get("location"):
                markers.append({
                    "lng": p["location"]["lng"], "lat": p["location"]["lat"],
                    "name": p.get("name", cat), "addr": p.get("address", "") or "",
                    "score": p.get("score", "") or "", "icon": emoji,
                    "color": color, "isDest": False
                })
    return markers
