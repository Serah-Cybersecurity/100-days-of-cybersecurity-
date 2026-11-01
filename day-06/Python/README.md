# Day 6 — Python Local HTTP Server & Client-Server Logging

## 1. Overview
This module demonstrates the practical relationship between an HTTP client (web browser) and an HTTP server using Python's built-in `http.server` module. By hosting a custom HTML webpage locally, empirical access logs are captured to analyze real-time request-response mechanics, status codes, and network traffic behavior.

---

## 2. Objectives
* Spin up a lightweight local web server using Python 3.
* Host custom HTML files (`index.html`) on a local socket (`localhost:8000`).
* Observe and record real-time incoming client requests in the terminal access logs.
* Interpret HTTP status codes (`200 OK` vs. `404 Not Found`) from raw server logs.

---

## 3. Environment & Execution
* **Operating System:** Windows Host / PowerShell
* **Language / Interpreter:** Python 3.14.7
* **Execution Command:**
  ```bash
  python3 -m http.server 8000
