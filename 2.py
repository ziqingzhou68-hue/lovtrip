import streamlit as st
import requests
from openai import OpenAI

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

/* ── Root Variables ── */
:root {
    --gradient-start: #ff6b8a;
    --gradient-mid: #e85d9e;
    --gradient-end: #7c3aed;
    --card-bg: rgba(255,255,255,0.18);
    --card-border: rgba(255,255,255,0.25);
    --text-primary: #1e1b4b;
    --text-secondary: #4a4567;
    --text-light: #ffffff;
    --shadow-soft: 0 4px 24px rgba(124,58,237,0.12);
    --shadow-card: 0 8px 40px rgba(124,58,237,0.15);
    --shadow-glow: 0 0 40px rgba(255,107,138,0.3);
    --radius-sm: 10px;
    --radius-md: 16px;
    --radius-lg: 24px;
    --radius-xl: 32px;
}

/* ── Global Reset ── */
.stApp {
    background: linear-gradient(135deg, #fdf2f8 0%, #fce7f3 20%, #ede9fe 50%, #e0e7ff 80%, #f0f9ff 100%);
    background-attachment: fixed;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}

/* ── Hide Streamlit Branding ── */
#MainMenu, footer, .stDeployButton, [data-testid="stDecoration"] {
    display: none !important;
}

header[data-testid="stHeader"] {
    background: transparent !important;
}

/* ── Main Content Area ── */
.main .block-container {
    padding-top: 2rem;
    max-width: 1100px;
}

/* ── Typography ── */
h1, h2, h3, h4 {
    font-family: 'Inter', sans-serif !important;
    font-weight: 700 !important;
    letter-spacing: -0.02em;
}

