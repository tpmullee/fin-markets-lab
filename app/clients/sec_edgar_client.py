import os, httpx, re
from bs4 import BeautifulSoup
class SecEdgarClient:
    def __init__(self): self.ua=os.getenv("SEC_USER_AGENT","email@domain.com")
    async def latest_10k_html(self, cik: str):
        idx=f"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={cik}&type=10-k&owner=exclude&count=1"
        async with httpx.AsyncClient(timeout=30, headers={"User-Agent": self.ua}) as c:
            r=await c.get(idx); r.raise_for_status()
            m=re.search(r'href="(/Archives/edgar/data/[^"]+\\.htm)"', r.text, re.I)
            if not m: return None
            url="https://www.sec.gov"+m.group(1)
            r2 = await c.get(url); r2.raise_for_status()
            soup=BeautifulSoup(r2.text,"lxml")
            return soup.get_text(separator="\\n")
