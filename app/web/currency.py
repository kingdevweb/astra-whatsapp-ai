"""Currency conversion."""
import httpx
from app.utils.logger import logger

async def convert(amount: float, from_c: str, to_c: str) -> dict:
    try:
        async with httpx.AsyncClient(timeout=15) as c:
            r = (await c.get(f"https://open.er-api.com/v6/latest/{from_c.upper()}")).json()
            if r.get("result") != "success": return {"error": f"Invalid: {from_c}"}
            rate = r["rates"].get(to_c.upper())
            if not rate: return {"error": f"Not supported: {to_c}"}
            return {"from": f"{amount} {from_c.upper()}", "to": f"{round(amount*rate, 2)} {to_c.upper()}", "rate": rate}
    except Exception as e: return {"error": str(e)}
