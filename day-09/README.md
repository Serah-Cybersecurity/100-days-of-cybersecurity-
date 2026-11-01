# Linux Security Fundamentals: File Permissions and Access Control

## 1. Overview
This portfolio module documents the practical mastery of Linux security fundamentals, focusing on user identity management, group structures, file ownership, `rwx` permission semantics, octal/symbolic modification (`chmod`), `umask` creation defaults, path traversal rules, special permission bits (`SUID`, `SGID`, Sticky Bit), and automated security auditing using Python.

## 2. Objectives
During this lab session, the following practical skills were demonstrated:
* Inspecting and auditing file metadata using `ls` and `stat`.
* Calculating and applying octal (numeric) and symbolic permission modes.
* Configuring secure sandbox directories (`private` and `shared`) following the Principle of Least Privilege.
* Investigating path traversal mechanics and directory execution (`x`) requirements using `namei` and `ls -ld`.
* Evaluating default creation rules using `umask`.
* Recognizing advanced special permission bits (`SUID`, `SGID`, Sticky Bit) and auditing system binaries.
* Developing and testing an automated Python-based permissions auditor.

## 3. Environment
* **Operating System:** Parrot OS (Virtual Machine / Containerized Lab Environment)
* **Execution Boundary:** All hands-on commands and scripts were restricted strictly to local user lab directories (`~/cybersecurity-labs/day-09/`) to ensure system integrity.

## 4. Tools Used
* **Linux Terminal & Shell:** Command-line execution and environment interaction.
* **`ls` / `ls -ld`:** Basic listing and directory metadata inspection.
* **`stat` / `stat -c`:** Deep file attribute and metadata extraction.
* **`chmod`:** Symbolic and octal permission modification.
* **`umask`:** Default file and directory creation mask analysis.
* **Python 3 (`pathlib`, `stat`):** Custom security auditing automation.
* **Git & GitHub:** Version control and professional portfolio publication.

## 5. Lab Description
A dedicated local practice workspace (`permissions-lab/`) was established to test attribute modifications safely. The lab structure includes:
* `notes.txt`: Sandbox file used for testing octal (`600`, `640`) and symbolic permission changes.
* `private/`: Directory locked to `700` (`drwx------`) to simulate strict user isolation.
* `shared/`: Directory configured with `750` (`drwxr-x---`) to practice collaborative group access controls.

## 6. Project Description (Python Permissions Auditor)
A custom script (`permissions_auditor.py`) was developed utilizing Python's standard library (`pathlib`, `stat`) to recursively scan the Day 9 lab directory. 
* **What it checks:** File types, relative paths, symbolic permissions, numeric octal modes, UID/GID ownership, world-writable bits, and explicit `777` modes.
* **What it does not check:** Access Control Lists (ACLs), Mandatory Access Control (MAC) policies, file content confidentiality, or behavioral file integrity tampering.

## 7. Testing Summary
The permissions auditor script was subjected to the following validation scenarios:
1. **Normal Run:** Successfully parsed and displayed metadata for all files and directories in the Day 9 workspace.
2. **Missing Directory:** Handled nonexistent path configurations gracefully by throwing configuration exceptions.
3. **World-Writable / `777` Flagging:** Created a disposable test file (`test-777.txt`), set its mode to `777`, verified that the auditor correctly triggered review flags, and subsequently restored the file to secure `600` permissions.

## 8. Key Security Lessons & Engineering Principles
* **Least Privilege:** Accounts and processes must operate with the absolute minimum access required for legitimate tasks to minimize blast radius.
* **Directory Traversal (`x`):** File permissions are meaningless if parent directories lack execute (`x`) traversal rights.
* **File vs. Directory Deletion:** Deleting or renaming a file is controlled by the parent directory's write (`w`) and execute (`x`) permissions, not the file's own write bit.
* **Context Over Raw Numbers:** Overly permissive modes (like `777` or world-writable bits) are review flags that require investigation into business purpose, not absolute proof of vulnerability.
* **Defense in Depth:** Permission settings alone cannot guarantee system security; they must be paired with monitoring, ACLs, and regular auditing.

## 9. Project Limitations
This project is an educational learning tool and proof-of-concept portfolio artifact. It is not a production-grade vulnerability scanner and does not evaluate complex kernel-level security frameworks.

## 10. Future Improvements
Planned enhancements for subsequent iterations include:
* Exporting audit reports to JSON format for SIEM ingestion.
* Adding automated unit tests for permission calculation logic.
* Improving input validation and error handling for restricted paths.
* Implementing configurable command-line arguments for custom scan directories.
* Generating executive summary reports separating raw observation from security risk interpretation.
