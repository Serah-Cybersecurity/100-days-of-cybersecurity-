# Day 8 - The Principle of Least Privilege

## Core Concepts & Analysis

### 1. What is the Principle of Least Privilege?
The Principle of Least Privilege (PoLP) is a core security concept stating that users, programs, and processes should be given only the minimum permissions necessary to complete their specific functions, and no more.

### 2. What is the difference between a user and a group?
* **User:** An individual identity assigned to a person or system service, tracked by a unique UID.
* **Group:** A collection mechanism used to bundle multiple users together, tracked by a GID, simplifying permission management across teams.

### 3. What is a UID and GID?
* **UID (User ID):** A unique numerical integer used by the Linux kernel internally to enforce file ownership and access control.
* **GID (Group ID):** A unique numerical integer representing a group, used to grant collective file access permissions to multiple users simultaneously.

### 4. Why should a security analyst avoid unnecessary administrative privileges?
Running everyday tasks or scripts as the `root` administrator creates massive risk. If a script contains a vulnerability or is exploited, an attacker instantly inherits full control of the machine. Limiting privileges limits the "blast radius" of security incidents.

### 5. What might go wrong if an ordinary application can modify system configuration?
If an unprivileged application or compromised script can alter system configuration files (such as `/etc/passwd` or network routing tables), an attacker can establish persistence, create rogue administrative accounts, or intercept network traffic undetected.
