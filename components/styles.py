"""LovTrip 自定义 CSS 样式模块"""


def get_custom_css():
    """返回 LovTrip Premium 主题的完整 CSS 样式

    Returns:
        CSS 字符串
    """
    return """
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
@keyframes pulse { 0%,100%{opacity:1;transform:scale(1)} 50%{opacity:0.3;transform:scale(0.7)} }
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
"""
