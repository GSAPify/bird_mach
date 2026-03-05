# Usage Metering

    ## Overview

    The usage metering module provides enterprise-grade functionality
    for the Mach audio visualization platform.

    ## Configuration

    ```python
    from enterprise.config.settings import USAGE_METERING_ENABLED
    ```

    ## Usage

    ```python
    from enterprise.usage_metering import UsageMeteringService

    service = UsageMeteringService()
    service.configure(timeout=30)
    result = service.execute()
    ```

    ## API Endpoints

    | Method | Path | Description |
    |--------|------|-------------|
    | GET | `/api/v2/usage_metering/` | List all |
    | GET | `/api/v2/usage_metering/{id}` | Get by ID |
    | POST | `/api/v2/usage_metering/` | Create new |
    | PUT | `/api/v2/usage_metering/{id}` | Update |
    | DELETE | `/api/v2/usage_metering/{id}` | Delete |
