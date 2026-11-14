# Handling Chargebacks (Merchants)

Document ID: FP-MER-010 | Owner: Merchant Operations | Version 2.3 | Effective: 1 March 2026

## Notification
When a cardholder disputes a payment, FinPay notifies the merchant by email, in the Merchant Dashboard, and via the `dispute.created` webhook. The disputed amount is held from the merchant's balance.

## Responding
Merchants have **7 calendar days** from the notification to submit evidence (representment). If no evidence is submitted within 7 days, the dispute is automatically accepted and the merchant loses the disputed amount.

## Useful evidence
- Proof of delivery with tracking number and signature.
- Customer communication showing agreement or satisfaction.
- Terms and refund policy shown at checkout.
- For digital goods: login or download logs with IP addresses.
- 3-D Secure authentication results for card-not-present transactions.

## Fees
A USD 15.00 chargeback fee is charged per dispute. The fee is refunded if the merchant wins.

## Excessive chargebacks
If a merchant's chargeback ratio exceeds **1% of transactions** in a calendar month, the merchant is placed on a remediation plan. If the ratio stays above 1% for 3 consecutive months, FinPay may apply a rolling reserve or terminate the merchant agreement.

## Prevention tips
Use clear billing descriptors, send order confirmations, enable 3-D Secure, and refund quickly when customers ask.
