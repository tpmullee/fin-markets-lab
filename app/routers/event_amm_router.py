from fastapi import APIRouter, Body
import math
router = APIRouter()
def lmsr_cost(q_yes: float, q_no: float, b: float=10.0) -> float:
    return b * math.log(math.exp(q_yes/b) + math.exp(q_no/b))
def lmsr_price_yes(q_yes: float, q_no: float, b: float=10.0) -> float:
    num = math.exp(q_yes/b); den = num + math.exp(q_no/b); return num/den
@router.post("/evt/amm/quote")
def quote(payload: dict = Body(...)):
    qy, qn, dy, b = payload["q_yes"], payload["q_no"], payload.get("delta_yes",0.0), payload.get("b",10.0)
    p_now = lmsr_price_yes(qy, qn, b)
    c0 = lmsr_cost(qy, qn, b); c1 = lmsr_cost(qy+dy, qn, b)
    return {"price_yes": p_now, "buy_cost_yes_delta": c1-c0}
