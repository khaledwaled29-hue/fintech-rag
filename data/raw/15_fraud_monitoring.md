# Fraud Monitoring Rules

Document ID: FP-RSK-015 | Owner: Risk & Fraud | Version 6.0 | Effective: 1 May 2026 | Classification: Internal

## Overview
Every transaction is scored in real time by the FinPay fraud engine on a scale from 0 (low risk) to 100 (high risk).

## Risk score actions
| Score | Action |
|---|---|
| 0 - 59 | Approve |
| 60 - 79 | Step-up authentication (one-time password or in-app confirmation) |
| 80 - 100 | Block and send to fraud analyst queue |

## Key rules
1. **Velocity rule:** more than 5 card transactions within 10 minutes triggers a temporary hold and a review.
2. **First international transaction:** a customer's first foreign card transaction above USD 500 requires step-up authentication.
3. **New device:** a login from a new device requires two-factor authentication, and outgoing transfers above USD 1,000 are blocked for 24 hours on that device.
4. **Account takeover signals:** a password reset followed by a change of phone number within 24 hours freezes outgoing payments pending review.
5. **High-risk merchant categories:** transactions at gambling and cryptocurrency merchants receive a +15 score adjustment.

## Analyst review
Blocked transactions are reviewed by a fraud analyst within **4 hours**, 24/7. The customer is contacted through the app to confirm whether the transaction is genuine.

## False positives
If a genuine transaction was blocked, the customer can confirm it in the app and retry. Confirmed patterns are fed back to improve the model.
