# Day 13 - Security Monitoring Investigation

## 1. Case information

- **Case ID:** DAY13-SIEM-001
- **Environment:** Synthetic multi-source lab (`events.jsonl`)
- **Investigation type:** Defensive event correlation and log analysis

## 2. Objective

To analyze synthetic multi-source security telemetry, evaluate structured log normalization, test custom Python correlation scripts against a brute-force pattern, and document defensive investigation findings according to standard security operations frameworks.

## 3. Scope

The investigation evaluated an 11-record synthetic event dataset comprising:
- Windows Security authentication and event logs (`WIN-LAB-01`)
- Network firewall logs (`FW-LAB-01`)
- Linux SSH syslog records (`LINUX-LAB-01`)
- Windows System service logs

## 4. Methodology

Events were ingested via a custom Python parsing engine (`mini_siem.py`), validated against a strict schema dictionary, normalized to UTC timestamps, verified for IP syntax via Python's native `ipaddress` library, and evaluated against a temporal sliding-window correlation rule ($\ge 3$ failures followed by a success within 10 minutes).

## 5. Findings

### Finding 1: Authentication activity
- **Observation:** Three consecutive failed Windows logon attempts (Event ID `4625`) were recorded for user `analyst` originating from source IP `198.51.100.27` between 08:00 and 08:02, followed immediately by a successful logon (Event ID `4624`) at 08:04.
- **Interpretation:** This sequence matches the configured heuristic for a brute-force password spraying or guessing attempt culminating in a successful account breach.
- **Limitations:** A threshold match highlights a candidate for review; it does not definitively confirm unauthorized compromise without endpoint behavioral verification.

### Finding 2: Network event
- **Observation:** A firewall denial (`FW_DENY`) was logged at 08:03 from source IP `198.51.100.27` targeting destination port `443`.
- **Interpretation:** Demonstrates multi-source activity from the attacking IP address, showing interaction with network perimeter defenses prior to successful authentication.
- **Limitations:** Proximity in time and shared IP do not automatically prove a direct causal relationship between the network denial and the subsequent Windows logon success.

### Finding 3: Privilege-related activity
- **Observation:** A Windows privilege assignment event (Event ID `4672`) and process creation event (Event ID `4688`, `notepad.exe`) were recorded for user `analyst` at 08:10 and 08:05 respectively.
- **Interpretation:** Indicates post-logon activity and special privileges assigned to the session.
- **Limitations:** Routine administrative actions or user startup tasks can trigger identical process creation events; additional endpoint telemetry is required to rule out malicious execution.

### Finding 4: Linux authentication
- **Observation:** SSH authentication logs for host `LINUX-LAB-01` showed a single failed SSH attempt (`SSH_FAIL`) followed by a successful login (`SSH_SUCCESS`) from IP `192.0.2.44`.
- **Interpretation:** Compares against baseline activity; because it recorded only one failure, it failed to meet the three-failure threshold and represents isolated activity.

## 6. Detection logic

- **Threshold:** $\ge 3$ failed authentication attempts.
- **Time Window:** 10-minute rolling sliding window (`window_minutes=10`).
- **Condition:** Preceding failures followed by a successful authentication for the same `username` and `src_ip`.

## 7. Testing

The Python correlation engine was validated across a 7-step test suite, confirming version compatibility, compilation integrity, standard dataset processing (`11` valid records, `1` review candidate), threshold adjustments (`--threshold 4`), time-window tuning (`--window-minutes 2`), missing file error handling (Exit Code `2`), and malformed JSON resilience.

## 8. Overall assessment

The evidence supports the detection of a synthetic authentication anomaly matching a brute-force-followed-by-success signature. However, contextual events require careful human triage rather than automated incident declaration.

## 9. Recommended next steps

In a real authorized investigation, analysts should:
1. Interview the user (`analyst`) to verify if they experienced typing errors or initiated the session.
2. Review endpoint process trees around 08:04 to check for anomalous parent-child execution chains.
3. Check threat intelligence databases for reputation history on IP `198.51.100.27`.

## 10. Limitations

This investigation was conducted on a small, controlled synthetic dataset (`11` events) and does not represent a complete enterprise forensic investigation.

## 11. Conclusion

The synthetic dataset contains a Windows authentication sequence that meets the configured review threshold. The associated privilege and network events provide additional context for investigation, but the available records do not establish unauthorised access or prove that the events share a common cause. Further validation would be required before reaching an incident conclusion.
