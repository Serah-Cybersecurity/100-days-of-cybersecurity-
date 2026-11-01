# URL Anatomy & Web Architecture Notes

## 1. What is a URL?
A Uniform Resource Locator (URL) is the standardized address string used by web clients to locate, identify, and access resources (such as web pages, images, and API endpoints) across a network.

## 2. Main Components of a URL
* **Scheme:** The protocol used to communicate (e.g., `http`, `https`, `ftp`).
* **Host / Domain Name:** The human-readable label identifying the target server (e.g., `example.com`).
* **Path:** The specific file location or application route on the server (e.g., `/products/item`).
* **Query String:** Key-value parameters passed to the server for dynamic processing (e.g., `?category=shoes&sort=asc`).
* **Port (Optional):** The explicit network port number used to connect (e.g., `:443` or `:8443`).
* **Fragment (Optional):** A client-side anchor (`#section`) processed entirely by the browser and never transmitted to the server in HTTP requests.

## 3. Hostname vs. IP Address
* **Hostname:** A human-friendly text alias (`example.com`) designed for easy human memorization.
* **IP Address:** The numeric routing address (`93.184.216.34`) used by routers and network cards to physically route data packets across the internet. DNS bridges the two.

## 4. The Purpose of a Path
The path tells the web server which specific file, directory, or application route the client wants to access. It mirrors a file directory structure (e.g., `/images/logo.png`) or maps to dynamic application endpoints (e.g., `/api/v1/users`).

## 5. The Purpose of a Query String
Query strings allow clients to send dynamic data variables to the server using key-value pairs separated by ampersands (`&`). They are heavily used in search bars, filters, and form submissions.

## 6. Three Examples of URLs in Security Investigations
1. **Phishing & Typosquatting:** Analyzing a deceptive hostname (e.g., `micros0ft-support.com`) designed to impersonate a trusted enterprise brand.
2. **Web Application Attack Payloads:** Spotting malicious script tags or SQL injection strings injected directly into query parameters (e.g., `?id=1' OR '1'='1`).
3. **Open Redirect Vulnerabilities:** Identifying external URLs embedded within query parameters that trick authentication portals into redirecting victims to malicious third-party sites after login.
