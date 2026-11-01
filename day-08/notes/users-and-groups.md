# Day 8 - User Identity & Group Audit Report

## Overview
Audited active user credentials, numerical identifiers (UID/GID), group memberships, system account databases, and administrative privilege availability (`sudo`) within the Parrot OS environment.

## User Identity Audit Log
* **Active Username:** `user` (verified via `whoami`)[cite: 12]
* **User ID (UID):** `1000`[cite: 12]
* **Primary Group ID (GID):** `1000` (`user`)[cite: 12]
* **Supplementary Groups:** `dialout`, `cdrom`, `floppy`, `sudo`, `audio`, `dip`, `video`, `plugdev`, `netdev`, `scanner`, `lpadmin`, `bluetooth`, `vboxsf`[cite: 12]
* **Home Directory:** `/home/user`[cite: 12]
* **Login Shell:** `/bin/bash`[cite: 12]

## System Account Database Query (`getent passwd`)
* **Query Executed:** `getent passwd "$(whoami)"`[cite: 12]
* **Result Structure:** `user:x:1000:1000::/home/user:/bin/bash`[cite: 12]
* **Security Insight:** Password hashes are isolated in protected system files (`/etc/shadow`), while `/etc/passwd` maps user accounts to numerical UIDs and shell environments.

## Administrative Privilege Availability (`sudo`)
* **Query Executed:** `command -v sudo`[cite: 12]
* **Result Path:** `/usr/bin/sudo`[cite: 12]
* **Security Insight:** Confirms that the `sudo` binary is installed and available for authorized users to execute commands with elevated privileges.
