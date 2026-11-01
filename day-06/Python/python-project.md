# Python Web Investigation Script Report

## 1. Problem Solved
The script automates the process of querying a web server, retrieving HTTP response metadata (status codes, headers), reading raw response bytes, and handling network or protocol errors gracefully without crashing.

## 2. Component Breakdown
* **`urllib.request.urlopen`:** Initiates HTTP connections and retrieves remote resources using the standard library.
* **`urllib.error.HTTPError` & `URLError`:** Catches server-side HTTP failures and network-level connection failures respectively.
* **`try-except` blocks:** Implements resilient error handling to ensure program stability during unexpected network conditions.

## 3. Execution & Output Observations
* **Successful Run:** When the local server was online, the script returned a `200 OK` status, parsed the `Content-Type` header (`text/html`), and printed the first 500 bytes of decoded HTML content.
* **Server-Down Test:** When the local web server was terminated, the script caught the `URLError` exception and reported a connection refused failure cleanly.

## 4. Script Limitations
* Configured specifically for local testing (`127.0.0.1:8000`).
* Reads only a fixed chunk (500 bytes) rather than streaming or parsing the entire document DOM.
* Lacks asynchronous concurrency for scanning multiple endpoints simultaneously.

## 5. Future Improvements
* Add command-line argument parsing (`argparse`) to accept dynamic URLs and port numbers.
* Implement full response body streaming and recursive link parsing.
