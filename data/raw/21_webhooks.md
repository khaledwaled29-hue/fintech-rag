# FinPay API: Webhooks

Document ID: FP-API-021 | Owner: Developer Platform | Version 2.1 | Effective: 1 May 2026

## What webhooks are
Webhooks notify your server when events happen in your FinPay account, so you do not need to poll the API.

## Common events
- `payment.succeeded`, `payment.failed`
- `refund.created`
- `dispute.created`, `dispute.closed`
- `payout.paid`, `payout.failed`
- `settlement.paid`

## Setup
Register an HTTPS endpoint URL in the Developer Dashboard and select the events to receive. HTTP (non-TLS) endpoints are not allowed.

## Verifying signatures
Every webhook includes an `X-FinPay-Signature` header containing an **HMAC-SHA256** signature of the raw request body, computed with your webhook signing secret. Always verify the signature before trusting the event, and reject events with a timestamp older than 5 minutes to prevent replay attacks.

## Responding
Your endpoint must return an HTTP 2xx status within **10 seconds**. Do heavy processing asynchronously after responding.

## Retries
If delivery fails (non-2xx response or timeout), FinPay retries up to **8 times over 24 hours** with exponential backoff. After the final failure, the event is marked as failed and can be resent manually from the Dashboard.

## Duplicates and ordering
The same event may occasionally be delivered more than once, and events may arrive out of order. Use the `event_id` to ignore duplicates.
