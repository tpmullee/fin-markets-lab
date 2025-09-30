from fastapi import APIRouter, Query
from ..clients.sec_edgar_client import SecEdgarClient
from ..openai_utils import extract_risks_from_filing
router = APIRouter()
@router.get("/sec/10k/risks")
async def risks(cik: str = Query(...)):
    text = await SecEdgarClient().latest_10k_html(cik)
    if not text: return {"error":"No 10-K found"}
    return {"risks": extract_risks_from_filing(text[:200000])}
