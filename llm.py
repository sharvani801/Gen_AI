import requests


OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "qwen2.5:3b"


def explain_repository(repository_code, files):

    prompt = f"""
You are an expert software engineer explaining a GitHub repository
to a beginner.

Analyze the repository code below.

Give the answer in simple and clear language.

Include these sections:

1. Project Overview
2. Main Technologies
3. Main Features
4. Important Files
5. How the Project Works
6. Overall Architecture

Only describe functionality that can be supported by the provided
repository code. Do not invent features.

Important files:
{files}

Repository code:
{repository_code}
"""

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False
        },
        timeout=300
    )

    response.raise_for_status()

    return response.json()["response"]