# Day 6 Capstone Project - Local Web Request Investigation Lab

## 1. Project Overview
This project establishes a complete local web environment to investigate the relationship between clients, servers, HTTP requests, responses, HTML/CSS rendering, and automated script interaction. Built entirely offline without commercial hosting, it serves as a reproducible sandbox for web fundamentals and security analysis.

## 2. Learning Objectives
* Master the 8-step web request lifecycle and URL anatomy.
* Understand HTTP methods, status codes, headers, cookies, and session management.
* Author semantic HTML5 documents and modular CSS stylesheets.
* Host a local development server using Python 3 (`http.server`).
* Inspect live network traffic via browser Developer Tools.
* Write automated Python networking scripts using standard-library modules (`urllib`).
* Apply foundational web security concepts (AuthN/AuthZ, input validation, XSS, SQLi).

## 3. Tools Used
* **Operating System:** Windows Host / PowerShell
* **Language / Scripting:** Python 3.14.7
* **Editor:** Visual Studio Code
* **Version Control:** Git & GitHub
* **Browser:** Google Chrome / Microsoft Edge Developer Tools

## 4. Architecture & Data Flow
1. **Client (Browser / Python Script):** Formulates an HTTP GET request targeting `http://127.0.0.1:8000/`.
2. **Transport / Network Stack:** Routes traffic over loopback (`127.0.0.1`) via TCP port 8000.
3. **Server (Python `http.server`):** Receives the request, parses the URI path, reads requested files (`index.html`, `style.css`) from disk, and returns HTTP responses with appropriate status codes (`200 OK`, `404 Not Found`).
4. **Rendering / Parsing:** The browser parses HTML DOM elements and applies CSS presentation rules to render the user interface.

