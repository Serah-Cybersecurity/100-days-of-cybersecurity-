# Day 9 - Access Control and Least Privilege Notes

## 1. Core Concepts & Definitions
* **Access Control:** The security mechanism that determines whether a subject (user/process) is authorized to perform an action (read/write/execute) on an object (file/directory).
* **Principle of Least Privilege (PoLP):** Granting users and processes only the minimum necessary permissions required to perform their intended tasks, minimizing security risk and blast radius.
* **Kernel Access Decision Order:** Evaluates identity sequentially: Root (EUID 0) $\rightarrow$ Directory Traversal ($x$) $\rightarrow$ Owner Bits $\rightarrow$ Group Bits $\rightarrow$ Others Bits. The first matching category determines access.

## 2. Case Study Analysis: `-rw-r----- 1 analyst security 200 report.txt`
* **Owner (`analyst`):** Read and Write (`rw-` / `6`). Can edit analysis.
* **Group (`security`):** Read-only (`r--` / `4`). Group members can review without risk of accidental or malicious alteration.
* **Others (`---` / `0`):** No access. Unauthorized system users are completely blocked.

## 3. The 11 Security-Engineering Audit Framework
When auditing file security, security professionals ask:
1. What is this file used for?
2. Who owns it?
3. Which group is associated with it?
4. What permissions does the owner have?
5. What permissions does the group have?
6. What permissions do others have?
7. Who genuinely needs access?
8. What is the consequence of unauthorized reading? (Confidentiality Impact)
9. What is the consequence of unauthorized modification? (Integrity Impact)
10. What is the consequence of execution? (Availability/Privilege Escalation Impact)
11. Are the permissions consistent with the intended business use?
