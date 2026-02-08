# Invoicing

    ## Overview

    The invoicing module provides enterprise-grade functionality
    for the Mach audio visualization platform.

    ## Configuration

    ```python
    from enterprise.config.settings import INVOICING_ENABLED
    ```

    ## Usage

    ```python
    from enterprise.invoicing import InvoicingService

    service = InvoicingService()
    service.configure(timeout=30)
    result = service.execute()
    ```

    ## API Endpoints

    | Method | Path | Description |
    |--------|------|-------------|
    | GET | `/api/v2/invoicing/` | List all |
    | GET | `/api/v2/invoicing/{id}` | Get by ID |
    | POST | `/api/v2/invoicing/` | Create new |
    | PUT | `/api/v2/invoicing/{id}` | Update |
    | DELETE | `/api/v2/invoicing/{id}` | Delete |
