# Day 9 - Special Permission Bits (`SUID`, `SGID`, and Sticky Bit) Notes

## 1. Core Concepts & Definitions
* **SUID (Set User ID):** Allows an executable file to run with the effective privileges of the file's owner (often `root`), enabling low-privileged users to perform restricted tasks securely (e.g., changing passwords via `/usr/bin/passwd`).
* **SGID (Set Group ID):** On executables, runs with the file group's identity. On directories, forces newly created files and subdirectories to inherit the parent directory's group ownership automatically.
* **Sticky Bit:** Applied to shared directories (like `/tmp`), ensuring that only the file owner, directory owner, or `root` can delete or rename a file, preventing users from deleting each other's work.

## 2. Terminal Observations & Lab Analysis
* **SUID Enumeration:** Executed `find / -perm -4000 2>/dev/null` to locate executable files with the SUID bit set. This technique is standard in security audits and privilege escalation assessments.
* **Sticky Bit Inspection:** Executed `ls -ld /tmp` and observed the output `drwxrwxrwt`. The trailing `t` indicates that the sticky bit is active, allowing global write access while restricting file deletion strictly to file owners and root.

## 3. Key Security & Forensic Insights
* **Privilege Escalation Risks:** Misconfigured or vulnerable SUID binaries owned by `root` are prime vectors for local privilege escalation during penetration tests.
* **Evidence-Driven Investigation:** Finding an SUID or SGID binary is not inherently malicious. Analysts must audit file ownership, vendor baseline expectations, and file integrity to determine legitimacy.
