import os
from typing import Any, Dict, List
from openai import OpenAI
_client = None
def client() -> OpenAI:
    global _client
    if _client is None:
        _client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    return _client

def summarize_transactions(txns: List[Dict[str, Any]]) -> str:
    text = "\n".join([f"- {t['date']} {t['merchant']}: ${t['amount']} [{t.get('category','?')}]" for t in txns[:100]])
    prompt = ("You are a finance analyst. Given recent transactions, produce: "
              "1) 3-sentence spend summary 2) 3 anomalies 3) category totals + 2 savings ideas.\n"+text)
    rsp = client().chat.completions.create(model="gpt-4o-mini", messages=[{"role":"user","content":prompt}], temperature=0.2)
    return rsp.choices[0].message.content

def extract_risks_from_filing(text: str) -> str:
    rsp = client().chat.completions.create(model="gpt-4o-mini",
        messages=[{"role":"system","content":"Extract material risks from SEC filings with terse bullets."},
                  {"role":"user","content":text[:12000]}], temperature=0.1)
    return rsp.choices[0].message.content

def nlq_timeseries_to_query(user_q: str) -> Dict[str, Any]:
    rsp = client().chat.completions.create(model="gpt-4o-mini",
        messages=[{"role":"system","content":"Return JSON with provider, symbol, timeframe, frequency."},
                  {"role":"user","content":user_q}], temperature=0.0)
    return {"provider":"polygon","symbol":"AAPL","timeframe":"2024-01-01:2024-12-31","frequency":"day","raw": rsp.choices[0].message.content}
