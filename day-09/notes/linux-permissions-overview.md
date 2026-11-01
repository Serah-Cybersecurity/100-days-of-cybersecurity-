# Day 9 - Linux Permissions Overview & Access Control Concepts

## 1. Symbolic vs. Numeric (Octal) Notation
Linux file permissions dictate who can read, write, or execute a file. These permissions can be represented in two distinct ways:

### Symbolic Notation
* Uses letters and operators to modify permissions relative to their current state.
* **Categories:** `u` (user/owner), `g` (group), `o` (others/world), `a` (all).
* **Operators:** `+` (add permission), `-` (remove permission), `=` (set exact permission).
* **Example:** `chmod u+x script.sh` adds execute permission specifically for the file owner.

### Numeric (Octal) Notation
* Uses a 3-digit number representing the sum of binary permission values for **User**, **Group**, and **Others**.
* **Values:** Read (`r`) = 4, Write (`w`) = 2, Execute (`x`) = 1, None = 0.
* **Calculation:** `rwx` = $4 + 2 + 1 = 7$. `r-x` = $4 + 0 + 1 = 5$. `rw-` = $4 + 2 + 0 = 6$.
* **Common Standards:**
  * `755` (`rwxr-xr-x`): Standard for executable scripts and directories (Owner full, others read/execute).
  * `644` (`rw-r--r--`): Standard for configuration files and documents (Owner read/write, others read-only).
  * `600` (`rw-------`): Standard for private keys and sensitive credentials (Owner read/write only).

---

## 2. Directory Traversal Rules (`r`, `w`, `x` on Directories)
Permissions behave fundamentally differently on directories compared to ordinary files:

* **Read (`r`):** Allows listing the contents of the directory (e.g., running `ls`).
* **Write (`w`):** Allows creating, deleting, or renaming files inside the directory, regardless of the permissions on the individual files inside.
* **Execute (`x`) [Traversal]:** Allows entering or traversing into the directory (e.g., running `cd folder`). 
  * *Critical Security Rule:* Without execute permission on a directory, you **cannot access or read any files inside it**, even if you have full read permissions (`r--`) on those individual files!

---

## 3. Special Permissions: SUID (Set User ID)
Beyond ordinary `rwx` bits, Linux supports special permission bits for advanced control:

* **What it is:** When the **SUID** bit is set on an executable file (represented by an `s` instead of an `x` in the owner field, e.g., `-rwsr-xr-x`), any user who runs that program executes it with the **temporary privileges of the file owner** (typically `root`).
* **Security Relevance:** SUID binaries are high-value targets during local privilege escalation assessments. If a SUID binary contains a vulnerability (such as a buffer overflow or unsafe file handling), an ordinary user can exploit it to execute arbitrary commands with root privileges.
