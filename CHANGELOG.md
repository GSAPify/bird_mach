# Changelog

## Unreleased

### Added
- **User management** (`bird_mach.auth`): registration, login, JWT
  access/refresh tokens (PyJWT), PBKDF2 password hashing, roles, password
  change, and account deletion, exposed under `/auth`. Durable SQLite-backed
  storage with an in-memory test backend.
- **Payments** (`bird_mach.billing`): Stripe-backed subscriptions with a plan
  catalog, hosted checkout, billing portal, and signature-verified webhooks
  under `/billing`. `require_subscription` gates premium features (402). State
  is persisted in SQLite and stays idempotent against replayed webhooks.
  Note: the live Stripe path is **not** exercised by the test suite — it needs
  real test-mode keys and webhook replay (see `docs/billing.md`).
- SQLite persistence helper (`bird_mach.db`) with WAL mode for the durable
  user/subscription stores.

### Fixed
- Repaired the test suite: a syntax error in `api/v2/versioning.py`, a missing
  `DEFAULT_DARK_BG` constant, ~198 over-indented enterprise test files, and 14
  pre-existing core test failures. The full suite (1467 tests) now passes.

### Changed
- Web UI overhauled into a near-black instrument-panel theme.
  Palette swung from green/yellow glass to amber primary
  (`#ffb454`) with cyan secondary (`#5fb6ff`) on a `#05070b`
  backdrop, with a faint grid + scanline texture and a single
  warm corner wash replacing the animated ambient orbs.
- Typography moved to JetBrains Mono throughout, with Space
  Grotesk reserved for the hero heading and brand mark. Labels,
  buttons, kickers, and metric values are now uppercase mono
  with letter-spacing for that telemetry-readout feel.
- Surfaces and controls were squared up: `--radius` dropped from
  8px to 4px, `--radius-pill` collapsed to 2px, glass blur
  halved, drop shadows removed, and the gradient/sheen sweeps on
  buttons and nav pills were stripped.
- Buttons are now flat amber chips (primary), or outline chips
  (ghost / warm / danger) with hover fills instead of gradients.
- Audio preview block redesigned as a TLM "spectrum" panel with
  grid background, square spectrum bars, and pixel-style points.
- Metric tiles, status pills, and the level meter are flat with
  a left amber accent bar; the level meter itself is now a 6px
  hairline with a solid amber fill.

## v0.5.1 (2026-05-13)

### Added
- Skip-to-content link, named main and nav landmarks, and aria-labelled
  drop zones / status region for keyboard and screen-reader users.
- Open Graph + Twitter card meta tags, canonical link, mask-icon and
  apple-touch-icon hints, and per-scheme `theme-color` entries.
- Live page now persists motion model, color-by, loop speed, max
  trail points, and bin count in `localStorage`.
- Webkit / Firefox custom scrollbars styled to match the glass theme.
- New `--radius-lg` and `--radius-pill` design tokens; existing pills
  and capsules refactored onto `--radius-pill`.

### Changed
- Web UI redesigned around a glassmorphism system: frosted topbar,
  cards, dropzones, status pills, and metric tiles backed by a shared
  set of glass tokens (background, blur, border, shadow, tint).
- Ambient gradient orbs and a subtle film grain now sit behind the
  page so the frosted surfaces refract real colour.
- Buttons, chips, and the audio player picked up matching glass
  chrome with hover sheen sweeps and a unified focus-visible ring.
- Startup banner moved to a `lifespan` handler so the FastAPI
  deprecation warning goes away.

### Fixed
- Object URLs are now released through a single `releaseObjectUrl`
  helper, so live mode no longer leaks blob URLs across reloads.
- Upload page clears the file label and removes the invalid state
  when the file input is reset.
- Live page `setStatus` and `resetMeters` no longer crash when their
  target elements are missing.

## v0.5.0 (2026-03-15)

### Added
- Real-time audio engine with WebSocket streaming
- Ring buffer, DSP utilities, mel filterbank
- Beat tracker, pitch tracker, loudness meter
- Audio fingerprinting (chromaprint + constellation)
- Fingerprint database with search and matching
- Collaboration rooms with presence tracking
- Time-stamped annotations with reactions
- Threaded comments and cursor sync
- Secure share links with password/expiry
- Plugin system with registry and hooks
- Effects chain with wet/dry mixing
- Built-in effects: gain, filters, compressor, reverb
- Preset effect chains (vocal, master, ambient)
- Analysis reports (markdown, HTML, batch)
- Comparison reports for A/B analysis
- JSONL/CSV/TSV export formats
- Dashboard stats, usage tracking, activity feed
- Alert rules and leaderboard
- Project manager, notifications, search engine
- Audio tagging, favorites, history tracking
- Token bucket rate limiter
- Stereo analysis (width, correlation, pan)
- Musical key detection, chromatic tuner
- Dynamic range analyzer, noise gate, level meter
- Tempo estimator, analyzer chain, audio router
- Config versioning with diff
- Plugin loader and sandbox
- Fine-grained collaboration permissions

## v0.4.0 (2026-03-05)
- REST API v1 with Pydantic schemas
- Clustering (K-Means, DBSCAN)
- Audio segmentation and pitch detection
- Effects (speed, pitch, fade, mix)
- Visualization package with themes
- Unified CLI
- Docker + CI/CD

## v0.3.0 (2026-02-21)
- Audio utilities and error handling
- Spectral flatness analysis
- Type aliases, constants, editorconfig

## v0.2.0 (2026-02-20)
- Audio comparison module
- RMS energy computation
- Onset visualization
- Docker and logging config

## v0.1.0 (2026-01-01)
- Initial release
- Log-mel feature extraction
- UMAP embedding (2D/3D)
- Live audio capture
