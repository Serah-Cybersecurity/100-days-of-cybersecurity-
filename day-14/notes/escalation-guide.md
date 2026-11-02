# Enterprise Incident Escalation & Response Protocol

## Incident Overview
- **Alert ID:** SOC-2026-001
- **Target Host:** WIN-LAB-01 (Asset Criticality: High)
- **Account:** analyst
- **Source Address:** 198.51.100.27 (Unapproved external source)
- **Time Window:** 2026-11-01T08:00:00 to 08:04:10+03:00

## Triage Observations
1. Three sequential authentication failures recorded between 08:00 and 08:02.
2. Successful logon recorded at 08:04 from the same external source IP (`198.51.100.27`).
3. Privilege assignment event recorded at 08:04:10 sharing a matching Logon ID with the successful login event.

## Baseline & Context Cross-Reference
- Source IP `198.51.100.27` is **not** listed in the approved administrative subnet inventory (`case-context.md`).
- No associated Change Request reference was found for this time window.

## Evidence Gaps & Limitations
- Endpoint process telemetry is not present (unable to verify if command execution followed logon).
- Network packet captures (PCAP) are unavailable.
- Direct account owner confirmation has not yet been obtained.

## Escalation Justification & Next Steps
- **Reason for Escalation:** Unapproved source IP initiating authentication failure-to-success sequence on a high-criticality host followed by privilege assignment.
- **Recommended IR Actions:**
  1. Contact account owner (`analyst`) via secondary out-of-band communication to verify authentication attempt.
  2. Query EDR telemetry on `WIN-LAB-01` for process creations under the assigned Logon ID.
  3. Check perimeter firewall logs for broader activity involving `198.51.100.27`.

## Analyst Operational Boundary Reminder
*L1 Analyst has documented and escalated the issue. No disruptive containment (host isolation/account lock) has been executed pending Tier 2 review.*
