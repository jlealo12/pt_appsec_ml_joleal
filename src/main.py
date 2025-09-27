"""Base API for the AntMan service"""

from fastapi import FastAPI

app = FastAPI(title="AntMan API", version="0.1.0")


@app.get("/")
async def root():
    return {"message": "Welcome to the AntMan API"}


@app.get("/health")
async def health_check():
    return {"status": "ok"}
