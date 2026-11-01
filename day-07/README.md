# Day 7 - Python Security Log Analyzer

## Project Overview
The **Python Security Log Analyzer** is a robust, beginner-friendly command-line tool built to ingest, validate, parse, and analyze structured JSON security event logs. It automates the detection of failed authentication attempts, aggregates event metrics by type and username, and implements defensive programming techniques to handle malformed data and missing fields gracefully.

## Learning Objectives
* Practiced core Python fundamentals: variables, conditional boundary categorization, and dynamic loops.
* Implemented modular code structure using custom functions and Python's built-in `pathlib` library.
* Mastered JSON file handling and defensive exception handling (`try...except`, `json.JSONDecodeError`, `FileNotFoundError`).
* Built automated unit tests using Python's native `unittest` testing framework.

## Tools Used
* **Language:** Python 3.14
* **Data Format:** JSON (JavaScript Object Notation)
* **Version Control:** Git & GitHub
* **Environment:** Windows PowerShell, Visual Studio Code

## Dataset
The project utilizes fictional training datasets stored in `day-07/data/`. These records simulate standard authentication and system access logs for educational analysis.

## How to Run
~To run the automated unit test suite:

`python -m unittest discover -s tests -v`


~To execute the primary security log analyzer from the `day-07` directory, run:
```powershell
python .\python\security_log_analyzer.py



