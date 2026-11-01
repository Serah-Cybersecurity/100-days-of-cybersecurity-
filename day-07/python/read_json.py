# Day 7 — Reading and Parsing JSON Files

import json
from pathlib import Path

# Build a robust relative path to our sample_events.json file
DATA_FILE = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "sample_events.json"
)

# Open the file safely using a context manager ('with' statement)
with DATA_FILE.open("r", encoding="utf-8") as file:
    # Parse the JSON text into native Python objects (List of Dictionaries)
    events = json.load(file)

# Output our analysis results
print("Number of records:", len(events))
print("First record:", events[0])