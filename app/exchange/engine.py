from dataclasses import dataclass, field
from typing import Dict, List, Optional, Callable, Tuple
import heapq, time, itertools

OnTrade = Callable[[Dict], None]

@dataclass(order=True)
class Order:
    ts: float = field(default_factory=time.time, compare=True)
    price: float = field(compare=False, default=0.0)
    qty: int = field(compare=False, default=0)
    side: str = field(compare=False, default="buy")  # buy/sell
    tif: str = field(compare=False, default="GTC")
    id: str = field(compare=False, default="")

class OrderBook:
    def __init__(self, symbol: str, on_trade: Optional[OnTrade]=None):
        self.symbol = symbol
        self.bid_heap: List[Tuple] = []  # (-price, ts, id, Order)
        self.ask_heap: List[Tuple] = []  # ( price, ts, id, Order)
        self.trades: List[Dict] = []
        self.seq = itertools.count(1)
        self.idmap: Dict[str, Tuple[str, Tuple]] = {}  # id -> ("bid"|"ask", heap_entry)
        self.on_trade = on_trade

    def _push(self, o: Order):
        key = (-o.price if o.side=="buy" else o.price, o.ts, o.id, o)
        if o.side=="buy": self.bid_heap.append(key); self.idmap[o.id]=("bid", key)
        else: self.ask_heap.append(key); self.idmap[o.id]=("ask", key)

    def _heapify(self): heapq.heapify(self.bid_heap); heapq.heapify(self.ask_heap)
    def add_limit(self, side: str, price: float, qty: int, tif="GTC", oid: Optional[str]=None):
        oid = oid or f"{self.symbol}:{next(self.seq)}"
        o = Order(side=side, price=price, qty=qty, tif=tif, id=oid); self._push(o); return oid

    def cancel(self, oid: str) -> bool:
        if oid not in self.idmap: return False
        side, entry = self.idmap.pop(oid)
        # lazy cancel: mark qty=0, let _cross() pop it when encountered
        entry[3].qty = 0
        return True

    def _emit_trade(self, tr: Dict):
        self.trades.append(tr)
        if self.on_trade: 
            try: self.on_trade(tr)
            except Exception: pass

    def _best_cross(self) -> bool:
        if not self.bid_heap or not self.ask_heap: return False
        bid_px, bts, bid_id, bid = self.bid_heap[0]
        ask_px, ats, ask_id, ask = self.ask_heap[0]
        if (-bid_px) < ask_px: return False
        fill = min(bid.qty, ask.qty)
        px = ask.price
        self._emit_trade({"symbol": self.symbol, "qty": fill, "price": px, "ts": time.time()})
        bid.qty -= fill; ask.qty -= fill
        if bid.qty==0: heapq.heappop(self.bid_heap)
        if ask.qty==0: heapq.heappop(self.ask_heap)
        return True

    def submit(self, side: str, price: float|None, qty: int, tif="GTC", typ="limit"):
        self._heapify()
        if typ=="market":
            # market cross against opposite heap
            target = self.ask_heap if side=="buy" else self.bid_heap
            remaining = qty
            while target and remaining>0:
                px, ts, oid, o = heapq.heappop(target)
                fill = min(remaining, o.qty)
                self._emit_trade({"symbol": self.symbol, "qty": fill, "price": o.price, "ts": time.time()})
                o.qty -= fill; remaining -= fill
                if o.qty>0: heapq.heappush(target, (px, ts, oid, o))
            if tif=="FOK" and remaining>0: return {"status":"rejected","reason":"FOK_not_filled"}
            if tif=="IOC" and remaining>0: return {"status":"partial","filled":qty-remaining}
            return {"status":"filled","filled":qty}
        # limit
        oid = self.add_limit(side, price or 0.0, qty, tif=tif)
        while self._best_cross(): pass
        return {"status":"accepted","id":oid}
