all: setup-env-variables setup-git-hooks install check test build-watch

.PHONY: build-watch
build-watch:
	docker compose up --build --watch

check: check-format check-lint check-types

check-format:
	uv run ruff format . --diff
	terraform fmt -check -recursive

check-lint:
	uv run ruff check .

check-types:
	uv run mypy .

.PHONY: indexation
indexation:
	uv run indexation https://sightcall.com/sitemap_index.xml --database-url postgresql://postgres:password@localhost:5432/vectordb

install:
	uv lock --locked
	uv sync --locked --group dev --group lint --group test --group indexation

lint:
	uv run ruff format .
	uv run ruff check . --fix
	terraform fmt -recursive

semantic-release:
	uv run semantic-release version --no-changelog --no-push --no-vcs-release --skip-build --no-commit --no-tag
	uv lock
	git add pyproject.toml uv.lock
	git commit --allow-empty --amend --no-edit 

.PHONY: setup-env-variables
setup-env-variables:
	cp .env.example .env

setup-git-hooks:
	chmod +x hooks/pre-commit
	chmod +x hooks/pre-push
	chmod +x hooks/post-commit
	git config core.hooksPath hooks

test:
	uv run pytest -v --cov=sightcall_qa_api --cov-report=xml

upgrade-dependencies:
	uv lock --upgrade

.PHONY: watch
watch:
	docker compose up --watch

.PHONY: all check check-format check-lint check-types install lint semantic-release setup-git-hooks test upgrade-dependencies