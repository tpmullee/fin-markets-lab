import os, httpx
class PolygonClient:
    def __init__(self): self.key=os.getenv("POLYGON_API_KEY")
    async def bars(self, symbol: str, start: str, end: str):
        url=f"https://api.polygon.io/v2/aggs/ticker/{symbol}/range/1/day/{start}/{end}"
        async with httpx.AsyncClient(timeout=30) as c:
            r=await c.get(url, params={"adjusted":"true","sort":"asc","limit":"50000","apiKey":self.key}); r.raise_for_status(); return r.json().get("results",[])
