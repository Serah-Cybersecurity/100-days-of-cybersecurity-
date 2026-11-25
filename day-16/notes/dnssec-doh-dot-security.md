# Day 16 - DNS Security: DNSSEC, DoH, and DoT

## 1. Executive Summary & Core Security Concepts

Security professionals and network administrators often confuse **DNSSEC**, **DoH (DNS over HTTPS)**, and **DoT (DNS over TLS)**. While all three enhance DNS security, they address fundamentally different threats in the cybersecurity landscape:

* **DNSSEC** guarantees **authenticity and integrity** (answering: *"Is this DNS answer really from the legitimate owner, or did an attacker tamper with it in transit?"*). It does **not** encrypt DNS traffic.
* **DoH & DoT** guarantee **confidentiality and privacy** (answering: *"Can eavesdroppers on my local network or ISP see which website names I am resolving?"*). They encrypt the transport channel between the client and resolver, but do **not** inherently validate whether the zone data itself was spoofed at the source.

---

## 2. DNSSEC (Domain Name System Security Extensions)

### 2.1 What Is DNSSEC?
Defined primarily in **RFC 4033**, DNSSEC adds cryptographic signatures to existing DNS records. When a resolver receives a response for a DNSSEC-enabled domain, it uses public key cryptography to mathematically verify that the response was signed by the legitimate zone operator and was not modified by a Man-in-the-Middle (MitM) attacker.

### 2.2 Why Do We Need DNSSEC?
Traditional DNS queries are sent in plaintext over UDP port 53 without authentication. An attacker on the network path can easily perform **DNS Cache Poisoning** or **ARP Spoofing** to inject fake IP addresses into recursive resolvers, redirecting users to malicious phishing portals. DNSSEC prevents this by signing zone data.

### 2.3 Key DNSSEC Resource Records

| Record Type | Full Name | Purpose & Function |
| :--- | :--- | :--- |
| **DNSKEY** | DNS Public Key | Holds the public signing key that resolvers use to verify signatures for a DNS zone. |
| **RRSIG** | Resource Record Signature | Holds the actual cryptographic signature for a specific record set (e.g., an `A` record paired with its `RRSIG`). |
| **DS** | Delegation Signer | Stored in the parent zone (e.g., `.com`) to establish a cryptographic "Chain of Trust" to the child zone (e.g., `example.com`). |
| **NSEC / NSEC3** | Next Secure | Cryptographically proves that a requested domain or record **does not exist** (authenticated denial of existence), preventing fake `NXDOMAIN` injection. |

> **Analyst Key Takeaway:** DNSSEC provides **integrity and origin authentication**. It does **NOT** hide what domain you are looking up. Anyone sniffing your traffic can still read your DNS queries in plaintext.

---

## 3. Encrypted DNS: DoH vs. DoT

To protect DNS queries from local network eavesdropping, ISP tracking, and transport-layer tampering, the industry developed encrypted DNS transport protocols.

### 3.1 DNS over TLS (DoT)
* **Standard:** RFC 7858.
* **Transport:** Encapsulates standard DNS messages inside a dedicated **TLS tunnel** over **TCP Port 853**.
* **Network Visibility:** Because DoT operates on a dedicated port (`853`), network administrators and firewalls can easily identify, monitor, or block DoT traffic at the perimeter.

### 3.2 DNS over HTTPS (DoH)
* **Standard:** RFC 8484.
* **Transport:** Encodes DNS queries inside standard HTTP/2 or HTTP/3 payloads over **TCP/UDP Port 443** (standard HTTPS).
* **Network Visibility:** Because DoH blends in with normal web browsing traffic over port `443`, it is extremely difficult for network firewalls to distinguish DoH queries from standard HTTPS website requests without deep packet inspection or endpoint telemetry.

---

## 4. Master Comparison Matrix

| Feature | Traditional DNS | DNSSEC | DoT (DNS over TLS) | DoH (DNS over HTTPS) |
| :--- | :--- | :--- | :--- | :--- |
| **Primary Goal** | Name Resolution | Data Integrity & Authenticity | Transport Confidentiality | Transport Confidentiality & Blend-in |
| **Transport Port** | UDP/TCP 53 | UDP/TCP 53 | TCP 853 | TCP 443 |
| **Encrypts Queries?** | ❌ No | ❌ No | ✅ Yes | ✅ Yes |
| **Authenticates Source?** | ❌ No | ✅ Yes (Cryptographic) | ❌ No (Transport only) | ❌ No (Transport only) |
| **Perimeter Visibility** | High (Cleartext) | High (Cleartext) | Easy to Block (Port 853) | Blends with Web Traffic (Port 443) |

---

## 5. SOC Analyst & Job Market Impact

### The Defensive Blindspot (The "DoH Dilemma")
While DoH increases user privacy, it presents a significant challenge for Enterprise SOC Security Operations:
1. **Blindspot Creation:** If an enterprise workstation enables DoH to a public resolver (like `1.1.1.1` or `8.8.8.8`), network-level DNS monitoring tools and firewalls lose visibility into outbound DNS lookups.
2. **Malware Exploitation:** Threat actors and C2 frameworks (e.g., Cobalt Strike, Godlua) increasingly use DoH to bypass corporate DNS filters and exfiltrate data undetected over port 443.

### How Enterprise Defenders Respond
* **Group Policy / MDM Enforcement:** Disable unauthorized DoH settings in web browsers across corporate endpoints.
* **Centralized Enterprise Resolvers:** Force all internal DNS through internal recursive resolvers that enforce security filtering.
* **Endpoint Telemetry (EDR):** Rely on endpoint agent logging (e.g., Sysmon Event ID 22 — DNS Query) to capture browser lookups **before** they are encrypted and sent out over DoH/DoT.

---

## 6. What to Document & What to Remember

* **What to Document:**
  * Endpoint configuration state regarding DoH/DoT policies.
  * Sysmon Event ID 22 or EDR logs when performing host-level DNS analysis.
  * Presence of DNSSEC validation flags (`AD` flag - Authenticated Data) in query logs.
* **What You Must Remember:**
  * **DNSSEC** = Prevents Spoofing / Proves Identity (No Encryption).
  * **DoT / DoH** = Prevents Eavesdropping / Encrypts Channel (No Zone Signing).
