# Api Keys

    ## Overview

    The api keys module provides enterprise-grade functionality
    for the Mach audio visualization platform.

    ## Configuration

    ```python
    from enterprise.config.settings import API_KEYS_ENABLED
    ```

    ## Usage

    ```python
    from enterprise.api_keys import ApiKeysService

    service = ApiKeysService()
    service.configure(timeout=30)
    result = service.execute()
    ```

    ## API Endpoints

    | Method | Path | Description |
    |--------|------|-------------|
    | GET | `/api/v2/api_keys/` | List all |
    | GET | `/api/v2/api_keys/{id}` | Get by ID |
    | POST | `/api/v2/api_keys/` | Create new |
    | PUT | `/api/v2/api_keys/{id}` | Update |
    | DELETE | `/api/v2/api_keys/{id}` | Delete |
