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
| [`tests/dashboard/test_activity.py`](../tests/dashboard/test_activity.py) | Tests for activity feed |
| [`tests/dashboard/test_alerts.py`](../tests/dashboard/test_alerts.py) | Tests for alert manager |
| [`tests/dashboard/test_leaderboard.py`](../tests/dashboard/test_leaderboard.py) | Tests for leaderboard |
| [`tests/dashboard/test_stats.py`](../tests/dashboard/test_stats.py) | Tests for stats aggregator |
| [`tests/dashboard/test_usage.py`](../tests/dashboard/test_usage.py) | Tests for usage tracker |
| [`tests/enterprise/admin/test_blue_green.py`](../tests/enterprise/admin/test_blue_green.py) | Tests for enterprise.admin.blue_green |
| [`tests/enterprise/admin/test_db_backup.py`](../tests/enterprise/admin/test_db_backup.py) | Tests for enterprise.admin.db_backup |
| [`tests/enterprise/admin/test_integration_testing.py`](../tests/enterprise/admin/test_integration_testing.py) | Tests for enterprise.admin.integration_testing |
| [`tests/enterprise/admin/test_memcached.py`](../tests/enterprise/admin/test_memcached.py) | Tests for enterprise.admin.memcached |
| [`tests/enterprise/admin/test_rate_limit.py`](../tests/enterprise/admin/test_rate_limit.py) | Tests for enterprise.admin.rate_limit |
| [`tests/enterprise/analytics/test_audio_transcode.py`](../tests/enterprise/analytics/test_audio_transcode.py) | Tests for enterprise.analytics.audio_transcode |
| [`tests/enterprise/analytics/test_plugin_system.py`](../tests/enterprise/analytics/test_plugin_system.py) | Tests for enterprise.analytics.plugin_system |
| [`tests/enterprise/api_v2/test_caching.py`](../tests/enterprise/api_v2/test_caching.py) | Tests for enterprise.api.v2.caching |
| [`tests/enterprise/api_v2/test_gcs_storage.py`](../tests/enterprise/api_v2/test_gcs_storage.py) | Tests for enterprise.api.v2.gcs_storage |
| [`tests/enterprise/api_v2/test_mfa.py`](../tests/enterprise/api_v2/test_mfa.py) | Tests for enterprise.api.v2.mfa |
| [`tests/enterprise/api_v2/test_rate_limit.py`](../tests/enterprise/api_v2/test_rate_limit.py) | Tests for enterprise.api.v2.rate_limit |
| [`tests/enterprise/api_v2/test_team_mgmt.py`](../tests/enterprise/api_v2/test_team_mgmt.py) | Tests for enterprise.api.v2.team_mgmt |
| [`tests/enterprise/api_v2/test_websockets.py`](../tests/enterprise/api_v2/test_websockets.py) | Tests for enterprise.api.v2.websockets |
| [`tests/enterprise/api_v2_auth/test_api_keys.py`](../tests/enterprise/api_v2_auth/test_api_keys.py) | Tests for enterprise.api.v2.auth.api_keys |
| [`tests/enterprise/api_v2_auth/test_distributed_cache.py`](../tests/enterprise/api_v2_auth/test_distributed_cache.py) | Tests for enterprise.api.v2.auth.distributed_cache |
| [`tests/enterprise/api_v2_auth/test_unit_testing.py`](../tests/enterprise/api_v2_auth/test_unit_testing.py) | Tests for enterprise.api.v2.auth.unit_testing |
| [`tests/enterprise/api_v2_endpoints/test_file_upload.py`](../tests/enterprise/api_v2_endpoints/test_file_upload.py) | Tests for enterprise.api.v2.endpoints.file_upload (FileUploadValidator via enterprise.ml.models.file_upload) |
| [`tests/enterprise/api_v2_endpoints/test_hook_registry.py`](../tests/enterprise/api_v2_endpoints/test_hook_registry.py) | Tests for enterprise.api.v2.endpoints.hook_registry |
| [`tests/enterprise/api_v2_endpoints/test_integration_testing.py`](../tests/enterprise/api_v2_endpoints/test_integration_testing.py) | Tests for enterprise.api.v2.endpoints.integration_testing |
| [`tests/enterprise/api_v2_endpoints/test_local_storage.py`](../tests/enterprise/api_v2_endpoints/test_local_storage.py) | Tests for enterprise.api.v2.endpoints.local_storage |
| [`tests/enterprise/api_v2_endpoints/test_video_thumb.py`](../tests/enterprise/api_v2_endpoints/test_video_thumb.py) | Tests for enterprise.api.v2.endpoints.video_thumb |
| [`tests/enterprise/api_v2_middleware/test_encryption.py`](../tests/enterprise/api_v2_middleware/test_encryption.py) | Tests for enterprise.api.v2.middleware.encryption |
| [`tests/enterprise/api_v2_middleware/test_ml_inference.py`](../tests/enterprise/api_v2_middleware/test_ml_inference.py) | Tests for enterprise.api.v2.middleware.ml_inference |
| [`tests/enterprise/audit/test_alerting.py`](../tests/enterprise/audit/test_alerting.py) | Tests for enterprise.audit.alerting |
| [`tests/enterprise/audit/test_ci_pipeline.py`](../tests/enterprise/audit/test_ci_pipeline.py) | Tests for enterprise.audit.ci_pipeline |
| [`tests/enterprise/audit/test_distributed_cache.py`](../tests/enterprise/audit/test_distributed_cache.py) | Tests for enterprise.audit.distributed_cache |
| [`tests/enterprise/auth/test_blue_green.py`](../tests/enterprise/auth/test_blue_green.py) | Tests for enterprise.auth.blue_green |
| [`tests/enterprise/auth/test_ci_pipeline.py`](../tests/enterprise/auth/test_ci_pipeline.py) | Tests for enterprise.auth.ci_pipeline |
| [`tests/enterprise/auth/test_ml_inference.py`](../tests/enterprise/auth/test_ml_inference.py) | Tests for enterprise.auth.ml_inference |
| [`tests/enterprise/auth/test_notifications.py`](../tests/enterprise/auth/test_notifications.py) | Tests for enterprise.auth.notifications |
| [`tests/enterprise/auth/test_redis_cache.py`](../tests/enterprise/auth/test_redis_cache.py) | Tests for enterprise.auth.redis_cache |
| [`tests/enterprise/auth_providers/test_db_backup.py`](../tests/enterprise/auth_providers/test_db_backup.py) | Tests for enterprise.auth.providers.db_backup |
| [`tests/enterprise/auth_providers/test_long_polling.py`](../tests/enterprise/auth_providers/test_long_polling.py) | Tests for enterprise.auth.providers.long_polling |
| [`tests/enterprise/billing/test_canary_deploy.py`](../tests/enterprise/billing/test_canary_deploy.py) | Tests for enterprise.billing.canary_deploy |
| [`tests/enterprise/billing/test_key_rotation.py`](../tests/enterprise/billing/test_key_rotation.py) | Tests for enterprise.billing.key_rotation |
| [`tests/enterprise/billing/test_redis_cache.py`](../tests/enterprise/billing/test_redis_cache.py) | Tests for enterprise.billing.redis_cache |
| [`tests/enterprise/cache/test_connection_pool.py`](../tests/enterprise/cache/test_connection_pool.py) | Tests for enterprise.cache.connection_pool |
| [`tests/enterprise/cache/test_i18n.py`](../tests/enterprise/cache/test_i18n.py) | Tests for enterprise.cache.i18n |
| [`tests/enterprise/cache/test_image_resize.py`](../tests/enterprise/cache/test_image_resize.py) | Tests for enterprise.cache.image_resize |
| [`tests/enterprise/cache/test_s3_storage.py`](../tests/enterprise/cache/test_s3_storage.py) | Tests for enterprise.cache.s3_storage |
| [`tests/enterprise/compliance/test_analytics.py`](../tests/enterprise/compliance/test_analytics.py) | Tests for enterprise.compliance.analytics |
| [`tests/enterprise/compliance/test_batch_processing.py`](../tests/enterprise/compliance/test_batch_processing.py) | Tests for enterprise.compliance.batch_processing |
| [`tests/enterprise/compliance/test_billing.py`](../tests/enterprise/compliance/test_billing.py) | Tests for enterprise.compliance.billing |
| [`tests/enterprise/compliance/test_image_resize.py`](../tests/enterprise/compliance/test_image_resize.py) | Tests for enterprise.compliance.image_resize |
