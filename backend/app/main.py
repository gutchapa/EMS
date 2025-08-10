
from fastapi import FastAPI
from app.db import init_db
from app.auth import auth_router
from app.importer import router as import_router
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI(title="EMS Minimal")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup():
    init_db()

app.include_router(auth_router, prefix="/auth")
app.include_router(import_router, prefix="/import")

@app.get("/")
def root():
    return {"ok": True}
