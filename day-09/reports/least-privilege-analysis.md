# Day 9 - Least Privilege & Real-World Access Control Analysis

## Overview
Analyzed the security implications of file permissions, user isolation, and service account privileges on enterprise Linux servers.

## Core Principles
1. **The Principle of Least Privilege (PoLP):** Users and processes must operate using the absolute minimum set of privileges necessary to complete their assigned tasks.
2. **Blast Radius Reduction:** Restricting service accounts and file permissions limits the damage an attacker can inflict if a single application or account is compromised.
3. **Separation of Duties:** Ensuring ordinary users, developers, and administrators maintain distinct access boundaries.

## Common Permission Misconfigurations & Risks
* **World-Writable Files (`777` or `o+w`):** Allows any local user to tamper with configuration files or inject malicious code into scripts.
* **Over-Privileged Daemons:** Running web servers or database daemons as `root` instead of dedicated service accounts.
* **Sensitive Data Exposure (`644` vs `600`):** Storing API keys or private keys in files readable by the entire system.

## Career Relevance
Mastering Linux permissions and ownership is essential across SOC investigations, incident response artifact collection, cloud infrastructure hardening, and authorized penetration testing.
