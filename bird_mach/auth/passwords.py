"""Password hashing using PBKDF2-HMAC-SHA256 from the standard library.

PBKDF2 is deliberately chosen over a bcrypt/argon2 dependency: it is FIPS-
approved, ships with CPython, and is the same primitive Django used by default
for years. Hashes are stored in a self-describing string so the iteration
count can be raised over time without invalidating existing hashes:

    pbkdf2_sha256$<iterations>$<salt_hex>$<hash_hex>

:func:`needs_rehash` lets the login path transparently upgrade a user's stored
hash to the current cost the next time they authenticate.
"""

from __future__ import annotations

import hashlib
import hmac
import secrets

_ALGORITHM = "pbkdf2_sha256"
# OWASP's 2023 floor for PBKDF2-HMAC-SHA256 is 600k iterations.
_DEFAULT_ITERATIONS = 600_000
_SALT_BYTES = 16


def hash_password(password: str, *, iterations: int = _DEFAULT_ITERATIONS) -> str:
    """Return an encoded PBKDF2 hash of ``password``."""
    if not password:
        raise ValueError("password must not be empty")
    salt = secrets.token_bytes(_SALT_BYTES)
    derived = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, iterations)
    return f"{_ALGORITHM}${iterations}${salt.hex()}${derived.hex()}"


def verify_password(password: str, encoded: str) -> bool:
    """Check ``password`` against a previously :func:`hash_password` value.

    Returns ``False`` for malformed or unknown-algorithm hashes rather than
    raising, so a corrupt stored value reads as an auth failure, not a 500.
    """
    try:
        algorithm, iterations_s, salt_hex, hash_hex = encoded.split("$")
        if algorithm != _ALGORITHM:
            return False
        iterations = int(iterations_s)
        salt = bytes.fromhex(salt_hex)
        expected = bytes.fromhex(hash_hex)
    except (ValueError, AttributeError):
        return False
    derived = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, iterations)
    # Constant-time comparison to avoid leaking equality timing.
    return hmac.compare_digest(derived, expected)


def needs_rehash(encoded: str, *, iterations: int = _DEFAULT_ITERATIONS) -> bool:
    """True if ``encoded`` was produced with a weaker cost than the current one."""
    try:
        algorithm, iterations_s, _, _ = encoded.split("$")
    except (ValueError, AttributeError):
        return True
    return algorithm != _ALGORITHM or int(iterations_s) < iterations
