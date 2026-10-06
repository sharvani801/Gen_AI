from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from github_processor import process_repository
from llm import explain_repository


app = FastAPI(
    title="GitHub Code Explainer",
    description="Local GenAI application for explaining GitHub repositories"
)


class RepositoryRequest(BaseModel):
    github_url: str


@app.get("/")
def home():
    return {
        "message": "GitHub Code Explainer API is running"
    }


@app.post("/explain")
def explain(request: RepositoryRequest):

    try:
        repository = process_repository(request.github_url)

        explanation = explain_repository(
            repository["code"],
            repository["files"]
        )

        return {
            "success": True,
            "files_analyzed": repository["files"],
            "explanation": explanation
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )