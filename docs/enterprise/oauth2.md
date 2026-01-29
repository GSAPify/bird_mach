# Oauth2

    ## Overview

    The oauth2 module provides enterprise-grade functionality
    for the Mach audio visualization platform.

    ## Configuration

    ```python
    from enterprise.config.settings import OAUTH2_ENABLED
    ```

    ## Usage

    ```python
    from enterprise.oauth2 import Oauth2Service

    service = Oauth2Service()
    service.configure(timeout=30)
    result = service.execute()
    ```

    ## API Endpoints

    | Method | Path | Description |
    |--------|------|-------------|
    | GET | `/api/v2/oauth2/` | List all |
    | GET | `/api/v2/oauth2/{id}` | Get by ID |
    | POST | `/api/v2/oauth2/` | Create new |
    | PUT | `/api/v2/oauth2/{id}` | Update |
    | DELETE | `/api/v2/oauth2/{id}` | Delete |
