from pathlib import Path
from fastapi.staticfiles import StaticFiles


from fastapi import FastAPI
from pydantic import BaseModel

from circuitmind.fix import fix_project


app = FastAPI(title="CircuitMind AI")
app.mount("/static", StaticFiles(directory="src/circuitmind/web/static"), name="static")


class FixRequest(BaseModel):
    project_path: str
    max_iterations: int = 3


@app.get("/")
def root():
    return {"message": "CircuitMind AI is running"}


@app.post("/fix")
def fix_project_endpoint(request: FixRequest):
    result = fix_project(
        Path(request.project_path),
        max_iterations=request.max_iterations,
    )

    iterations = []

    for iteration in result.iterations:
        iterations.append(
            {
                "iteration": iteration.iteration,
                "diagnosis": iteration.diagnosis.diagnosis,
                "root_cause": iteration.diagnosis.root_cause,
                "confidence": iteration.diagnosis.confidence,
                "message": iteration.message,
                "workspace_dir": str(iteration.workspace_dir)
                if iteration.workspace_dir
                else None,
                "build_exit_code": iteration.build_exit_code,
                "success": iteration.success,
            }
        )

    return {
        "project_path": request.project_path,
        "max_iterations": request.max_iterations,
        "success": result.success,
        "final_workspace": str(result.final_workspace)
        if result.final_workspace
        else None,
        "iterations": iterations,
    }