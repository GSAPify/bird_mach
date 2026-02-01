# Billing

    ## Overview

    The billing module provides enterprise-grade functionality
    for the Mach audio visualization platform.

    ## Configuration

    ```python
    from enterprise.config.settings import BILLING_ENABLED
    ```

    ## Usage

    ```python
    from enterprise.billing import BillingService

    service = BillingService()
    service.configure(timeout=30)
    result = service.execute()
    ```

    ## API Endpoints

    | Method | Path | Description |
    |--------|------|-------------|
    | GET | `/api/v2/billing/` | List all |
    | GET | `/api/v2/billing/{id}` | Get by ID |
    | POST | `/api/v2/billing/` | Create new |
    | PUT | `/api/v2/billing/{id}` | Update |
    | DELETE | `/api/v2/billing/{id}` | Delete |
