.PHONY: help run dev install test validate

# Port for the local dev server. Override with: make run PORT=9000
PORT ?= 8000

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-10s\033[0m %s\n", $$1, $$2}'

run: ## Run the dev server with autoreload (http://localhost:$(PORT))
	uv run granian kjvstudy_org.server:api \
		--interface asgi --host 127.0.0.1 --port $(PORT) --reload \
		--static-path-route /static --static-path-mount kjvstudy_org/static

dev: run ## Alias for `run`

install: ## Sync dependencies with uv
	uv sync

test: ## Run the test suite
	uv run pytest tests/ -v

validate: ## Validate JSON data files against their Pydantic models
	uv run python scripts/validate_data.py
