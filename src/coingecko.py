import aiohttp
from typing import Dict

class CoinGeckoClient:
    BASE = "https://api.coingecko.com/api/v3"

    def __init__(self, session: aiohttp.ClientSession, api_key: str | None = None):
        self.session = session
        self.api_key = api_key

    async def prices_usd(self, ids: list[str]) -> Dict[str, float]:
        params = {
            "ids": ",".join(ids),
            "vs_currencies": "usd",
            "precision": "full",
        }
        
        headers = {"accept": "application/json"}
        if self.api_key:
            headers["x-cg-demo-api-key"] = self.api_key
            
        async with self.session.get(f"{self.BASE}/simple/price", params=params, headers=headers, timeout=10) as r:
            r.raise_for_status()
            data = await r.json()
            return {k: float(v.get("usd")) for k, v in data.items() if v and v.get("usd") is not None}