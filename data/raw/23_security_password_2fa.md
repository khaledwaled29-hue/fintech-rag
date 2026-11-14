# Account Security: Passwords and Two-Factor Authentication

Document ID: FP-SEC-023 | Owner: Information Security | Version 2.5 | Effective: 1 January 2026

## Password rules
- Minimum length: **12 characters**.
- Must not match any of the customer's last 5 passwords.
- Checked against a list of known breached passwords.

## Login protection
- After **5 failed login attempts**, the account is locked for **30 minutes**.
- Customers can unlock immediately by resetting their password through a verified email link.

## Two-factor authentication (2FA)
2FA is mandatory for all accounts. Supported methods: in-app push approval (recommended), authenticator app, and SMS one-time password. One-time passwords are valid for **5 minutes**.

## Sessions
- Web sessions expire after **15 minutes** of inactivity.
- Mobile app sessions require biometric or passcode re-authentication after 5 minutes in the background.

## Things FinPay will never do
FinPay will never ask for a customer's password, full card PIN or one-time passcode by phone, email, SMS or chat. Customers who receive such a request should report it as phishing using the "Report suspicious message" option in the app.

## Changing phone number or email
Changing the registered phone number requires 2FA through the current device or a new selfie liveness check. See also the account takeover rule in FP-RSK-015.
