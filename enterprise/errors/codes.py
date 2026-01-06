"""Enterprise error codes."""

class MachError(Exception):
    code = "E0000"


class QuotaExceeded(MachError):
    """[E1009] Usage quota has been exceeded"""
    code = "E1009"
    message = "Usage quota has been exceeded"
    status_code = 546
