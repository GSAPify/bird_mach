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

### Frontend

- Build new surfaces on the existing **glass tokens** declared at the top of
  `bird_mach/web/static/css/theme.css` (`--glass-bg`, `--glass-blur`,
  `--glass-border`, `--glass-highlight`, `--glass-shadow`, `--glass-tint-*`).
  Avoid introducing new ad-hoc backgrounds — extend the token set instead.
- Pair every backdrop-filter rule with the `-webkit-` prefix and respect the
  `prefers-reduced-transparency` and `prefers-reduced-motion` fallbacks
  already defined in the stylesheet.
- Use the `--radius-pill` token for capsule-shaped controls (pills, status
  chips, level meter, audio player) so the curve scale stays consistent.

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
