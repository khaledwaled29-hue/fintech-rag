# Troubleshooting Declined Payments

Document ID: FP-SUP-028 | Owner: Customer Support | Version 2.3 | Effective: 1 March 2026

Use this guide when a customer reports that a card payment or transfer was declined.

## Step 1: Check the decline reason in the agent console
| Reason shown | Likely cause | Advice to the customer |
|---|---|---|
| Insufficient funds | Balance too low | Top up the wallet and retry. |
| Limit exceeded | Daily, monthly or new-account limit reached | Show remaining limit in app; Plus/Business can request a temporary increase. |
| Card frozen | Customer froze the card | Unfreeze in Cards > Unfreeze. |
| Wrong PIN | Incorrect PIN entered | After 3 wrong attempts the PIN is blocked; unblock in the app. |
| Fraud block | Fraud engine score 80 or higher | Customer confirms the transaction in the app, then retries. |
| Step-up failed | OTP not completed | Retry and complete the authentication within 5 minutes. |
| Merchant category blocked | Customer disabled gambling or online payments in card settings | Change card settings if the customer wishes. |

## Step 2: Check for account-level issues
- Account frozen or pending re-verification (FP-ACC-017, FP-KYC-003).
- Account in the first 30 days (50% limits apply).

## Step 3: Check for incidents
Look at the internal status board. If there is an active SEV1 or SEV2 incident, use the incident script and do not troubleshoot further.

## Step 4: Escalate
If no reason is found, escalate to Payments Operations with the transaction ID, timestamp and merchant name.
