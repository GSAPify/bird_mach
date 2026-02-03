# Push

    ## Overview

    The push module provides enterprise-grade functionality
    for the Mach audio visualization platform.

    ## Configuration

    ```python
    from enterprise.config.settings import PUSH_ENABLED
    ```

    ## Usage

    ```python
    from enterprise.push import PushService

    service = PushService()
    service.configure(timeout=30)
    result = service.execute()
    ```

    ## API Endpoints

    | Method | Path | Description |
    |--------|------|-------------|
    | GET | `/api/v2/push/` | List all |
    | GET | `/api/v2/push/{id}` | Get by ID |
    | POST | `/api/v2/push/` | Create new |
    | PUT | `/api/v2/push/{id}` | Update |
    | DELETE | `/api/v2/push/{id}` | Delete |
