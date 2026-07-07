"""
main.py – FastAPI application entry point
"""
from __future__ import annotations
import os
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from config import get_settings
from api.hla import router as hla_router
from api.sdd import router as sdd_router
from api.cwb import router as cwb_router

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Ensure output / temp directories exist on startup
    Path(settings.temp_dir).mkdir(exist_ok=True)
    Path(settings.output_dir).mkdir(exist_ok=True)
    yield


app = FastAPI(
    title=settings.app_name,
    version=settings.api_version,
    description="AI-powered Oracle Fusion HCM solution design: questionnaire generation, analysis, SDD and CWB creation.",
    lifespan=lifespan,
)

# ── CORS ──────────────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routers ───────────────────────────────────────────────────────────────────
API_PREFIX = f"/api/{settings.api_version}"

app.include_router(hla_router, prefix=f"{API_PREFIX}/hla", tags=["HLA – High Level Assessment"])
app.include_router(sdd_router, prefix=f"{API_PREFIX}/sdd", tags=["SDD – Solution Design Document"])
app.include_router(cwb_router, prefix=f"{API_PREFIX}/cwb", tags=["CWB – Configuration Workbooks"])


# ── Health check ──────────────────────────────────────────────────────────────
@app.get("/health", tags=["Health"])
async def health():
    return {"status": "ok", "service": settings.app_name, "version": settings.api_version}


# ── Dev runner ────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=5000,
        reload=settings.debug,
        log_level="debug" if settings.debug else "info",
    )
