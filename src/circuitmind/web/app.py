from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="CircuitMind AI")


class FixRequest(BaseModel):
    project_path: str
    max_iterations: int = 3


@app.get("/")
def root():
    return {"message": "CircuitMind AI is running"}


@app.post("/fix")
def fix_project_endpoint(request: FixRequest):
    return {
        "project_path": request.project_path,
        "max_iterations": request.max_iterations,
        "status": "received",
    }