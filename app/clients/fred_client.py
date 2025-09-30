import os, httpx
class FREDClient:
    def __init__(self): self.key=os.getenv("FRED_API_KEY")
    async def series(self, series_id: str, limit=12):
        async with httpx.AsyncClient(timeout=20) as c:
            r=await c.get("https://api.stlouisfed.org/fred/series/observations",
                          params={"series_id":series_id,"api_key":self.key,"file_type":"json","sort_order":"desc","limit":limit})
            r.raise_for_status(); return r.json()["observations"]
