# Contributing to Mach

Thanks for your interest in contributing! Here's how to get started.

## Setup

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
pip install ruff mypy
```

## Running locally

```bash
uvicorn bird_mach.webapp:app --reload
```

## Code style

- Format and lint with **ruff** (`ruff check . && ruff format .`).
- Type-check with **mypy** (`mypy bird_mach/`).
- Keep functions short and well-documented.

## Commit messages

Follow the conventional-commit format:

```
type(scope): short description

Longer body if needed.
```

Types: `feat`, `fix`, `refactor`, `docs`, `ci`, `build`, `chore`, `test`.

## Pull requests

1. Branch from `main`.
2. Keep PRs focused — one feature or fix per PR.
3. Ensure CI passes before requesting review.
