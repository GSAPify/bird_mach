# Video Thumb

    ## Overview

    The video thumb module provides enterprise-grade functionality
    for the Mach audio visualization platform.

    ## Configuration

    ```python
    from enterprise.config.settings import VIDEO_THUMB_ENABLED
    ```

    ## Usage

    ```python
    from enterprise.video_thumb import VideoThumbService

    service = VideoThumbService()
    service.configure(timeout=30)
    result = service.execute()
    ```

    ## API Endpoints

    | Method | Path | Description |
    |--------|------|-------------|
    | GET | `/api/v2/video_thumb/` | List all |
    | GET | `/api/v2/video_thumb/{id}` | Get by ID |
    | POST | `/api/v2/video_thumb/` | Create new |
    | PUT | `/api/v2/video_thumb/{id}` | Update |
    | DELETE | `/api/v2/video_thumb/{id}` | Delete |
