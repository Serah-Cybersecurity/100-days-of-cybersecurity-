# Day 9 Test Results

## Environment

- Operating system: Parrot OS (Linux)
- Python version: Python 3.x
- Test date: October 29, 2026

## Test cases

| Test | Expected result | Actual result | Status |
|---|---|---|---|
| Normal run | Metadata is printed | Successfully scanned and printed metadata for all lab files and directories (`permissions-lab/`, `notes.txt`, `private/`, `shared/`) | Passed |
| Empty directory | No entries message | Correctly reported that no entries were found when targeted at an empty test directory | Passed |
| Missing directory | Configuration error | Caught `FileNotFoundError` and reported a clean configuration error message | Passed |
| Mode 777 | Entry flagged for review | Successfully detected `test-777.txt` and triggered both ordinary mode `777` and world-writable review flags | Passed |
| Mode restored | Numeric mode is 600 | Verified via `stat` that `test-777.txt` successfully restored to mode `600` (`-rw-------`) after testing | Passed |

## Issues encountered

No critical errors encountered during test execution. Initial path resolution was handled correctly using `pathlib.Path.home()`.

## Limitations

The permissions auditor is an educational learning tool and does not evaluate:
- Access Control Lists (ACLs).
- Mandatory Access Control (MAC) policies (SELinux / AppArmor).
- Contextual business purpose or file content sensitivity.
- File integrity or cryptographic signatures.
