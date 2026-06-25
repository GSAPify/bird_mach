"""Custom exception hierarchy for Mach audio visualization."""

from __future__ import annotations


class MachError(Exception):
    """Base exception for all Mach errors."""


class AudioLoadError(MachError):
    """Raised when an audio file cannot be loaded or decoded."""


class AudioTooLongError(MachError):
    """Raised when audio exceeds the maximum allowed duration."""

    def __init__(self, duration_s: float, max_s: float) -> None:
        self.duration_s = duration_s
        self.max_s = max_s
        super().__init__(
            f"Audio is {duration_s:.1f}s but the limit is {max_s:.1f}s"
        )


class AudioTooLargeError(MachError):
    """Raised when an audio file exceeds the maximum upload size."""

    def __init__(self, size_mb: float, max_mb: float) -> None:
        self.size_mb = size_mb
        self.max_mb = max_mb
        super().__init__(
            f"File is {size_mb:.1f} MB but the limit is {max_mb:.0f} MB"
        )


class URLFetchError(MachError):
    """Raised when fetching audio from a remote URL fails."""


class AuthError(MachError):
    """Base class for authentication and account errors."""


class EmailAlreadyRegisteredError(AuthError):
    """Raised when registering an email that already has an account."""


class InvalidCredentialsError(AuthError):
    """Raised when login fails due to a bad email/password combination."""


class UserNotFoundError(AuthError):
    """Raised when an account lookup finds no matching user."""


class InactiveUserError(AuthError):
    """Raised when a deactivated account attempts to authenticate."""


class TokenError(AuthError):
    """Raised when a token is missing, malformed, expired, or invalid."""


class BillingError(MachError):
    """Base class for payment and subscription errors."""


class PaymentProviderError(BillingError):
    """Raised when the upstream payment provider rejects or fails a call."""


class WebhookVerificationError(BillingError):
    """Raised when a payment webhook signature cannot be verified."""
