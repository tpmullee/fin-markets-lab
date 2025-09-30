import importlib, pkgutil, os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Fin Markets Lab", version="0.1.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True,
                   allow_methods=["*"], allow_headers=["*"])

_loaded = []
def _autoload_routers():
    pkg = "app.routers"
    package = importlib.import_module(pkg)
    for _, modname, ispkg in pkgutil.iter_modules(package.__path__):
        if ispkg or not modname.endswith("_router"): continue
        module = importlib.import_module(f"{pkg}.{modname}")
        if hasattr(module, "router"):
            prefix = ""  # each router defines its own path segment(s)
            app.include_router(module.router)
            _loaded.append(modname)

_autoload_routers()

@app.get("/health")
def health():
    return {"status":"ok","routers": sorted(_loaded)}
