"""Tests for PBKDF2 password hashing."""

from __future__ import annotations

import pytest

from bird_mach.auth.passwords import hash_password, needs_rehash, verify_password


class TestHashPassword:
    def test_roundtrip(self):
        encoded = hash_password("correct horse battery staple")
        assert verify_password("correct horse battery staple", encoded)

    def test_wrong_password_rejected(self):
        encoded = hash_password("s3cret")
        assert not verify_password("guess", encoded)

    def test_salt_makes_hashes_unique(self):
        a = hash_password("same")
        b = hash_password("same")
        assert a != b

    def test_empty_password_rejected(self):
        with pytest.raises(ValueError):
            hash_password("")

    def test_encoded_format(self):
        encoded = hash_password("x", iterations=1000)
        algo, iters, salt, digest = encoded.split("$")
        assert algo == "pbkdf2_sha256"
        assert iters == "1000"
        assert len(salt) == 32  # 16 bytes hex
        assert len(digest) == 64  # sha256 hex


class TestVerifyPassword:
    def test_malformed_hash_is_false_not_error(self):
        assert verify_password("anything", "not-a-valid-hash") is False

    def test_unknown_algorithm_rejected(self):
        assert verify_password("x", "md5$1$aa$bb") is False


class TestNeedsRehash:
    def test_weaker_cost_needs_rehash(self):
        encoded = hash_password("x", iterations=1000)
        assert needs_rehash(encoded, iterations=600_000)

    def test_current_cost_does_not(self):
        encoded = hash_password("x", iterations=600_000)
        assert not needs_rehash(encoded, iterations=600_000)

    def test_garbage_needs_rehash(self):
        assert needs_rehash("garbage")
