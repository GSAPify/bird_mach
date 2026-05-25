# Bird Mach Memory Guide

## Overview
Bird Mach is a Python 3.11 enterprise audio intelligence platform. The repo
contains the `bird_mach` package, a broad `tests` suite, project docs under
`docs`, workflow docs under `workflows`, and packaging/tooling in
`pyproject.toml`.

## Architecture
- `bird_mach` contains runtime modules for audio analysis, realtime processing,
  caching, collaboration, observability, reporting, SDK helpers, webhooks, and
  enterprise-style API support.
- `tests` mirrors many runtime and enterprise feature areas.
- `docs` contains user guides, runbooks, enterprise feature docs, and ADRs.
- Tooling uses Ruff for linting and pytest for tests.

## User Defined Namespaces
- [Leave blank - user populates]

## Components
- `bird_mach/realtime`: realtime audio engine, buffering, meters, trackers, and
  websocket support.
- `bird_mach/plugin_system`: effect chains, registries, builtin effects, and
  sandbox-related plugin behavior.
- `bird_mach/reporting`: report generation and export formats.
- `bird_mach/webhooks`: webhook event types, dispatching, signing, and retry
  behavior.
- `docs`: architecture, API, runbook, enterprise feature, and ADR references.

## Patterns
- Prefer existing module and test naming conventions when adding code.
- Keep models at the top of files rather than defining models inside functions.
- Avoid emojis in code.
- For large commit batches, keep changes real and reviewable; documentation
  index updates are lower risk than runtime changes when the goal is history
  maintenance.
