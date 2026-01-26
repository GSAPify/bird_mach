# Sorting

    ## Overview

    The sorting module provides enterprise-grade functionality
    for the Mach audio visualization platform.

    ## Configuration

    ```python
    from enterprise.config.settings import SORTING_ENABLED
    ```

    ## Usage

    ```python
    from enterprise.sorting import SortingService

    service = SortingService()
    service.configure(timeout=30)
    result = service.execute()
    ```

    ## API Endpoints

    | Method | Path | Description |
    |--------|------|-------------|
    | GET | `/api/v2/sorting/` | List all |
    | GET | `/api/v2/sorting/{id}` | Get by ID |
    | POST | `/api/v2/sorting/` | Create new |
    | PUT | `/api/v2/sorting/{id}` | Update |
    | DELETE | `/api/v2/sorting/{id}` | Delete |
