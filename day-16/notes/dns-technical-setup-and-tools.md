# Day 16 - Technical Setup and DNS Investigation Tooling

## 1. Setting Up the Lab Environment

Before we dive into heavy packet analysis or write custom Python scripts, we need to make sure our lab environment is locked and loaded. The great news? You don't need any expensive commercial software or complex virtual machine setups. 

We are using the exact setup you already have:
* **Host System:** Windows running Oracle VirtualBox.
* **Guest VM:** Parrot OS Security VM.
* **Core Toolkit:** Wireshark, TShark, Python 3, Git, and standard Linux terminal utilities.

## 2. Checking Your Existing Tools

Whenever you sit down to investigate an incident or run a lab, a good security analyst always checks their toolbox first. Open up your Parrot OS terminal and run these quick verification commands:

```bash
python3 --version
tshark --version
wireshark --version
```

Next, let's check if your DNS lookup utilities are registered in your system's `$PATH`:

```bash
command -v dig
command -v nslookup
```

If everything is set up correctly, you should see file paths returned (like `/usr/bin/dig`).

## 3. Installing DNS Utilities (`dnsutils`)

If `dig` isn't installed on your virtual machine, don't sweat it. You can grab it easily using the Debian package manager. 

Run these commands in your terminal:

```bash
sudo apt update
sudo apt install dnsutils -y
```

Once the installation wraps up, verify it by checking the version:

```bash
dig -v
```

> **Beginner Pro-Tip:** If `apt` throws an error or can't find the package, don't start messing with your `/etc/apt/sources.list` or running risky system upgrades. Just document the error in your lab notes. On standard Parrot OS or Kali builds, `dnsutils` is usually ready to roll out of the box.

## 4. Meet Your Best Friend: `dig` (Domain Information Groper)

Short for **Domain Information Groper**, `dig` is the absolute gold standard for command-line DNS lookups. 

Unlike web browsers or standard OS ping tools—which rely on cached system data—`dig` queries DNS name servers **directly**. It gives you the raw, unedited truth: complete response headers, RCODEs, flags, and exact TTL counts.

### Why Analysts Use It in the Real World
When a SOC analyst gets an alert about a suspicious domain or a potential phishing link, `dig` is usually the very first command they type into their terminal. It lets you instantly check:
* Where a domain points (`A` and `AAAA` records).
* Who handles mail delivery (`MX` records).
* What security policies are in place (`TXT` records for SPF/DMARC).

Get comfortable with `dig`—you'll be using it constantly throughout your cybersecurity journey!
