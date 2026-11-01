# Day 5 Technical Vocabulary 

## 1. DNS (Domain Name System)

### Domain Name
* **Definition:** A human-readable text label used to identify a specific entity, server, or resource on the internet instead of relying on IP addresses.
* **Explanation in my own words:** A friendly name or address for a website that humans can easily remember instead of memorizing long strings of numbers.
* **Example:** `example.com` or `google.com`.
* **Security relevance:** Attackers register lookalike domain names (typosquatting/phishing) to trick users into visiting malicious websites that clone legitimate services.

### DNS Resolver
* **Definition:** A recursive server managed by an ISP, enterprise network, or public provider that receives DNS queries from clients and queries root, TLD, and authoritative nameservers to fetch the matching IP address.
* **Explanation in my own words:** The middleman or digital librarian that takes your request for a domain name and goes around asking servers until it finds the exact IP address.
* **Example:** Google Public DNS (`8.8.8.8`) or Cloudflare DNS (`1.1.1.1`).
* **Security relevance:** If an attacker compromises or hijacks a DNS resolver, they can redirect all network traffic to malicious IP addresses (DNS Spoofing).

### DNS Query
* **Definition:** An outbound request sent by a client machine asking a DNS resolver or server to provide record information for a specified domain name.
* **Explanation in my own words:** A computer asking the internet, "What is the IP address for this domain name?"
* **Example:** A workstation sending a UDP packet on port 53 asking for the `A` record of `api.service.com`.
* **Security relevance:** High volumes of unexpected DNS queries can indicate automated malware beaconing, network scanning, or DNS tunneling.

### DNS Response
* **Definition:** The reply packet sent by a DNS server or resolver back to the requesting client containing resource records or error codes.
* **Explanation in my own words:** The answer sent back containing the requested IP address or confirming that the domain does not exist.
* **Example:** A DNS packet answering that `example.com` resolves to `93.184.216.34`.
* **Security relevance:** Monitoring DNS responses allows defenders to spot dynamic DNS lookups or malicious domains returning sinkholed/blacklisted IP addresses.

### DNS Cache
* **Definition:** A temporary local storage space maintained by operating systems, browsers, and resolvers containing recent domain-to-IP mappings.
* **Explanation in my own words:** A local notepad on your device that remembers recent website IP addresses so it doesn't have to ask the internet every single time.
* **Example:** Windows saving `example.com -> 93.184.216.34` in memory after the first lookup.
* **Security relevance:** Attackers can perform DNS Cache Poisoning to insert fraudulent IP mappings into the cache, redirecting users to malicious sites without their knowledge.

### A Record
* **Definition:** Address Record; a fundamental DNS resource record type that maps a domain name directly to a 32-bit IPv4 address.
* **Explanation in my own words:** A record that points a domain name to a standard IPv4 address.
* **Example:** `example.com IN A 93.184.216.34`.
* **Security relevance:** SOC analysts verify A records against threat intelligence feeds to see if domains point to known malicious infrastructure or dynamic bulletproof hosting servers.

### AAAA Record
* **Definition:** Quad-A Record; a DNS resource record type that maps a domain name to a 128-bit IPv6 address.
* **Explanation in my own words:** A record that points a domain name to a modern, longer IPv6 address.
* **Example:** `example.com IN AAAA 2606:2800:220:1:248:1893:25c8:1946`.
* **Security relevance:** Security monitoring systems must audit both A and AAAA records to ensure malware does not bypass IPv4-only monitoring filters by communicating over IPv6.

### CNAME
* **Definition:** Canonical Name Record; a DNS record type that aliases one domain name to another domain name rather than pointing to an explicit IP address.
* **Explanation in my own words:** A nickname or alias that forwards one domain name to another primary domain name.
* **Example:** `www.example.com CNAME host.example-cdn.net`.
* **Security relevance:** Misconfigured CNAME records pointing to decommissioned third-party cloud resources can lead to Subdomain Takeover attacks.

### MX
* **Definition:** Mail Exchanger Record; a DNS resource record specifying the mail server responsible for accepting email on behalf of a domain.
* **Explanation in my own words:** A signpost telling the internet which server handles incoming emails for a specific domain.
* **Example:** `example.com IN MX 10 mail.example.com`.
* **Security relevance:** Verification of MX records alongside SPF, DKIM, and DMARC policies prevents email spoofing, spam distribution, and phishing attacks.

### NS
* **Definition:** Name Server Record; a DNS record indicating which authoritative name servers hold the master DNS records for a domain.
* **Explanation in my own words:** A record stating which servers are the official source of truth for a domain's settings.
* **Example:** `example.com IN NS ns1.dns-provider.com`.
* **Security relevance:** Unauthorized changes to NS records signify domain hijacking, granting an attacker full administrative control over all traffic for that domain.

### TXT
* **Definition:** Text Record; a versatile DNS record used to store arbitrary human and machine-readable text strings attached to a domain.
* **Explanation in my own words:** A notes field in DNS used for domain verification, security policies, or metadata.
* **Example:** `v=spf1 include:_spf.google.com ~all`.
* **Security relevance:** TXT records house key email authentication frameworks (SPF, DMARC) but can also be abused by threat actors for C2 data staging and DNS Tunneling payloads.

---

## 2. Web

### HTTP
* **Definition:** Hypertext Transfer Protocol; an application-layer protocol used to transfer unencrypted hypermedia documents (such as HTML web pages) across the web over TCP port 80.
* **Explanation in my own words:** The standard language browsers and web servers use to exchange web pages, sent completely in plain text without encryption.
* **Example:** Accessing `http://example.com` on TCP port 80.
* **Security relevance:** Plaintext HTTP traffic is vulnerable to Man-in-the-Middle (MitM) eavesdropping, credential sniffing, and packet tampering.

### HTTPS
* **Definition:** Hypertext Transfer Protocol Secure; the encrypted extension of HTTP that utilizes TLS/SSL encryption over TCP port 443 to secure communication between client and server.
* **Explanation in my own words:** The secure version of HTTP that scrambles web traffic so no one on the network can snoop on your passwords or data.
* **Example:** Navigating to `https://secure.bank.com` on TCP port 443.
* **Security relevance:** HTTPS protects user privacy and integrity, but encrypted traffic also limits network analysts' visibility, requiring SSL inspection or endpoint telemetry to detect hidden malware payloads.

### TLS
* **Definition:** Transport Layer Security; a cryptographic protocol designed to provide privacy, data integrity, and mutual authentication between two communicating computer applications over a network.
* **Explanation in my own words:** The modern security lock and encryption engine working behind HTTPS to secure internet connections.
* **Example:** TLS 1.3 performing a cryptographic handshake before sending encrypted web data.
* **Security relevance:** Outdated versions (SSL v2/v3, TLS 1.0/1.1) contain severe cryptographic flaws (e.g., POODLE, BEAST) and must be disabled across all enterprise endpoints and servers.

### Request
* **Definition:** A client-initiated message sent to a web server requesting a specific action, resource, or data payload.
* **Explanation in my own words:** A message from your browser asking a server to show a page or submit data.
* **Example:** A `GET /login.html HTTP/1.1` request sent to a web server.
* **Security relevance:** Analyzing HTTP requests allows defenders to detect web attacks such as SQL Injection (SQLi), Cross-Site Scripting (XSS), and directory traversal attempts.

### Response
* **Definition:** The server-generated reply returned to a client following an HTTP request, containing a status code, response headers, and requested content payload.
* **Explanation in my own words:** The answer sent back by a website server containing the page code or an error message.
* **Example:** An HTTP reply starting with `HTTP/1.1 200 OK` followed by HTML code.
* **Security relevance:** Server responses can reveal sensitive information leakage, such as server software versions (`Server: Apache/2.4.41`), helping attackers tailor exploits.

### Header
* **Definition:** Key-value pairs included in HTTP requests and responses that convey metadata, configuration options, session tokens, and security rules.
* **Explanation in my own words:** Meta-information attached to the top of an HTTP message giving context about the browser, server, session, or security policies.
* **Example:** `User-Agent: Mozilla/5.0` or `Content-Type: application/json`.
* **Security relevance:** Security headers (like `Content-Security-Policy` and `Strict-Transport-Security`) harden web applications against clickjacking, XSS, and downgrade attacks.