h1 { font-size: 2.5rem !important; background: linear-gradient(135deg, #7c3aed, #e85d9e); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; }
h2 { font-size: 1.75rem !important; color: #1e1b4b !important; }
h3 { font-size: 1.25rem !important; color: #1e1b4b !important; }

p, li, label, .stMarkdown {
    color: #4a4567;
    line-height: 1.7;
}

/* ── Sidebar — Dark Glassmorphism ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1e1b4b 0%, #2d1b69 40%, #3b1f8c 100%) !important;
    border-right: 1px solid rgba(255,255,255,0.08) !important;
}

[data-testid="stSidebar"] .block-container {
    padding: 2rem 1.5rem;
}

[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] h4 {
    color: #ffffff !important;
    font-weight: 700 !important;
}

[data-testid="stSidebar"] p,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] .stMarkdown,
[data-testid="stSidebar"] .stCaption {
    color: rgba(255,255,255,0.8) !important;
}

[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stTextInput label,
[data-testid="stSidebar"] .stTextArea label {
    color: rgba(255,255,255,0.9) !important;
    font-weight: 500;
}

/* ── Sidebar Inputs ── */
[data-testid="stSidebar"] input,
[data-testid="stSidebar"] textarea,
[data-testid="stSidebar"] .stSelectbox [data-baseweb="select"] {
    background: rgba(255,255,255,0.1) !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
    border-radius: 12px !important;
    color: #ffffff !important;
    padding: 10px 14px !important;
    font-size: 0.9rem !important;
    transition: all 0.3s ease !important;
}

[data-testid="stSidebar"] input::placeholder,
[data-testid="stSidebar"] textarea::placeholder {
    color: rgba(255,255,255,0.4) !important;
}

[data-testid="stSidebar"] input:focus,
[data-testid="stSidebar"] textarea:focus {
    border-color: rgba(255,255,255,0.4) !important;
    box-shadow: 0 0 0 3px rgba(255,107,138,0.2) !important;
    outline: none !important;
}

/* ── Sidebar Selectbox ── */
[data-testid="stSidebar"] [data-baseweb="select"] > div {
    background: rgba(255,255,255,0.1) !important;
    border-color: rgba(255,255,255,0.15) !important;
    color: #ffffff !important;
}

/* ── Sidebar Toggle ── */
[data-testid="stSidebar"] .stCheckbox label,
[data-testid="stSidebar"] [data-testid="stToggle"] label {
    color: rgba(255,255,255,0.9) !important;
}

/* ── Sidebar Divider ── */
[data-testid="stSidebar"] hr {
    border-color: rgba(255,255,255,0.1) !important;
    margin: 1.5rem 0 !important;
}

/* ── Sidebar Success/Info boxes ── */
[data-testid="stSidebar"] .stAlert {
    background: rgba(255,255,255,0.1) !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
    color: #ffffff !important;
    border-radius: 12px !important;
}

/* ── Main Content Cards ── */
div[data-testid="stVerticalBlock"] > div[style] .stMarkdown {
    background: rgba(255,255,255,0.6);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border: 1px solid rgba(255,255,255,0.8);
    border-radius: 20px;
    padding: 1.5rem 2rem;
    box-shadow: 0 4px 24px rgba(124,58,237,0.08);
}

/* ── Primary Button ── */
.stButton > button {
    background: linear-gradient(135deg, #ff6b8a 0%, #e85d9e 50%, #7c3aed 100%) !important;
    color: #ffffff !important;
    font-weight: 600 !important;
    font-size: 1.05rem !important;
    padding: 0.8rem 2.5rem !important;
    border: none !important;
    border-radius: 50px !important;
    cursor: pointer !important;
    transition: all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1.2) !important;
    box-shadow: 0 4px 20px rgba(232,93,158,0.35), 0 0 0 0 rgba(124,58,237,0.4) !important;
    letter-spacing: 0.02em;
    width: auto !important;
    min-width: 220px;
}

.stButton > button:hover {
    transform: translateY(-3px) scale(1.02);
    box-shadow: 0 8px 32px rgba(232,93,158,0.5), 0 0 0 8px rgba(124,58,237,0.08) !important;
}

.stButton > button:active {
    transform: translateY(-1px) scale(0.99);
}

/* ── Text Inputs (Main Area) ── */
.main input, .main textarea {
    border: 2px solid rgba(124,58,237,0.15) !important;
    border-radius: 14px !important;
    padding: 12px 16px !important;
    font-size: 0.95rem !important;
    transition: all 0.3s ease !important;
    background: rgba(255,255,255,0.7) !important;
}

.main input:focus, .main textarea:focus {
    border-color: #7c3aed !important;
    box-shadow: 0 0 0 4px rgba(124,58,237,0.08) !important;
    outline: none !important;
    background: #ffffff !important;
}

/* ── Select Box (Main) ── */
.main [data-baseweb="select"] > div {
    border-color: rgba(124,58,237,0.15) !important;
    border-radius: 14px !important;
    background: rgba(255,255,255,0.7) !important;
}

/* ── Expander / Horizontal Rule ── */
hr {
    border: none !important;
    height: 1px !important;
    background: linear-gradient(90deg, transparent, rgba(124,58,237,0.15), transparent) !important;
    margin: 2rem 0 !important;
}

/* ── Info / Success / Warning Boxes ── */
.stAlert {
    border-radius: 16px !important;
    border: none !important;
    padding: 1rem 1.5rem !important;
    font-weight: 500;
}

div[data-testid="stInfo"] {
    background: rgba(224,231,255,0.6) !important;
    backdrop-filter: blur(12px);
    border: 1px solid rgba(124,58,237,0.15) !important;
}

div[data-testid="stSuccess"] {
    background: rgba(220,252,231,0.7) !important;
    backdrop-filter: blur(12px);
    border: 1px solid rgba(34,197,94,0.2) !important;
}

/* ── Spinner ── */
.stSpinner > div {
    border-top-color: #7c3aed !important;
    border-width: 3px !important;
}

/* ── Download Button ── */
.stDownloadButton > button {
    background: linear-gradient(135deg, #7c3aed, #6366f1) !important;
    color: #ffffff !important;
    font-weight: 600 !important;
    border: none !important;
    border-radius: 50px !important;
    padding: 0.6rem 2rem !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 16px rgba(124,58,237,0.25) !important;
}

.stDownloadButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(124,58,237,0.4) !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 8px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(124,58,237,0.2); border-radius: 10px; }
::-webkit-scrollbar-thumb:hover { background: rgba(124,58,237,0.35); }

/* ── Tabs (if used) ── */
.stTabs [data-baseweb="tab"] {
    font-weight: 500 !important;
    color: #4a4567 !important;
    border-radius: 12px 12px 0 0 !important;
}

.stTabs [aria-selected="true"] {
    color: #7c3aed !important;
    font-weight: 600 !important;
}

/* ── Floating Animations ── */
@keyframes float {
    0%, 100% { transform: translateY(0px) rotate(0deg); }
    25% { transform: translateY(-12px) rotate(3deg); }
    75% { transform: translateY(-6px) rotate(-2deg); }
}

@keyframes floatSlow {
    0%, 100% { transform: translateY(0px); }
    50% { transform: translateY(-18px); }
}

@keyframes floatReverse {
    0%, 100% { transform: translateY(0px) rotate(0deg); }
    50% { transform: translateY(-14px) rotate(-4deg); }
}

@keyframes pulseGlow {
    0%, 100% { box-shadow: 0 4px 20px rgba(232,93,158,0.3); }
    50% { box-shadow: 0 4px 36px rgba(232,93,158,0.55); }
}

@keyframes shimmer {
    0% { background-position: -200% center; }
    100% { background-position: 200% center; }
}

@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(30px); }
    to { opacity: 1; transform: translateY(0); }
}

@keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
}

.float { animation: float 4s ease-in-out infinite; }
.float-slow { animation: floatSlow 6s ease-in-out infinite; }
.float-reverse { animation: floatReverse 5s ease-in-out infinite; }

/* ── Feature Card Grid (3-column) ── */
.feature-grid {
    display: flex;
    gap: 1.5rem;
    margin: 1.5rem 0;
    flex-wrap: wrap;
    justify-content: center;
}

.feature-card {
    flex: 1;
    min-width: 200px;
    max-width: 320px;
    background: rgba(255,255,255,0.7);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border: 1px solid rgba(255,255,255,0.9);
    border-radius: 24px;
    padding: 2rem 1.5rem;
    text-align: center;
    box-shadow: 0 4px 24px rgba(124,58,237,0.08);
    transition: all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1.2);
    animation: fadeInUp 0.6s ease-out both;
}

