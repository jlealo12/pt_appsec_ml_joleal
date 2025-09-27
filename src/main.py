"""Base API for the AntMan service
Ref: https://auth0.com/blog/build-and-secure-fastapi-server-with-auth0/"""

from fastapi import FastAPI

app = FastAPI(title="AntMan API", version="0.1.0")


@app.get("/")
async def root():
    return {"message": "Welcome to the AntMan API"}


@app.get("/health")
async def health_check():
    return {"status": "ok"}
