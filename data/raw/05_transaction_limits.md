# Transaction Limits

Document ID: FP-ACC-005 | Owner: Risk & Fraud | Version 3.0 | Effective: 1 January 2026

Limits protect customers from fraud and help FinPay meet regulatory obligations. All limits are in USD and reset at 00:00 UTC (daily) and on the 1st of each month (monthly).

## Transfer limits (outgoing)
| Tier | Daily limit | Monthly limit |
|---|---|---|
| Basic | 1,000 | 5,000 |
| Plus | 10,000 | 50,000 |
| Business | 100,000 | 1,000,000 |

## Card limits
| Tier | Daily card spending | Daily ATM withdrawal |
|---|---|---|
| Basic | 1,500 | 300 |
| Plus | 7,500 | 1,000 |
| Business | 25,000 | 2,000 |

## New account restriction
During the first 30 days after an account is opened, all limits are set at **50%** of the normal tier limit. Full limits apply automatically on day 31.

## International transfers
The maximum single international transfer is USD 25,000 for Plus and USD 100,000 for Business.

## Temporary limit increases
Plus and Business customers may request a one-time temporary increase through the app. Requests are reviewed by Risk within 1 business day and may require proof of source of funds.

## What happens when a limit is reached
The transaction is declined with error code FP-2002 (limit exceeded). The customer sees the remaining limit in the app.
