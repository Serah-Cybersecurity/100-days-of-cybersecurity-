# Practical Lab Guide: DNS Traffic Capture & Offline Suricata Analysis

**Author:** Serah Mulwa

**Module:** Day 18 - Network Security Monitoring & Intrusion Detection

## 1. Lab Overview & Objectives

In this hands-on lab exercise, we transition from theoretical concepts to practical execution on our Parrot OS virtual machine. Rather than relying on generic, pre-packaged sample files, we capture real network traffic generated from our own workstation, process it offline using Suricata, write custom detection rules, and analyze the resulting telemetry.

### Core Objectives:
1. Identify and verify active network interface controllers in a Linux environment.
2. Capture clean, targeted DNS traffic using `tcpdump` with Berkeley Packet Filter (BPF) expressions.
3. Generate controlled DNS query traffic using `dig`.
4. Replay the resulting packet capture (`.pcap`) offline through Suricata.
5. Verify rule matches against generated alert logs (`fast.log`) and structured JSON telemetry (`eve.json`).

---

## 2. Step-by-Step Lab Execution

### Step 1: Identify Your Active Network Interface
Virtualization environments (such as VirtualBox) assign specific interface names. Never hardcode network interface names without checking your system.

```bash
# Check link status and find the active interface (e.g., enp0s3)
ip -br link

# Check IP address allocations
ip -br addr
```

### Step 2: Start Packet Capture with `tcpdump`
We isolate DNS traffic over UDP port 53 to keep our capture clean and focused.

```bash
sudo tcpdump -i enp0s3 -nn -s 0 -w pcap/dns-example.pcap 'udp port 53'
```

#### Command Flag Breakdown:
* **`-i enp0s3`**: Listens specifically on our active network interface.
* **`-nn`**: Disables reverse DNS and port name resolution, printing raw IP numbers and port numbers for clarity and speed.
* **`-s 0`**: Sets snaplen to infinite, ensuring the entire packet payload is recorded without truncation.
* **`-w pcap/dns-example.pcap`**: Writes raw frames directly into our project's `pcap/` directory.
* **`'udp port 53'`**: BPF filter ensuring we only capture DNS traffic.

### Step 3: Generate Controlled Traffic (`dig`)
While `tcpdump` is running in terminal one, open a second terminal and generate ordinary DNS queries:

```bash
dig +notcp +tries=1 +time=2 example.com A
dig +notcp +tries=1 +time=2 example.com AAAA
```

### Step 4: Stop Capture & Verify PCAP
Return to the first terminal and press `CTRL + C` to stop `tcpdump`. Verify that the PCAP file was successfully created:

```bash
ls -lh pcap/
tcpdump -nn -r pcap/dns-example.pcap
```

---

## 3. Running Suricata Offline Against the PCAP

With our verified `.pcap` file ready, we invoke Suricata in offline detection mode (`-r`) to evaluate the packet stream against our custom ruleset:

```bash
sudo suricata -c /etc/suricata/suricata.yaml -r pcap/dns-example.pcap -l output/
```

### Writing and Testing a Custom Rule
To ensure our traffic triggers an alert, we added a custom rule to `/var/lib/suricata/rules/suricata.rules`:

```text
alert udp any any -> any 53 (msg:"DNS Query Detected"; sid:1000002; rev:1;)
```

After re-running the capture through Suricata, we inspected the generated alert log (`output/fast.log`):

```bash
cat output/fast.log
```

**Observed Output:**
```text
11/04/2026-19:14:10.557921  [**] [1:1000002:1] DNS Query Detected [**] [Classification: (null)] [Priority: 3] {UDP} 10.0.2.15:60749 -> 192.168.100.1:53
```

---

## 4. Key Takeaways & Job Market Relevance

* **Reproducibility:** Capturing your own clean lab PCAPs allows you to test and debug detection rules in an isolated, predictable environment.
* **Filter Discipline:** Using precise BPF filters (`udp port 53`) prevents unnecessary background noise from bloating your capture files.
* **Offline Forensics:** In real-world incident response, SOC analysts frequently ingest historical PCAP captures into Suricata or Wireshark to reconstruct attacker activity post-incident.
