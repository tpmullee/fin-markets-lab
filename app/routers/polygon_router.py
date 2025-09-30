from fastapi import APIRouter, Query
from ..openai_utils import nlq_timeseries_to_query
from ..clients.polygon_client import PolygonClient
router = APIRouter()
@router.get("/polygon/nlq")
async def nlq(query: str = Query(...)):
    parsed = nlq_timeseries_to_query(query)
    if parsed["provider"]!="polygon": return {"note":"demo mapped to polygon only", "parsed": parsed}
    start,end = parsed["timeframe"].split(":")
    bars = await PolygonClient().bars(parsed["symbol"], start, end)
    return {"parsed":parsed, "points":len(bars), "sample":bars[:3]}
