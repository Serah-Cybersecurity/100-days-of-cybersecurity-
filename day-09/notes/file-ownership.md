# Day 9 - Linux File Ownership and Metadata Notes

## 1. Core Concepts & Definitions
* **File Ownership:** Every file and directory in Linux is assigned a specific user owner and an associated group, which dictate access rights alongside permission bits.
* **`ls -l` Breakdown:** Displays file type, link count, owner, group, size, modification timestamp, and filename.
* **`stat` Command:** Provides granular file metadata, including inode numbers, security context, precise timestamps, and exact UID/GID mappings.

## 2. Why Ownership Matters in a Multi-User System
* **Application Integrity:** Services must run with appropriate file ownership to function correctly without permission denials or crashes.
* **Security & Access Control:** Incorrectly assigned ownership can allow unauthorized users to read, modify, or execute sensitive files.
* **Forensic Value:** During incident response, examining file ownership and timestamps helps identify how and when files were introduced to a system.

## 3. Practical Observations (Terminal Inspection)
* **Target Inspected:** `bandit14.key` and current working directory (`.`)
* **Owner (`ls -l` / `stat`):** `user` (UID: 1000)
* **Group (`ls -l` / `stat`):** `user` (GID: 1000)
* **Permissions (`stat`):** `-rw-------` (octal 0600) for `bandit14.key`; `drwx------` (octal 0700) for directory `.`
* **File Type:** Regular file (`bandit14.key`) and directory (`.`)
* **Modification Timestamp:** Captured successfully via system metadata output.
