# Day 9 - Permission Interpretation & Octal Calculation Exercises

## Part 1: Symbolic Permission String Interpretations

### 1. Permission String: `-rw-------` (Octal: 600)
* **File Type:** Regular file (`-`)
* **Owner Permissions (`rw-`):** Can read and write/modify the file contents.
* **Group Permissions (`---`):** Has no permissions at all.
* **Others Permissions (`---`):** Has no permissions at all.
* **Practical Use Case:** Highly sensitive private files, such as SSH private keys (`id_rsa`) or local database credentials.

### 2. Permission String: `-rw-r--r--` (Octal: 644)
* **File Type:** Regular file (`-`)
* **Owner Permissions (`rw-`):** Can read and write/modify the file contents.
* **Group Permissions (`r--`):** Can read the file, but cannot modify it.
* **Others Permissions (`r--`):** Can read the file, but cannot modify it.
* **Practical Use Case:** Standard public read-only text files or README documentation where only the owner has editing rights.

### 3. Permission String: `-rwxr-x---` (Octal: 750)
* **File Type:** Regular file (`-`)
* **Owner Permissions (`rwx`):** Has full control (read, write, and execute/run).
* **Group Permissions (`r-x`):** Can read and execute/run the file, but cannot modify it.
* **Others Permissions (`---`):** Has no permissions at all.
* **Practical Use Case:** Team scripts or utility binaries where trusted group members can execute the program, but outsiders are strictly blocked.

### 4. Permission String: `drwx------` (Octal: 0700)
* **File Type:** Directory (`d`)
* **Owner Permissions (`rwx`):** Can list contents (`r`), add/delete files (`w`), and traverse/enter (`x`).
* **Group Permissions (`---`):** Has no access.
* **Others Permissions (`---`):** Has no access.
* **Practical Use Case:** Secure private working directories or user home folders where no other user is permitted to peer inside.

---

## Part 2: Numeric & Octal Permission Conversions

### 1. Numeric Mode to Symbolic Mapping
* **`600`** $\rightarrow$ `-rw-------` *(Owner read/write; group/others none)*
* **`640`** $\rightarrow$ `-rw-r-----` *(Owner read/write; group read; others none)*
* **`644`** $\rightarrow$ `-rw-r--r--` *(Owner read/write; group/others read)*
* **`700`** $\rightarrow$ `-rwx------` *(Owner full control; group/others none)*
* **`750`** $\rightarrow$ `-rwxr-x---` *(Owner full control; group read/execute; others none)*
* **`755`** $\rightarrow$ `-rwxr-xr-x` *(Owner full control; group/others read/execute)*

### 2. Requirement-to-Numeric Mode Mapping
* **Owner read/write; no access for group or others:** `600`
* **Owner read/write/execute; group read/execute; others no access:** `750`
* **Owner read/write; group read; others read:** `644`
* **Owner read/write/execute; group and others read/execute:** `755`
