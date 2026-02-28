.PHONY: dev lint format typecheck clean help

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'

dev: ## Start the dev server with hot reload
	uvicorn bird_mach.webapp:app --reload --host 0.0.0.0 --port 8000

lint: ## Run ruff linter
	ruff check bird_mach/ scripts/

format: ## Auto-format code with ruff
	ruff format bird_mach/ scripts/

typecheck: ## Run mypy type checker
	mypy bird_mach/

clean: ## Remove caches and build artifacts
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .mypy_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .ruff_cache -exec rm -rf {} + 2>/dev/null || true
	rm -rf dist/ build/ *.egg-info
