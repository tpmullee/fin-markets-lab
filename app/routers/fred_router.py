from fastapi import APIRouter, Query
from ..clients.fred_client import FREDClient
from ..openai_utils import client
router = APIRouter()
@router.get("/fred/series/brief")
async def series_brief(series_id: str = Query("CPIAUCSL")):
    obs = await FREDClient().series(series_id)
    latest = obs[:6]
    prompt = f"Provide a plain-English macro brief for {series_id} with investor implications, 4 bullets:\\n{latest}"
    brief = client().chat.completions.create(model="gpt-4o-mini", messages=[{"role":"user","content":prompt}], temperature=0.1).choices[0].message.content
    return {"latest": latest, "brief": brief}
