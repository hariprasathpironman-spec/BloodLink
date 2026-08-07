# Blood Donor & Emergency Request Network - Security Architecture

This document outlines the prominent security features and OWASP Top 10 mitigations implemented in this project, designed specifically to meet rigorous evaluation criteria for cybersecurity standards.

## 1. Tamper-Evident Cryptographic Audit Log
* **Feature:** Every critical state-changing action (User Registration, Login, Hospital Approval, Emergency Request Creation/Closing) is logged immutably.
* **Mechanism:** We employ a blockchain-style hash chain. Each log entry calculates its `current_hash` using `SHA-256(previous_hash + action + actor_id + event_payload)`.
* **Mitigation:** Protects against **A08:2021-Software and Data Integrity Failures**. If an attacker gains DB access and alters an emergency request log or tries to delete a malicious action, the hash chain breaks instantly, alerting administrators via the `verify_audit_log.py` utility.

## 2. Document-Based Identity Verification & RBAC
* **Feature:** Hospitals cannot post emergency requests immediately upon registration. They are forced into an "Unverified" state.
* **Mechanism:** A valid institutional registration/license document must be uploaded to Cloudinary. An `Admin` must manually review the document in the Admin Dashboard and approve the account. Only then does the `@hospital_required` RBAC decorator permit request creation.
* **Mitigation:** Protects against **A01:2021-Broken Access Control** and **A04:2021-Insecure Design** by employing a zero-trust model for high-impact actions (creating life-or-death alerts).

## 3. Fraud and Anomaly Detection Engine
* **Feature:** The backend automatically analyzes incoming emergency requests for fraudulent behavior patterns.
* **Mechanism:** If a hospital posts > 5 requests in a 24-hour rolling window, or if a hospital posts a request for a `patient_name` that already has an active open request, the request is marked with `flagged_suspicious = True`. This alerts Admins in the dashboard.
* **Mitigation:** Mitigates **A04:2021-Insecure Design** (Business Logic Flaws) by preventing bad actors from spamming the network and exhausting donor resources.

## 4. API Rate Limiting (Flask-Limiter)
* **Feature:** Strict limits on endpoints.
* **Mechanism:**
  - `POST /api/auth/login`: 5 requests per minute.
  - `POST /api/auth/register/*`: 3 requests per minute.
  - `POST /api/request/`: 10 requests per hour per verified hospital.
* **Mitigation:** Protects against **A07:2021-Identification and Authentication Failures** (Credential Stuffing/Brute Force) and DDoS attacks.

## 5. Defense Against Injection & XSS
* **Feature:** Data sanitization and secure headers.
* **Mechanism (SQLi):** SQLAlchemy ORM parameterizes all database queries by default. No raw SQL strings are concatenated with user input.
* **Mechanism (XSS):** `Flask-Talisman` enforces a strict Content Security Policy (CSP), allowing scripts and styles only from `'self'` and trusted CDNs (Cloudinary, Google Fonts), preventing malicious script execution in the frontend.
* **Mitigation:** Addresses **A03:2021-Injection**.

## 6. Secure Authentication (JWT + Bcrypt)
* **Feature:** Stateless, secure token-based authentication.
* **Mechanism:** Passwords are hashed using `Bcrypt` with a randomly generated salt. The system issues short-lived Access Tokens (1 hour) and long-lived Refresh Tokens, minimizing the impact of a stolen access token. Email OTP is required for all new registrations.
* **Mitigation:** Addresses **A02:2021-Cryptographic Failures** and **A07:2021-Identification and Authentication Failures**.

## 7. Comprehensive Input Validation
* **Feature:** Strict payload validation.
* **Mechanism:** We use `Marshmallow` schemas for all incoming API data. Enforces data types (e.g., age as integer), value boundaries (e.g., weight > 45.0), and allowed categorical values (Blood Groups: 'A+', 'O-', etc.) before the business logic is ever executed.
* **Mitigation:** Core defense against **A04:2021-Insecure Design** and Injection variants.
