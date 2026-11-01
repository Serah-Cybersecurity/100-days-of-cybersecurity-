# Day 1 — Foundations

## Date

24 September 2026

## Objective

Establish foundational competence in computer architecture, operating system design, core security principles (CIA Triad, Data Encoding, Cryptography), and introductory Python programming from absolute zero.

## What I learned

### Computers
* Dissected the foundational data processing loop: Input, Processing, Storage, and Output.
* Explored how hardware interprets abstract logic via binary data representations (bits, bytes, and base-2 number systems).

### Hardware
* Mastered the 7 core desktop components required for system assembly: CPU (processing brain), RAM (volatile working memory), Motherboard (interconnect bus), Storage (SSD/HDD persistence), Desktop GPU (rendering pipeline), PSU (power delivery), and I/O Panel (peripherals).
* Diagnosed and resolved hardware boot errors, distinguishing between slower mechanical HDDs and faster solid-state drives during startup drive selection.

### Software
* Explored the division between system software (managing raw metal and resource allocation) and application software (executing user tasks).
* Analyzed software abstraction layers that isolate developers from direct hardware-level manipulation.

### Operating systems
* Examined core OS responsibilities including process management, memory allocation, and file system indexing.
* Differentiated between **kernel space** (unrestricted hardware access) and **user space** (sandboxed application execution).
* Compared interface mechanisms: Graphical User Interfaces (GUI) for intuitive navigation vs. Command-Line Interfaces (CLI) for precise, scriptable execution.
* Categorized global OS landscapes into Desktop, Server (headless, high-uptime), Mobile (sandboxed), Embedded (minimal footprint), and Virtual/Cloud systems.

### Command line
* Practiced core shell navigation and file inspection to move efficiently through directory trees.

### Security fundamentals
* **CIA Triad:** Mapped real-world security incidents to Confidentiality (data leaks, access control), Integrity (unauthorized modifications, log deletion), and Availability (DoS attacks, service outages).
* **Data Encoding & Representation:** Explored base conversions (Decimal, Binary, Octal, Hexadecimal) and character sets including ASCII, UTF-8, UTF-16, and UTF-32 (handling special characters, symbols, and emoji encodings).
* **Cryptography Concepts:** Differentiated symmetric vs. asymmetric encryption, identified the role of public/private key pairs, and understood how asymmetric key exchange solves the foundational key distribution problem before handing off bulk traffic to symmetric ciphers.

### Programming & Python
* Learned basic script execution inside VS Code and integrated terminal workflows.
* Explored variable assignment, data typing, and the necessity of explicit type casting (e.g., wrapping `input()` strings in `int()` or `float()` for mathematical operations).
* Practiced reading stack traces and treating error codes as diagnostic feedback rather than failures.

## Commands I learned

* `pwd`: Print the absolute path of the current working directory.
* `ls`: List directory contents.
* `cd`: Change the current working directory.
* `python3`: Invoke the Python interpreter to execute scripts.

## Python concepts

* **Variables & Dynamic Typing:** Storing values cleanly in memory under descriptive identifiers.
* **Type Conversion:** Casting string data returned by user input into integers or floats for calculations.
* **Arithmetic & Logic:** Performing basic calculations and managing clean script syntax.

## Problems I encountered

* Encountered path execution errors when attempting to run scripts from parent directories rather than the working file directory.
* Encountered TryHackMe hardware validation warnings regarding incorrect startup drive priorities (mechanical HDD vs. SSD).
* Handled string concatenation bugs in Python where uncasted `input()` values appended numbers instead of adding them mathematically.

## How I solved them

* Resolved path issues by explicitly shifting directories using the `cd` command and verifying paths with `pwd`.
* Corrected hardware builds by removing redundant/slower storage devices to meet the exact 7-component specifications.
* Fixed Python math errors by explicitly wrapping input functions with `int()`.

## Evidence

* Python installation, VS Code workspace configuration, and Git repository initialization.
* Completed Python scripts: `hello.py`, `variables.py`, `student_profile.py`, `study_calc.py`, and `debug_test.py`.
* Completed TryHackMe introductory modules: Computer Hardware, Operating Systems, Data Representation, Data Encoding, The CIA Triad, and Cryptography Concepts.

## Questions I still have

* How do operating systems handle kernel-level context switching under extreme multi-threading loads without introducing security race conditions?

## Tomorrow

* Transition into networking fundamentals: examining the OSI and TCP/IP models, IP addressing schemes, subnetting, and transport layer protocols.
