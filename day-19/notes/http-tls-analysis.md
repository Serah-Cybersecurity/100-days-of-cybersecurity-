# Technical Note: Zeek HTTP & TLS Metadata Analysis Mechanics

**Author:** Serah Mulwa  
**Module:** Day 19 - Network Threat Hunting with Zeek  

---

## 1. Executive Summary

Web traffic accounts for the vast majority of enterprise network communications. Investigating web protocols requires understanding the critical distinction between unencrypted clear-text traffic (**HTTP**) and cryptographically protected traffic (**HTTPS/TLS**).

While Zeek parses full application headers, URIs, and user-agents for clear-text HTTP into **`http.log`**, it cannot read encrypted payload bodies in HTTPS. Instead, Zeek extracts unencrypted handshake metadata, server names, cipher suites, and certificate details into **`ssl.log`**. This technical note explores `http.log` and `ssl.log` field structures, modern encryption visibility challenges (such as Encrypted Client Hello), and practical SOC threat hunting methodologies.

---

## 2. Unencrypted Web Inspection: `http.log`

When traffic travels unencrypted over HTTP (typically TCP port 80), Zeek parses full HTTP request and response structures.

### 2.1 Anatomy of a Zeek HTTP Record

```json
{
  "ts": 1791234000.312,
  "uid": "C9xKz13aR8b3xQ1",
  "id.orig_h": "10.0.2.15",
  "id.orig_p": 54321,
  "id.resp_h": "198.51.100.45",
  "id.resp_p": 80,
  "trans_depth": 1,
  "method": "GET",
  "host": "example.com",
  "uri": "/api/v1/update.php?id=892",
  "version": "1.1",
  "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
  "request_body_len": 0,
  "response_body_len": 1420,
  "status_code": 200,
  "status_msg": "OK",
  "resp_mime_types": ["text/html"]
}
```

### 2.2 Field Breakdown & SOC Value

| Field Name | Technical Definition | SOC Investigation Value |
| :--- | :--- | :--- |
| **`uid`** | Unique 18-character session string. | **Forensic Pivot:** Correlates HTTP requests directly back to `conn.log` and `dns.log`. |
| **`method`** | HTTP request verb (`GET`, `POST`, `PUT`). | `POST` requests with high `request_body_len` suggest potential data staging or exfiltration. |
| **`host`** | HTTP Host header string. | Identifies requested domain name regardless of raw IP destination. |
| **`uri`** | Universal Resource Identifier string. | Exposes full web request path, query parameters, and targeted file names. |
| **`user_agent`** | Client user-agent browser signature. | Flags non-browser script headers (`python-requests`, `curl`, `powershell`, `Go-http-client`). |
| **`status_code`** | Server response status code. | Identifies successful downloads (`200 OK`), redirects (`302`), or blocked access (`403 Forbidden`). |
| **`request_body_len`** | Payload bytes uploaded by client. | High upload volume during `POST` verbs signals data exfiltration. |
| **`response_body_len`** | Payload bytes downloaded by server. | High download volume during `GET` verbs indicates file or payload execution drops. |

---

## 3. Encrypted Web Inspection: `ssl.log`

HTTPS encrypts application-layer headers and payloads using Transport Layer Security (TLS). Passive sensors like Zeek do not decrypt application payloads without a middlebox TLS proxy. Instead, Zeek extracts metadata from the clear-text **TLS Handshake** packets (Client Hello, Server Hello, and Certificate Exchange).

### 3.1 Anatomy of a Zeek TLS Record

```json
{
  "ts": 1791234000.415,
  "uid": "C9xKz13aR8b3xQ1",
  "id.orig_h": "10.0.2.15",
  "id.orig_p": 54322,
  "id.resp_h": "104.20.23.154",
  "id.resp_p": 443,
  "version": "TLSv13",
  "cipher": "TLS_AES_128_GCM_SHA256",
  "server_name": "example.com",
  "established": true,
  "cert_chain_fps": ["a8f9b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3"]
}
```

### 3.2 Field Breakdown & SOC Value

| Field Name | Technical Definition | SOC Investigation Value |
| :--- | :--- | :--- |
| **`uid`** | Unique 18-character session string. | Correlates TLS sessions with `conn.log` and `dns.log`. |
| **`version`** | Negotiated TLS protocol version. | Outdated versions (`TLSv10`, `SSLv3`) identify vulnerable legacy systems or old malware tools. |
| **`cipher`** | Cryptographic suite negotiated. | Evaluates cryptographic strength and identifies weak or non-standard encryption algorithms. |
| **`server_name`** | Server Name Indication (SNI). | Uncovers targeted domain name transmitted in clear text during initial TLS `Client Hello`. |
| **`established`** | Handshake completion status (`true`/`false`). | `false` indicates failed TLS handshakes, expired certificates, or active connection termination. |
| **`cert_chain_fps`** | SHA1/SHA256 SSL cert fingerprints. | Identifies untrusted, self-signed, or known malicious command-and-control (C2) certificates. |

---

## 4. Modern Visibility Challenges: Encrypted Client Hello (ECH)

As perimeter defense evolves, analysts must understand the architectural boundaries of passive monitoring:

1. **Traditional TLS 1.2 / TLS 1.3:** The `SNI` (Server Name Indication) field in the `Client Hello` packet is transmitted in **clear text**, allowing Zeek to populate `server_name` in `ssl.log`.
2. **Encrypted Client Hello (ECH):** ECH encrypts the sensitive portions of the `Client Hello` header—including the SNI. When ECH is enabled between modern endpoints and supporting web edge networks, **Zeek cannot observe the requested domain string in `ssl.log`**.
3. **Analyst Action:** When `server_name` is absent due to ECH or missing SNIs, the analyst must pivot using the connection **`uid`** back to the preceding DNS query in **`dns.log`** or analyze target IP addresses. **Always document the visibility limits of your monitoring sensors!**

---

## 5. Threat Hunting Scenarios

### Scenario A: Script-Based Downloader in `http.log`
* **Observation:** Outbound HTTP request containing `user_agent: "Python-urllib/3.10"` or `user_agent: "curl/7.68.0"` requesting an executable file extension (`/payload.exe`).
* **Interpretation:** Automated script execution or command-line downloader running on a workstation, bypassing standard web browser policies.

### Scenario B: Default C2 Infrastructure in `ssl.log`
* **Observation:** Outbound TLS session to port 443 with `established: true`, where `server_name` is an IP address rather than a domain name, and the SSL certificate is self-signed or untrusted.
* **Interpretation:** High-probability default deployment of offensive framework command-and-control servers (e.g., Cobalt Strike, Metasploit) using unconfigured default certificates.

---

## 6. Key Takeaways

* **Zeek does NOT decrypt HTTPS payload contents natively; it logs handshake metadata in `ssl.log`.**
* **The `uid` field is the universal key linking `http.log` and `ssl.log` back to transport flows in `conn.log`.**
* **Never assume complete network visibility:** Protocol advancements like ECH limit passive SNI logging—correlate across DNS, endpoints, and IP telemetry to confirm findings.
