import streamlit as st
import re
from openai import OpenAI

# ── LovTrip 模块导入 ──
from config import API_KEY, BASE_URL, MODEL, BAIDU_AK, PEXELS_KEY, SYSTEM_PROMPT
from components.styles import get_custom_css
from components.map import render_map, build_map_markers
from components.poi import render_poi_grid
from services.weather import get_weather
from services.baidu_map import baidu_geocode, baidu_place_search

# ── Page Config ──
st.set_page_config(
    page_title="LovTrip — 智能旅游规划助手",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS Injection ──
st.markdown(get_custom_css(), unsafe_allow_html=True)

# ── API Key 验证 ──
if not API_KEY:
    st.error("⚠️ 未找到 API Key！请在 .streamlit/secrets.toml 或环境变量中配置 OPENAI_API_KEY。")
    st.info("💡 复制 .env.example 为 .env 并填入你的 API Key，或参考 README 配置。")
    st.stop()

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

    dest_val = st.session_state.get('dest', '') or '广州'
    dur_val = st.session_state.get('dur', '') or '3天2晚'
    budget_val = st.session_state.get('budget', '') or '适中'
    default_prompt = (
        f"请为我规划{dest_val}的旅行方案，出行时长{dur_val}，"
        f"出行模式为{travel_style}，出行人群为{traveler_type}，预算等级为{budget_val}。"
    )

    last_dest = st.session_state.get('_last_dest', None)
    if last_dest != dest_val:
        st.session_state.user_text = default_prompt
        st.session_state._last_dest = dest_val

    user_input = st.text_area(
        "旅行需求描述",
        height=130,
        placeholder="例如：我想去北京玩3天，带父母一起，预算适中…",
        key="user_text",
        on_change=sync_dest_from_text,
    )
    generate_clicked = st.button("🚀 开始生成行程", type="primary", use_container_width=True)

    # ── Travel Tips (fill right column) ──
    st.markdown("---")
    st.markdown("#### 💡 旅行贴士")
    tips = [
        ("📅", "最佳季节", "春秋两季气候宜人，避开节假日高峰"),
        ("🎒", "行前准备", "提前预订机票酒店，下载离线地图"),
        ("📸", "打卡攻略", "早出晚归避开人流，黄金时段拍照"),
        ("🍜", "美食秘诀", "远离景区餐厅，钻进小巷寻地道味"),
    ]
    for emoji, title, desc in tips:
        st.markdown(f"""
        <div style="background:rgba(255,255,255,0.5); border-radius:14px; padding:0.6rem 0.8rem; margin:0.3rem 0;
            border:1px solid rgba(124,58,237,0.08); display:flex; align-items:center; gap:0.6rem;">
            <span style="font-size:1.4rem;">{emoji}</span>
            <div><strong style="color:#1e1b4b; font-size:0.85rem;">{title}</strong>
            <p style="margin:0; font-size:0.72rem; color:#8b889e;">{desc}</p></div>
        </div>
        """, unsafe_allow_html=True)

with map_col:
    # Map loading placeholder (used during AI generation)
    map_placeholder = st.empty()

    # ── THE MAP ──
    if destination.strip():
        coords = baidu_geocode(destination.strip())
        if coords:
            with map_placeholder.container():
                st.markdown("""
                <div style="text-align:center; margin-bottom:0.25rem;">
                    <span class="section-badge">🗺️ 目的地地图</span>
                </div>
                """, unsafe_allow_html=True)

                poi_cats = {}
                for cat in ["景点", "酒店", "美食"]:
                    pois = baidu_place_search(cat, coords["lng"], coords["lat"])
                    if cat == "景点" and not pois:
                        pois = baidu_place_search("景区", coords["lng"], coords["lat"])
                    if cat == "景点" and not pois:
                        pois = baidu_place_search("旅游", coords["lng"], coords["lat"])
                    if cat == "酒店" and not pois:
                        pois = baidu_place_search("宾馆", coords["lng"], coords["lat"])
                    poi_cats[cat] = pois

                map_markers = build_map_markers(coords, destination.strip(), poi_cats)
                map_html = render_map(coords["lng"], coords["lat"], map_markers, height=520)
                st.markdown('<div class="map-wrapper">', unsafe_allow_html=True)
                st.components.v1.html(map_html, height=540, scrolling=False)
                st.markdown('</div>', unsafe_allow_html=True)
        else:
            with map_placeholder.container():
                st.info("🌍 正在查找目的地坐标…（如无结果请尝试更具体的地名）")
    else:
        with map_placeholder.container():
            st.markdown("""
            <div style="
                background: rgba(255,255,255,0.35); backdrop-filter: blur(20px);
                border: 2px dashed rgba(124,58,237,0.2); border-radius: 24px;
                padding: 4rem 2rem; text-align: center; min-height: 440px;
                display: flex; flex-direction: column; align-items: center; justify-content: center;
            ">
                <span style="font-size:4rem; display:block; margin-bottom:1rem;">🗺️</span>
                <h3 style="color:#4a4567; margin:0 0 0.5rem;">输入目的地，探索你的专属地图</h3>
                <p style="color:#9b97b8; margin:0;">在左侧边栏输入目的地 → 地图将自动加载</p>
                <p style="color:#9b97b8; margin:0.25rem 0 0;">可拖拽缩放 · 点击标记查看详情 · 多维度探索</p>
            </div>
            """, unsafe_allow_html=True)

# ═══════════════════════════════════════
#  AI GENERATION (runs before POI)
# ═══════════════════════════════════════
gen_result = None
if generate_clicked:
    if not user_input.strip():
        st.warning("⚠️ 请输入您的旅行需求")
    else:
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

        map_placeholder.empty()
        map_placeholder.markdown("""
        <div style="
            background: rgba(255,255,255,0.5); backdrop-filter: blur(20px);
            border-radius: 24px; padding: 6rem 2rem; text-align: center;
            border: 1px solid rgba(124,58,237,0.12);
            display: flex; flex-direction: column; align-items: center; justify-content: center;
        ">
            <span style="font-size:3.5rem; display:block; margin-bottom:1rem; animation: floatSlow 2s ease-in-out infinite;">✨</span>
            <h3 style="color:#7c3aed !important; margin:0 0 0.5rem;">AI 正在为您量身定制行程…</h3>
            <p style="color:#8b889e; margin:0;">正在分析目的地 · 筛选景点 · 规划最优路线</p>
            <div style="margin-top:1.5rem; display:flex; gap:0.5rem; justify-content:center;">
                <span style="width:8px;height:8px;border-radius:50%;background:#7c3aed;animation:pulse 1.4s ease-in-out infinite;"></span>
                <span style="width:8px;height:8px;border-radius:50%;background:#e85d9e;animation:pulse 1.4s ease-in-out 0.2s infinite;"></span>
                <span style="width:8px;height:8px;border-radius:50%;background:#ff6b8a;animation:pulse 1.4s ease-in-out 0.4s infinite;"></span>
            </div>
        </div>
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
        gen_result = response.choices[0].message.content

        map_placeholder.empty()
        if destination.strip():
            coords = baidu_geocode(destination.strip())
            if coords:
                with map_placeholder.container():
                    poi_cats2 = {}
                    for cat in ["景点", "酒店", "美食"]:
                        pois2 = baidu_place_search(cat, coords["lng"], coords["lat"])
                        if cat == "景点" and not pois2:
                            pois2 = baidu_place_search("旅游", coords["lng"], coords["lat"])
                        if cat == "酒店" and not pois2:
                            pois2 = baidu_place_search("宾馆", coords["lng"], coords["lat"])
                        poi_cats2[cat] = pois2
                    map_markers2 = build_map_markers(coords, destination.strip(), poi_cats2)
                    map_html2 = render_map(coords["lng"], coords["lat"], map_markers2, height=520)
                    st.markdown('<div class="map-wrapper">', unsafe_allow_html=True)
                    st.components.v1.html(map_html2, height=540, scrolling=False)
                    st.markdown('</div>', unsafe_allow_html=True)

        # 🎉 Celebration + Completion banner (between map and POI)
        st.balloons()
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, rgba(124,58,237,0.08), rgba(232,93,158,0.08));
            border: 2px solid rgba(124,58,237,0.2); border-radius: 20px;
            padding: 1.2rem 1.5rem; margin: 0.5rem 0 0;
            display: flex; align-items: center; gap: 1rem; animation: fadeInUp 0.5s ease-out;
        ">
            <span style="font-size:2.5rem;">🎉</span>
            <div style="flex:1;">
                <h4 style="color:#7c3aed; margin:0 0 0.2rem; font-size:1.15rem;">行程规划完成！向下滑动查看完整行程 👇</h4>
                <p style="color:#8b889e; margin:0; font-size:0.85rem;">AI 已为您量身定制专属旅行方案</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ── POI Explorer (between completion banner and result) ──
if destination.strip() and BAIDU_AK:
    coords_q = baidu_geocode(destination.strip())
    if coords_q:
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown("""
        <div style="text-align:center; margin-bottom:0.25rem;">
            <span class="section-badge">🔍 周边热门探索</span>
        </div>
        """, unsafe_allow_html=True)
        qtab1, qtab2, qtab3 = st.tabs(["🎯 热门景点", "🏨 住宿推荐", "🍜 美食餐饮"])
        with qtab1:
            spots = baidu_place_search("景点", coords_q["lng"], coords_q["lat"])
            if not spots:
                spots = baidu_place_search("景区", coords_q["lng"], coords_q["lat"])
            if not spots:
                spots = baidu_place_search("旅游", coords_q["lng"], coords_q["lat"])
            if not spots:
                spots = baidu_place_search("公园", coords_q["lng"], coords_q["lat"])
            if not spots:
                spots = baidu_place_search("广场", coords_q["lng"], coords_q["lat"])
            st.markdown(f'<div class="poi-grid">{render_poi_grid(spots, coords_q["lng"], coords_q["lat"], "🎯")}</div>', unsafe_allow_html=True)
        with qtab2:
            hotels = baidu_place_search("酒店", coords_q["lng"], coords_q["lat"])
            if not hotels:
                hotels = baidu_place_search("宾馆", coords_q["lng"], coords_q["lat"])
            if not hotels:
                hotels = baidu_place_search("住宿", coords_q["lng"], coords_q["lat"])
            st.markdown(f'<div class="poi-grid">{render_poi_grid(hotels, coords_q["lng"], coords_q["lat"], "🏨")}</div>', unsafe_allow_html=True)
        with qtab3:
            foods = baidu_place_search("美食", coords_q["lng"], coords_q["lat"])
            if not foods:
                foods = baidu_place_search("餐厅", coords_q["lng"], coords_q["lat"])
            if not foods:
                foods = baidu_place_search("小吃", coords_q["lng"], coords_q["lat"])
            if not foods:
                foods = baidu_place_search("火锅", coords_q["lng"], coords_q["lat"])
            if not foods:
                foods = baidu_place_search("面馆", coords_q["lng"], coords_q["lat"])
            st.markdown(f'<div class="poi-grid">{render_poi_grid(foods, coords_q["lng"], coords_q["lat"], "🍜")}</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════
#  RESULT CARD (after POI)
# ═══════════════════════════════════════
if gen_result:
    st.markdown(f'<div class="result-container">{gen_result}</div>', unsafe_allow_html=True)

    filename = f"{destination or '旅行'}_行程规划.txt"
    st.download_button(
        label="📥 下载行程规划",
        data=gen_result.encode("utf-8"),
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
