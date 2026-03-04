# Websockets

    ## Overview

    The websockets module provides enterprise-grade functionality
    for the Mach audio visualization platform.

    ## Configuration

    ```python
    from enterprise.config.settings import WEBSOCKETS_ENABLED
    ```

    ## Usage

    ```python
    from enterprise.websockets import WebsocketsService

    service = WebsocketsService()
    service.configure(timeout=30)
    result = service.execute()
    ```

    ## API Endpoints

    | Method | Path | Description |
    |--------|------|-------------|
    | GET | `/api/v2/websockets/` | List all |
    | GET | `/api/v2/websockets/{id}` | Get by ID |
    | POST | `/api/v2/websockets/` | Create new |
    | PUT | `/api/v2/websockets/{id}` | Update |
    | DELETE | `/api/v2/websockets/{id}` | Delete |
