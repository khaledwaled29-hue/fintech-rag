# FinPay API: Error Codes

Document ID: FP-API-020 | Owner: Developer Platform | Version 3.2 | Effective: 1 May 2026

All errors return a JSON body with `code`, `message` and `request_id`. Always log the `request_id` and include it when contacting support.

| Code | HTTP | Meaning | What to do |
|---|---|---|---|
| FP-1001 | 401 | Invalid access token | Check the Authorization header format and token. |
| FP-1002 | 401 | Access token expired | Request a new token from /oauth/token. |
| FP-1003 | 403 | Insufficient permissions | The client is not allowed to call this endpoint. |
| FP-2001 | 402 | Insufficient funds | The account balance is too low. Do not retry automatically. |
| FP-2002 | 402 | Limit exceeded | A daily, monthly or per-transaction limit was reached (see FP-ACC-005). |
| FP-2003 | 403 | Account frozen | The account is frozen (see FP-ACC-017). Do not retry. |
| FP-3001 | 400 | Invalid card details | Check card number, expiry and CVV. |
| FP-3002 | 400 | Card expired | Ask the customer for a valid card. |
| FP-3003 | 402 | Card declined by issuer | Ask the customer to contact their card issuer. |
| FP-4000 | 400 | Validation error | A request field is missing or invalid; see `message`. |
| FP-4001 | 409 | Idempotency key conflict | The key was already used with a different request body. |
| FP-4040 | 404 | Resource not found | Check the ID in the URL. |
| FP-4290 | 429 | Rate limit exceeded | Wait for the time in the Retry-After header. |
| FP-5000 | 500 | Internal error | Retry with exponential backoff, up to 3 times. |
| FP-5030 | 503 | Service temporarily unavailable | Retry with exponential backoff; check status.finpay.example. |

## Retry guidance
Only retry errors in the 5xx range and FP-4290. Never retry FP-2001, FP-2003 or other 4xx errors without changing the request, because the result will be the same. Always reuse the same Idempotency-Key when retrying a payment request.
