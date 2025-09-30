from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query
import asyncio, json, time
router = APIRouter()
_clients=set()
@router.websocket("/demo/ws/market")
async def ws_market(ws: WebSocket, symbol: str = Query("ESZ5")):
    await ws.accept(); _clients.add(ws)
    try:
        await ws.send_json({"type":"hello","symbol":symbol})
        while True: await asyncio.sleep(60)
    except WebSocketDisconnect:
        _clients.discard(ws)
@router.post("/demo/tick")
async def tick(price: float, size: int=1):
    dead=[]
    for c in list(_clients):
        try: await c.send_text(json.dumps({"type":"md","row":{"ts":time.time(),"last":price,"last_size":size}}))
        except: dead.append(c)
    for d in dead: _clients.discard(d)
    return {"sent": len(_clients)}
