# Merchant Settlement Schedule

Document ID: FP-FIN-012 | Owner: Finance & Settlement | Version 3.4 | Effective: 1 February 2026

## Standard settlement
Established merchants are settled on **T+1**: card payments captured on a business day are paid to the merchant's bank account on the next business day.

## New merchants
For the first **90 days** after onboarding, merchants are settled on **T+3** to manage risk. After 90 days without significant chargebacks, the merchant moves to T+1 automatically.

## Cut-off time
The daily settlement cut-off is **18:00 UTC**. Payments captured after the cut-off are treated as captured on the next business day.

## Weekends and holidays
No settlements are paid on weekends or public holidays. Payments captured on Friday after cut-off, Saturday or Sunday are settled on the following business day according to the merchant's schedule.

## Rolling reserve
High-risk merchants may have a rolling reserve of **5%** of each day's volume held for 180 days. Reserves are released automatically at the end of the holding period.

## Settlement reports
A settlement report (CSV) is available in the Merchant Dashboard and via the `settlement.paid` webhook for each payout, listing every transaction, fee and adjustment.

## Delayed settlements
If a settlement does not arrive within 2 business days of the expected date, merchants should contact Merchant Support with the settlement ID.
