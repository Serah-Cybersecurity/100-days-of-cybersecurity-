# Day 9 - Linux Groups and Access Management Notes

## 1. Core Concepts & Definitions
* **What is a Group?** A Linux security construct used to associate multiple user accounts with a common set of access permissions, allowing scalable access control without modifying individual file permissions.
* **User vs. Group:** A user represents an individual human or service identity (with a unique UID), whereas a group represents a collection of users sharing unified access rights (identified by a GID).
* **Primary Group:** The default group assigned to newly created files and processes for a user.
* **Supplementary Group:** Additional security memberships that grant access to shared team resources, devices, or administrative tools.

## 2. Scalability & Security Risks
* **How Groups Simplify Access:** Instead of managing permissions file-by-file for every user, administrators update group memberships, instantly applying access changes across all shared resources.
* **Security Risk (Stale Memberships):** When users change roles or leave an organization, failing to audit and remove them from sensitive groups violates the Principle of Least Privilege, leaving systems vulnerable to insider threats or compromised accounts.

## 3. Inspection Commands & System Files
* **Commands Used:** `groups`, `id`, `getent passwd`, `getent group`, `less /etc/passwd`, `less /etc/group`.
* **System Files:** 
  * `/etc/passwd`: Stores account metadata and UIDs (does not store plain-text passwords or active hashes).
  * `/etc/group`: Maps system group names to GIDs and lists member accounts.
