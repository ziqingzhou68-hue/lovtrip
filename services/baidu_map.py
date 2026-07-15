"""百度地图 API 服务模块

提供地理编码和地点搜索功能。
"""

import requests
from config import BAIDU_AK


def baidu_geocode(city):
    """百度地图地理编码：城市名 → 经纬度

    Args:
        city: 城市名称

    Returns:
        {"lng": float, "lat": float} 或 None
    """
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


def baidu_place_search(query, lng, lat, radius=5000):
    """百度地图地点搜索

    Args:
        query: 搜索关键词（如"景点"、"酒店"、"美食"）
        lng: 中心经度
        lat: 中心纬度
        radius: 搜索半径（米）

    Returns:
        地点列表
    """
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
