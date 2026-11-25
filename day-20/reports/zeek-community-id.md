# Technical Note: Enabling Community ID Flow Hashing in Zeek

**Author:** Serah Mulwa   
**Module:** Day 20 - Integrated Network Threat Hunting & Detection Engineering  

---

## 1. Executive Summary

Zeek provides deep protocol analysis and behavioral network metadata, but by default, it indexes sessions using internal `uid` strings unique to Zeek. To correlate Zeek's structured logs (`conn.log`, `dns.log`, `ssl.log`) directly with signature alerts from Suricata, Zeek must be instructed to output standardized **Community ID** flow hashes.

This technical note documents the implementation, seed configuration, and syntax compilation testing for Zeek's Community ID policy module on Day 20.

---

## 2. The Zeek Community ID Policy Module

Zeek includes a built-in policy script specifically designed for generating standardized flow hashes:

```zeek
policy/protocols/conn/community-id-logging
```

When loaded, this policy extends Zeek’s core `conn.log` schema by appending a `community_id` field to every connection record.

---

## 3. Policy Script Implementation (`scripts/community_id.zeek`)

To enable hash generation and maintain mathematical parity with Suricata, a custom configuration script was created at `scripts/community_id.zeek`:

```zeek
@load policy/protocols/conn/community-id-logging

redef CommunityID::seed = 0;
```

### Script Logic Breakdown:

1. **`@load policy/protocols/conn/community-id-logging`**: Loads the native Zeek script module responsible for calculating SHA-1 flow hashes across 5-tuple connection states.
2. **`redef CommunityID::seed = 0;`**: Overrides the default seed variable to explicitly use `0`. 

> **Critical Seed Parity Rule:** Because Suricata was configured with `community-id-seed: 0`, Zeek must use seed `0`. If seeds differ between tools, identical network streams will generate completely different hash strings, breaking cross-tool correlation.

---

## 4. Verification and Compilation Testing

Before parsing packet captures, the environment paths and script syntax were validated using Zeek's command-line interface within `~/cybersecurity-journey/day-20`:

### Step 1: Check Zeek Installation Prefix
```bash
zeek-config --prefix
```
* **Output:** `/opt/zeek`

### Step 2: Validate Script Compilation
```bash
zeek -b scripts/community_id.zeek
```
* **Verification Result:** The command executed and returned silently to the prompt with zero error messages, confirming successful syntax compilation and policy resolution.

---

## 5. Portfolio Evidence & Screenshot Mapping

* **`zeek-community-id-script-validation.png`**: Validates project path resolution, Zeek installation prefix (`/opt/zeek`), and silent compilation of `scripts/community_id.zeek`.

---

## 6. Key Portfolio Takeaways

* Enabling Community ID in Zeek requires explicitly loading the `community-id-logging` policy script.
* Seed alignment (`seed = 0`) across both Suricata and Zeek is mandatory for deterministic cross-tool hash matching.
* Testing scripts using `zeek -b` ensures policy syntax is valid before processing live or PCAP network streams.
