# Sandbox Testing Guide

Document ID: FP-API-022 | Owner: Developer Platform / QA | Version 1.7 | Effective: 1 May 2026

## Purpose
The sandbox is a safe test environment that behaves like the live API but moves no real money. Sandbox keys start with `fp_test_`.

## Test cards
| Card number | Behaviour |
|---|---|
| 4000 0000 0000 0002 | Payment approved |
| 4000 0000 0000 0010 | Declined: insufficient funds (FP-2001) |
| 4000 0000 0000 0028 | Requires 3-D Secure challenge |
| 4000 0000 0000 0036 | Declined: card expired (FP-3002) |
| 4000 0000 0000 0044 | Declined by issuer (FP-3003) |
Use any future expiry date and any 3-digit CVV.

## Magic amounts
- An amount ending in **.99** simulates a timeout, returning FP-5030 on the first attempt and success on retry. Use it to test retry and idempotency handling.
- An amount of exactly **666.00** triggers a fraud block (risk score 90).

## Webhooks in sandbox
Sandbox sends real webhook calls to your endpoint. You can also trigger any event manually from the Developer Dashboard (Webhooks > Send test event).

## Data reset
Sandbox data is reset on the first Sunday of every month. Do not rely on sandbox IDs for long-term tests.

## Going live checklist
1. All test cards above handled correctly.
2. Webhook signatures verified.
3. Idempotency keys used on every payment POST.
4. Errors logged with request_id.
5. Live keys stored in a secrets manager, never in code.
