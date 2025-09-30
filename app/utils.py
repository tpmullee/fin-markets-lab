import httpx
from typing import Any, Dict, Optional

class ApiError(Exception):
    def __init__(self, status: int, detail: str):
        super().__init__(detail); self.status = status

async def get_json(url: str, headers: Optional[Dict[str,str]] = None, params: Optional[Dict[str,Any]] = None):
    async with httpx.AsyncClient(timeout=30.0) as c:
        r = await c.get(url, headers=headers, params=params)
        if r.status_code >= 400:
            raise ApiError(r.status_code, r.text)
        return r.json()
