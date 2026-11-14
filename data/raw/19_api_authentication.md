# FinPay API: Authentication

Document ID: FP-API-019 | Owner: Developer Platform | Version 3.0 | Effective: 1 May 2026

## Overview
The FinPay API uses **OAuth 2.0 client credentials**. Each integration has a client ID and a client secret, created in the Developer Dashboard. Only Business accounts and approved partners have API access.

## Environments
| Environment | Base URL | Key prefix |
|---|---|---|
| Sandbox | https://sandbox.api.finpay.example | fp_test_ |
| Live | https://api.finpay.example | fp_live_ |

## Getting an access token
Send a POST request to `/oauth/token` with `grant_type=client_credentials`, your client ID and client secret. The response contains an `access_token` valid for **3600 seconds** (1 hour). Request a new token before it expires; tokens cannot be refreshed.

## Using the token
Include the header `Authorization: Bearer <access_token>` in every request.

## Rate limits
- Live: **100 requests per second** per client.
- Sandbox: **25 requests per second** per client.
Exceeding the limit returns HTTP 429 with error code FP-4290. Use the `Retry-After` header to know when to retry.

## Idempotency
POST requests that create payments or payouts must include an `Idempotency-Key` header (a unique UUID). Keys are stored for 24 hours. Re-using a key with a different request body returns FP-4001.

## Security
Never put client secrets in mobile apps or front-end code. Rotate secrets at least every 90 days. Compromised secrets can be revoked instantly in the Developer Dashboard.
