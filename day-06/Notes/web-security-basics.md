# Web Security Fundamentals & Threat Analysis Notes

| Field | Details |
| :--- | :--- |
| **Concept** | **1. Broken Authentication & Session Management** |
| Plain-English Explanation | Flaws in how applications verify user identities or manage session tokens after login, allowing attackers to hijack active user accounts. |
| Why It Matters | Enables unauthorized account takeover, data theft, and impersonation of privileged users or system administrators. |
| Defensive Practice | Enforce multi-factor authentication (MFA), set `HttpOnly`, `Secure`, and `SameSite` cookie flags, and properly invalidate sessions upon logout. |
| Evidence Needed | Server access logs, cookie inspection headers, session token entropy analysis, and authentication workflow captures. |
| Limitation | Inspecting cookies alone cannot determine whether session tokens are securely generated on the backend server. |

| Field | Details |
| :--- | :--- |
| **Concept** | **2. Input Validation & SQL Injection (SQLi)** |
| Plain-English Explanation | Vulnerability where untrusted user input is concatenated directly into database queries, allowing attackers to manipulate backend database logic. |
| Why It Matters | Can lead to unauthorized data disclosure, database tampering, full system compromise, or complete data loss. |
| Defensive Practice | Use parameterized queries (prepared statements) and enforce strict server-side input validation rules. |
| Evidence Needed | HTTP request parameters, error response bodies revealing database exceptions, and backend query logs. |
| Limitation | A 500 Internal Server Error does not automatically confirm SQL injection without explicit database feedback or payload testing. |

| Field | Details |
| :--- | :--- |
| **Concept** | **3. Cross-Site Scripting (XSS)** |
| Plain-English Explanation | Flaw where untrusted data is reflected or stored by an application and rendered in a victim's browser as executable JavaScript. |
| Why It Matters | Permits attackers to steal session cookies, perform actions on behalf of users, or redirect victims to malicious phishing sites. |
| Defensive Practice | Implement context-appropriate output encoding, sanitize user input, and deploy a robust Content Security Policy (CSP). |
| Evidence Needed | Rendered HTML source code, browser console error logs, and HTTP response body analysis. |
| Limitation | Static code review cannot always predict how complex modern JavaScript frameworks will handle DOM rendering in real time. |

| Field | Details |
| :--- | :--- |
| **Concept** | **4. Transport Security vs. Application Security (HTTPS)** |
| Plain-English Explanation | Distinguishing encrypted network transmission (TLS) from secure application logic, access controls, and input handling. |
| Why It Matters | Relying on HTTPS alone gives a false sense of security; encrypted traffic can still contain severe application-layer vulnerabilities. |
| Defensive Practice | Combine TLS transport encryption with rigorous application-level authorization checks, input validation, and secure headers. |
| Evidence Needed | SSL/TLS certificate inspection, cipher suite analysis, and application penetration test results. |
| Limitation | A valid HTTPS certificate proves the connection is encrypted; it does not prove the website content is safe or free of application bugs. |

| Field | Details |
| :--- | :--- |
| **Concept** | **5. Security Headers (CSP & HSTS)** |
| Plain-English Explanation | HTTP response headers configured by servers to instruct browsers to enforce security policies and restrict risky behaviors. |
| Why It Matters | Provides defense-in-depth against XSS, clickjacking, protocol downgrade attacks, and unauthorized resource loading. |
| Defensive Practice | Properly configure headers such as `Content-Security-Policy`, `Strict-Transport-Security`, and `X-Content-Type-Options`. |
| Evidence Needed | Browser DevTools Network response header inspection or automated header scanning tools. |
| Limitation | The absence of a single security header does not automatically mean an application is exploitable; context and architecture matter. |
