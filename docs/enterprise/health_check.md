# Health Check

    ## Overview

    The health check module provides enterprise-grade functionality
    for the Mach audio visualization platform.

    ## Configuration

    ```python
    from enterprise.config.settings import HEALTH_CHECK_ENABLED
    ```

    ## Usage

    ```python
    from enterprise.health_check import HealthCheckService

    service = HealthCheckService()
    service.configure(timeout=30)
    result = service.execute()
    ```

    ## API Endpoints

    | Method | Path | Description |
    |--------|------|-------------|
    | GET | `/api/v2/health_check/` | List all |
    | GET | `/api/v2/health_check/{id}` | Get by ID |
    | POST | `/api/v2/health_check/` | Create new |
    | PUT | `/api/v2/health_check/{id}` | Update |
    | DELETE | `/api/v2/health_check/{id}` | Delete |