### Status Code
* **Definition:** A 3-digit numerical code returned by a server indicating the outcome of an HTTP request.
* **Explanation in my own words:** A standard 3-digit report card number showing whether a web request succeeded or failed.
* **Example:** `200` (Success), `404` (Not Found), `500` (Server Error), or `403` (Forbidden).
* **Security relevance:** A spike in `404` errors indicates automated web directory brute-forcing (e.g., Gobuster/FFUF), while `401/403` spikes suggest credential stuffing.

### Client
* **Definition:** An application or endpoint device (such as a web browser or API script) that initiates requests to a remote server.
* **Explanation in my own words:** The program or device asking for data or services from a central server.
* **Example:** Google Chrome browser or a Python `requests` script running on a user workstation.
* **Security relevance:** Compromised clients can be leveraged as footholds within an internal network to perform lateral movement or internal port scanning.

### Server
* **Definition:** A computer system or software application that listens for incoming network requests and serves data, applications, or services to clients.
* **Explanation in my own words:** A central, high-capacity computer that hosts applications, websites, or databases and delivers them when asked.
* **Example:** Nginx or IIS hosting a corporate portal.
* **Security relevance:** Unpatched servers exposed directly to the public internet are high-value targets for remote code execution (RCE) and ransomware attacks.

### Certificate
* **Definition:** An electronic document (X.509 standard) issued by a Certificate Authority (CA) that binds a public key to an identity (domain name) to enable TLS encryption.
* **Explanation in my own words:** A digital ID card for a website that proves its identity and enables secure, encrypted connections.
* **Example:** A certificate issued by Let's Encrypt validating `https://example.com`.
* **Security relevance:** Expired, self-signed, or untrusted certificates trigger browser security warnings; compromised private keys allow attackers to intercept and decrypt secure sessions.

---

## 3. Networking

### Socket
* **Definition:** An internal software endpoint created by the operating system kernel, defined by a combination of an IP address and a port number.
* **Explanation in my own words:** A specific digital doorway on a computer created by binding an IP address together with a port number.
* **Example:** `192.0.2.10:443`.
* **Security relevance:** Active network sockets are monitored using commands like `ss` or `netstat` to detect suspicious or unauthorized network connections.

### Listening Socket
* **Definition:** A socket configured by a service to passively wait for incoming connection requests from remote clients.
* **Explanation in my own words:** An open digital door on a server sitting quietly and waiting for outside computers to connect to it.
* **Example:** An SSH daemon listening for connections on `0.0.0.0:22`.
* **Security relevance:** Unnecessary listening sockets expand an organization's attack surface and must be audited and closed if unneeded.

### Source Address
* **Definition:** The IP address of the originating machine that created and transmitted a network packet.
* **Explanation in my own words:** The return address printed on a network packet showing who sent it.
* **Example:** `192.0.2.10`.
* **Security relevance:** Source addresses can be spoofed in UDP-based denial-of-service (DoS) attacks to disguise the true source of an attack.

### Destination Address
* **Definition:** The target IP address specifying the intended recipient machine of a network packet.
* **Explanation in my own words:** The receiving address printed on a network packet showing where it is going.
* **Example:** `198.51.100.20`.
* **Security relevance:** Tracking destination addresses helps SOC analysts flag host connections to known malicious Command & Control (C2) servers or unauthorized external targets.

### Source Port
* **Definition:** An ephemeral port number (typically between 49152 and 65535) dynamically assigned by the client OS to identify the local socket sending data.
* **Explanation in my own words:** A temporary random port assigned by your computer so it knows which specific app should receive the reply data.
* **Example:** Port `54321` dynamically chosen by a web browser to initiate a request.
* **Security relevance:** High source port randomness helps prevent TCP sequence prediction and session hijacking attacks.

