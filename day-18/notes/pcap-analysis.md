# Technical Note: PCAP Analysis & DNS Protocol Dissection

**Author:** Serah Mulwa

**Module:** Day 18 - Network Security Monitoring & Intrusion Detection

## 1. Executive Summary

When a network intrusion detection engine flags suspicious activity, security analysts cannot rely solely on alert summaries. Effective incident triage requires deep packet inspection (DPI) to examine raw protocol headers, transaction states, and payload contents. 

This technical report documents the offline forensic analysis of our custom-captured DNS packet capture (`dns-example.pcap`) using Wireshark. By dissecting transaction IDs, query types, and response codes, we establish a baseline understanding of normal DNS behavior versus anomalous traffic patterns.

---

## 2. Lab Forensic Investigation Findings

Using Wireshark and advanced display filters (such as `dns` and `dns.flags.response == 0`), we interrogated our captured packet file. Below are the definitive answers derived directly from our lab capture:

### 1. How many packets were captured?
* **Finding:** Exactly **8 packets** were recorded in the capture file (`dns-example.pcap`).

### 2. How many DNS requests were present?
* **Finding:** There were **4 outbound DNS requests** present (consisting of two IPv4 `A` record lookups and two IPv6 `AAAA` record lookups for `example.com`, factoring in system retry queries).

### 3. What domain names were queried?
* **Finding:** The sole domain queried across all captured packets was **`example.com`**.

### 4. Which query types were used?
* **Finding:** Two query types were utilized:
  * **Type A (Value 1):** IPv4 address resolution.
  * **Type AAAA (Value 28):** IPv6 address resolution.

### 5. Did the resolver return a response?
* **Finding:** Yes. Every single outbound query was successfully paired with a matching response packet returned by the local resolver (`192.168.100.1`).

### 6. What response code was recorded?
* **Finding:** The response code (Rcode) recorded in all server responses was **`NoError (0)`**, indicating that the queries were successfully processed and valid records were returned.

### 7. Were there any retransmissions or timeouts?
* **Finding:** No retransmissions, dropped packets, or timeouts were observed. All queries resolved cleanly within a rapid timeframe (~5 to 8 milliseconds response latency).

---

## 3. Wireshark Display Filter Reference Guide

During packet analysis, utilizing precise display filters isolates relevant traffic from background noise:

* **View only DNS traffic:**
  ```wireshark
  dns
  ```
* **Isolate unanswered or outbound queries only:**
  ```wireshark
  dns.flags.response == 0
  ```
* **Isolate server responses only:**
  ```wireshark
  dns.flags.response == 1
  ```
* **Filter by specific domain name:**
  ```wireshark
  dns.qry.name == "example.com"
  ```

---

## 4. Job Market Relevance & SOC Application

* **Incident Triage:** When alerts fire for unauthorized domain resolution or suspected DNS tunneling, analysts inspect the DNS payload in Wireshark to verify if subdomains contain encoded data payloads or base64-encrypted text.
* **Transaction Validation:** Inspecting transaction IDs (`TxID`) helps security engineers identify potential cache poisoning or spoofing attempts where unsolicited responses arrive with mismatched identifiers.
