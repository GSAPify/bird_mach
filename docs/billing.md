# Billing & Payments

`bird_mach.billing` adds Stripe-backed subscriptions on top of the auth layer.
The design keeps the app's view of "who is entitled" durable and in lock-step
with Stripe, so a paywall check never makes a network call.

## Architecture

```
                         ┌──────────────────┐
  POST /billing/checkout │  BillingService  │  create_customer / checkout
  POST /billing/portal   │                  │──────────────┐
  POST /billing/webhook  └────────┬─────────┘              ▼
  GET  /billing/subscription      │              ┌───────────────────┐
  GET  /billing/plans             │              │ PaymentProvider    │
                                  │              │  ├ Fake (test/off) │
                          ┌───────┴────────┐     │  └ Stripe (prod)   │
                          │ Subscription   │     └───────────────────┘
                          │ Repository     │              ▲
                          │ (SQLite/memory)│   verified webhook events
                          └────────────────┘              │
                                  ▲              ┌─────────┴─────────┐
                                  └──────────────│  Stripe (webhook) │
                                  upsert by      └───────────────────┘
                                  stripe_subscription_id
```

## How entitlement works

1. A user calls `POST /billing/checkout`. `BillingService.ensure_customer`
   creates a Stripe customer (storing `stripe_customer_id` on the account) and
   returns a Checkout URL.
2. The user pays on Stripe's hosted page.
3. Stripe sends a `customer.subscription.created` webhook. The signature is
   **verified before any state change** (`stripe.Webhook.construct_event`).
4. The handler resolves the user from the Stripe customer id and upserts a
   `Subscription` row keyed by the Stripe subscription id — so replayed
   webhooks are idempotent.
5. `require_subscription` checks `is_entitled(user)` (active/trialing) locally
   and returns **402 Payment Required** otherwise.

Only `active` and `trialing` grant access; `past_due`, `canceled`, `unpaid`,
and `incomplete` do not (`SubscriptionStatus.grants_access`).

## Configuration

| Env var | Default | Notes |
|---|---|---|
| `STRIPE_API_KEY` | _(empty)_ | Empty → **offline mode** (fake provider). Set to a real key to enable Stripe. |
| `STRIPE_WEBHOOK_SECRET` | _(empty)_ | `whsec_…`; required to verify webhooks. |
| `STRIPE_PRICE_PRO` | _(empty)_ | The Stripe Price ID backing the Pro plan. |

## Endpoints

| Method | Path | Auth | Description |
|---|---|---|---|
| `GET`  | `/billing/plans` | — | The plan catalog. |
| `GET`  | `/billing/subscription` | Bearer | Current subscription + entitlement. |
| `POST` | `/billing/checkout` | Bearer | Start a hosted checkout for a plan. |
| `POST` | `/billing/portal` | Bearer | Open the self-service billing portal. |
| `POST` | `/billing/cancel` | Bearer | Cancel at the end of the current period. |
| `GET`  | `/billing/invoices` | Bearer | The caller's recent invoices. |
| `POST` | `/billing/webhook` | signature | Stripe webhook (verified before any state change). |

Metered analysis and the premium batch route live under `/api/v1` (see below).

## Gating a premium feature

```python
from fastapi import Depends
from bird_mach.billing.dependencies import require_subscription
from bird_mach.auth.models import User

@router.post("/analyze/batch")
def batch_analyze(user: User = Depends(require_subscription)):
    ...  # only reachable with an active subscription
```

## Verification status

The fake provider and the full webhook→entitlement flow are covered by tests.
The **live Stripe path is not exercised by the test suite** — verifying it
requires real test-mode keys and replaying events with the Stripe CLI:

```bash
stripe listen --forward-to localhost:8000/billing/webhook
stripe trigger customer.subscription.created
```

Treat the live integration as unverified until those checks are run against a
test-mode account.
