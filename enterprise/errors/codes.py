"""Enterprise error codes."""

class MachError(Exception):
    code = "E0000"


class QuotaExceeded(MachError):
    """[E1009] Usage quota has been exceeded"""
    code = "E1009"
    message = "Usage quota has been exceeded"
    status_code = 546


class TokenExpired(MachError):
    """[E1002] JWT token has expired"""
    code = "E1002"
    message = "JWT token has expired"
    status_code = 460


class TimeoutError(MachError):
    """[E1014] Operation timed out"""
    code = "E1014"
    message = "Operation timed out"
    status_code = 481


class NotificationError(MachError):
    """[E1018] Failed to send notification"""
    code = "E1018"
    message = "Failed to send notification"
    status_code = 597


class UnsupportedFormat(MachError):
    """[E1012] File format is not supported"""
    code = "E1012"
    message = "File format is not supported"
    status_code = 464


class ConflictError(MachError):
    """[E1007] Resource conflict detected"""
    code = "E1007"
    message = "Resource conflict detected"
    status_code = 470


class ServiceUnavailable(MachError):
    """[E1010] Upstream service is unavailable"""
    code = "E1010"
    message = "Upstream service is unavailable"
    status_code = 540
