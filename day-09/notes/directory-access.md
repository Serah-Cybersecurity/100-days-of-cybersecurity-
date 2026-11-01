# Day 9 - Directory Permissions and Access Paths Notes

## 1. Core Concepts & Definitions
* **Sequential Path Evaluation:** Linux evaluates permissions at every directory level along a path, starting from root (`/`) down to the target resource.
* **Directory Execute (`x`) Permission:** Acts as the traversal bit (`cd` or crossing through). Without execute permission on a directory, files inside it cannot be reached, regardless of the file's own permissions.
* **Deletion Mechanics:** Deleting or renaming a file is governed by the **write (`w`) and execute (`x`) permissions of the parent directory**, not by the permissions set on the file itself.

## 2. Key Answers & Observations
* **Why Directory Execute Permission Matters:** It grants traversal rights. Even if a user owns a file with full `rwx` permissions, lacking `x` on any parent directory results in a `Permission Denied` error.
* **How Parent Directories Affect Access:** Access is only as open as the most restrictive directory in the path. Every parent directory must grant traversal (`x`) rights.
* **File Write vs. Directory Entry Deletion:** 
  * File write (`w`) allows editing or modifying the contents inside the file.
  * Directory write (`w`) allows creating, renaming, or deleting filenames stored inside that directory.
* **Path Investigation with `namei -l`:** Running `namei -l` expands the full path structure, showing owners, groups, and permissions for every segment from root (`/`) to the target file[cite: 3]. This allows security analysts to pinpoint the exact directory causing a permission denial.

## 3. Terminal Verification Log
* **Path Inspected:** `~/cybersecurity-labs/day-09/permissions-lab/notes.txt`[cite: 3]
* **Tool Used:** `namei -l` and `ls -ld`[cite: 3]
* **Observation:** Confirmed that parent directories (`/home`, `cybersecurity-labs`, `day-09`, `permissions-lab`) maintain execute (`x`) permissions, allowing seamless path traversal down to `notes.txt`[cite: 3].
