# Linux Filesystem Hierarchy & Concepts

## 1. The Root Directory (`/`)
Unlike Windows (which separates drives into `C:`, `D:`), Linux uses a single, unified virtual filesystem tree starting at the root directory represented by a forward slash (`/`). Every file, folder, storage drive, and hardware device plugs into this single tree structure.

## 2. Key Directory Structure Breakdown
* `/bin` — Essential command binaries (executable programs like `ls`, `cp`, `cat`) needed for system repair.
* `/etc` — System-wide configuration files (e.g., user databases, network configs, service settings).
* `/home` — User home directories (e.g., `/home/user/`), where personal files and project workspaces reside.
* `/root` — The home directory specifically reserved for the superuser (`root`).
* `/var` — Variable data files, including log files (`/var/log/`), mail spools, and temporary data.
* `/tmp` — Temporary files storage space cleared upon system reboots.

## 3. Pathing Concepts
* **Absolute Path:** The full path starting explicitly from the root directory (e.g., `/home/user/day-03/linux-lab/`).
* **Relative Path:** The path relative to your current working directory location (e.g., `./cyber-lab` or `../day-02/`).
