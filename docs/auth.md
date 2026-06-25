# Authentication & User Management

Mach ships a self-contained user-management layer under `bird_mach.auth`. It is
intentionally dependency-light: password hashing uses the standard library and
tokens use PyJWT.

## Architecture

```
┌─────────────┐     ┌──────────────┐     ┌───────────────────┐
│  routes.py  │────▶│  service.py  │────▶│   store.py        │
│ (FastAPI)   │     │ AuthService  │     │ UserRepository    │
└─────────────┘     └──────┬───────┘     │  ├ InMemory (test)│
       │                   │             │  └ SQLite (prod)  │
       │            ┌──────┴───────┐     └───────────────────┘
       │            │ passwords.py │
 dependencies.py    │  tokens.py   │
 (current_user,     └──────────────┘
  require_role)
```

- **`passwords.py`** — PBKDF2-HMAC-SHA256 at OWASP's 600k-iteration floor.
  Hashes are self-describing (`pbkdf2_sha256$iterations$salt$hash`), and the
  login path transparently re-hashes when the cost factor rises.
- **`tokens.py`** — HS256 JWTs via PyJWT. Access and refresh tokens carry a
  `type` claim so a refresh token can't be replayed as an access token. The
  signing secret must be at least 32 bytes (RFC 7518).
- **`store.py`** — `UserRepository` with an in-memory backend (tests) and a
  durable SQLite backend (default). Swap in Postgres by implementing the same
  interface.
- **`service.py`** — orchestration. `authenticate()` returns the same error for
  unknown-email and wrong-password, so responses can't enumerate accounts.

## Configuration

| Env var | Default | Notes |
|---|---|---|
| `JWT_SECRET` | _(empty)_ | **Required in production** (≥32 bytes). In dev an ephemeral secret is generated. |
| `ACCESS_TOKEN_TTL_S` | `900` | Access-token lifetime (15 min). |
| `REFRESH_TOKEN_TTL_S` | `2592000` | Refresh-token lifetime (30 days). |
| `AUTH_DB_PATH` | `mach.db` | SQLite file for users + subscriptions. |

Generate a secret:

```bash
python -c "import secrets; print(secrets.token_urlsafe(48))"
```

## Endpoints

| Method | Path | Auth | Description |
|---|---|---|---|
| `POST` | `/auth/register` | — | Create an account. Returns the public user. |
| `POST` | `/auth/login` | — | Exchange credentials for an access+refresh pair. |
| `POST` | `/auth/refresh` | — | Exchange a refresh token for a new pair. |
| `GET`  | `/auth/me` | Bearer | Current user. |
| `POST` | `/auth/change-password` | Bearer | Change password (verifies the current one). |
| `DELETE` | `/auth/me` | Bearer | Delete the current account. |
| `GET`  | `/auth/events` | Bearer | The user's recent security events (audit log). |
| `POST` | `/auth/password-reset/request` | — | Begin a reset. Always 202 (no enumeration). |
| `POST` | `/auth/password-reset/confirm` | — | Complete a reset with a token. |
| `POST` | `/auth/verify-email/request` | Bearer | Issue an email-verification token. |
| `POST` | `/auth/verify-email/confirm` | — | Confirm verification with a token. |

Login and registration are rate-limited per client IP (token bucket) to blunt
brute-force and enumeration. Login/register/password-change/deletion are
written to a durable audit log.

### Admin (requires the `admin` role)

| Method | Path | Description |
|---|---|---|
| `GET`  | `/auth/admin/users` | List users (paginated). |
| `GET`  | `/auth/admin/users/{id}` | Inspect one user. |
| `POST` | `/auth/admin/users/{id}/deactivate` | Deactivate an account. |
| `POST` | `/auth/admin/users/{id}/activate` | Reactivate an account. |
| `PUT`  | `/auth/admin/users/{id}/role` | Change a user's role. |

> Password-reset and email-verification tokens are emailed in production. With
> no email provider wired here, the token is logged and returned in the
> response **only when `ENVIRONMENT` is not production**, for local testing.

### Example

```bash
curl -X POST localhost:8000/auth/register \
  -H 'content-type: application/json' \
  -d '{"email":"a@b.com","password":"supersecret"}'

TOKEN=$(curl -s -X POST localhost:8000/auth/login \
  -H 'content-type: application/json' \
  -d '{"email":"a@b.com","password":"supersecret"}' | jq -r .access_token)

curl localhost:8000/auth/me -H "Authorization: Bearer $TOKEN"
```

## Protecting routes

```python
from fastapi import Depends
from bird_mach.auth.dependencies import get_current_user, require_role
from bird_mach.auth.models import Role, User

@router.get("/secret")
def secret(user: User = Depends(get_current_user)):
    return {"hello": user.email}

@router.get("/admin")
def admin(user: User = Depends(require_role(Role.ADMIN))):
    return {"ok": True}
```
