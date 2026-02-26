# Subscriptions

    ## Overview

    The subscriptions module provides enterprise-grade functionality
    for the Mach audio visualization platform.

    ## Configuration

    ```python
    from enterprise.config.settings import SUBSCRIPTIONS_ENABLED
    ```

    ## Usage

    ```python
    from enterprise.subscriptions import SubscriptionsService

    service = SubscriptionsService()
    service.configure(timeout=30)
    result = service.execute()
    ```

    ## API Endpoints

    | Method | Path | Description |
    |--------|------|-------------|
    | GET | `/api/v2/subscriptions/` | List all |
    | GET | `/api/v2/subscriptions/{id}` | Get by ID |
    | POST | `/api/v2/subscriptions/` | Create new |
    | PUT | `/api/v2/subscriptions/{id}` | Update |
    | DELETE | `/api/v2/subscriptions/{id}` | Delete |
