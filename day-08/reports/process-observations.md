# Day 8 - Process Observation & System Activity Report

## Overview
Performed real-time process audits inside the Parrot OS environment using `ps`, `grep`, and `top`, analyzing Process IDs (PIDs), Parent Process IDs (PPIDs), execution user contexts, and kernel-level resource management structures.

## Process Observation Table (Captured via `ps -eo pid,ppid,user,comm --sort=pid`)

| PID | PPID | User | Command Name | Purpose / Identification |
| :--- | :--- | :--- | :--- | :--- |
| **1** | 0 | root | `systemd` | The primordial initialization daemon and parent of all user-space processes. |
| **2** | 0 | root | `kthreadd` | Kernel thread daemon responsible for spawning other kernel tasks. |
| **3** | 2 | root | `pool_workqueue_release` | Kernel worker thread handling asynchronous background system operations. |
| **1279** | 1 | user | `kwin_wayland` | The Wayland window manager handling desktop graphics and display composition. |
| **1428** | 1 | user | `plasmashell` | KDE Plasma desktop user-interface shell managing panels and widgets. |
| **1777** | 1 | user | `konsole` | The terminal emulator instance executing user commands. |

## Security Analysis & Findings
* **Process Lineage:** Verified that PID 1 (`systemd`) acts as the ultimate parent process for all user applications, while user-space processes like `konsole` (PID 1777) spawn interactive shell environments.
* **Resource Monitoring (`top`):** Evaluated real-time CPU and memory metrics. Confirmed that normal desktop environments (`kwin_wayland`, `plasmashell`) consume standard resource allocations without anomalous spikes, reinforcing that resource evaluation requires contextual system knowledge before drawing conclusions.
