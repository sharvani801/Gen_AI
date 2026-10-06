import os
import tempfile
from git import Repo


ALLOWED_EXTENSIONS = {
    ".py", ".js", ".jsx", ".ts", ".tsx",
    ".java", ".c", ".cpp", ".html", ".css",
    ".sql", ".json", ".md"
}

IGNORED_DIRS = {
    ".git", "node_modules", "venv", ".venv",
    "__pycache__", "dist", "build"
}


def process_repository(github_url: str):
    if not github_url.startswith("https://github.com/"):
        raise ValueError("Please provide a valid GitHub repository URL.")

    temp_dir = tempfile.mkdtemp()

    Repo.clone_from(github_url, temp_dir, depth=1)

    files = []
    code_parts = []

    for root, dirs, filenames in os.walk(temp_dir):
        dirs[:] = [d for d in dirs if d not in IGNORED_DIRS]

        for filename in filenames:
            extension = os.path.splitext(filename)[1].lower()

            if extension in ALLOWED_EXTENSIONS:
                path = os.path.join(root, filename)

                try:
                    with open(path, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()

                    relative_path = os.path.relpath(path, temp_dir)

                    files.append(relative_path)

                    code_parts.append(
                        f"\n\n===== FILE: {relative_path} =====\n{content}"
                    )

                except Exception:
                    continue

    combined_code = "".join(code_parts)

    # Prevent sending extremely large repositories to the LLM
    combined_code = combined_code[:60000]

    return {
        "files": files,
        "code": combined_code
    }