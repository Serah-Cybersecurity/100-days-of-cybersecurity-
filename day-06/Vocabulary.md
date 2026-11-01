# Day 6 Comprehensive Web & Security Glossary

## 1. Core Web Architecture & Infrastructure

* **World Wide Web:** An interconnected global information space made up of web pages, documents, and digital resources linked together via URLs, accessed over the internet using network protocols.
* **Client:** Any software program or physical device (such as a web browser, mobile application, or custom Python script) that initiates a connection to request data or services from a server.
* **Server:** A dedicated computer or software daemon running on a network that listens for incoming client requests, processes them, and returns the requested data, files, or services.
* **URL (Uniform Resource Locator):** The global address of a specific resource on the internet, specifying the protocol scheme, domain hostname, network port, file path, and optional query parameters.
* **Hostname:** A human-readable label assigned to a device or server connected to a network (e.g., `example.com`), which is translated into a numeric IP address by DNS.
* **DNS (Domain Name System):** The decentralized "phonebook" of the internet that automatically translates user-friendly domain hostnames into machine-readable IP addresses over UDP port 53.
* **Localhost:** A standard hostname alias (`localhost`) that always points directly back to your own local computer.
* **Loopback address:** The reserved IP address (`127.0.0.1`) used by a device's operating system to route network traffic internally back to itself, enabling offline development and testing.
* **Port:** A logical 16-bit numerical endpoint identifier (ranging from 0 to 65535) used by operating systems to direct incoming network traffic to the correct software application or service.
* **Web server:** Software running on a host machine (such as Python's `http.server`, Nginx, or Apache) that handles incoming HTTP requests, reads files from disk, and serves web assets to clients.

---

## 2. HTTP Protocol & Message Structure

* **HTTP (Hypertext Transfer Protocol):** The foundational text-based application-layer protocol that governs how web clients and servers format and exchange messages.
* **HTTPS (HTTP Secure):** The secure version of HTTP where all communication traffic is encrypted and authenticated using TLS, protecting data against eavesdropping and tampering.
* **TLS (Transport Layer Security):** A cryptographic protocol that provides secure, encrypted, and tamper-proof communication channels over computer networks.
* **Request:** A structured text message sent from a client to a server, consisting of a request line (method and path), headers, and an optional body payload.
* **Response:** A structured text message returned by a server to a client, consisting of a status line (protocol, status code, and reason phrase), headers, and an optional response body.
* **HTTP method:** A verb (such as `GET`, `POST`, `PUT`, `PATCH`, or `DELETE`) that tells the server what intended action to perform on a resource.
* **Status code:** A 3-digit numeric code returned in an HTTP response indicating the result category of the request (e.g., `200 OK`, `404 Not Found`, `500 Internal Server Error`).
* **Header:** Key-value metadata pairs attached to an HTTP request or response that provide environmental context, configuration rules, or security directives.
* **Request body:** The auxiliary data payload transmitted alongside a request (such as form input values or JSON data) during `POST` or `PUT` operations.
* **Response body:** The primary payload data returned by the server inside a response message, such as HTML code, JSON application data, or image bytes.
* **Cookie:** A small snippet of data stored locally in the browser by a server via the `Set-Cookie` header and sent back automatically in subsequent requests.
* **Session:** An application-level mechanism used to track and recognize a specific authenticated user across multiple independent, stateless HTTP requests.

---

## 3. Web Technologies & Inspection

* **HTML (HyperText Markup Language):** The foundational markup language that uses nested tags to define the structure, outline, and semantic meaning of content on a webpage.
* **CSS (Cascading Style Sheets):** A stylesheet language used to control the visual presentation, typography, layout, and aesthetic formatting of HTML documents.
* **JavaScript:** A high-level, dynamic programming language that executes inside the browser to add interactive behaviors, animations, and dynamic application logic to web pages.
* **Browser Developer Tools:** Built-in diagnostic suites within modern browsers (opened via `F12` or Inspect) that allow developers and security analysts to inspect DOM elements, monitor live network traffic, and debug code.

---

## 4. Web Application Security Fundamentals

* **Authentication:** The process of verifying *who* a user or system is (answering the question: "Who is making this request?", usually via credentials or tokens).
* **Authorization:** The process of determining whether an authenticated identity is *permitted* to perform a specific action or access a protected resource.
* **Input validation:** The critical security practice of inspecting, filtering, and validating incoming user data against strict defined rules on the server side before processing or storing it.
* **XSS (Cross-Site Scripting):** A web vulnerability where untrusted user input is improperly handled by an application and rendered as executable JavaScript in a victim's browser.
* **SQL injection:** A vulnerability where untrusted user input is improperly concatenated directly into a database query string, allowing attackers to manipulate backend database logic and data.

---

## 5. Analytical Methodology & Investigation

* **Evidence:** Empirical, verifiable data and observations extracted directly from raw logs, network captures, or system artifacts to support an investigation.
* **Interpretation:** A reasoned explanation or hypothesis of what observed evidence means within a given operational context.
* **Limitation:** A strict boundary or constraint on what can be logically concluded from available evidence, protecting analysts from making unproven or overgeneralized claims.
