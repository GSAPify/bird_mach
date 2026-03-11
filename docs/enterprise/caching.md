# Caching

    ## Overview

    The caching module provides enterprise-grade functionality
    for the Mach audio visualization platform.

    ## Configuration

    ```python
    from enterprise.config.settings import CACHING_ENABLED
    ```

    ## Usage

    ```python
    from enterprise.caching import CachingService

    service = CachingService()
    service.configure(timeout=30)
    result = service.execute()
    ```

    ## API Endpoints

    | Method | Path | Description |
    |--------|------|-------------|
    | GET | `/api/v2/caching/` | List all |
    | GET | `/api/v2/caching/{id}` | Get by ID |
    | POST | `/api/v2/caching/` | Create new |
    | PUT | `/api/v2/caching/{id}` | Update |
    | DELETE | `/api/v2/caching/{id}` | Delete |
