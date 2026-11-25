# Technical Note: Environment Provisioning, APT Pinning, & Zeek Installation

**Author:** Serah Mulwa

**Module:** Day 19 - Network Threat Hunting with Zeek

## 1. Executive Summary

Before conducting network threat hunting and protocol analysis, establishing a clean, structured, and reproducible technical environment is essential. 

This technical note documents the complete environment setup on Parrot OS (running within VirtualBox on a Windows host), detailing the creation of a standardized project repository, system tool inspections, and the successful resolution of Linux package dependencies to install **Zeek LTS (Version 9.0.1)** using official openSUSE Debian repositories and APT pinning.

## 2. Project Directory Architecture

To maintain organization during forensic investigations and threat-hunting exercises, we established a structured project directory tree under `~/cybersecurity-journey/day-19/`:

```
day-19/
├── pcap/              # Stores raw packet capture (.pcap) files
├── output/            # Contains generated Zeek log outputs (conn.log, dns.log, etc.)
├── scripts/           # Custom Zeek policy scripts and Python analysis utilities
├── notes/             # Technical notes and portfolio documentation (.md files)
├── reports/           # Final incident reports and triage summaries
└── screenshots/       # Terminal execution proof and verification captures
```

### Directory Initialization Commands:

```bash
mkdir -p ~/cybersecurity-journey/day-19/{pcap,output,scripts,notes,reports,screenshots}
cd ~/cybersecurity-journey/day-19
pwd
```

## 3. System Tool Inspection

Before installing new security packages, we inspected the underlying operating system and existing toolchain:

* **OS Release:** Parrot Security 7.4 (echo) — Debian-derived Linux distribution.
* **Python Version:** Python 3.13.5
* **Packet Capture & Parsing:** `tcpdump` (v4.99.5), `libpcap` (v1.10.5), and `jq` (v1.7) for command-line JSON parsing.

```bash
cat /etc/os-release
python3 --version
tcpdump --version
jq --version
```

## 4. Resolving Linux Package Dependencies & Installing Zeek 9.0.1

### A. The Dependency Challenge

When initially attempting to install Zeek via Parrot's default system repositories (`sudo apt install -y zeek`), the package manager encountered a dependency conflict with system library `libc6` versions. 

### B. The Professional Resolution: APT Pinning & Official Repositories

Rather than mixing incompatible third-party sources or breaking system stability, we resolved this by adding the official openSUSE security repository for Zeek on Debian 12 and configuring APT pinning to prioritize official builds:

1. **Add Official Zeek Repository Source:**
   ```bash
   echo 'deb http://download.opensuse.org/repositories/security:/zeek/Debian_12/ /' | sudo tee /etc/apt/sources.list.d/security.zeek.list
   ```

2. **Import Repository Signing Key:**
   ```bash
   curl -fsSL https://download.opensuse.org/repositories/security:/zeek/Debian_12/Release.key | gpg --dearmor | sudo tee /etc/apt/trusted.gpg.d/security_zeek.gpg > /dev/null
   ```

3. **Configure APT Pinning (`/etc/apt/preferences.d/zeek`):**
   ```bash
   echo -e "Package: zeek*\nPin: origin download.opensuse.org\nPin-Priority: 1001" | sudo tee /etc/apt/preferences.d/zeek
   ```

4. **Update and Install Zeek LTS 9.0.1:**
   ```bash
   sudo apt update
   sudo apt install -y zeek jq tcpdump
   ```

5. **Verify Installation and Update Path:**
   ```bash
   /opt/zeek/bin/zeek --version
   echo 'export PATH=$PATH:/opt/zeek/bin' >> ~/.bashrc
   source ~/.bashrc
   ```
   * **Verified Version:** `zeek version 9.0.1`

## 5. Validating Zeek Execution Against Sample PCAPs

To test our environment, we processed an offline packet capture (`dns-example.pcap`) and validated the generated telemetry logs:

```bash
zeek -C -r ../day-18/pcap/dns-example.pcap -o output/
ls -l output/
```

### Generated Output Files:
* `conn.log` — Connection telemetry and 5-tuple session summary.
* `dns.log` — DNS request and response records.
* `packet_filter.log` — BPF compilation log.

## 6. Key Takeaways

* **Structured workspaces prevent data loss:** Keeping raw PCAPs, scripts, and output logs separated into dedicated folders is standard SOC engineering practice.
* **APT pinning solves dependency conflicts safely:** Utilizing official project repositories with explicit priority pinning avoids breaking Parrot OS system libraries.
* **Zeek LTS 9.0.1 is fully operational:** Our Parrot OS environment is primed for advanced protocol analysis and threat hunting.
