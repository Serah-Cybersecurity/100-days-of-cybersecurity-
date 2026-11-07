# Technical Note: Laboratory Environment Provisioning, Workspace Architecture & Resource Discipline

**Author:** Serah Kathini Mulwa  
**Program:** Women Techsters Fellowship — Cybersecurity Track  
**Module:** Day 21 — SIEM Architecture, Log Ingestion & Security Data Engineering  

---

## 1. Executive Summary & Personal Reflections

In security engineering, technical capability is demonstrated not just by writing code, but by the discipline with which you construct your working environment. Before ingesting raw log telemetry or writing normalization parsers, a professional engineer verifies system stability, resource limits, dependencies, and workspace separation.

A common mistake when starting out with SIEM concepts is attempting to install heavy enterprise platforms (such as a full multi-node Wazuh cluster) directly inside a local virtual machine without auditing hardware capacity. Official Wazuh documentation recommends a minimum of **4 vCPUs, 8 GiB RAM, and 50 GB of disk storage** for a small all-in-one deployment. Attempting to run an enterprise-scale SIEM alongside active log generators on a resource-constrained development laptop leads to system throttling and crashes.

On Day 21, I took an engineering-first approach: provision a lean, highly structured Linux environment on Parrot OS, build an isolated Python 3 virtual environment (`.venv`), enforce zero external dependency bloat by leveraging Python’s standard library, and design a production-grade directory hierarchy to handle raw inputs, normalized events, and quarantine dead-letter queues.

---

## 2. Environment Diagnostics & System Verification

Before initiating pipeline development, I performed diagnostic checks to establish baseline operating metrics (kernel, CPU architecture, memory availability, and disk capacity).

### Verification Commands & Executed Outputs:

```bash
whoami
hostname
uname -a
python3 --version
git --version
free -h
df -h
```

### Diagnostic Assessment:

* **User Context & System Identity:** Executed as user `user` on host `parrot`.
* **Kernel & OS Build:** Linux `7.0.9+parrot7-amd64` (x86_64 architecture running Debian-based Parrot Security OS).
* **Runtime & Version Control:** Python `3.13.5` and Git `2.47.3` verified.
* **Memory Allocation (`free -h`):** 3.8 GiB total RAM, 1.3 GiB used, 1.4 GiB free, and 2.5 GiB available. This confirms sufficient headroom for in-memory streaming without risking Out-of-Memory (OOM) crashes.
* **Disk Capacity (`df -h`):** Main root partition (`/dev/sda2`) allocated 64 GB with 41 GB available (34% utilization), providing ample disk space for log storage, quarantine dead-letter queues, and report outputs.

---

## 3. Package Management & Dependency Strategy

In high-security enterprise environments, package bloat introduces unnecessary software supply-chain risks and dependency conflicts. I updated the local package indices while keeping installed tools minimal.

```bash
sudo apt update
sudo apt install python3 python3-venv python3-pip git
```

### Dependency Architecture Decision:

Rather than pulling in external third-party parsing libraries, my ingestion pipeline script relies strictly on Python's built-in standard library modules (`json`, `pathlib`, `sys`, `datetime`, `argparse`). 

Building data pipelines with the standard library ensures:
1. **Zero External Vulnerabilities:** Eliminates third-party package security risks.
2. **Instant Reproducibility:** The project runs natively on any system with Python 3 installed without requiring complex `pip install` setups.
3. **Execution Speed:** Avoids heavy framework overhead during streaming operations.

---

## 4. Production Workspace Directory Architecture

A flat project folder where logs, scripts, reports, and screenshots are mixed together is unacceptable in production security engineering. I constructed a directory hierarchy that enforces strict **separation of concerns**:

```bash
mkdir -p ~/cybersecurity/day21-mini-siem
cd ~/cybersecurity/day21-mini-siem
mkdir -p data/raw data/processed data/quarantine reports screenshots src tests docs
```

### Architectural Breakdown:

```
day21-mini-siem/
├── data/
│   ├── raw/          # Preserves untouched input logs (maintains evidentiary lineage)
│   ├── processed/    # Stores cleaned, ECS-normalized JSONL events
│   └── quarantine/   # Stores malformed/corrupt records (Dead-Letter Queue)
├── docs/             # Holds architectural specifications & technical notes
├── reports/          # Stores automated ingestion metrics and data-quality reports
├── screenshots/      # Contains terminal output visual proofs
├── src/              # Source code directory for ingestion and normalization scripts
├── tests/            # Automated test suites for schema validation
├── README.md         # Project entry point and documentation
└── requirements.txt  # Project dependency manifest
```

---

## 5. Isolated Python Virtual Environment (`.venv`) Setup

To prevent pollution of system-level Python packages and guarantee project isolation, I configured and activated a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
which python
```

### Verification Result:
Executing `which python` returns `/home/user/cybersecurity-journey/day21-mini-siem/.venv/bin/python`, confirming that the shell is operating exclusively within the isolated virtual environment context.

---

## 6. Verification Checklist

| Environment Verification | Terminal Command / Artifact | Status |
| :--- | :--- | :--- |
| **System Diagnostics** | `day21-01-environment-check.png` | Validated (`whoami`, `uname`, `free -h`, `df -h`) |
| **Toolchain Integrity** | `day21-02-package-updates.png` | Validated (Python 3.13.5, Git 2.47.3) |
| **Directory & Virtual Env** | `day21-03-directory-structure-and-venv.png` | Validated (`.venv` activated, `which python` verified) |
