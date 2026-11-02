# Chain of Custody & Evidence Integrity Register

## Evidence Summary Table

| Evidence ID | Description | Source System | Collection Timestamp (UTC) | Collected By | SHA-256 Integrity Hash | Storage Location |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **EV-001** | Synthetic Alert Queue (`alert-queue.jsonl`) | Local Lab Environment | 2026-11-02T18:00:00+03:00 | Analyst (Serah) | `1fbf4499646a7428503e5ab7dc9bafd2e54ebe6648e74517522850e90dd075` | `day-14/lab/data/` |
| **EV-002** | Synthetic Case Context (`case-context.md`) | Local Lab Environment | 2026-11-02T18:05:00+03:00 | Analyst (Serah) | *Pending Verification* | `day-14/lab/data/` |
| **EV-003** | Malformed Test Queue (`malformed.jsonl`) | Local Test Suite | 2026-11-02T18:12:00+03:00 | Analyst (Serah) | *Pending Verification* | `day-14/tests/` |

---

## Evidence Handling Protocols

1. **Acquisition Protocol:** All log files and datasets are ingested into read-only analytical directories to prevent accidental modification during triage.
2. **Verification Protocol:** Prior to running parsing scripts or performing forensic investigations, the SHA-256 hash must be calculated and verified against the acquisition baseline.
3. **Storage & Access Protocol:** Evidence files reside inside secure project folders (`day-14/lab/data/`) with standard POSIX file permissions.
4. **Retention & Destruction:** Evidence maintained for portfolio documentation and lab retention guidelines.
