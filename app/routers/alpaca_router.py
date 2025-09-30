from fastapi import APIRouter
import os, httpx
router = APIRouter()
@router.get("/alpaca/account")
async def acct():
    base="https://paper-api.alpaca.markets"; h={"APCA-API-KEY-ID": os.getenv("ALPACA_KEY_ID",""), "APCA-API-SECRET-KEY": os.getenv("ALPACA_SECRET_KEY","")}
    async with httpx.AsyncClient(timeout=20) as c:
        r=await c.get(f"{base}/v2/account", headers=h); r.raise_for_status(); return r.json()
