# Fin Markets Lab
A unified FastAPI app that demos:
- Finance/banking/crypto/trading APIs (with LLM overlays),
- Futures/options exchange core (engine, risk, clearing),
- Kalshi-style event markets,
- Live demos via WebSockets.

### Run
python -m pip install -U pip
pip install -e .
uvicorn app.main:app --reload

Open http://127.0.0.1:8000/docs

> Branding and deployment align with patmullee.com (S3/CloudFront + GitHub Actions). Not financial advice.
