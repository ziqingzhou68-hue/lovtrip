import streamlit as st
import requests
from openai import OpenAI
import json
import re

# ── Page Config ──
st.set_page_config(
    page_title="LovTrip — 智能旅游规划助手",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS Injection ──
st.markdown("""
<style>
/* ============================================
   LOVTRIP PREMIUM THEME — Inspired by lovtrip.app
   ============================================ */

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

:root {
    --gradient-start: #ff6b8a;
    --gradient-mid: #e85d9e;
    --gradient-end: #7c3aed;
}

/* ── Global ── */
.stApp {
    background: linear-gradient(135deg, #fdf2f8 0%, #fce7f3 20%, #ede9fe 50%, #e0e7ff 80%, #f0f9ff 100%);
    background-attachment: fixed;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}

#MainMenu, footer, .stDeployButton, [data-testid="stDecoration"] { display: none !important; }
header[data-testid="stHeader"] { background: transparent !important; }
.main .block-container { padding-top: 1rem; max-width: 100%; }

/* ── Typography ── */
h1, h2, h3, h4, h5 { font-family: 'Inter', sans-serif !important; font-weight: 700 !important; letter-spacing: -0.02em; }
h1 { font-size: 2.2rem !important; background: linear-gradient(135deg, #7c3aed, #e85d9e); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; }

/* ── Sidebar (Light theme, matching main area) ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #eff6ff 0%, #dbeafe 25%, #e0f2fe 55%, #f0f9ff 100%) !important;
    border-right: 1px solid rgba(59,130,246,0.12) !important;
}
[data-testid="stSidebar"] .block-container { padding: 1.5rem 1.2rem; }
[data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3, [data-testid="stSidebar"] h4 { color: #1e1b4b !important; }
[data-testid="stSidebar"] p, [data-testid="stSidebar"] label, [data-testid="stSidebar"] .stMarkdown { color: #4a4567 !important; }
[data-testid="stSidebar"] input, [data-testid="stSidebar"] textarea {
    background: rgba(255,255,255,0.85) !important; border: 2px solid rgba(124,58,237,0.25) !important;
    border-radius: 12px !important; color: #1e1b4b !important; padding: 10px 14px !important;
    font-weight: 500 !important;
}
[data-testid="stSidebar"] input::placeholder, [data-testid="stSidebar"] textarea::placeholder { color: rgba(30,27,75,0.35) !important; }
[data-testid="stSidebar"] [data-baseweb="select"] > div {
    background: rgba(255,255,255,0.85) !important; border-color: rgba(124,58,237,0.25) !important; color: #1e1b4b !important; font-weight: 500 !important;
}
[data-testid="stSidebar"] [data-baseweb="select"] * { color: #1e1b4b !important; }
[data-testid="stSidebar"] [role="option"], [data-testid="stSidebar"] [role="listbox"] { background: #ffffff !important; color: #1e1b4b !important; }
[data-testid="stSidebar"] ul[role="listbox"] li { color: #1e1b4b !important; background: #ffffff !important; }
[data-testid="stSidebar"] ul[role="listbox"] li:hover { background: #ede9fe !important; color: #1e1b4b !important; }
[data-testid="stSidebar"] hr { border-color: rgba(124,58,237,0.12) !important; margin: 1rem 0 !important; }
[data-testid="stSidebar"] .stAlert { background: rgba(124,58,237,0.08) !important; border-radius: 12px !important; color: #1e1b4b !important; border: 1px solid rgba(124,58,237,0.15) !important; }
[data-testid="stSidebar"] .st-emotion-cache-yfq0x5 { color: #1e1b4b !important; }

/* ── Main Inputs ── */
.main input, .main textarea {
    border: 2px solid rgba(124,58,237,0.15) !important; border-radius: 14px !important;
    padding: 12px 16px !important; background: rgba(255,255,255,0.7) !important; z-index: 1; position: relative;
}
.main textarea { min-height: 80px !important; }

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(135deg, #ff6b8a 0%, #e85d9e 50%, #7c3aed 100%) !important;
    color: #ffffff !important; font-weight: 600 !important; font-size: 1.05rem !important;
    padding: 0.8rem 2.5rem !important; border: none !important; border-radius: 50px !important;
    transition: all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1.2) !important;
    box-shadow: 0 4px 20px rgba(232,93,158,0.35) !important; min-width: 220px;
}
.stButton > button:hover { transform: translateY(-3px) scale(1.02); box-shadow: 0 8px 32px rgba(232,93,158,0.5) !important; }
.stDownloadButton > button {
    background: linear-gradient(135deg, #7c3aed, #6366f1) !important; color: #ffffff !important;
    font-weight: 600 !important; border: none !important; border-radius: 50px !important;
    padding: 0.6rem 2rem !important; box-shadow: 0 4px 16px rgba(124,58,237,0.25) !important;
}

/* ── Cards & Containers ── */
hr { border: none !important; height: 1px !important; background: linear-gradient(90deg, transparent, rgba(124,58,237,0.12), transparent) !important; margin: 1.5rem 0 !important; }
.stAlert { border-radius: 16px !important; border: none !important; padding: 1rem 1.5rem !important; }

.map-wrapper {
    border-radius: 24px; overflow: hidden; border: 3px solid rgba(255,255,255,0.9);
    box-shadow: 0 8px 40px rgba(124,58,237,0.12); margin: 1rem 0; animation: fadeInUp 0.6s ease-out;
}
.result-container {
    background: rgba(255,255,255,0.75); backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px);
    border: 1px solid rgba(255,255,255,0.9); border-radius: 24px; padding: 2rem;
    box-shadow: 0 8px 40px rgba(124,58,237,0.1); line-height: 1.8;
}

.feature-grid { display: flex; gap: 1rem; margin: 1rem 0; flex-wrap: wrap; justify-content: center; }
.feature-card {
    flex: 1; min-width: 180px; max-width: 280px; background: rgba(255,255,255,0.7);
    backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px); border: 1px solid rgba(255,255,255,0.9);
    border-radius: 20px; padding: 1.5rem 1rem; text-align: center; box-shadow: 0 4px 20px rgba(124,58,237,0.06);
    transition: all 0.35s cubic-bezier(0.25, 0.8, 0.25, 1.2); animation: fadeInUp 0.6s ease-out both;
}
.feature-card:nth-child(2) { animation-delay: 0.1s; }
.feature-card:nth-child(3) { animation-delay: 0.2s; }
.feature-card:hover { transform: translateY(-6px); box-shadow: 0 12px 36px rgba(124,58,237,0.15); }
.feature-card .icon { font-size: 2.2rem; margin-bottom: 0.5rem; display: block; }

.poi-grid { display: flex; gap: 0.75rem; flex-wrap: wrap; justify-content: center; margin: 0.25rem 0 1rem; }
.poi-card {
    flex: 1; min-width: 200px; max-width: 260px; background: rgba(255,255,255,0.85);
    backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px); border: 1px solid rgba(255,255,255,0.9);
    border-radius: 18px; overflow: hidden; text-align: left;
    box-shadow: 0 3px 16px rgba(124,58,237,0.06); transition: all 0.35s cubic-bezier(0.25,0.8,0.25,1.2);
    animation: fadeInUp 0.4s ease-out both;
}
.poi-card:hover { transform: translateY(-6px); box-shadow: 0 12px 36px rgba(124,58,237,0.15); }
.poi-card .poi-img {
    width: 100%; height: 140px; object-fit: cover; display: block; background: linear-gradient(135deg, #ede9fe, #fce7f3);
}
.poi-card .poi-body { padding: 0.75rem 0.85rem; }
.poi-card h4 { font-size: 0.9rem; color: #1e1b4b; margin: 0 0 0.3rem; font-weight: 700; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.poi-card .poi-score { font-size: 0.75rem; color: #e85d9e; margin: 0.1rem 0; }
.poi-card .poi-addr { font-size: 0.72rem; color: #8b889e; margin: 0.1rem 0; line-height: 1.4; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }
.poi-card .poi-extra { font-size: 0.72rem; color: #a09db8; margin-top: 0.3rem; }

.section-badge {
    display: inline-block; background: linear-gradient(135deg, rgba(124,58,237,0.1), rgba(232,93,158,0.1));
    color: #7c3aed; font-weight: 600; font-size: 0.85rem; padding: 0.35rem 1rem;
    border-radius: 50px; letter-spacing: 0.05em; text-transform: uppercase; margin-bottom: 0.5rem;
}

/* ── Hero (compact) ── */
.hero { text-align: center; padding: 1.5rem 2rem 0.5rem; animation: fadeIn 0.8s ease-out; }
.hero .floating-icons { display: flex; justify-content: center; gap: 1.5rem; margin-bottom: 0.75rem; }
.hero .floating-icons span { font-size: 2rem; display: inline-block; }
.hero h1 { font-size: 2.4rem; }
.hero .subtitle { font-size: 0.95rem; color: #6b6880; max-width: 500px; margin: 0 auto; }

.footer { text-align: center; padding: 1.5rem 1rem; color: #9b97b8; font-size: 0.85rem; }
.footer .heart { color: #ff6b8a; animation: float 2s ease-in-out infinite; display: inline-block; }

/* ── Animations ── */
@keyframes float { 0%,100%{transform:translateY(0)rotate(0)} 25%{transform:translateY(-10px)rotate(2deg)} 75%{transform:translateY(-5px)rotate(-2deg)} }
@keyframes floatSlow { 0%,100%{transform:translateY(0)} 50%{transform:translateY(-14px)} }
@keyframes floatReverse { 0%,100%{transform:translateY(0)rotate(0)} 50%{transform:translateY(-12px)rotate(-3deg)} }
@keyframes fadeInUp { from{opacity:0;transform:translateY(30px)} to{opacity:1;transform:translateY(0)} }
@keyframes fadeIn { from{opacity:0} to{opacity:1} }
.float { animation: float 4s ease-in-out infinite; }
.float-slow { animation: floatSlow 6s ease-in-out infinite; }
.float-reverse { animation: floatReverse 5s ease-in-out infinite; }

::-webkit-scrollbar { width: 8px; }
::-webkit-scrollbar-thumb { background: rgba(124,58,237,0.2); border-radius: 10px; }

@media (max-width: 768px) {
    .hero h1 { font-size: 1.6rem; }
    .feature-card { max-width: 100%; }
}
</style>
""", unsafe_allow_html=True)

# ── Secrets ──
try:
    API_KEY = st.secrets["OPENAI_API_KEY"]
    BASE_URL = st.secrets.get("OPENAI_BASE_URL", "https://tokenhub.tencentmaas.com/v1/")
    MODEL = st.secrets.get("MODEL_NAME", "kimi-k2.7-code")
    BAIDU_AK = st.secrets.get("BAIDU_MAP_AK", "")
except KeyError:
    st.error("⚠️ 未找到 API Key！请在 .streamlit/secrets.toml 或 Streamlit Cloud 中配置。")
    st.stop()

# ── System Prompt ──
SYSTEM_PROMPT = """你是贴心专业、灵活全能的全域旅游规划助手，支持全球任意目的地、完全由用户自主决定出行时长，适配亲子、情侣、闺蜜、独自出行、家庭团建等全人群，可按需适配穷游、轻奢、休闲慢游、特种兵打卡等各类出行模式。

专注定制可直接落地的个性化旅游方案，整合目的地核心资源：精准筛选适配预算与地段的酒店民宿、梳理必游景点小众秘境、深挖本地特色美食老字号门店。

配套完整出行细节：交通接驳、最佳游玩时段、避雷攻略、穿搭建议、注意事项。行程规划时务必结合天气信息：若天气晴好推荐户外景点；若遇雨雪极端天气调整为室内替代方案。

输出格式要求：使用清晰的markdown排版，包含emoji图标、分级标题、重点加粗，让行程方案赏心悦目。"""

# ── Weather ──
def get_weather(city):
    try:
        url = f"https://wttr.in/{city}?format=j1"
        resp = requests.get(url, timeout=10)
        if resp.status_code != 200:
            return None
        data = resp.json()
        current = data.get("current_condition", [{}])[0]
        return {
            "weather": current.get("weatherDesc", [{}])[0].get("value", "未知"),
            "temp": f"{current.get('temp_C', '?')}°C",
            "feels_like": f"{current.get('FeelsLikeC', '?')}°C",
            "humidity": f"{current.get('humidity', '?')}%",
            "wind": f"{current.get('windspeedKmph', '?')} km/h"
        }
    except Exception:
        return None

# ── Baidu Geocoding ──
def baidu_geocode(city):
    if not BAIDU_AK:
        return None
    try:
        url = f"https://api.map.baidu.com/geocoding/v3/?address={city}&output=json&ak={BAIDU_AK}"
        resp = requests.get(url, timeout=10)
        data = resp.json()
        if data.get("status") == 0:
            loc = data["result"]["location"]
            return {"lng": loc["lng"], "lat": loc["lat"]}
    except Exception:
        pass
    return None

# ── Baidu Place Search ──
def baidu_place_search(query, lng, lat, radius=5000):
    if not BAIDU_AK:
        return []
    try:
        url = (
            f"https://api.map.baidu.com/place/v2/search?"
            f"query={query}&location={lat},{lng}&radius={radius}"
            f"&output=json&ak={BAIDU_AK}&scope=2&page_size=10"
        )
        resp = requests.get(url, timeout=10)
        data = resp.json()
        if data.get("status") == 0:
            return data.get("results", [])[:10]
    except Exception:
        pass
    return []

# ── Leaflet Map (FREE! No API key needed, works everywhere) ──
def render_map(center_lng, center_lat, markers=None, height=500):
    """Generate an interactive Leaflet map — no API key, works on any domain"""
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


def render_poi_grid(pois, emoji="📍"):
    if not pois:
        return '<p style="text-align:center;color:#9b97b8;padding:1.5rem;">🔍 输入目的地后自动搜索周边热门地点</p>'

    # Beautiful gradient pairs for fallback
    gradients = [
        ("#ff6b8a,#e85d9e"), ("#7c3aed,#6366f1"), ("#f59e0b,#f97316"),
        ("#10b981,#34d399"), ("#ec4899,#f472b6"), ("#3b82f6,#06b6d4"),
        ("#8b5cf6,#a78bfa"), ("#ef4444,#f87171"), ("#14b8a6,#2dd4bf"),
    ]

    import urllib.parse
    cards = ""
    for i, poi in enumerate(pois[:9]):
        name = poi.get("name", "未知")
        addr = poi.get("address", "") or ""
        score = poi.get("score", "") or ""
        price = poi.get("price", "") or ""
        delay = 0.08 * (i % 3)
        stars = "⭐" * min(5, max(1, int(float(score) // 20))) if score else ""
        grad = gradients[i % len(gradients)]

        # Try Picsum for real photos (Cloudflare CDN, works in China)
        seed = urllib.parse.quote(f"{name}")
        img_url = f"https://picsum.photos/seed/{seed}/400/300"

        cards += f"""
        <div class="poi-card" style="animation-delay:{delay}s;">
            <div class="poi-img" style="position:relative;background:linear-gradient(135deg,{grad});">
                <img src="{img_url}" alt="{name}" loading="lazy"
                    style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;"
                    onerror="this.style.display='none'"/>
                <span style="font-size:3rem;position:absolute;inset:0;display:flex;align-items:center;justify-content:center;">{emoji}</span>
            </div>
            <div class="poi-body">
                <h4 title="{name}">{name[:18]}{'…' if len(name) > 18 else ''}</h4>
                <p class="poi-score">{stars} {score or ''}</p>
                <p class="poi-addr">📍 {addr[:40]}{'…' if len(addr) > 40 else ''}</p>
                <p class="poi-extra">{'💰 ' + price if price else ''}</p>
            </div>
        </div>"""
    return cards


def build_map_markers(dest_coords, dest_name, pois_by_cat):
    """Build marker list from destination + POI categories"""
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


# ── Init OpenAI Client ──
client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

# ── Session State Init ──
if 'dest' not in st.session_state:
    st.session_state.dest = ''
if 'dur' not in st.session_state:
    st.session_state.dur = ''
if 'budget' not in st.session_state:
    st.session_state.budget = '适中'

# ── Sync callback: extract destination from text area → update sidebar ──
def sync_dest_from_text():
    """When user edits the text area, try to extract destination city"""
    txt = st.session_state.get('user_text', '')
    m = re.search(r'规划(.+?)的旅行方案', txt)
    if m:
        city = m.group(1).strip()
        if city and city != st.session_state.get('dest', ''):
            st.session_state.dest = city

# ═══════════════════════════════════════
#  HERO (compact)
# ═══════════════════════════════════════
st.markdown("""
<div class="hero">
    <div class="floating-icons">
        <span class="float">✈️</span><span class="float-slow">🗺️</span><span class="float-reverse">🌍</span>
        <span class="float">🏝️</span><span class="float-slow">🎒</span><span class="float-reverse">📸</span>
    </div>
    <h1>LovTrip · 智能旅游规划</h1>
    <p class="subtitle">全球目的地 · 随心定制天数 · AI 为您打造专属高品质旅行方案 ✨</p>
</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════
#  SIDEBAR
# ═══════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div style="text-align:center; margin-bottom:0.5rem;">
        <span style="font-size:2rem;">💜</span>
        <h4 style="margin:0.25rem 0; color:#1e1b4b !important;">行程偏好设置</h4>
    </div>
    """, unsafe_allow_html=True)

    destination = st.text_input("🌏 目的地", placeholder="例如：北京、东京、巴黎…", key="dest")

    col_d1, col_d2 = st.columns(2)
    with col_d1:
        duration = st.text_input("📅 出行时长", placeholder="3天2晚", key="dur")
    with col_d2:
        budget = st.selectbox("💰 预算等级", ["经济", "适中", "轻奢", "奢华"], key="budget")

    col_s1, col_s2 = st.columns(2)
    with col_s1:
        travel_style = st.selectbox("🎯 出行模式", ["经典游玩", "穷游", "轻奢", "休闲慢游", "特种兵打卡"])
    with col_s2:
        traveler_type = st.selectbox("👥 出行人群", ["独自出行", "情侣", "亲子", "闺蜜", "家庭团建", "朋友结伴"])

    additional_req = st.text_area("📝 其他需求", placeholder="例如：带老人、喜欢拍照…", key="extra")

    st.markdown("---")
    st.markdown("#### 🌤️ 天气系统")
    enable_weather = st.toggle("启用天气自适应规划", value=True)
    weather_city = st.text_input("天气查询城市", placeholder="默认同目的地", key="wxcity")

    # Auto-display weather when destination is entered
    if enable_weather and (weather_city or destination).strip():
        wx_query = (weather_city or destination).strip()
        wx = get_weather(wx_query)
        if wx:
            st.markdown(f"""
            <div style="background:rgba(124,58,237,0.06); border-radius:14px; padding:0.8rem; margin-top:0.5rem;
                border:1px solid rgba(124,58,237,0.12); text-align:center;">
                <p style="margin:0 0 0.3rem; font-size:0.8rem; color:#7c3aed; font-weight:600;">📍 {wx_query} 实时天气</p>
                <p style="margin:0; font-size:1.3rem; font-weight:700; color:#1e1b4b;">{wx['weather']} {wx['temp']}</p>
                <p style="margin:0.2rem 0 0; font-size:0.75rem; color:#6b6880;">
                    体感 {wx['feels_like']} · 湿度 {wx['humidity']} · 风速 {wx['wind']}
                </p>
            </div>
            """, unsafe_allow_html=True)

# ═══════════════════════════════════════
#  MAIN LAYOUT: Map Left | Controls Right
# ═══════════════════════════════════════
map_col, ctrl_col = st.columns([3, 2])

with ctrl_col:
    st.markdown("### 💬 描述您的旅行想法")

    # Build prompt from current sidebar values
    dest_val = st.session_state.get('dest', '') or '广州'
    dur_val = st.session_state.get('dur', '') or '3天2晚'
    budget_val = st.session_state.get('budget', '') or '适中'
    default_prompt = (
        f"请为我规划{dest_val}的旅行方案，出行时长{dur_val}，"
        f"出行模式为{travel_style}，出行人群为{traveler_type}，预算等级为{budget_val}。"
    )

    # Sync sidebar → text area: if dest changed, update user_text
    last_dest = st.session_state.get('_last_dest', None)
    if last_dest != dest_val:
        st.session_state.user_text = default_prompt
        st.session_state._last_dest = dest_val

    user_input = st.text_area(
        "旅行需求描述",
        height=150,
        placeholder="例如：我想去北京玩3天，带父母一起，预算适中…",
        key="user_text",
        on_change=sync_dest_from_text,
    )
    generate_clicked = st.button("🚀 开始生成行程", type="primary", use_container_width=True)

    # ── Quick POI Cards (below button) ──
    if destination.strip() and BAIDU_AK:
        coords_q = baidu_geocode(destination.strip())
        if coords_q:
            st.markdown("---")
            st.markdown("#### 🔍 周边热门", )
            qtab1, qtab2, qtab3 = st.tabs(["🎯 景点", "🏨 酒店", "🍜 美食"])
            with qtab1:
                spots = baidu_place_search("景点", coords_q["lng"], coords_q["lat"])
                st.markdown(f'<div class="poi-grid">{render_poi_grid(spots, "🎯")}</div>', unsafe_allow_html=True)
            with qtab2:
                hotels = baidu_place_search("酒店", coords_q["lng"], coords_q["lat"])
                st.markdown(f'<div class="poi-grid">{render_poi_grid(hotels, "🏨")}</div>', unsafe_allow_html=True)
            with qtab3:
                foods = baidu_place_search("美食", coords_q["lng"], coords_q["lat"])
                st.markdown(f'<div class="poi-grid">{render_poi_grid(foods, "🍜")}</div>', unsafe_allow_html=True)

with map_col:
    # ── THE MAP (centerpiece) ──
    if destination.strip():
        coords = baidu_geocode(destination.strip())
        if coords:
            st.markdown("""
            <div style="text-align:center; margin-bottom:0.25rem;">
                <span class="section-badge">🗺️ 目的地地图</span>
            </div>
            """, unsafe_allow_html=True)

            # Collect all POIs for map markers
            poi_cats = {}
            for cat in ["景点", "酒店", "美食"]:
                pois = baidu_place_search(cat, coords["lng"], coords["lat"])
                poi_cats[cat] = pois

            map_markers = build_map_markers(coords, destination.strip(), poi_cats)
            map_html = render_map(coords["lng"], coords["lat"], map_markers, height=580)
            st.markdown('<div class="map-wrapper">', unsafe_allow_html=True)
            st.components.v1.html(map_html, height=600, scrolling=False)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.info("🌍 正在查找目的地坐标…（如无结果请尝试更具体的地名）")
    else:
        # Empty state — beautiful placeholder
        st.markdown("""
        <div style="
            background: rgba(255,255,255,0.35); backdrop-filter: blur(20px);
            border: 2px dashed rgba(124,58,237,0.2); border-radius: 24px;
            padding: 5rem 2rem; text-align: center; min-height: 500px;
            display: flex; flex-direction: column; align-items: center; justify-content: center;
        ">
            <span style="font-size:4rem; display:block; margin-bottom:1rem;">🗺️</span>
            <h3 style="color:#4a4567; margin:0 0 0.5rem;">输入目的地，探索你的专属地图</h3>
            <p style="color:#9b97b8; margin:0;">在左侧边栏输入目的地 → 地图将自动加载</p>
            <p style="color:#9b97b8; margin:0.25rem 0 0;">可拖拽缩放 · 点击标记查看详情 · 多维度探索</p>
        </div>
        """, unsafe_allow_html=True)

# ═══════════════════════════════════════
#  GENERATION RESULT (full width)
# ═══════════════════════════════════════
if generate_clicked:
    if not user_input.strip():
        st.warning("⚠️ 请输入您的旅行需求")
    else:
        # Weather
        weather_info = None
        if enable_weather:
            query_city = weather_city or destination or "广州"
            with st.spinner(f"🌤️ 正在查询 {query_city} 实时天气…"):
                weather_info = get_weather(query_city)
            if weather_info:
                st.sidebar.success(f"✅ {query_city} 天气已获取")
                st.sidebar.info(
                    f"🌤️ **{weather_info['weather']}** | 🌡️ **{weather_info['temp']}**\n\n"
                    f"🤔 体感 {weather_info['feels_like']} | 💧 {weather_info['humidity']} | 🌬️ {weather_info['wind']}"
                )
            else:
                st.sidebar.warning("⚠️ 天气查询失败")

        # Visible loading state
        loading_placeholder = st.empty()
        loading_placeholder.markdown("""
        <div style="text-align:center; padding:3rem 2rem; animation:pulse 2s ease-in-out infinite;">
            <span style="font-size:3rem; display:block; margin-bottom:1rem;">✨</span>
            <h3 style="color:#7c3aed !important; margin:0 0 0.5rem;">AI 正在为您量身定制行程…</h3>
            <p style="color:#8b889e; margin:0;">正在分析目的地、筛选景点、规划路线，请稍候</p>
        </div>
        <style>
        @keyframes pulse { 0%,100%{opacity:1} 50%{opacity:0.6} }
        </style>
        """, unsafe_allow_html=True)

        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        msg = user_input
        if weather_info:
            msg += (
                f"\n\n【天气】{weather_city or destination}: "
                f"{weather_info['weather']} {weather_info['temp']}（体感{weather_info['feels_like']}）"
                f"湿度{weather_info['humidity']} 风速{weather_info['wind']}"
                f"\n请结合天气调整行程。"
            )
        if additional_req:
            msg += f"\n\n额外要求：{additional_req}"
        messages.append({"role": "user", "content": msg})

        response = client.chat.completions.create(
            model=MODEL, messages=messages, temperature=1, max_tokens=4000
        )
        result = response.choices[0].message.content

        # Clear loading placeholder
        loading_placeholder.empty()

        st.success("✅ 行程规划完成！")
        st.markdown(f'<div class="result-container">{result}</div>', unsafe_allow_html=True)

        # Download
        filename = f"{destination or '旅行'}_行程规划.txt"
        st.download_button(
            label="📥 下载行程规划",
            data=result.encode("utf-8"),
            file_name=filename,
            mime="text/plain",
        )

# ═══════════════════════════════════════
#  FOOTER
# ═══════════════════════════════════════
st.markdown("---")
st.markdown("""
<div class="footer">
    <p>Made with <span class="heart">❤️</span> by LovTrip · AI 智能旅游规划助手</p>
    <p style="font-size:0.78rem; opacity:0.65;">Powered by TokenHub LLM & Leaflet Maps</p>
</div>
""", unsafe_allow_html=True)
