from fastapi import FastAPI
from app.api import loader, report

app = FastAPI(title="Raw Data Ingestion API")

app.include_router(report.router, tags=["Shows latest report"])
app.include_router(loader.router, prefix="/load", tags=["Data Loading"])
