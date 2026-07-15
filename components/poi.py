"""POI 卡片组件模块

景点/酒店/美食卡片网格渲染与 Pexels 图片获取。
"""

import urllib.parse
import requests
from config import BAIDU_AK, PEXELS_KEY


def get_pexels_photo(query):
    """从 Pexels API 获取真实旅行照片

    Args:
        query: 搜索关键词

    Returns:
        图片 URL 或 None
    """
    if not PEXELS_KEY:
        return None
    try:
        url = f"https://api.pexels.com/v1/search?query={query}&per_page=1&orientation=landscape&size=medium"
        headers = {"Authorization": PEXELS_KEY}
        resp = requests.get(url, headers=headers, timeout=8)
        data = resp.json()
        photos = data.get("photos", [])
        if photos:
            return photos[0]["src"]["medium"]
    except Exception:
        pass
    return None


def render_poi_grid(pois, center_lng, center_lat, emoji="📍"):
    """渲染 POI 卡片网格 HTML

    Args:
        pois: POI 列表
        center_lng: 中心经度（用于 fallback 图片）
        center_lat: 中心纬度（用于 fallback 图片）
        emoji: 默认 emoji（未使用，保留兼容）

    Returns:
        HTML 字符串
    """
    if not pois:
        return '<p style="text-align:center;color:#9b97b8;padding:1.5rem;">🔍 输入目的地后自动搜索周边热门地点</p>'

    gradients = [
        ("#ff6b8a,#e85d9e"), ("#7c3aed,#6366f1"), ("#f59e0b,#f97316"),
        ("#10b981,#34d399"), ("#ec4899,#f472b6"), ("#3b82f6,#06b6d4"),
        ("#8b5cf6,#a78bfa"), ("#ef4444,#f87171"), ("#14b8a6,#2dd4bf"),
    ]

    cards = ""
    for i, poi in enumerate(pois[:9]):
        name = poi.get("name", "未知")
        addr = poi.get("address", "") or ""
        score = poi.get("score", "") or ""
        price = poi.get("price", "") or ""
        delay = 0.06 * (i % 3)
        stars = "⭐" * min(5, max(1, int(float(score) // 20))) if score else ""
        grad = gradients[i % len(gradients)]

        # Real photo from Pexels API, fallback to Baidu static map
        photo_url = get_pexels_photo(urllib.parse.quote(f"{name} travel landmark"))
        loc = poi.get("location", {})
        plng = loc.get("lng", center_lng) if loc else center_lng
        plat = loc.get("lat", center_lat) if loc else center_lat
        fallback_img = f"https://api.map.baidu.com/staticimage/v2?ak={BAIDU_AK}&width=400&height=250&center={plng},{plat}&markers={plng},{plat}&markerStyles=l,{plng},{plat}&zoom=16"

        cards += f"""
        <div class="poi-card" style="animation-delay:{delay}s;">
            <div class="poi-img" style="position:relative;background:linear-gradient(135deg,{grad});overflow:hidden;">
                <img src="{photo_url or fallback_img}" alt="{name}" loading="lazy"
                    style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;"
                    onerror="this.onerror=null;this.src='{fallback_img}';"/>
            </div>
            <div class="poi-body">
                <h4 title="{name}">{name[:18]}{'…' if len(name) > 18 else ''}</h4>
                <p class="poi-score">{stars} {score or ''}</p>
                <p class="poi-addr">📍 {addr[:40]}{'…' if len(addr) > 40 else ''}</p>
                <p class="poi-extra">{'💰 ' + price if price else ''}</p>
            </div>
        </div>"""
    return cards
