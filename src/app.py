"""Base API for the AntMan service
Ref: https://auth0.com/blog/build-and-secure-fastapi-server-with-auth0/"""

import asyncio
import os

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from .utils import get_env_variable
from .workflow import OwaspWorkflow

# Load environment variables
load_dotenv()

app = FastAPI(title="AntMan API", version="0.1.0")

# Initialize the workflow
try:
    CONFIG_PATH = os.path.join(
        os.path.dirname(__file__),
        get_env_variable("CONFIG_PATH"),
    )
    workflow = OwaspWorkflow(CONFIG_PATH)
except Exception as e:
    print(f"Warning: Could not initialize OwaspWorkflow: {e}")
    workflow = None


class CodeEvaluationRequest(BaseModel):
    code: str


class CodeEvaluationResponse(BaseModel):
    result: list
    status: str = "success"


class CommitValidationRequest(BaseModel):
    hash: str


class CommitValidationResponse(BaseModel):
    result: list
    status: str = "success"


@app.get("/")
async def root():
    return {"message": "Welcome to the AntMan API"}


@app.get("/health")
async def health_check():
    return {"status": "ok"}


@app.post("/evaluate", response_model=CodeEvaluationResponse)
async def evaluate_code(request: CodeEvaluationRequest):
    """
    Evaluate code snippet using the OWASP workflow
    """
    if workflow is None:
        raise HTTPException(
            status_code=503,
            detail="Service unavailable: OWASP workflow not initialized",
        )

    try:
        # Run the async inference with the provided code
        result = await workflow.run_async_inference(request.code)

        return CodeEvaluationResponse(result=result, status="success")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error evaluating code: {str(e)}")


@app.post("/validate", response_model=CommitValidationResponse)
async def validate_commit(request: CommitValidationRequest):
    """Validates a commit to check the evaluation results"""
    try:
        print(f"Validating commit: {request.hash}")
        return CommitValidationResponse(result=["TODO: implementar"], status="success")
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error validating commit: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8080)
