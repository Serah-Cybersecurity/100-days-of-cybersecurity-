# Day 13 - Technical Setup & Lab Environment Strategy

* **Author:** Serah Mulwa  
* **Date:** October 31, 2026  
* **Module:** SIEM Fundamentals & Lab Architecture  

---

## 1. Environment Specifications

For Day 13 execution, the lab relies entirely on existing, lightweight local tools alongside web-based interactive platforms:

* **Host OS:** Windows 10/11
* **Guest OS / VM:** Parrot OS Linux (Security Edition)
* **Runtime:** Python 3.x (Standard Library)
* **Version Control:** Git & GitHub
* **Interactive Platforms:** TryHackMe (Free Tier) & Splunk Free Education

---

## 2. Architecture & Deployment Analysis

### Why Enterprise Local Deployments Were Excluded
1. **System Resource Overhead:** Enterprise SIEM engines (e.g., Splunk Enterprise) require dedicated 8GB+ RAM allocations and high IOPS storage controllers that risk destabilizing local virtualization environments.
2. **Compatibility:** Distribution-specific packages target enterprise server builds (Ubuntu LTS / Debian Stable) rather than specialized pentesting OS builds.
3. **Licensing Caps:** Standalone free software tiers frequently disable alerting triggers, role-based controls, and distributed search functions.

---

## 3. Practical Learning Pathways

```
┌────────────────────────────────────────────────────────────────────────┐
│                      DAY 13 PRACTICAL EXECUTION                        │
├───────────────────┬───────────────────────────────┬────────────────────┤
│ Option A          │ Option B                      │ Option C           │
│ TryHackMe SIEM    │ Splunk Official Training      │ Python Correlator  │
│ (Interactive GUI) │ (Vendor Fundamentals & SPL)   │ (Custom Engine)    │
└───────────────────┴───────────────────────────────┴────────────────────┘
```

1. **Option A — TryHackMe (Intro to SIEM):** Teaches dashboard mechanics, incident triage, and centralized log visibility.
2. **Option B — Splunk Free Training:** Teaches search syntax, field usage, time modifiers, and statistical functions directly from vendor sources.
3. **Option C — Python Correlation Engine (`day-13/scripts/siem_correlator.py`):** Primary code deliverable demonstrating ingestion, timestamp normalization, threshold evaluation, and alert generation.

---

## 4. Analyst Axioms

> 💡 **Axiom 1:** *Understand the mechanics behind the GUI; building a custom correlation script proves first-principles mastery.*  
> 💡 **Axiom 2:** *Resource efficiency matters; prioritize light, controllable simulation scripts over resource-heavy deployments during initial learning stages.*
