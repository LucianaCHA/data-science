# app/main.py
from fastapi import FastAPI
from app.api import loader

app = FastAPI(title="Raw Data Ingestion API")

app.include_router(loader.router, prefix="/load", tags=["Data Loading"])
