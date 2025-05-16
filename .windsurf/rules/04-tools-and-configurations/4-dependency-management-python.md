---
trigger: model_decision
description: APPLY Python dependency management standards WHEN managing Python dependencies to ensure reproducible builds and efficient package management
globs: ["**/pyproject.toml", "**/uv.lock"]
---

Package Manager:
- Use uv as package manager for Python projects
- Never modify `uv.lock` manually; use uv commands instead

Dependencies:
- Define all dependencies in `pyproject.toml`
- Specify exact versions or version ranges for production dependencies
- Group development dependencies under appropriate optional groups (dev, test, lint)

Available Commands:
- Use `uv add <package>` to add a new package
- Use `uv lock --upgrade` to upgrade all dependencies
- Use `uv sync --locked` to install dependencies from lock file

Best Practices:
- Keep dependencies minimal and justified
- Regularly review and update dependencies for security patches
- Document any specific version requirements or constraints