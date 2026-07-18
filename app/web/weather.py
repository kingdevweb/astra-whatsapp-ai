"""Weather — Open-Meteo (free, no key)."""
import httpx
from app.utils.logger import logger

async def get_weather(city: str, units: str = "metric") -> dict:
    try:
        async with httpx.AsyncClient(timeout=15) as c:
            geo = (await c.get("https://geocoding-api.open-meteo.com/v1/search", params={"name":city,"count":1})).json()
            if not geo.get("results"): return {"error": f"City not found: {city}"}
            loc = geo["results"][0]; lat, lon = loc["latitude"], loc["longitude"]
            w = (await c.get("https://api.open-meteo.com/v1/forecast", params={"latitude":lat,"longitude":lon,"current_weather":"true","timezone":"auto"})).json()
            cur = w.get("current_weather",{})
            codes = {0:"Clear ☌️",1:"Mainly Clear 🌤",2:"Partly Cloudy ✅",3:"Overcast ☁️",45:"Foggy 🌱",51:"Drizzle 🌧",61:"Rain 🌧",71:"Snow ❄️",80:"Showers 🌦",95:"Thunderstorm ✈"}
            return {"city":loc.get("name",city),"country":loc.get("country",""),"temperature":cur.get("temperature"),"condition":codes.get(cur.get("weathercode",0),"Unknown"),"unit":"°C" if units=="metric" else.°F"}
    except Exception as e: return {"error": str(e)}
