from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import asyncio, json
router = APIRouter()
_subs=set()
@router.websocket("/exch/ws/dropcopy")
async def dropcopy(ws: WebSocket):
    await ws.accept(); _subs.add(ws)
    try:
        while True: await asyncio.sleep(60)
    except WebSocketDisconnect:
        _subs.discard(ws)
async def publish_exec(exec_msg: dict):
    dead=[]
    for s in list(_subs):
        try: await s.send_text(json.dumps(exec_msg))
        except: dead.append(s)
    for d in dead: _subs.discard(d)
