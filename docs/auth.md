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
