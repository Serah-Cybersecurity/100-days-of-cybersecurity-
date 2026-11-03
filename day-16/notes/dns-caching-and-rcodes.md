# Day 16 - DNS Caching, TTL, and Response Codes (RCODEs)

## 1. DNS Caching: Why the Internet Doesn't Grind to a Halt

Every single time you open a web page, check your email, or connect to an API, your computer relies on DNS. If every client had to query root and authoritative servers across the global internet for every single connection, the infrastructure would collapse instantly.

This is where **DNS caching** comes in. 

* **What it is:** Caching is the temporary storage of DNS lookup results by operating systems, local routers, and recursive resolvers. 

* **Why it matters:** Once a resolver learns that `example.com` points to `93.184.216.34`, it stores that answer in memory. The next time a user requests the same domain, the resolver serves the answer instantly without hitting external servers.

* **Security relevance:** While caching speeds things up, attackers also work around it. For instance, if malware needs to rotate command-and-control (C2) servers rapidly to avoid IP blocks, it will use extremely short cache durations.

## 2. What Is TTL (Time-to-Live)?

Attached to every DNS record is a value called the **TTL (Time-to-Live)**, measured in **seconds**. 

```text
example.com.   300   IN   A   192.0.2.10
```

In this example, `300` means **300 seconds (5 minutes)**. This tells any resolver caching this record: *"You are allowed to keep this answer in memory for five minutes. After that, you must throw it away and perform a fresh lookup."*

### 2.1 Why TTL Matters for Troubleshooting & Investigations
* **Website Migrations:** Have you ever migrated a website to a new server IP, only to find that some users can reach it while others are stuck on the old page? That is a **TTL propagation delay**. Different resolvers across the globe are still holding onto cached records until their timers expire.
* **Fast Flux Networks:** When investigating malicious infrastructure, watch out for abnormally low TTLs (e.g., 5 or 10 seconds). Attackers use ultra-short TTLs to constantly swap out the IP addresses behind a malicious domain, making it difficult for defenders to block them.

### 2.2 Negative Caching
DNS doesn't just cache successful lookups—it also caches failures. If an endpoint queries a domain that doesn't exist, the resolver caches that negative result (`NXDOMAIN`) for a set period. This prevents clients from spamming the global DNS root servers with endless requests for misspelled URLs.

## 3. Mastering DNS Response Codes (RCODEs)

When you examine DNS packet captures in Wireshark or review SIEM query logs, you need to look beyond whether a packet arrived and check its **RCODE (Response Code)**. 

| Response Code | What It Means | Operational & Security Significance |
| :--- | :--- | :--- |
| **NOERROR** | Query completed successfully without errors. | The server processed the request fine. *(Note: This does not guarantee the record was found!)* |
| **NXDOMAIN** | Non-Existent Domain (Name Error). | The domain queried does not exist in the authoritative zone. **High threat relevance:** A sudden spike in unique `NXDOMAIN` responses from an endpoint often indicates malware running a Domain Generation Algorithm (DGA) to find an active C2 server. |
| **SERVFAIL** | Server Failed to Complete the Query. | The upstream recursive resolver ran into an internal error or failed to reach authoritative servers. |
| **REFUSED** | Server Refused the Request. | The DNS server blocked the query due to access control lists (ACLs) or security policy restrictions. |
| **TIMEOUT** | No usable response arrived within the expected window. | Indicates network connectivity loss, heavy packet drop, or a firewall blocking port 53. |

## 4. The Analyst Trap: `NOERROR` vs. `NODATA`

A classic beginner mistake is assuming that an `NOERROR` response means you successfully received the record you asked for.

* **The Reality:** A response can return an `NOERROR` RCODE (meaning *"I understood your request and the domain exists"*), but the **Answer section** can be completely empty. 
* This is known as a **NODATA** response. For example, if you query an `AAAA` (IPv6) record for a domain that only has an IPv4 `A` record, the server replies with `NOERROR` because the domain is real, but it returns zero answers for IPv6.

As an analyst, always inspect the internal packet sections (Answer, Authority, Additional) rather than relying solely on the top-level RCODE!
