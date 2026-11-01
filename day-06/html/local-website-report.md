# Local Website Project Report

## 1. Objective
Build, host, and inspect a local web application using Python 3 and HTML/CSS to understand real-time client-server communication, request-response lifecycles, and access log analysis.

## 2. Environment
* **Operating System:** Windows Host / PowerShell
* **Python Version:** Python 3.14.7
* **Browser:** Google Chrome / Microsoft Edge
* **Code Editor:** Visual Studio Code

## 3. Files Created
* `day-06/html/index.html` (Document structure and content)
* `day-06/html/style.css` (Presentation and styling rules)

## 4. Server Command & URL
* **Command Used:** `python -m http.server 8000 --bind 127.0.0.1`
* **Local Access URL:** `http://127.0.0.1:8000/`

## 5. Observations & HTTP Evidence
* **Page Load Behavior:** Upon navigating to `http://127.0.0.1:8000/`, the browser issued a `GET / HTTP/1.1` request. The Python server returned a `200 OK` status code along with the HTML payload. 
* **Stylesheet Request:** Upon parsing the HTML, the browser automatically issued a secondary `GET /style.css HTTP/1.1` request, which the server successfully fulfilled with a `200 OK` status code.

## 6. Changes Tested
* **HTML Modification:** Editing text inside `index.html` and reloading updated the DOM tree instantly upon browser refresh.
* **CSS Modification:** Altering styling rules in `style.css` instantly modified visual presentation without altering underlying content.

## 7. Troubleshooting Log
* *No blocking errors encountered; file paths and port bindings verified successfully.*

## 8. Security Considerations
* **Why bind to `127.0.0.1`?** Restricting the server to the loopback interface prevents unauthorized external network exposure during development.
* **Why is Python's `http.server` unsuitable for production?** It lacks enterprise security features, encryption controls, high-concurrency performance tuning, and robust access controls.

## 9. Lessons Learned
Successfully bridged theoretical networking concepts (IPs, ports, protocols) with practical application layer execution, observing real-time HTTP requests in server logs.
