# Day 8 - File Permissions & Security Investigation Report

## Overview
Completed hands-on Linux file permission experiments using octal modes (`chmod`), analyzed the differences between file and directory permissions, and evaluated access control risks in a multi-user environment.

## 1. Chmod Hands-On Test Sequence
Tested permission modifications on a local test file (`permission-practice.txt`) within the native Linux filesystem (`/home/user/cybersecurity-journey/day-08`):

* **Initial State (`rw-r--r--` / Default):** Standard read/write for owner, read-only for group and others.
* **Owner-Only Restricted (`chmod 600`):** Resulted in `-rw-------`. Owner has full read/write access; all group members and other users on the system have zero access. Used for private keys and sensitive credentials.
* **Standard Read-Only (`chmod 644`):** Resulted in `-rw-r--r--`. Owner can read/write; group and others can read. Used for public documents or open configuration files.
* **Restricted Group Access (`chmod 640`):** Resulted in `-rw-r-----`. Owner can read/write, assigned group members can read, and outsiders have zero access. Used for shared team assets or application-specific logs.

---

## 2. Security Investigation Scenario Analysis

### Scenario: An application creates a sensitive configuration file with `644` permissions.

1. **Does the file contain information that should be private?**
   * Yes. Application configuration files frequently store database passwords, API secret keys, encryption passphrases, and administrative credentials.
2. **Which users actually need access?**
   * Only the specific service account user or daemon running that application. Ordinary local users have no operational business reading it.
3. **What are the current permissions (`644`)?**
   * `-rw-r--r--` means any local user or unprivileged malware running on the machine can read the file and steal the secrets.
4. **What permissions would be appropriate?**
   * Tightening permissions to `600` (`rw-------`) or `640` (`rw-r-----` restricted to a dedicated service group) is required to prevent unauthorized local reading.
5. **Could changing permissions break the application?**
   * It could break the application **if** the application process runs under a different user account than the file owner and lacks group membership. You must ensure the service account retains read access.
6. **Does the application require a group to access the file?**
   * If multiple cooperative services or privileged daemons need to read the configuration, assigning a dedicated user group and using `640` is the correct enterprise practice.
