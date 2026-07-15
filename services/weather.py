"""天气服务模块

使用 Open-Meteo 免费 API（无需 Key）+ 百度地图地理编码。
"""

import requests
from services.baidu_map import baidu_geocode


def get_weather(city):
    """获取城市实时天气

    使用 Open-Meteo 免费 API，无需 API Key。
    先用百度地图进行地理编码获取坐标。

    Args:
        city: 城市名称

    Returns:
        {"weather": str, "temp": str, "feels_like": str, "humidity": str, "wind": str} 或 None
    """
    try:
        # 地理编码获取坐标
        coords = baidu_geocode(city)
        if not coords:
            return None
        # Open-Meteo API (免费，无需 Key)
        url = (
            f"https://api.open-meteo.com/v1/forecast?"
            f"latitude={coords['lat']}&longitude={coords['lng']}"
            f"&current_weather=true&timezone=auto"
        )
        resp = requests.get(url, timeout=10)
        if resp.status_code != 200:
            return None
        data = resp.json()
        cw = data.get("current_weather", {})
        if not cw:
            return None
        code = cw.get("weathercode", 0)
        weather_map = {
            0: "☀️ 晴朗", 1: "🌤️ 大部晴", 2: "⛅ 多云", 3: "☁️ 阴天",
            45: "🌫️ 雾", 51: "🌦️ 小雨", 61: "🌧️ 中雨", 71: "🌨️ 小雪",
            80: "🌦️ 阵雨", 95: "⛈️ 雷雨",
        }
        return {
            "weather": weather_map.get(code, f"代码{code}"),
            "temp": f"{cw.get('temperature', '?')}°C",
            "feels_like": f"{cw.get('temperature', '?')}°C",
            "humidity": "—",
            "wind": f"{cw.get('windspeed', '?')} km/h",
        }
    except Exception:
        return None
