# Day 13 Case Context

## Environment
This is a synthetic multi-source security monitoring exercise.

## Systems
- WIN-LAB-01: Windows workstation
- LINUX-LAB-01: Linux server
- FW-LAB-01: Firewall

## Supplied Baseline
- `192.0.2.44` is an approved administrative source (RFC 5737 Test-Net-1).
- `198.51.100.27` is **not** listed as an approved administrative source (RFC 5737 Test-Net-2).
- The `backup-agent` service is expected to start around `08:30`.

## Investigation Objective
Identify unusual authentication patterns and examine related events across the supplied sources.

## Limitations
- The dataset contains only eleven records.
- The records are synthetic.
- There is no complete session history.
- There are no packet captures.
- There are no complete endpoint process trees.
- No conclusion about a real compromise is possible.
