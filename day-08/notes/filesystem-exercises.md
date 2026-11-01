# Day 8 - Linux Filesystem Investigation Report

## Overview
Completed hands-on Linux filesystem navigation, examining root directory hierarchies, system configuration files, file permissions, shared folders (`/media/sf_cybersec`), and terminal search utilities inside the Parrot OS environment.

## Practical Exercise Task Log

### Task 1: Printing Current Directory (`pwd`)
* **Objective:** Determine the absolute path of the current working directory.
* **Command:** `pwd`
* **Result:** Output confirmed path at `/home/user`.
* **Learning:** Established baseline reference point before executing relative navigation commands.

### Task 2: Listing Directory Contents & Hidden Files (`ls -la`)
* **Objective:** Inspect visible and hidden files within the user home directory.
* **Command:** `ls -la ~`
* **Result:** Displayed long-format listings including hidden configuration folders and files (e.g., `.bashrc`, `.ssh/`, `.config/`).
* **Learning:** In Linux, files starting with a period are hidden by default to reduce clutter. Security analysts frequently inspect hidden directories like `.ssh/` during forensic reviews.

### Task 3: Directory Navigation & Root Exploration (`cd`, `pwd`)
* **Objective:** Navigate through system-wide directories and return home.
* **Commands:** 
  ```bash
  cd /etc
  pwd
  cd ~
  pwd

- **Result:** Successfully transitioned to the system configuration directory (`/etc`) and returned to the user home directory (`/home/user`).
- **Learning:** The root directory `/` serves as the base of the entire Linux filesystem, while `~` acts as a shortcut to the active user's home directory.

### Task 4: Inspecting System Configuration Files (`cat`, `less`)

- **Objective:** Read system operating system metadata.
- **Command:** 
  ```bash
  cat /etc/os-release
  less /etc/os-release

* **Result:** Printed distribution details (`Parrot Security 7.3`) to the terminal and opened it interactively in `less` (exited using `q`).
* **Learning:** `cat` dumps small text files immediately, whereas `less` provides scrollable pagination, preventing terminal flooding when reading massive log files.

### Task 5: Workspace File Discovery (`find`)

* **Objective:** Locate all regular files within the Day 8 workspace directory.
* **Command:** `find /media/sf_cybersec/day-08 -type f`
* **Result:** Listed placeholder and setup files inside data, python, reports, and screenshots subdirectories successfully (handling an initial shared-folder permission restriction via path verification).
* **Learning:** The `-type f` flag restricts search results exclusively to files, which is essential when auditing large directories for specific artifacts.

### Task 6: Searching Text Patterns (`grep`)

* **Objective:** Extract specific configuration keys from text files.
* **Command:** `grep "PRETTY_NAME" /etc/os-release`
* **Result:** Output: `PRETTY_NAME="Parrot Security 7.3 (echo)"`.
* **Learning:** `grep` is a powerful pattern-matching utility that enables security analysts to filter through gigabytes of logs or configuration files to find precise indicators of compromise (IOCs) or system versions.

```

```