.feature-card:nth-child(2) { animation-delay: 0.15s; }
.feature-card:nth-child(3) { animation-delay: 0.3s; }

.feature-card:hover {
    transform: translateY(-8px);
    box-shadow: 0 16px 48px rgba(124,58,237,0.18);
    border-color: rgba(232,93,158,0.3);
}

.feature-card .icon {
    font-size: 3rem;
    margin-bottom: 1rem;
    display: block;
}

.feature-card h3 {
    font-size: 1.15rem;
    color: #1e1b4b;
    margin-bottom: 0.5rem;
    font-weight: 700;
}

.feature-card p {
    font-size: 0.9rem;
    color: #6b6880;
    line-height: 1.6;
}

/* ── Hero Banner ── */
.hero {
    text-align: center;
    padding: 3rem 2rem 2rem;
    position: relative;
    overflow: hidden;
    animation: fadeIn 0.8s ease-out;
}

.hero::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(ellipse at center, rgba(232,93,158,0.06) 0%, transparent 70%);
    pointer-events: none;
}

.hero .floating-icons {
    display: flex;
    justify-content: center;
    gap: 2rem;
    margin-bottom: 1.5rem;
    flex-wrap: wrap;
}

.hero .floating-icons span {
    font-size: 2.5rem;
    display: inline-block;
}

