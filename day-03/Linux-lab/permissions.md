# Linux File Permissions & Access Control

## 1. Anatomy of `ls -l`
When running `ls -l`, file permissions appear on the far left of the output (e.g., `-rwxr-xr--`).
* **First Character:** Denotes file type (`-` for regular file, `d` for directory).
* **Triad 1 (Positions 2–4):** **Owner** permissions.
* **Triad 2 (Positions 5–7):** **Group** permissions.
* **Triad 3 (Positions 8–10):** **Others** permissions.

## 2. Permission Bits
* **`r` (Read):** Permission to open and read file contents or list directory contents.
* **`w` (Write):** Permission to modify, edit, or delete files/directories.
* **`x` (Execute):** Permission to run a file as an executable program or script, or traverse into a directory.

## 3. Security Significance & Enforcement
* **Operating Systems Enforce Access Rules:** Files created by default (like via `touch`) do not have execute permissions (`-rw-r--r--`). Attempting to run them results in a `Permission denied` kernel error.
* **`chmod +x`:** Explicitly adds execution privileges to a script so the shell can load it into memory.
* **Security Relevance:** Proper permission management enforces **Least Privilege**—ensuring users and software only hold the minimum permissions required to function, mitigating unauthorized tampering or privilege escalation.
