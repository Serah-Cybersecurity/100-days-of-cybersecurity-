# Day 7 - Errors and Exception Handling in Python

## 1. The Three Categories of Programming Errors

### Syntax Errors
* **Definition:** Grammatical errors in code structure that prevent Python from parsing or compiling the script.
* **Cybersecurity Relevance:** Caught immediately before execution. Usually caused by typos, missing colons, or unclosed parentheses.

### Runtime Errors (Exceptions)
* **Definition:** Errors that occur while the program is actively running when an operation cannot be completed.
* **Cybersecurity Relevance:** Examples include `FileNotFoundError` (missing log files) or `json.JSONDecodeError` (corrupted SIEM logs). Handled using `try` and `except` blocks.

### Logical Errors
* **Definition:** Flaws in program design where the script runs without crashing but yields incorrect analytical outputs.
* **Cybersecurity Relevance:** The most dangerous error type in security analytics. A flawed threshold condition or inverted operator will silently miss real threats or produce false alarms without throwing any exception.

## 2. Defensive Programming & Validation Best Practices
* **Never assume external file integrity:** Always wrap file I/O and JSON parsing in `try-except` blocks.
* **Validate data types explicitly:** Use `isinstance(data, list)` to verify top-level structures and `enumerate()` to check individual records before processing.
* **Never fail silently:** Always log or report malformed data rather than ignoring it, ensuring complete audit trails for security investigations.