.hero h1 {
    font-size: 3rem;
    font-weight: 800;
    letter-spacing: -0.03em;
    margin-bottom: 0.75rem;
    background: linear-gradient(135deg, #7c3aed 0%, #e85d9e 60%, #ff6b8a 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.hero .subtitle {
    font-size: 1.15rem;
    color: #6b6880;
    font-weight: 400;
    max-width: 520px;
    margin: 0 auto;
    line-height: 1.7;
}

/* ── Result Card ── */
.result-container {
    background: rgba(255,255,255,0.75);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border: 1px solid rgba(255,255,255,0.9);
    border-radius: 24px;
    padding: 2rem;
    box-shadow: 0 8px 40px rgba(124,58,237,0.1);
    animation: fadeInUp 0.5s ease-out;
    line-height: 1.8;
}

/* ── Map Container ── */
.map-wrapper {
    border-radius: 24px;
    overflow: hidden;
    box-shadow: 0 8px 40px rgba(124,58,237,0.12);
    border: 1px solid rgba(255,255,255,0.8);
    margin: 1.5rem 0;
    animation: fadeInUp 0.6s ease-out;
}

/* ── POI Card Grid ── */
.poi-grid {
    display: flex;
    gap: 1rem;
    flex-wrap: wrap;
    justify-content: center;
    margin: 0.5rem 0 1.5rem;
}

.poi-card {
    flex: 1;
    min-width: 180px;
    max-width: 280px;
    background: rgba(255,255,255,0.7);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border: 1px solid rgba(255,255,255,0.9);
    border-radius: 20px;
    padding: 1.25rem 1rem;
    text-align: center;
    box-shadow: 0 4px 20px rgba(124,58,237,0.06);
    transition: all 0.35s cubic-bezier(0.25, 0.8, 0.25, 1.2);
}

.poi-card:hover {
    transform: translateY(-6px);
    box-shadow: 0 12px 36px rgba(124,58,237,0.15);
    border-color: rgba(232,93,158,0.25);
}

.poi-card .icon {
    font-size: 2rem;
    display: block;
    margin-bottom: 0.5rem;
}

.poi-card h4 {
    font-size: 0.95rem;
    color: #1e1b4b;
    margin: 0.3rem 0;
    font-weight: 700;
}

.poi-card .poi-score {
    font-size: 0.8rem;
    color: #e85d9e;
    margin: 0.2rem 0;
}

.poi-card .poi-addr {
    font-size: 0.78rem;
    color: #8b889e;
    margin: 0.2rem 0;
    line-height: 1.4;
}

.poi-card .poi-extra {
    font-size: 0.75rem;
    color: #a09db8;
    margin-top: 0.3rem;
}

/* ── Tab Buttons ── */
.poi-tabs {
    display: flex;
    gap: 0.5rem;
    justify-content: center;
    margin: 0.5rem 0 1rem;
    flex-wrap: wrap;
}

.poi-tab {
    padding: 0.5rem 1.25rem;
    border-radius: 50px;
    border: 1.5px solid rgba(124,58,237,0.2);
    background: rgba(255,255,255,0.5);
    color: #4a4567;
    font-weight: 500;
    font-size: 0.9rem;
    cursor: pointer;
    transition: all 0.3s ease;
    backdrop-filter: blur(10px);
}

.poi-tab:hover, .poi-tab.active {
    background: linear-gradient(135deg, #7c3aed, #e85d9e);
    color: #fff;
    border-color: transparent;
    box-shadow: 0 4px 16px rgba(124,58,237,0.3);
}

/* ── Footer ── */
.footer {
    text-align: center;
    padding: 2rem 1rem;
    color: #9b97b8;
    font-size: 0.85rem;
    font-weight: 400;
}

.footer .heart {
    color: #ff6b8a;
    animation: float 2s ease-in-out infinite;
    display: inline-block;
}

/* ── Responsive ── */
@media (max-width: 768px) {
    .hero h1 { font-size: 2rem; }
    .hero .floating-icons span { font-size: 1.8rem; }
    .feature-grid { flex-direction: column; align-items: center; }
    .feature-card { max-width: 100%; }
}

/* ── Section headers ── */
.section-badge {
    display: inline-block;
    background: linear-gradient(135deg, rgba(124,58,237,0.1), rgba(232,93,158,0.1));
    color: #7c3aed;
    font-weight: 600;
    font-size: 0.85rem;
    padding: 0.35rem 1rem;
    border-radius: 50px;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    margin-bottom: 0.5rem;
}

</style>
""", unsafe_allow_html=True)

# Local: set in .streamlit/secrets.toml
# Cloud: set in Streamlit Community Cloud dashboard → Settings → Secrets
try:
    API_KEY = st.secrets["OPENAI_API_KEY"]
    BASE_URL = st.secrets.get("OPENAI_BASE_URL", "https://tokenhub.tencentmaas.com/v1/")
    MODEL = st.secrets.get("MODEL_NAME", "kimi-k2.7-code")
    BAIDU_AK = st.secrets.get("BAIDU_MAP_AK", "")
except KeyError:
    st.error("⚠️ 未找到 API Key！请在 .streamlit/secrets.toml 或 Streamlit Cloud 中配置。")
    st.stop()

# ── System Prompt ──
SYSTEM_PROMPT = """你是贴心专业、灵活全能的全域旅游规划助手，支持全球任意目的地、完全由用户自主决定出行时长（半日/单日/多日、随心定制天数时段），适配亲子、情侣、闺蜜、独自出行、家庭团建等全人群，可按需适配穷游、轻奢、休闲慢游、特种兵打卡等各类出行模式。

专注定制可直接落地的个性化旅游方案，全方位整合目的地核心资源：精准筛选适配预算与地段的酒店、民宿、特色住宿；梳理必游景点、小众秘境、免费打卡地，合理规划游玩顺序与停留时长；深挖本地特色美食、地道小吃、老字号门店，搭配专属餐饮推荐。

同时配套完整出行细节，包含交通接驳、最佳游玩时段、避雷攻略、穿搭建议、注意事项，行程节奏可自由松紧调整，全程无固定模板，完全贴合用户的时间、预算、游玩偏好，打造专属高品质出行方案。

行程规划时务必结合天气信息：若天气晴好，推荐户外景点和露天活动；若遇雨雪或极端天气，调整为室内景点、博物馆、商场等替代方案，并给出相应的出行提醒和穿搭建议。

输出格式要求：使用清晰的markdown排版，包含emoji图标、分级标题、重点加粗，让行程方案赏心悦目。"""

# ── Weather Function ──
def get_weather(city):
    try:
        url = f"https://wttr.in/{city}?format=j1"
        resp = requests.get(url, timeout=10)
        if resp.status_code != 200:
            return None
        data = resp.json()
        current = data.get("current_condition", [{}])[0]
        weather_desc = current.get("weatherDesc", [{}])[0].get("value", "未知")
        temp = current.get("temp_C", "?")
        humidity = current.get("humidity", "?")
        wind = current.get("windspeedKmph", "?")
        feels_like = current.get("FeelsLikeC", "?")
        return {
            "weather": weather_desc,
            "temp": f"{temp}°C",
            "feels_like": f"{feels_like}°C",
            "humidity": f"{humidity}%",
            "wind": f"{wind} km/h"
        }
    except Exception:
        return None

# ── Baidu Maps API Functions ──

@st.cache_data(ttl=3600, show_spinner=False)
def baidu_geocode(city):
    """Convert city name to coordinates using Baidu Geocoding API"""
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


@st.cache_data(ttl=1800, show_spinner=False)
def baidu_place_search(query, lng, lat, radius=5000):
    """Search for POIs near a location using Baidu Place API"""
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


def render_baidu_map(center_lng, center_lat, markers=None, height=420):
    """Generate an interactive Baidu Map iframe"""
    if markers is None:
        markers = []

    # Build marker JS
    marker_js = ""
    for i, m in enumerate(markers):
        lng, lat, name, addr = m["lng"], m["lat"], m.get("name", ""), m.get("addr", "")
        icon_color = m.get("color", "#7c3aed")
        marker_js += f"""
        (function() {{
            var pt = new BMap.Point({lng}, {lat});
            var mk = new BMap.Marker(pt);
            var label = new BMap.Label("{name}", {{offset: new BMap.Size(20, -10)}});
            label.setStyle({{
                color: "#1e1b4b", fontSize: "12px", fontWeight: "600",
                padding: "4px 10px", borderRadius: "20px",
                background: "rgba(255,255,255,0.9)", border: "1px solid rgba(124,58,237,0.3)",
                boxShadow: "0 2px 8px rgba(0,0,0,0.1)", whiteSpace: "nowrap"
            }});
            mk.setLabel(label);
            var info = new BMap.InfoWindow(
                '<div style="font-family:Inter,sans-serif;padding:4px;">' +
                '<h4 style="margin:0 0 4px;color:#7c3aed;">{name}</h4>' +
                '<p style="margin:0;font-size:12px;color:#666;">{addr}</p></div>',
                {{width: 200, title: ""}}
            );
            mk.addEventListener("click", function() {{ this.openInfoWindow(info); }});
            map.addOverlay(mk);
        }})();
        """

    html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<style>
  * {{ margin:0; padding:0; }}
  html, body, #map {{ width:100%; height:{height}px; border-radius:20px; overflow:hidden; }}
  .bmap-copyright {{ display:none !important; }}
  .anchorBL {{ display:none !important; }}
</style>
<script src="https://api.map.baidu.com/api?v=3.0&ak={BAIDU_AK}"></script>
</head>
<body>
<div id="map"></div>
<script>
try {{
    var map = new BMap.Map("map");
    var center = new BMap.Point({center_lng}, {center_lat});
    map.centerAndZoom(center, 13);
    map.enableScrollWheelZoom(true);
    map.addControl(new BMap.NavigationControl({{anchor:BMAP_ANCHOR_TOP_RIGHT, offset:new BMap.Size(16,60)}}));
    map.addControl(new BMap.ScaleControl({{anchor:BMAP_ANCHOR_BOTTOM_LEFT, offset:new BMap.Size(16,30)}}));
    map.setMapStyle({{style:'midnight'}});
    // Center marker with pulse circle
    var centerMarker = new BMap.Marker(center);
    map.addOverlay(centerMarker);
    {marker_js}
}} catch(e) {{ console.log("Map init error:", e); }}
</script>
</body>
</html>"""
    return html


def render_poi_grid(pois, emoji="📍"):
    """Render POI cards in a 3-column glassmorphism grid"""
    if not pois:
        return '<p style="text-align:center;color:#9b97b8;padding:1rem;">暂无数据，请输入目的地后搜索</p>'

    cards = ""
    for i, poi in enumerate(pois[:9]):
        name = poi.get("name", "未知")
        addr = poi.get("address", "") or ""
        score = poi.get("score", "") or ""
        price = poi.get("price", "") or ""
        tel = poi.get("telephone", "") or ""
        delay = 0.1 * (i % 3)
        stars = "⭐" * min(5, max(1, int(float(score) // 20))) if score else ""
        cards += f"""
        <div class="poi-card" style="animation: fadeInUp 0.5s ease-out {delay}s both;">
            <span class="icon">{emoji}</span>
            <h4>{name}</h4>
            <p class="poi-score">{stars} {score or ''}</p>
            <p class="poi-addr">📍 {addr[:40]}{'…' if len(addr) > 40 else ''}</p>
            <p class="poi-extra">{'💰 ' + price if price else ''}{' 📞 ' + tel if tel else ''}</p>
        </div>"""
    return cards


# ── Init OpenAI Client ──
client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

# ═══════════════════════════════════════
#  HERO SECTION
# ═══════════════════════════════════════
st.markdown("""
<div class="hero">
    <div class="floating-icons">
        <span class="float">✈️</span>
        <span class="float-slow">🗺️</span>
        <span class="float-reverse">🌍</span>
        <span class="float">🏝️</span>
        <span class="float-slow">🎒</span>
        <span class="float-reverse">📸</span>
    </div>
    <h1>LovTrip · 智能旅游规划</h1>
    <p class="subtitle">
        全球目的地 · 随心定制天数 · 适配全人群全模式<br>
        AI 为您打造专属高品质旅行方案 ✨
    </p>
</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════
#  FEATURE CARDS
# ═══════════════════════════════════════
st.markdown("""
<div style="text-align:center; margin-bottom:0.5rem;">
    <span class="section-badge">🌟 为什么选择 LovTrip</span>
</div>

<div class="feature-grid">
    <div class="feature-card">
        <span class="icon">🎯</span>
        <h3>千人千面</h3>
        <p>亲子、情侣、闺蜜、独自出行…<br>精准匹配你的旅行 DNA</p>
    </div>
    <div class="feature-card">
        <span class="icon">🌤️</span>
        <h3>天气自适应</h3>
        <p>实时天气智能调整行程<br>晴天户外 · 雨天备选</p>
    </div>
    <div class="feature-card">
        <span class="icon">💎</span>
        <h3>深度定制</h3>
        <p>穷游到奢华 · 慢游到特种兵<br>每一程都与众不同</p>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

# ═══════════════════════════════════════
#  SIDEBAR
# ═══════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div style="text-align:center; margin-bottom:1rem;">
        <span style="font-size:2.5rem;">💜</span>
        <h3 style="margin:0.5rem 0; color:#fff;">行程偏好</h3>
    </div>
    """, unsafe_allow_html=True)

    destination = st.text_input(
        "🌏 目的地",
        placeholder="例如：北京、东京、巴黎…",
        label_visibility="visible"
    )
    duration = st.text_input(
        "📅 出行时长",
        placeholder="例如：3天2晚、半日游…",
        label_visibility="visible"
    )

    col1, col2 = st.columns(2)
    with col1:
        travel_style = st.selectbox("🎯 出行模式", ["经典游玩", "穷游", "轻奢", "休闲慢游", "特种兵打卡"])
    with col2:
        traveler_type = st.selectbox("👥 出行人群", ["独自出行", "情侣", "亲子", "闺蜜", "家庭团建", "朋友结伴"])

    budget = st.select_slider("💰 预算等级", options=["经济", "适中", "轻奢", "奢华"])
    additional_req = st.text_area("📝 其他需求（可选）", placeholder="例如：带老人、喜欢拍照、不吃辣…")

    st.markdown("---")
    st.markdown("#### 🌤️ 天气系统")
    enable_weather = st.toggle("启用天气自适应规划", value=True)
    weather_city = st.text_input("查询城市", placeholder="默认同目的地")

# ═══════════════════════════════════════
#  MAP + POI EXPLORER
# ═══════════════════════════════════════
if destination.strip() and BAIDU_AK:
    coords = baidu_geocode(destination.strip())
    if coords:
        st.markdown("""
        <div style="text-align:center; margin-bottom:0.5rem;">
            <span class="section-badge">🗺️ 目的地探索</span>
        </div>
        """, unsafe_allow_html=True)

        # Interactive Map
        dest_marker = [{
            "lng": coords["lng"], "lat": coords["lat"],
            "name": destination.strip(), "addr": "",
            "color": "#ff6b8a"
        }]
        map_html = render_baidu_map(coords["lng"], coords["lat"], dest_marker, height=420)
        st.markdown('<div class="map-wrapper">', unsafe_allow_html=True)
        st.components.v1.html(map_html, height=440, scrolling=False)
        st.markdown('</div>', unsafe_allow_html=True)

        # POI Explorer Tabs
        st.markdown("""
        <div style="text-align:center; margin:1rem 0 0.25rem;">
            <h4 style="color:#1e1b4b;">🔍 探索周边热门地点</h4>
        </div>
        """, unsafe_allow_html=True)

        tab1, tab2, tab3 = st.tabs(["🎯 热门景点", "🏨 住宿推荐", "🍜 美食餐饮"])

        with tab1:
            with st.spinner("🔍 搜索周边景点…"):
                spots = baidu_place_search("景点", coords["lng"], coords["lat"])
            st.markdown(f'<div class="poi-grid">{render_poi_grid(spots, "🎯")}</div>', unsafe_allow_html=True)

        with tab2:
            with st.spinner("🔍 搜索周边酒店…"):
                hotels = baidu_place_search("酒店", coords["lng"], coords["lat"])
            st.markdown(f'<div class="poi-grid">{render_poi_grid(hotels, "🏨")}</div>', unsafe_allow_html=True)

        with tab3:
            with st.spinner("🔍 搜索周边美食…"):
                foods = baidu_place_search("美食", coords["lng"], coords["lat"])
            st.markdown(f'<div class="poi-grid">{render_poi_grid(foods, "🍜")}</div>', unsafe_allow_html=True)

        st.markdown("<hr>", unsafe_allow_html=True)

# ═══════════════════════════════════════
#  MAIN CONTENT
# ═══════════════════════════════════════
st.markdown("### 💬 描述您的旅行想法")

default_prompt = (
    f"请为我规划{destination or '广州'}的旅行方案，出行时长{duration or '3天2晚'}，"
    f"出行模式为{travel_style}，出行人群为{traveler_type}，预算等级为{budget}。"
)

user_input = st.text_area(
    "旅行需求描述",
    value=default_prompt,
    height=130,
    placeholder="例如：我想去北京玩3天，带父母一起，预算适中…",
    label_visibility="collapsed",
)

# ── Center the button ──
col_btn1, col_btn2, col_btn3 = st.columns([1, 1.2, 1])
with col_btn2:
    generate_clicked = st.button("🚀 开始生成行程", type="primary", use_container_width=True)

# ── Generation Logic ──
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
                    f"🌤️ **{weather_info['weather']}**  |  🌡️ **{weather_info['temp']}**\n\n"
                    f"🤔 体感 **{weather_info['feels_like']}**  |  💧 {weather_info['humidity']}  |  🌬️ {weather_info['wind']}"
                )
            else:
                st.sidebar.warning("⚠️ 天气查询失败，将按默认模式规划")

        with st.spinner("✨ AI 正在为您量身定制行程，请稍候…"):
            messages = [{"role": "system", "content": SYSTEM_PROMPT}]

            if weather_info:
                weather_context = (
                    f"\n\n【当前目的地天气信息】\n"
                    f"城市：{weather_city or destination or '广州'}\n"
                    f"天气状况：{weather_info['weather']}\n"
                    f"温度：{weather_info['temp']}（体感 {weather_info['feels_like']}）\n"
                    f"湿度：{weather_info['humidity']}\n"
                    f"风速：{weather_info['wind']}\n"
                    f"请结合以上天气信息，合理调整行程安排，推荐适合当前天气的景点、活动和穿搭。"
                )
                msg_content = user_input + weather_context
                if additional_req:
                    msg_content += f"\n\n额外要求：{additional_req}"
                messages.append({"role": "user", "content": msg_content})
            else:
                msg_content = user_input
                if additional_req:
                    msg_content += f"\n\n额外要求：{additional_req}"
                messages.append({"role": "user", "content": msg_content})

            response = client.chat.completions.create(
                model=MODEL,
                messages=messages,
                temperature=1,
                max_tokens=4000
            )
            result = response.choices[0].message.content

            st.success("✅ 行程规划完成！")
            st.markdown("---")

            # ── Beautiful Result Card ──
            st.markdown(f'<div class="result-container">{result}</div>', unsafe_allow_html=True)

            # ── Download ──
            filename = f"{destination or '旅行'}_行程规划.txt"
            st.download_button(
                label="📥 下载行程规划",
                data=result.encode("utf-8"),
                file_name=filename,
                mime="text/plain",
            )

            # ── Itinerary Overview Map ──
            if BAIDU_AK:
                dest_city = destination.strip() or "广州"
                dest_coords = baidu_geocode(dest_city)
                if dest_coords:
                    st.markdown("---")
                    st.markdown("""
                    <div style="text-align:center; margin-bottom:0.5rem;">
                        <span class="section-badge">📍 行程地图总览</span>
                    </div>
                    """, unsafe_allow_html=True)

                    # Collect POI markers
                    all_markers = [{
                        "lng": dest_coords["lng"], "lat": dest_coords["lat"],
                        "name": dest_city, "addr": "目的地", "color": "#ff6b8a"
                    }]
                    for cat in ["景点", "酒店", "美食"]:
                        pois = baidu_place_search(cat, dest_coords["lng"], dest_coords["lat"])
                        for p in pois[:4]:
                            if p.get("location"):
                                all_markers.append({
                                    "lng": p["location"]["lng"],
                                    "lat": p["location"]["lat"],
                                    "name": p.get("name", ""),
                                    "addr": p.get("address", "") or "",
                                    "color": "#7c3aed" if cat == "景点" else "#f59e0b" if cat == "酒店" else "#10b981"
                                })

                    overview_map = render_baidu_map(dest_coords["lng"], dest_coords["lat"], all_markers[:20], height=480)
                    st.markdown('<div class="map-wrapper">', unsafe_allow_html=True)
                    st.components.v1.html(overview_map, height=500, scrolling=False)
                    st.markdown('</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════
#  FOOTER
# ═══════════════════════════════════════
st.markdown("---")
st.markdown("""
<div class="footer">
    <p>Made with <span class="heart">❤️</span> by LovTrip · AI 智能旅游规划助手</p>
    <p style="font-size:0.8rem; opacity:0.7;">Powered by TokenHub LLM · 贴心专业 · 灵活全能</p>
</div>
""", unsafe_allow_html=True)
