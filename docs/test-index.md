# Test Index

This index maps representative test files to the behavior they cover so contributors can find regression coverage quickly.

| Test File | Coverage |
|-----------|----------|
| [`tests/accessibility/test_color_blind.py`](../tests/accessibility/test_color_blind.py) | Tests for color-blind palettes |
| [`tests/accessibility/test_screen_reader.py`](../tests/accessibility/test_screen_reader.py) | Tests for screen reader descriptions |
| [`tests/accessibility/test_shortcuts.py`](../tests/accessibility/test_shortcuts.py) | Tests for keyboard shortcuts |
| [`tests/api_v2/test_filters.py`](../tests/api_v2/test_filters.py) | Tests for query filters |
| [`tests/api_v2/test_pagination.py`](../tests/api_v2/test_pagination.py) | Tests for pagination |
| [`tests/api_v2/test_rate_limit.py`](../tests/api_v2/test_rate_limit.py) | Tests for rate limiter |
| [`tests/api_v2/test_versioning.py`](../tests/api_v2/test_versioning.py) | Tests for API versioning |
| [`tests/audio_formats/test_detector.py`](../tests/audio_formats/test_detector.py) | Tests for format detection |
| [`tests/audio_formats/test_normalize.py`](../tests/audio_formats/test_normalize.py) | Tests for normalization |
| [`tests/auth/test_admin.py`](../tests/auth/test_admin.py) | End-to-end tests for the admin user-management API |
| [`tests/auth/test_audit.py`](../tests/auth/test_audit.py) | Tests for the auth audit log |
| [`tests/auth/test_passwords.py`](../tests/auth/test_passwords.py) | Tests for PBKDF2 password hashing |
| [`tests/auth/test_ratelimit.py`](../tests/auth/test_ratelimit.py) | Tests for auth rate limiting |
| [`tests/auth/test_revocation.py`](../tests/auth/test_revocation.py) | Tests for the refresh-token revocation denylist |
| [`tests/auth/test_routes.py`](../tests/auth/test_routes.py) | End-to-end API tests for the auth router |
| [`tests/auth/test_service.py`](../tests/auth/test_service.py) | Tests for the authentication service |
| [`tests/auth/test_store.py`](../tests/auth/test_store.py) | Tests for the user repositories |
| [`tests/auth/test_tokens.py`](../tests/auth/test_tokens.py) | Tests for JWT issuance and verification |
| [`tests/batch/test_pipeline.py`](../tests/batch/test_pipeline.py) | Tests for batch pipeline |
| [`tests/batch/test_progress.py`](../tests/batch/test_progress.py) | Tests for batch progress |
| [`tests/batch/test_queue.py`](../tests/batch/test_queue.py) | Tests for job queue |
| [`tests/batch/test_scanner.py`](../tests/batch/test_scanner.py) | Tests for file scanner |
| [`tests/billing/test_dependencies.py`](../tests/billing/test_dependencies.py) | Tests for billing dependency wiring |
| [`tests/billing/test_models.py`](../tests/billing/test_models.py) | Tests for billing models and the plan catalog |
| [`tests/billing/test_provider.py`](../tests/billing/test_provider.py) | Tests for the fake payment provider (real Stripe path is integration-only) |
| [`tests/billing/test_routes.py`](../tests/billing/test_routes.py) | End-to-end API tests for the billing router |
| [`tests/billing/test_service.py`](../tests/billing/test_service.py) | Tests for the billing service, including the webhook → entitlement flow |
| [`tests/billing/test_store.py`](../tests/billing/test_store.py) | Tests for subscription repositories (both backends, same cases) |
| [`tests/caching/test_cache_key.py`](../tests/caching/test_cache_key.py) | Tests for cache key generation |
| [`tests/caching/test_disk_cache.py`](../tests/caching/test_disk_cache.py) | Tests for disk cache |
| [`tests/caching/test_memory_cache.py`](../tests/caching/test_memory_cache.py) | Tests for memory cache |
| [`tests/caching/test_tiered_cache.py`](../tests/caching/test_tiered_cache.py) | Tests for tiered cache |
| [`tests/collaboration/test_annotations.py`](../tests/collaboration/test_annotations.py) | Tests for annotations |
| [`tests/collaboration/test_comments.py`](../tests/collaboration/test_comments.py) | Tests for comments |
| [`tests/collaboration/test_permissions.py`](../tests/collaboration/test_permissions.py) | Tests for permissions |
| [`tests/collaboration/test_presence.py`](../tests/collaboration/test_presence.py) | Tests for presence tracker |
| [`tests/collaboration/test_rooms.py`](../tests/collaboration/test_rooms.py) | Tests for collaboration rooms |
| [`tests/collaboration/test_sharing.py`](../tests/collaboration/test_sharing.py) | Tests for sharing service |
| [`tests/collaboration/test_versioning.py`](../tests/collaboration/test_versioning.py) | Tests for config versioning |
| [`tests/conftest.py`](../tests/conftest.py) | Shared fixtures for Mach test suite |
| [`tests/conftest_enterprise.py`](../tests/conftest_enterprise.py) | Enterprise test configuration |
