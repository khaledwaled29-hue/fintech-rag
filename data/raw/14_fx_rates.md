# Foreign Exchange (FX) Rates and Markup

Document ID: FP-FIN-014 | Owner: Treasury | Version 1.9 | Effective: 1 April 2026

## Rate source
FinPay uses wholesale market rates from its liquidity providers. Rates are refreshed every **60 seconds** during market hours.

## Markup
FinPay adds a markup to the wholesale rate:
- Weekdays (Monday 00:00 UTC to Friday 22:00 UTC): **0.5%**.
- Weekends (Friday 22:00 UTC to Monday 00:00 UTC): **1.0%**, because markets are closed and rates may move sharply when they reopen.

## Where the markup applies
- International transfers.
- Card payments and ATM withdrawals in a foreign currency.

## Rate lock
When a customer views a quote for an international transfer, the rate is locked for **30 seconds**. If the customer does not confirm within 30 seconds, a new quote is shown.

## Card transactions
For card payments, the exchange rate is applied when the card network settles the transaction, which may be 1 to 2 days after the payment. The final amount can therefore differ slightly from the amount shown when the payment was made.

## Transparency
The app always shows the rate used, the markup and the total cost before confirmation, in line with FinPay's clear-pricing commitment.
