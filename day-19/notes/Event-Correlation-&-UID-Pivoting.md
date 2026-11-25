# Technical Note: Cross-Log Event Correlation & UID Pivoting

**Author:** Serah Mulwa  
**Module:** Day 19 - Network Threat Hunting with Zeek  

---

## 1. Executive Summary

In enterprise Security Operations Centers (SOCs), analyzing network logs in isolation limits an investigator's visibility. While `dns.log` captures application-layer intent (which domain an endpoint tried to reach), `conn.log` records transport-layer execution (how bytes flowed, session duration, and connection states). Connecting these disparate logs into a unified timeline is essential for thorough incident triage and threat hunting.

This technical note documents the execution of **UID Pivoting**—a core forensic technique using Zeek’s 5-tuple Unique Identifier (`uid`) to track an event across multiple protocol logs, transforming isolated observations into actionable forensic evidence.

---

## 2. The Mechanics of Zeek UIDs

Every network connection evaluated by Zeek is assigned a globally unique alphanumeric string called a **Session UID**. This identifier persists across all generated log files for that specific transaction.

* **In `dns.log`:** The `uid` links the requested domain and returned resolution records to the underlying session.
* **In `conn.log`:** The matching `uid` identifies the master 5-tuple connection summary, byte counts, duration, and final state (`SF`, `REJ`, `S0`).
* **In `ssl.log` / `http.log`:** The same `uid` ties encrypted TLS handshakes or unencrypted web request headers to the exact same network flow.

---

## 3. Step-by-Step Investigation Workflow

During our practical lab, we executed a real-world correlation workflow to link a DNS query for `example.com` directly to its transport session in `conn.log`.

### Step 1: Query `dns.log` and Extract the Session UID

Using `jq`, we searched for DNS records matching `example.com` and extracted the associated `uid`:

```bash
jq -r '
select(.query == "example.com") |
.uid
' output/zeek/dns.log | head -1
```

* **Extracted Session UID:** `C1ylQ419432UMYnqn2`

---

### Step 2: Pivot and Search `conn.log`

Using `grep -F`, we searched `conn.log` using the extracted UID string:

```bash
grep -F "C1ylQ419432UMYnqn2" output/zeek/conn.log
```

#### Retreived Matched Connection Record:
```json
{
  "ts": 1793879608.917106,
  "uid": "C1ylQ419432UMYnqn2",
  "id.orig_h": "10.0.2.15",
  "id.orig_p": 42276,
  "id.resp_h": "192.168.100.1",
  "id.resp_p": 53,
  "proto": "udp",
  "service": "dns",
  "duration": 0.045783,
  "orig_bytes": 52,
  "resp_bytes": 100,
  "conn_state": "SF",
  "local_orig": true,
  "local_resp": true,
  "missed_bytes": 0,
  "history": "Dd",
  "orig_pkts": 1,
  "orig_ip_bytes": 80,
  "resp_pkts": 1,
  "resp_ip_bytes": 128,
  "ip_proto": 17
}
```

---

## 4. SOC Investigation Analysis Checklist

By correlating the session across `dns.log` and `conn.log`, we successfully answered all 8 core SOC investigative questions:

| Investigation Question | Telemetry Field Source | Lab Evidence & Finding |
| :--- | :--- | :--- |
| **1. Originating Endpoint** | `conn.log` (`id.orig_h`) | `10.0.2.15` (Internal Parrot OS Workstation) |
| **2. DNS Resolver Involved** | `dns.log` / `conn.log` (`id.resp_h`) | `192.168.100.1` (Local Gateway Resolver) |
| **3. Domain Queried** | `dns.log` (`query`) | `example.com` |
| **4. Record Type Requested** | `dns.log` (`qtype_name`) | `A` (IPv4 Host Address) |
| **5. DNS Response Code** | `dns.log` (`rcode_name`) | `NOERROR` (Query completed successfully) |
| **6. Transport Protocol** | `conn.log` (`proto`) | `udp` (User Datagram Protocol) |
| **7. Destination Port** | `conn.log` (`id.resp_p`) | `53` (Standard DNS Service Port) |
| **8. Final Connection State** | `conn.log` (`conn_state`) | `SF` (Normal, successful completion) |

---

## 5. Key Portfolio & Job Market Takeaways

* **UID Pivoting proves correlation:** Using session UIDs eliminates assumptions when linking application requests to connection metadata.
* **Rapid triage with standard CLI tools:** Combining `jq` filters with `grep -F` allows security analysts to trace malicious sessions in seconds without relying solely on heavy GUI interfaces.
* **Complete evidence building:** Demonstrating how to tie intent (`dns.log`) to execution (`conn.log`) forms the backbone of incident reporting in enterprise SOC environments.
