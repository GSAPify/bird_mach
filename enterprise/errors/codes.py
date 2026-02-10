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


class ValidationError(MachError):
    """[E1006] Input validation failed"""
    code = "E1006"
    message = "Input validation failed"
    status_code = 552


class ProcessingFailed(MachError):
    """[E1013] Audio processing pipeline failed"""
    code = "E1013"
    message = "Audio processing pipeline failed"
    status_code = 437


class EncryptionError(MachError):
    """[E1020] Encryption/decryption failed"""
    code = "E1020"
    message = "Encryption/decryption failed"
    status_code = 422


class WebhookError(MachError):
    """[E1019] Webhook delivery failed"""
    code = "E1019"
    message = "Webhook delivery failed"
    status_code = 572


class DatabaseError(MachError):
    """[E1015] Database operation failed"""
    code = "E1015"
    message = "Database operation failed"
    status_code = 507


class CacheError(MachError):
    """[E1016] Cache operation failed"""
    code = "E1016"
    message = "Cache operation failed"
    status_code = 476


class PaymentRequired(MachError):
    """[E1008] Payment is required for this action"""
    code = "E1008"
    message = "Payment is required for this action"
    status_code = 503


class InsufficientPermissions(MachError):
    """[E1003] User lacks required permissions"""
    code = "E1003"
    message = "User lacks required permissions"
    status_code = 435
