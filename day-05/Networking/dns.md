# DNS (Domain Name System)

## Definition
DNS is the distributed naming system that translates human-readable domain names (e.g., example.com) into machine-readable IP addresses.

## Why DNS Exists
IP addresses are numeric and difficult for humans to memorize. DNS provides a dynamic, scalable directory service that links names to network locations.

## How a Lookup Works
1. Local OS/browser cache check.
2. Query sent to a configured recursive resolver.
3. Resolver queries Root servers, TLD servers (.com), and Authoritative servers.
4. Response returned to the client application.

## Common DNS Record types
- **A:** Maps name to IPv4 address.
- **AAAA:** Maps name to IPv6 address.
- **CNAME:** Creates domain aliases.
- **MX:** Designates mail servers.
- **TXT:** Stores arbitrary text for security and validation policies.

## What DNS Caching Means
Storing previous query results locally or on resolvers to speed up performance and reduce global network traffic overhead.

## Why DNS Matters in Cybersecurity
Essential for investigating phishing, domain reputation, C2 beaconing, and unauthorized data exfiltration (DNS tunneling).

## What a Suspicious DNS Observation Does and Does Not Prove
- **Observation:** A machine queried an unknown external domain at 3:00 AM.
- **Does NOT prove:** Immediate malware infection. It requires contextual investigation of process execution, user activity, and endpoint logs.

## Questions I Still Have
- How do advanced security tools detect high-entropy DGA domains in real-time streaming DNS logs?
