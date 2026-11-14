# Incident Response Runbook

Document ID: FP-ENG-027 | Owner: Site Reliability Engineering | Version 4.0 | Effective: 1 June 2026 | Classification: Internal

## Severity levels
| Severity | Definition | Response |
|---|---|---|
| SEV1 | Payments or logins unavailable for all or most customers; data breach | On-call paged immediately, must acknowledge within 5 minutes |
| SEV2 | Major feature degraded (e.g. card payments failing for one network, settlements delayed) | Acknowledge within 15 minutes |
| SEV3 | Minor feature broken, workaround available | Next business day |
| SEV4 | Cosmetic issue | Normal backlog |

## SEV1 procedure
1. The on-call engineer acknowledges the page and opens an incident channel.
2. An Incident Commander (IC) is assigned; the IC coordinates and does not debug.
3. The status page (status.finpay.example) is updated within **15 minutes** and then every **30 minutes** until resolved.
4. Customer Support is informed so agents can use the incident script.
5. Prefer rollback of the latest deployment if the incident started after a release.

## Communication
Merchants with P1 issues are contacted directly by Merchant Support. Regulators are notified for major operational incidents according to the Compliance policy.

## After the incident
A blameless postmortem is written within **5 business days** for every SEV1 and SEV2. It includes a timeline, root cause, impact, and action items with owners and due dates.

## Common first checks
Recent deployments, database replication lag, card network connectivity, third-party provider status pages, and error-rate dashboards (FP-5000 and FP-5030 spikes).
