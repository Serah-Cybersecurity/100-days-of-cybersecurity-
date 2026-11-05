# Technical Note: Fundamentals of Detection Engineering

**Author:** Serah Mulwa

**Module:** Day 20 - Integrated Network Threat Hunting & Detection Engineering

## 1. Executive Summary

A common misconception among beginner security analysts is that monitoring network traffic simply involves downloading pre-written rules from GitHub, pasting them into an intrusion detection system, and waiting for alerts. In enterprise environments, this approach leads directly to **alert fatigue**—flooding the Security Operations Center (SOC) with thousands of false alarms until real threats are ignored.

This technical note documents **Detection Engineering**: the disciplined, software-engineering-inspired practice of designing, testing, tuning, and maintaining security detection logic to maximize true threat visibility while minimizing noise.

## 2. What is Detection Engineering?

Detection engineering treats security rules like production software code. It encompasses the entire lifecycle of identifying adversary behaviors, mapping them to appropriate data sources, writing detection rules, testing them against packet captures, and continuously refining them based on operational feedback.

### The Detection Lifecycle:

```
┌───────────────────────────────┐
│      1. SECURITY QUESTION     │
└──────────────┬────────────────┘
               │
               ▼
┌───────────────────────────────┐
│      2. DETECTION DESIGN      │
└──────────────┬────────────────┘
               │
               ▼
┌───────────────────────────────┐
│      3. RULE DEVELOPMENT      │
└──────────────┬────────────────┘
               │
               ▼
┌───────────────────────────────┐
│        4. TESTING (PCAP)      │
└──────────────┬────────────────┘
               │
               ▼
┌───────────────────────────────┐
│    5. FALSE-POSITIVE REVIEW   │
└──────────────┬────────────────┘
               │
               ▼
┌───────────────────────────────┐
│     6. PRODUCTION DEPLOYMENT  │
└──────────────┬────────────────┘
               │
               ▼
┌───────────────────────────────┐
│ 7. TUNING & ITERATIVE REVIEW  │
└───────────────────────────────┘
```

1. **Security Question / Hypothesis:** Define the specific adversary technique or anomalous behavior you aim to catch.
2. **Detection Design:** Determine which telemetry source (Suricata, Zeek, EDR, Firewall) has the required visibility.
3. **Rule Development:** Write the syntax for the chosen detection platform (e.g., Suricata signature or Sigma rule).
4. **Testing:** Run the rule against representative PCAPs or test traffic to ensure it triggers correctly.
5. **False-Positive Evaluation:** Assess whether normal organizational activity accidentally triggers the rule.
6. **Deployment:** Push the tuned rule to production sensors.
7. **Iterative Review:** Continuously update thresholds as attacker tactics evolve.

## 3. The 6 Core Quality Questions of Detection

Before deploying any detection rule to production, a professional detection engineer must be able to answer six foundational questions:

1. **What behavior are we trying to identify?** (e.g., C2 beaconing, DNS tunneling, unauthorized administrative access).
2. **Which data source supports this detection?** (e.g., Suricata EVE JSON alerts or Zeek connection metadata).
3. **What exact condition generates the alert?** (e.g., Regex string match, abnormal port usage, or high connection frequency).
4. **What legitimate activity could match this condition?** (e.g., Software updates, legitimate administrative tools, standard cloud backups).
5. **What activity might the detection miss?** (e.g., Evasion techniques such as domain fronting, encryption, or alternative protocols).
6. **What additional evidence is required to confirm the alert?** (e.g., EDR process execution trees or neighboring Zeek protocol logs).

## 4. Lab Rules vs. Production Realities

* **Educational Lab Rules:** For today's lab, we use a benign Suricata signature detecting DNS requests for `example.com`. Its sole purpose is to test your multi-tool correlation pipeline and Community ID hashing.
* **Production Detections:** Real-world enterprise rules target high-entropy domains, known malicious command-and-control (C2) IP reputation lists, or anomalous query volumes. 

## 5. Key Portfolio Takeaways

* Detection engineering requires rigorous testing and tuning, not blind rule copying.
* Every rule must account for legitimate business activity to prevent false-positive alert fatigue.
* Documenting the limitations and assumptions behind your detection rules demonstrates elite operational maturity.
