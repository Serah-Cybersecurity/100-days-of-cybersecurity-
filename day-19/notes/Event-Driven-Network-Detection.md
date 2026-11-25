# Technical Note: Event-Driven Network Detection with Custom Zeek Scripts

**Author:** Serah Mulwa

**Module:** Day 19 - Network Threat Hunting with Zeek

## 1. Executive Summary

Standard Network Security Monitoring (NSM) tools generate default logs containing pre-defined fields. However, advanced Detection Engineers and SOC Analysts often need to write custom rules to hook directly into packet parsing streams, compute real-time metrics, enforce local compliance policies, or detect non-standard threat vectors.

This technical note documents the creation, dissection, and execution of our first custom Zeek event script (**`watch_dns.zeek`**). It highlights the fundamental shift from static log analysis (`jq`) to real-time, event-driven network programming.

## 2. Event-Driven Architecture vs. Sequential Scripting

Unlike traditional scripting languages (such as Python or Bash) that execute instructions sequentially from top to bottom, Zeek is an **event-driven** domain-specific language.

* **The Event Engine:** As Zeek processes raw network packets, its internal protocol analyzers generate granular asynchronous **events** (e.g., `new_connection`, `dns_request`, `http_header`, `ssl_established`).

* **Event Handlers:** A `.zeek` script defines functions called event handlers. When Zeek's Event Engine encounters a matching packet event, it passes protocol parameters into the script's event block and executes the logic.

## 3. Script Source Code: `scripts/watch_dns.zeek`

Below is the complete source code of our custom DNS monitoring script:

```zeek
event dns_request(
    c: connection,
    msg: dns_msg,
    query: string,
    qtype: count,
    qclass: count
)
{
    if (query == "example.com")
    {
        print fmt(
            "LAB DNS QUERY: originator=%s resolver=%s query=%s qtype=%d",
            c$id$orig_h,
            c$id$resp_h,
            query,
            qtype
        );
    }
}
```

## 4. In-Depth Code Breakdown

| Code Component | Type / Structure | Forensic Function & Purpose |
| ----- | ----- | ----- |
| **`event dns_request(...)`** | Event Hook | Registers a listener for DNS query packet events emitted by Zeek's DNS protocol analyzer. |
| **`c: connection`** | Record Structure | Object holding 5-tuple connection metadata. Fields are accessed via the `$` operator (`c$id$orig_h` for source IP, `c$id$resp_h` for resolver IP). |
| **`msg: dns_msg`** | Record Structure | Low-level DNS message header attributes (transaction ID, flags, recursion flags). |
| **`query: string`** | String Variable | The exact hostname string requested by the client (e.g., `"example.com"`). |
| **`qtype: count`** | Unsigned Integer | Numeric DNS query record type (`1` = `A` record for IPv4, `28` = `AAAA` record for IPv6). |
| **`if (query == "example.com")`** | Conditional Match | Filters event triggers to execute printer logic only when the domain string matches our lab target. |
| **`print fmt(...)`** | Formatting Function | Formats output using C-style specifiers (`%s` for strings/IPs, `%d` for integers) and prints directly to standard output (`stdout`). |

## 5. Lab Execution & Results

From our custom output directory (`output/custom/`), we executed Zeek against our captured PCAP (`day19.pcap`), passing the custom script path as an additional argument:

```bash
zeek -C -r ../../pcap/day19.pcap LogAscii::use_json=T ../../scripts/watch_dns.zeek
```

### Verified Terminal Output:

```text
LAB DNS QUERY: originator=10.0.2.15 resolver=192.168.100.1 query=example.com qtype=1
LAB DNS QUERY: originator=10.0.2.15 resolver=192.168.100.1 query=example.com qtype=28
LAB DNS QUERY: originator=10.0.2.15 resolver=192.168.100.1 query=example.com qtype=1
LAB DNS QUERY: originator=10.0.2.15 resolver=192.168.100.1 query=example.com qtype=28
```

* **Observation:** The script printed four distinct log entries, accurately capturing both IPv4 (`qtype=1`) and IPv6 (`qtype=28`) DNS queries originated by host `10.0.2.15` to gateway resolver `192.168.100.1`.

## 6. Key Portfolio Takeaways

* **Event handlers enable real-time detection:** Writing custom event handlers allows defenders to inspect network telemetry in memory before or alongside log generation.

* **Record members use `$` notation:** Accessing nested fields within Zeek data structures requires the dollar sign operator (e.g., `c$id$orig_h`).

* **Debugging prints vs. SIEM Alerts:** Terminal `print` statements serve as an ideal educational debugging tool. In enterprise environments, production Zeek scripts hook into the `Notice` framework (`Notice::populate`) to dispatch SIEM alerts.
