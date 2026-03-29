"""SDK-specific exceptions."""

class MachSDKError(Exception):
    """Base exception for Mach SDK errors."""

class AuthenticationError(MachSDKError):
    """Raised when API key is invalid or missing."""

class RateLimitError(MachSDKError):
    """Raised when API rate limit is exceeded."""
    def __init__(self, retry_after_s: float = 60.0):
        super().__init__(f"Rate limited. Retry after {retry_after_s}s")
        self.retry_after_s = retry_after_s

class AnalysisError(MachSDKError):
    """Raised when audio analysis fails."""
    def __init__(self, audio_id: str, reason: str):
        super().__init__(f"Analysis failed for {audio_id}: {reason}")
        self.audio_id = audio_id
        self.reason = reason

class NotFoundError(MachSDKError):
    """Raised when a resource is not found."""
