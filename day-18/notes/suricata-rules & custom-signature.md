# Technical Note: Suricata Rules & Custom Signature Engineering

**Author:** Serah Kathini Mulwa

**Module:** Day 18 - Network Security Monitoring & Intrusion Detection

## 1. Executive Summary

Network Intrusion Detection Systems (NIDS) are only as effective as the rules that power them. While commercial and open-source rulesets (such as Emerging Threats) provide broad coverage against known threats, security engineers must understand how to write, test, and tune custom signatures to detect specific organizational risks or lab anomalies.

This technical guide documents the anatomical structure of a Suricata rule, breaks down individual rule components and protocol buffers, and details our implementation of a custom local rule designed to detect DNS queries targeting `example.com`.

## 2. Anatomy of a Suricata Detection Signature

A standard Suricata rule is divided into two primary sections: **The Rule Header** (which determines what traffic to look at and what action to take) and **The Rule Options** (which define the exact matching criteria inside parentheses).

```
ACTION PROTOCOL SOURCE_IP SOURCE_PORT DIRECTION DESTINATION_IP DESTINATION_PORT ( RULE_OPTIONS )
```

### Deconstructing Our Custom Local Rule:
```
alert dns any any -> any any (msg:"LOCAL LAB DNS query for example.com"; dns.query; content:"example.com"; nocase; sid:1000001; rev:1;)
```

| Component | Value in Rule | Purpose & Explanation |
| :--- | :--- | :--- |
| **Action** | `alert` | Instructs Suricata to generate an alert log entry when the signature matches traffic. |
| **Protocol** | `dns` | Tells the inspection engine to parse the packet stream using the application-layer DNS parser. |
| **Source IP / Port** | `any any` | Matches traffic originating from any IP address across any ephemeral port. |
| **Direction** | `->` | Specifies unidirectional traffic flow from source to destination. |
| **Dest IP / Port** | `any any` | Matches traffic heading toward any destination IP address and port. |
| **Message** | `msg:"..."` | Human-readable string recorded in logs (`fast.log`, `eve.json`) when the rule triggers. |
| **Buffer Keyword** | `dns.query` | A sticky buffer restricting the search exclusively to the requested domain name string. |
| **Content Match** | `content:"example.com"` | The specific string pattern the engine searches for inside the designated buffer. |
| **Modifier** | `nocase` | Makes the content search case-insensitive (catching `Example.com`, `EXAMPLE.COM`, etc.). |
| **Signature ID** | `sid:1000001` | Unique numeric identifier. Local custom rules conventionally start at `1000000`. |
| **Revision** | `rev:1` | Version tracker; incremented whenever the detection logic is updated. |

## 3. Creating and Testing Custom Rules

### Step 1: Write the Rule File
We created a dedicated local rules file inside our project workspace:
```bash
nano rules/local.rules
```
Inside this file, we inserted our custom signature targeting `example.com`.

### Step 2: Validate Syntax (`-T` and `-S` Flags)
Before running Suricata against live traffic or PCAP captures, you must always validate rule syntax to prevent engine crashes in production environments. We ran:
```bash
sudo suricata -T -c /etc/suricata/suricata.yaml -S rules/local.rules
```

* **`-T`**: Runs Suricata in configuration and rule testing mode (syntax check only).
* **`-S rules/local.rules`**: Forces Suricata to load *only* our custom signature file, isolating the test from default rule sets.

**Successful Validation Output:**
```text
i: suricata: This is Suricata version 7.0.10 RELEASE running in SYSTEM mode
i: suricata: Configuration provided was successfully loaded. Exiting.
```

## 4. Common Rule Writing Mistakes to Avoid

1. **Missing Semicolons (`;`):** Every individual option inside the parentheses must end with a semicolon. Forgetting one will throw a syntax error.
2. **Mismatched Parentheses:** Ensure options are fully enclosed within opening `(` and closing `)` brackets.
3. **Invalid SID Ranges:** Always assign unique numbers to your custom signatures to prevent rule collisions.

## 5. Job Market Relevance & SOC Application

* **Detection Engineers:** Continuously write custom signatures in staging environments using `-T` testing flags before pushing them to enterprise sensor fleets to defend against zero-day exploits.
* **SOC Analysts:** Investigate alerts triggered by specific SIDs (such as `sid:1000001`), reviewing rule logic to differentiate between true positive attacks and false positives caused by normal business activity.
