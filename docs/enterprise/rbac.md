# Rbac

    ## Overview

    The rbac module provides enterprise-grade functionality
    for the Mach audio visualization platform.

    ## Configuration

    ```python
    from enterprise.config.settings import RBAC_ENABLED
    ```

    ## Usage

    ```python
    from enterprise.rbac import RbacService

    service = RbacService()
    service.configure(timeout=30)
    result = service.execute()
    ```

    ## API Endpoints

    | Method | Path | Description |
    |--------|------|-------------|
    | GET | `/api/v2/rbac/` | List all |
    | GET | `/api/v2/rbac/{id}` | Get by ID |
    | POST | `/api/v2/rbac/` | Create new |
    | PUT | `/api/v2/rbac/{id}` | Update |
    | DELETE | `/api/v2/rbac/{id}` | Delete |
