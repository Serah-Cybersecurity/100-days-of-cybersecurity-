# Day 7 - Python Data Types & Cybersecurity Applications

## 1. Core Python Data Types Explained

### String (`str`)
* **Definition:** An ordered sequence of characters enclosed in quotes used to represent text data.
* **Cybersecurity Example:** `ip_address = "192.0.2.15"` or `log_message = "Unauthorized access attempt"`. Storing IP addresses as strings is essential because they act as identifiers rather than mathematical quantities.

### Integer (`int`)
* **Definition:** Whole numbers without fractional or decimal components.
* **Cybersecurity Example:** `failed_login_count = 5` or `destination_port = 443`. Used for counting discrete security events, tracking ports, or analyzing numerical thresholds.

### Float (`float`)
* **Definition:** Numbers containing fractional decimal components.
* **Cybersecurity Example:** `scan_duration_seconds = 3.45` or `cpu_load_percentage = 91.2`. Used in performance monitoring and telemetry analysis.

### Boolean (`bool`)
* **Definition:** A logical binary value representing either `True` or `False`.
* **Cybersecurity Example:** `is_mfa_enabled = True` or `ip_is_blacklisted = False`. Essential for conditional logic in threat detection rules.

### List (`list`)
* **Definition:** An ordered, mutable collection of items accessible via zero-based integer indexing.
* **Cybersecurity Example:** `allowed_ports = [80, 443, 22, 53]`. Used for holding collections of indicators or target IP ranges.

### Dictionary (`dict`)
* **Definition:** An unordered collection of key-value pairs used to store structured data attributes.
* **Cybersecurity Example:** 
  ```python
  siem_alert = {
      "severity": "HIGH",
      "signature": "Brute Force Detected",
      "source_ip": "192.0.2.99"
  }

  ---

## How This Applies in the Job Market:
In a Security Operations Center (SOC), when parsing raw SIEM logs (from Splunk, ELK, or Microsoft Sentinel), logs are typically ingested as JSON objects (Python dictionaries). Extracting IP addresses (strings), event codes (integers), and alert statuses (booleans) requires absolute fluency in handling these exact Python data types.
