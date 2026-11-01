# Linux Commands Reference Guide

## Navigation & Directory Management
* `pwd` — Print Working Directory: Displays the absolute path of your current directory location.
* `ls` — List: Lists files and directories in the current folder.
  * `ls -l` — Long format: Unlocks rich metadata (permissions, ownership, size, timestamps).
  * `ls -la` — All files: Includes hidden files (files starting with a dot `.`).
* `cd` — Change Directory: Navigates between directory paths (e.g., `cd cyber-lab`).
* `mkdir` — Make Directory: Creates a new directory (e.g., `mkdir -p day-03/linux-lab`).

## File Creation & Manipulation
* `touch` — Creates an empty file or updates access/modification timestamps.
* `cp` — Copy: Copies a file from a source to a destination (e.g., `cp notes.txt backup.txt`).
* `mv` — Move / Rename: Moves files or renames them by shifting file pointers in the directory table.
* `rm` — Remove: Deletes files permanently.
* `cat` — Concatenate: Reads data from a file sequentially and prints output to the terminal.

## Search & Inspection
* `grep` — Global Regular Expression Print: Searches text files for specific matching patterns or strings.
* `find` — Searches the filesystem for files matching criteria like size, name, or ownership.
* `file` — Determines a file's true data format/type based on its content rather than its file extension.

## System & Process Information
* `whoami` — Prints your currently active username.
* `id` — Displays user ID and group ID settings.
* `uname -a` — Prints kernel and system architecture information.
* `hostname` — Displays the system's network hostname.
* `ps` — Process Status: Displays active processes running in your current shell session.
  * `ps aux` — Displays all running processes across all users on the system.

## Permissions & Security
* `chmod` — Change Mode: Modifies file permission bits (e.g., `chmod +x script.py` to grant execution rights).
