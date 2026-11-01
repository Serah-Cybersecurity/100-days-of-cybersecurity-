# Day 9 - `umask` and Default Permissions Notes

## 1. Core Concepts & Definitions
* **`umask` Definition:** A permission mask that determines which permission bits are withheld or stripped away from newly created files and directories.
* **Subtraction Logic:** `umask` removes permissions rather than granting them. Standard files request a maximum base of `666` (`rw-rw-rw-`), and directories request a base of `777` (`rwxrwxrwx`).
* **Security Importance:** Serves as an automated baseline protection mechanism, preventing applications from accidentally exposing newly created files to unauthorized users.

## 2. Terminal Observations & Lab Results
* **Observed System `umask`:** `0002`[cite: 4]
* **New Test File (`umask-test.txt`) Permissions:** `-rw-rw-r--` (octal `664`)
* **New Test Directory (`umask-test-dir`) Permissions:** `drwxrwxr-x` (octal `775`)

## 3. Mathematical Verification
* **File Calculation:** $666 - 002 = 664$ (`-rw-rw-r--`)[cite: 4]
* **Directory Calculation:** $777 - 002 = 775$ (`drwxrwxr-x`)[cite: 4]

## 4. Key Security Insights
* **Why a `umask` Exists:** It enforces system-wide security baselines automatically so users and applications do not have to manually set restrictive permissions every time a file is created.
* **Why Actual Creation Behavior Can Differ:** The final permission state depends on the initial mode requested by the creating program, the active process `umask`, parent directory default ACLs, and OS-specific file creation rules.
* **Security Risks of Inappropriate Defaults:** 
  * A loose `umask` (e.g., `0000`) creates world-writable files (`666`) and directories (`777`), enabling unauthorized local users to alter sensitive logs, inject malicious code, or read private credentials.
  * In enterprise environments, sensitive service accounts are assigned strict masks like `0027` or `0077` to guarantee zero exposure to unauthorized users.
