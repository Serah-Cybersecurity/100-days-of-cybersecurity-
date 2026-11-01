# OverTheWire: Bandit Wargame - Progress Tracker

## Level-by-Level Completion Log

### Level 0 $\rightarrow$ Level 1
* **Objective:** Establish the initial SSH connection to the game server.
* **Solution:** Connect via SSH using port `2220` with username `bandit0` and password `bandit0`.
* **Commands:** `ssh bandit0@bandit.labs.overthewire.org -p 2220`
* **Key Concept:** Basic SSH syntax and connecting to non-standard ports.

---

### Level 1 $\rightarrow$ Level 2
* **Objective:** Read the password stored in a file named `-` located in the home directory.
* **Solution:** Standard `cat -` waits for stdin input. Use relative paths (`cat ./-`) to specify the file.
* **Commands:** `cat ./-`
* **Key Concept:** Handling filenames that conflict with command-line option flags.

---

### Level 2 $\rightarrow$ Level 3
* **Objective:** Read the password stored in a file with spaces in its name (`spaces in this filename`).
* **Solution:** Wrap the filename in quotes or use backslash escaping for spaces.
* **Commands:** `cat "spaces in this filename"` or `cat spaces\ in\ this\ filename`
* **Key Concept:** Character escaping and handling whitespace in bash commands.

---

### Level 3 $\rightarrow$ Level 4
* **Objective:** Retrieve the password hidden in a hidden directory named `inhere`.
* **Solution:** Navigate into `inhere` and list all files, including dotfiles (`.hidden`).
* **Commands:** `cd inhere && ls -la && cat .hidden`
* **Key Concept:** Hidden files (prefixed with `.`) and directory navigation.

---

### Level 4 $\rightarrow$ Level 5
* **Objective:** Identify the single human-readable file stored inside the `inhere` directory among multiple binary files.
* **Solution:** Use the `file` command across all files in the directory to find the ASCII text file.
* **Commands:** `cd inhere && file ./*` then `cat ./-file07`
* **Key Concept:** Identifying file types by content rather than file extension.

---

### Level 5 $\rightarrow$ Level 6
* **Objective:** Search the `inhere` directory for a file matching specific criteria: human-readable, 1033 bytes in size, and not executable.
* **Solution:** Use `find` with parameters for size and file type.
* **Commands:** `find inhere -type f -size 1033c ! -executable -exec cat {} +`
* **Key Concept:** Advanced `find` command filtering with exact size (`c` for bytes) and attributes.

---

### Level 6 $\rightarrow$ Level 7
* **Objective:** Search the entire server file system for a file owned by user `bandit7`, group `bandit6`, and 33 bytes in size.
* **Solution:** Query the root directory `/` and suppress "Permission denied" errors using stderr redirection (`2>/dev/null`).
* **Commands:** `find / -user bandit7 -group bandit6 -size 33c 2>/dev/null`
* **Key Concept:** Searching system-wide files based on ownership, permissions, and stream redirection.

---

### Level 7 $\rightarrow$ Level 8
* **Objective:** Retrieve the password next to the word `millionth` inside `data.txt`.
* **Solution:** Pipe `data.txt` to `grep` to extract the exact line.
* **Commands:** `grep "millionth" data.txt`
* **Key Concept:** Pattern matching and text extraction using `grep`.

---

### Level 8 $\rightarrow$ Level 9
* **Objective:** Find the only line of text in `data.txt` that occurs only once.
* **Solution:** Sort the lines alphabetically first (required for `uniq`), then use `uniq -u` to isolate the unique entry.
* **Commands:** `sort data.txt | uniq -u`
* **Key Concept:** Combining sorting and uniqueness filters in Linux pipelines.

---

### Level 9 $\rightarrow$ Level 10
* **Objective:** Extract the human-readable password from the binary file `data.txt`, preceded by several `=` characters.
* **Solution:** Extract ASCII strings from the binary file using `strings`, then filter with `grep`.
* **Commands:** `strings data.txt | grep "="`
* **Key Concept:** Extracting printable strings from binary and unformatted files.

