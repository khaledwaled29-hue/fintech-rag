# Account Freezes and Closure

Document ID: FP-ACC-017 | Owner: Customer Operations | Version 2.1 | Effective: 1 January 2026

## Why an account may be frozen
- Suspected fraud or account takeover.
- Incomplete or failed re-verification (KYC).
- A compliance review or legal order.
- A customer request (for example, if the phone was stolen).

## What a freeze means
While an account is frozen, outgoing payments, card transactions and withdrawals are blocked. Incoming payments are still accepted. API calls on a frozen account return error FP-2003.

## Review time
FinPay reviews frozen accounts within **5 business days**. The customer is told which documents (if any) are needed. Where a freeze is due to a legal order or compliance review, FinPay may not be able to share the reason (see FP-CMP-016).

## Closing an account (customer request)
1. Withdraw or transfer the remaining balance, or provide bank details for its return.
2. Cancel any active subscriptions linked to the card.
3. Request closure in the app (Settings > Close account) or through support.
The account closes within 2 business days. Any remaining balance is returned within **10 business days**. Closure is free.

## Closure by FinPay
FinPay may close an account with 60 days' notice, or immediately in cases of fraud, serious breach of terms, or legal requirement.

## Records after closure
Transaction records are kept after closure as described in the Data Retention policy (FP-LEG-026).
