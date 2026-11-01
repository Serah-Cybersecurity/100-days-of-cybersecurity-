# HTTP Fundamentals & Web Communication Notes

## 1. What is HTTP?
Hypertext Transfer Protocol (HTTP) is the foundational application-layer protocol used for communication between web clients (browsers) and web servers across a network.

## 2. Difference Between Requests and Responses
* **HTTP Request:** A message sent from a client to a server requesting a resource, specifying an HTTP method, path, headers, and optional body.
* **HTTP Response:** A message returned by a server to a client containing a status code, response headers, and an optional body payload (HTML, JSON, etc.).

## 3. Five HTTP Methods
1. **GET:** Retrieves a resource from a server without altering server state.
2. **POST:** Submits data for processing (e.g., form submission, account login).
3. **PUT:** Creates or completely replaces a resource at a target URL.
4. **PATCH:** Partially modifies an existing resource.
5. **DELETE:** Requests the deletion of a specified resource.

## 4. Ten HTTP Status Codes
1. **200 OK:** Request succeeded.
2. **201 Created:** Request succeeded and a new resource was created.
3. **301 Moved Permanently:** Resource has a permanent redirect.
4. **302 Found:** Temporary redirect.
5. **400 Bad Request:** Request syntax was invalid.
6. **401 Unauthorized:** Authentication required or failed.
7. **403 Forbidden:** Server refuses to fulfill the request due to permissions.
8. **404 Not Found:** Requested resource does not exist.
9. **429 Too Many Requests:** Client is being rate-limited.
10. **500 Internal Server Error:** Server encountered an unexpected failure condition.

## 5. Six Headers and Their Purposes
1. **Host:** Identifies the domain host for HTTP/1.1 requests.
2. **Accept:** Describes media types the client can process.
3. **Content-Type:** Describes the media type of the message body.
4. **Content-Length:** Indicates the size of the message body in bytes.
5. **Cache-Control:** Provides caching directives for clients and proxies.
6. **Location:** Identifies redirect destinations in response messages.

## 6. What are Cookies and Sessions?
* **Cookie:** Small piece of data stored by the browser and sent back to the server.
* **Session:** Mechanism used by applications to maintain authenticated state across multiple stateless HTTP requests.

## 7. Purposes of Secure, HttpOnly, and SameSite Cookie Flags
* **Secure:** Restricts cookie transmission strictly to encrypted HTTPS channels.
* **HttpOnly:** Prevents client-side JavaScript from reading the cookie, mitigating XSS-based theft.
* **SameSite:** Controls cross-site cookie transmission to defend against CSRF attacks.

## 8. Three Security Questions Investigated Using HTTP Evidence
1. Are sensitive session cookies properly protected with `Secure` and `HttpOnly` attributes?
2. Do HTTP request headers or query parameters show evidence of malicious injection payloads?
3. Are server response headers exposing vulnerable software versions or internal configurations?
