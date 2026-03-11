# Search

    ## Overview

    The search module provides enterprise-grade functionality
    for the Mach audio visualization platform.

    ## Configuration

    ```python
    from enterprise.config.settings import SEARCH_ENABLED
    ```

    ## Usage

    ```python
    from enterprise.search import SearchService

    service = SearchService()
    service.configure(timeout=30)
    result = service.execute()
    ```

    ## API Endpoints

    | Method | Path | Description |
    |--------|------|-------------|
    | GET | `/api/v2/search/` | List all |
    | GET | `/api/v2/search/{id}` | Get by ID |
    | POST | `/api/v2/search/` | Create new |
    | PUT | `/api/v2/search/{id}` | Update |
    | DELETE | `/api/v2/search/{id}` | Delete |