---

### Level 10 $\rightarrow$ Level 11
* **Objective:** Decode the Base64-encoded password stored inside `data.txt`.
* **Solution:** Pass the file content through the `base64` command-line utility with the decode flag (`-d`).
* **Commands:** `base64 -d data.txt`
* **Key Concept:** Base64 encoding/decoding on the Linux command line.

---

### Level 11 $\rightarrow$ Level 12
* **Objective:** Decrypt the ROT13 Caesar cipher text stored in `data.txt`.
* **Solution:** Use `tr` to transpose upper and lower case character sets shifted by 13 positions.
* **Commands:** `tr 'A-Za-z' 'N-ZA-Mn-za-m' < data.txt`
* **Key Concept:** Character substitution and basic ciphers via command line tools.

---

### Level 12 $\rightarrow$ Level 13
* **Objective:** Decompress a file repeatedly compressed using multiple archive types (`gzip`, `bzip2`, `tar`).
* **Solution:** Work in a temporary directory (`mktemp -d`), dump the hex dump back to binary with `xxd -r`, check file types with `file`, rename with matching extensions, and decompress iteratively.
* **Commands:** 
  - `cd $(mktemp -d)`
  - `xxd -r data.txt > data`
  - Repeatedly check with `file data` and unpack using `gzip -d`, `bzip2 -d`, or `tar -xf`.
* **Key Concept:** Multi-stage reverse engineering, hex restoration, and nested archive decompression.

---

### Level 13 $\rightarrow$ Level 14
* **Objective:** Log into Level 14 using the provided private SSH key file (`sshkey.private`) stored in the home directory.
* **Solution:** Connect via `ssh` specifying the identity file with `-i`.
* **Commands:** `ssh -i sshkey.private bandit14@localhost -p 2220`
* **Key Concept:** Public/Private key pair authentication in OpenSSH.

---

### Level 14 $\rightarrow$ Level 15
* **Objective:** Submit the Level 14 password (`/etc/bandit_pass/bandit14`) to port `30000` on `localhost` to retrieve the next password.
* **Solution:** Send the raw plaintext string over a basic TCP socket using Netcat (`nc`).
* **Commands:** `cat /etc/bandit_pass/bandit14 | nc localhost 30000`
* **Key Concept:** Basic network socket interaction and raw TCP communication.

---

### Level 15 $\rightarrow$ Level 16
* **Objective:** Submit the Level 15 password to port `30001` on `localhost` using SSL/TLS encryption.
* **Solution:** Use `openssl s_client` to establish an encrypted socket connection and prevent premature disconnects using `-ign_eof`.
* **Commands:** `cat /etc/bandit_pass/bandit15 | openssl s_client -connect localhost:30001 -ign_eof`
* **Key Concept:** Encrypted socket streams and client-side SSL/TLS handshakes.

---

### Level 16 $\rightarrow$ Level 17
* **Objective:** Scan ports `31000-32000` on `localhost` to find an SSL service that accepts the Level 16 password and returns an RSA Private Key.
* **Solution:** 
  1. Scan ports with `nmap -p 31000-32000 -sV localhost` to find SSL services.
  2. Query candidate ports (Port `31790`) using `openssl s_client` while suppressing handshake noise with `2>/dev/null`.
  3. Extract the RSA Private Key, save it locally, set file permissions to `chmod 600`, and SSH directly into Level 17.
* **Commands:**
  - `cat /etc/bandit_pass/bandit16 | openssl s_client -connect localhost:31790 -ign_eof 2>/dev/null > key.txt`
  - `chmod 600 bandit17.key`
  - `ssh -i bandit17.key bandit17@bandit.labs.overthewire.org -p 2220`
* **Key Concept:** Network port scanning, service enumeration, noise suppression on `stderr`, and private key permissions.
