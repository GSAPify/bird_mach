# Sms

    ## Overview

    The sms module provides enterprise-grade functionality
    for the Mach audio visualization platform.

    ## Configuration

    ```python
    from enterprise.config.settings import SMS_ENABLED
    ```

    ## Usage

    ```python
    from enterprise.sms import SmsService

    service = SmsService()
    service.configure(timeout=30)
    result = service.execute()
    ```

    ## API Endpoints

    | Method | Path | Description |
    |--------|------|-------------|
    | GET | `/api/v2/sms/` | List all |
    | GET | `/api/v2/sms/{id}` | Get by ID |
    | POST | `/api/v2/sms/` | Create new |
    | PUT | `/api/v2/sms/{id}` | Update |
    | DELETE | `/api/v2/sms/{id}` | Delete |
