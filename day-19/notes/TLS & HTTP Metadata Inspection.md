# Technical Note: TLS & HTTP Metadata Inspection with Zeek

**Author:** Serah Mulwa

**Module:** Day 19 - Network Threat Hunting with Zeek

## 1. Executive Summary

With modern network communications heavily encrypted using Transport Layer Security (TLS/HTTPS), defenders can no longer inspect packet payloads directly without performing intrusive SSL decryption. Fortunately, Zeek extracts rich cryptographic metadata from the unencrypted TLS handshake phase, outputting detailed telemetry into `ssl.log`.

This technical note documents the analysis of TLS metadata extracted from controlled HTTPS traffic (`https://example.com`), detailing field parsing with `jq`, cleartext Server Name Indication (SNI) inspection, protocol version evaluation, and the security impacts of emerging standards like Encrypted Client Hello (ECH).

## 2. TLS Handshake Telemetry Extraction

To inspect encrypted sessions recorded in `ssl.log`, we executed a structured `jq` query extracting critical security fields into a TSV summary:

```bash
jq -r '
[
  .server_name // "-",
  .version // "-",
  .cipher // "-",
  .established // false
] | @tsv
' output/zeek/ssl.log
```

### Extracted Field Breakdown:

* **`.server_name`:** Cleartext Server Name Indication (SNI) requested by the client (e.g., `example.com`).
* **`.version`:** Negotiated TLS protocol version (`TLSv1.3` or `TLSv1.2`).
* **`.cipher`:** Cryptographic cipher suite negotiated for session encryption (`TLS_AES_256_GCM_SHA384`).
* **`.established`:** Boolean value (`true`/`false`) confirming whether the 3-way TLS handshake successfully completed.

## 3. The Power & Limitations of SNI Telemetry

### A. What SNI Reveals

During the initial `Client Hello` message of a standard TLS handshake, the client sends the destination hostname in plain text within the Server Name Indication (SNI) extension. This allows Zeek to log the exact domain requested (`example.com`) even though the subsequent HTTP headers and payload are completely encrypted.

### B. The ECH Challenge (Encrypted Client Hello)

As modern privacy standards evolve, **Encrypted Client Hello (ECH)**—an extension to TLS 1.3—encrypts the SNI extension using a public key published in DNS (via `HTTPS` or `SVCB` records).

* **Security Impact:** When ECH is enabled, network sensors like Zeek can no longer extract cleartext domain names from `ssl.log`.
* **Analyst Adaptation:** In ECH environments, analysts must rely even more heavily on `dns.log` correlation, IP reputation, and endpoint telemetry (EDR).

## 4. Protocol Security Evaluation

When analyzing TLS logs across an enterprise network, analysts check for legacy or insecure configurations:

| Protocol Version | Security Status | SOC Action / Recommendation |
| :--- | :--- | :--- |
| **`SSLv2 / SSLv3`** | **CRITICAL / DEPRECATED** | Block immediately; vulnerable to POODLE and DROWN attacks. |
| **`TLSv1.0 / TLSv1.1`** | **DEPRECATED** | Flag for deprecation; lacks modern cipher support (BEAST/POODLE vulnerabilities). |
| **`TLSv1.2`** | **ACCEPTABLE** | Secure when paired with strong AES-GCM or ChaCha20 cipher suites. |
| **`TLSv1.3`** | **OPTIMAL** | Modern security standard; enforces forward secrecy and reduces handshake latency. |

## 5. Key Portfolio Takeaways

* **`ssl.log` enables unencrypted visibility:** SNI logging provides domain visibility without payload decryption.
* **Handshake status (`established`) is vital:** A `false` value in `.established` indicates a failed or intercepted TLS session (potential port scan or certificate validation error).
* **Adapt to encrypted standards:** Understand how privacy innovations like ECH impact network monitoring and compensate by correlating DNS and endpoint telemetry.
