# Day 16 - DNS Security Fundamentals & Architecture

## 1. Why DNS Matters in Cybersecurity

### 1.1 What Is DNS?
The Domain Name System (DNS) is the distributed, hierarchical naming database that translates human-readable domain names (such as `example.com`) into machine-routable IP addresses (such as `93.184.216.34`). 

Without DNS, users would have to memorize raw numeric IP addresses for every resource on the internet.

### 1.2 Why Should a SOC Analyst Understand DNS?
When an endpoint in an organization makes repeated DNS requests to unfamiliar domains, it could indicate several activities:
* A legitimate application communicating with backend services.
* A software update check or external resource loading.
* Misconfigured network applications.
* **Malicious activity:** Malware attempting external command-and-control (C2) communication or data exfiltration.

For a Security Operations Center (SOC) analyst, DNS telemetry answers critical investigative questions:
* Which endpoint initiated the request?
* What exact domain name or subdomain was queried?
* Which recursive resolver received the query?
* What resource record type was requested (`A`, `TXT`, `MX`, etc.)?
* Did the resolver return a successful answer (`NOERROR`) or an error (`NXDOMAIN`)?
* Is the request frequency and destination domain normal for this host?

## 2. The DNS Architecture & Hierarchy

### 2.1 The DNS Hierarchy
Domain names are constructed from hierarchical labels separated by periods (dots), parsed from right to left:

| Component | Example | Meaning |
| :--- | :--- | :--- |
| **Root** | `.` | Top of the global DNS namespace |
| **TLD (Top-Level Domain)** | `.com` | Category or country code extension |
| **Second-Level Domain** | `example` | The unique name registered under the TLD |
| **Subdomain** | `www` | Specific host or service designation |
| **FQDN (Fully Qualified Domain Name)** | `www.example.com` | The complete, absolute domain name |

### 2.2 The Four Important DNS Server Roles

1. **Stub Resolver:** The client-side operating system or application component that initiates the DNS request.
2. **Recursive Resolver:** An intermediary server (e.g., ISP resolver, Cloudflare `1.1.1.1`, Google `8.8.8.8`) that accepts queries from stub resolvers, checks its cache, and performs iterative lookups on behalf of the client.
3. **Root DNS Server:** Sits at the top of the global namespace, directing recursive resolvers to the appropriate Top-Level Domain (TLD) servers.
4. **Authoritative DNS Server:** The definitive source of truth that holds the actual zone records (`A`, `AAAA`, `TXT`, `MX`) for a specific domain.

### 2.3 How a DNS Lookup Works (Step-by-Step)

```
          YOUR COMPUTER (Stub Resolver)
                │
                v
         RECURSIVE RESOLVER
                │
                │ (Cache miss)
                v
            ROOT DNS (.)
                │
                v
             TLD DNS (.com)
                │
                v
         AUTHORITATIVE DNS (example.com)
                │
                v
         RECORD / ANSWER RETURNED
```

1. **Application Request:** An application or browser requests domain resolution from the operating system.
2. **Cache Check:** The operating system checks its local cache and hosts file.
3. **Stub to Recursive:** If uncached, the stub resolver sends a query to the configured recursive resolver.
4. **Recursive Cache Check:** The recursive resolver checks its internal cache.
5. **Root Referral (Cache Miss):** If uncached, the recursive resolver queries a Root DNS server, receiving a referral to the TLD server.
6. **TLD Referral:** The resolver queries the TLD server (e.g., `.com`), receiving a referral to the authoritative nameserver.
7. **Authoritative Answer:** The resolver queries the authoritative server, which returns the exact IP record.
8. **Caching & Client Response:** The resolver caches the record according to its TTL and returns the IP address to the client.
