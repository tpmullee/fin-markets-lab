from fastapi import APIRouter, Body, Query
from ..exchange.engine import OrderBook
from .dropcopy_router import publish_exec
import anyio
router = APIRouter()
_books = {}
def book(sym: str) -> OrderBook:
    if sym not in _books: _books[sym] = OrderBook(sym, on_trade=lambda tr: anyio.from_thread.run(publish_exec,tr))
    return _books[sym]
@router.post("/exch/engine/submit")
def submit_order(symbol: str = Query("ESZ5"), payload: dict = Body(...)):
    ob = book(symbol)
    res = ob.submit(side=payload.get("side","buy"), price=payload.get("price"), qty=int(payload.get("qty",1)),
                    tif=payload.get("tif","GTC"), typ=payload.get("type","limit"))
    return {"result": res, "trades": ob.trades[-5:]}
