# Day 15 - DNS and HTTP/HTTPS Application-Layer Analysis

## Overview

Application-layer protocols (Layer 7) such as DNS, HTTP, and HTTPS provide the behavioral telemetry that SOC analysts rely on most during security investigations. While transport protocols establish connectivity, application protocols reveal what users and applications are actually requesting and transmitting across the network.

---

## 1. Core Topic Three: Domain Name System (DNS) Analysis

### 1.1 What is DNS?
The Domain Name System translates human-readable domain names (e.g., `example.com`) into machine-routable IP addresses (e.g., `93.184.216.34`). Before a TCP handshake or HTTP request can occur, operating systems must resolve the target hostname via DNS.

### 1.2 DNS Transaction Mechanics
* **Transport Protocol:** Typically operates over **UDP Port 53** (falling back to TCP Port 53 for zone transfers or oversized responses).
* **Key Record Types:**
  * **A:** Maps a domain name to an IPv4 address.
  * **AAAA:** Maps a domain name to an IPv6 address.
  * **CNAME:** Canonical Name alias pointing one domain to another.
  * **MX:** Mail Exchange records for email routing.
  * **TXT:** Text records (often abused for DNS tunneling and command delivery).
  * **PTR:** Pointer records for reverse DNS IP lookups.

### 1.3 Important DNS Fields in Wireshark
* **Transaction ID (TxID):** Matches queries to corresponding responses.
* **Flags:** Indicates query vs. response state, recursion desired, and authoritativeness.
* **Response Code (RCODE):** 
  * `NOERROR`: Successful resolution.
  * `NXDOMAIN`: Non-Existent Domain (queried domain does not exist).
  * `SERVFAIL`: Server failed to process request.

### 1.4 Security Interpretation & Context
* **Suspicious Indicator:** High volumes of failed `NXDOMAIN` lookups or randomized subdomains (indicative of Domain Generation Algorithms / DGAs or malware C2 beaconing).
* **Legitimate Explanations:** Mistyped URLs, local network outages, or CDN health checks. Always correlate with client process activity.

---

## 2. Core Topic Four: HTTP and HTTPS Analysis

### 2.1 Hypertext Transfer Protocol (HTTP)
HTTP is an unencrypted Layer 7 protocol used for web communications. In PCAP files, analysts can inspect request headers, methods, URIs, and response bodies in plaintext.

* **Common Request Methods:** `GET` (retrieve resource), `POST` (submit data), `PUT` (update resource), `HEAD` (headers only).
* **Status Codes:**
  * `2xx (Success):` `200 OK`
  * `3xx (Redirection):` `301 Moved Permanently`, `302 Found`
  * `4xx (Client Error):` `403 Forbidden`, `404 Not Found`
  * `5xx (Server Error):` `500 Internal Server Error`, `503 Service Unavailable`

### 2.2 HTTP Redirects
Redirect status codes (`301`/`302`) instruct clients to automatically navigate to alternative URLs. Tracing redirect chains helps analysts map out phishing infrastructure or web application routing.

### 2.3 HTTPS and Transport Layer Security (TLS)
HTTPS secures HTTP traffic using TLS, encrypting all application-layer payloads.

* **What is Hidden:** URIs, POST parameters, cookies, and page content.
* **What Remains Visible (Metadata):**
  * Source and destination IP addresses and ports.
  * TCP connection handshakes, packet sizes, and flow timing.
  * **TLS SNI (Server Name Indication):** The cleartext domain name requested by the client during the initial TLS handshake negotiation.