### Destination Port
* **Definition:** The port number assigned on the target server to direct incoming traffic to a specific service or application.
* **Explanation in my own words:** The specific target port number on a server indicating which service (e.g., web, SSH, mail) you want to talk to.
* **Example:** Port `22` for SSH or Port `443` for HTTPS.
* **Security relevance:** Network firewalls rely on destination ports to restrict unauthorized traffic and enforce strict access control policies.

### TCP
* **Definition:** Transmission Control Protocol; a connection-oriented, reliable transport-layer protocol that guarantees ordered, error-checked packet delivery via a 3-way handshake.
* **Explanation in my own words:** A careful, reliable way to send data over the network that checks if every single piece arrived safely and in order.
* **Example:** Loading a website or transferring a file where missing data cannot be tolerated.
* **Security relevance:** Attackers abuse TCP mechanisms to conduct SYN flood denial-of-service attacks or perform port scans to map open services.

### UDP
* **Definition:** User Datagram Protocol; a connectionless, lightweight transport-layer protocol that prioritizes speed and low overhead without guaranteeing delivery or packet ordering.
* **Explanation in my own words:** A fast, direct way to send network data without checking if every packet arrived, making it great for real-time traffic.
* **Example:** Video streaming, online gaming, or DNS lookups.
* **Security relevance:** Because UDP lacks connection handshakes, it is heavily exploited for IP spoofing and amplification reflection DDoS attacks.

### Packet Capture
* **Definition:** The process of intercepting, recording, and analyzing raw data frames traversing a network interface using specialized software or hardware.
* **Explanation in my own words:** Taking a complete recording of all the digital traffic passing through a network card for deep analysis.
* **Example:** Capturing network traffic using Wireshark or `tcpdump` into a `.pcap` file.
* **Security relevance:** Packet captures provide incontrovertible deep-packet inspection evidence during incident response and threat hunting investigations.

### Display Filter
* **Definition:** A logical rule applied inside packet analysis software (like Wireshark) to reduce visible network frames to only those matching specific criteria.
* **Explanation in my own words:** A search filter used in Wireshark to hide irrelevant network traffic and focus only on specific ports, IPs, or protocols.
* **Example:** Typing `dns` or `ip.addr == 192.0.2.10` in Wireshark.
* **Security relevance:** Display filters allow analysts to rapidly filter out background noise (like routine broadcast packets) and isolate suspicious events during live investigations.

---

## 4. Investigation

### Observation
* **Definition:** A direct, empirical fact explicitly present in telemetry, logs, or evidence without any personal interpretation or assumption added.
* **Explanation in my own words:** Pure, unvarnished facts pulled straight from logs that cannot be argued against.
* **Example:** "The dataset shows 5 TCP connection events to port 443."
* **Security relevance:** Keeping observations strictly factual prevents analysts from contaminating incident timelines with unfounded guesses.

### Interpretation
* **Definition:** An analytical hypothesis that explains what a direct observation likely means based on technical standards, context, and domain experience.
* **Explanation in my own words:** Educated reasoning explaining what the observed facts might indicate.
* **Example:** "Traffic on port 443 suggests possible HTTPS web browsing."
* **Security relevance:** Interpretations help direct the next investigative steps, but analysts must remember that an interpretation is a testable hypothesis, not proven fact.

### Evidence
* **Definition:** Verified, documented data (such as log files, packet captures, and disk images) collected in a legally sound manner to support analytical findings.
* **Explanation in my own words:** The concrete proof and recorded data that supports your investigation findings.
* **Example:** A timestamped JSON log record or a `.pcap` file verifying network connectivity.
* **Security relevance:** Proper chain of custody and data integrity management ensure evidence remains admissible during legal or disciplinary proceedings.

### Hypothesis
* **Definition:** A proposed, testable explanation for a set of observations used as a starting point for further technical investigation.
* **Explanation in my own words:** A working theory about what might have happened that you still need to prove or disprove with more data.
* **Example:** "The host is communicating on port 8080 due to an unconfigured proxy client."
* **Security relevance:** Formulating rival hypotheses prevents confirmation bias during complex incident response investigations.

### Conclusion
* **Definition:** A final operational determination that is strictly bounded and supported by verified evidence.
* **Explanation in my own words:** The final verdict of an investigation based strictly
