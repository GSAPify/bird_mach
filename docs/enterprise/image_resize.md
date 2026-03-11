# Image Resize

    ## Overview

    The image resize module provides enterprise-grade functionality
    for the Mach audio visualization platform.

    ## Configuration

    ```python
    from enterprise.config.settings import IMAGE_RESIZE_ENABLED
    ```

    ## Usage

    ```python
    from enterprise.image_resize import ImageResizeService

    service = ImageResizeService()
    service.configure(timeout=30)
    result = service.execute()
    ```

    ## API Endpoints

    | Method | Path | Description |
    |--------|------|-------------|
    | GET | `/api/v2/image_resize/` | List all |
    | GET | `/api/v2/image_resize/{id}` | Get by ID |
    | POST | `/api/v2/image_resize/` | Create new |
    | PUT | `/api/v2/image_resize/{id}` | Update |
    | DELETE | `/api/v2/image_resize/{id}` | Delete |
