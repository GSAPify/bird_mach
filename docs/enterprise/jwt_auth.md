# Jwt Auth

    ## Overview

    The jwt auth module provides enterprise-grade functionality
    for the Mach audio visualization platform.

    ## Configuration

    ```python
    from enterprise.config.settings import JWT_AUTH_ENABLED
    ```

    ## Usage

    ```python
    from enterprise.jwt_auth import JwtAuthService

    service = JwtAuthService()
    service.configure(timeout=30)
    result = service.execute()
    ```

    ## API Endpoints

    | Method | Path | Description |
    |--------|------|-------------|
    | GET | `/api/v2/jwt_auth/` | List all |
    | GET | `/api/v2/jwt_auth/{id}` | Get by ID |
    | POST | `/api/v2/jwt_auth/` | Create new |
    | PUT | `/api/v2/jwt_auth/{id}` | Update |
    | DELETE | `/api/v2/jwt_auth/{id}` | Delete |
