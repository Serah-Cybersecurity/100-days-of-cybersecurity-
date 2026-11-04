# Firewall Fundamentals, ACLs, and Network Segmentation

**Author:** Serah Mulwa  
**Date:** November 4, 2026  
**Module:** Day 17 - Network Control & Boundary Defence  

---

## 1. Introduction to Boundary Defence

In enterprise security, a perimeter is only as strong as its boundary controls. While Day 15 and Day 16 focused on packet observation and DNS telemetry, Day 17 shifts directly into **active enforcement**: how network infrastructure controls traffic flow, isolates sensitive subnets, and blocks unauthorized communication. 

This reference note explores the operational mechanics of firewalls, Access Control Lists (ACLs), evaluation logic, and network segmentation principles.

---

## 2. Stateful vs. Stateless Firewalls

Understanding how a firewall evaluates incoming and outgoing packets is essential for both network engineers and security analysts.

### 2.1 Stateless (Packet Filtering) Firewalls
* **How it works:** A stateless firewall inspects every single packet in complete isolation. It relies strictly on static matching criteria (the five-tuple: Source IP, Destination IP, Source Port, Destination Port, and Protocol).
* **The Limitation:** It has no memory of connection context. If an administrator creates a rule allowing inbound HTTPS (Port 443) traffic to a web server, the stateless firewall evaluates every incoming packet independently, unable to easily distinguish between a legitimate ongoing session and a spoofed attack packet.

### 2.2 Stateful Firewalls
* **How it works:** A stateful firewall maintains a **connection state table** that tracks the lifecycle of active communications.
* **Key Connection States:**
  * `NEW`: A connection is being initiated (e.g., a TCP SYN packet).
  * `ESTABLISHED`: Traffic belongs to an active, successfully handshaked connection (subsequent packets pass automatically without re-evaluating rules).
  * `RELATED`: Traffic is logically tied to an existing session (e.g., an FTP data channel spawned from an established control channel).
  * `INVALID`: Packets that do not match any valid state are dropped immediately.
* **Why it matters in the job market:** When reviewing firewall logs, a stateful firewall significantly reduces log volume because return traffic for authorized outbound connections is permitted dynamically without requiring redundant inbound rules.

---

## 3. Firewall Actions: Allow, Block, Drop, and Reject

When a firewall rule matches a packet, it enforces one of four primary actions:
1. **Allow:** Actively permits matching traffic to cross the interface.
2. **Block / Drop:** Silently discards the packet without sending any notification back to the sender. This is preferred for security and stealth, causing an attacker's scan to time out.
3. **Reject:** Denies the packet *and* actively returns an ICMP "Destination Unreachable" message back to the sender. Useful on internal networks where legitimate applications need instant failure feedback.

---

## 4. Access Control Lists (ACLs) & Rule Ordering

An **Access Control List (ACL)** is an ordered sequence of rules applied to network interfaces to filter traffic.

### 4.1 The "First Match Wins" Principle
ACLs are evaluated **top-to-bottom, sequentially**. 
* The moment a packet satisfies the matching criteria of a rule, that rule's action (`permit` or `deny`) is executed immediately. **All remaining rules below it are ignored.**
* **The Implicit Deny:** At the absolute bottom of every standard and extended ACL sits an invisible, automatic rule: `deny ip any any`. If a packet passes through all explicit rules without matching any of them, it is dropped by default.

### 4.2 Practical Policy Analysis
Consider this sample ACL:
```text
Rule 1: Source 192.0.2.10  -> Destination 198.51.100.20  -> Service TCP 443  -> Action: PERMIT
Rule 2: Source 192.0.2.0/24 -> Destination Any             -> Service TCP 22   -> Action: DENY
Rule 3: Source Any          -> Destination Any             -> Service Any      -> Action: DENY (Implicit)
```
* **Analysis:** Workstation `192.0.2.10` can reach the destination server over HTTPS (`TCP 443`) via Rule 1. However, any attempt by other hosts on the subnet to SSH (`TCP 22`) hits Rule 2 and is blocked. 
* **Design Rule:** Specific rules must always be placed *above* broad or general rules. Placing a broad rule (`permit ip any any`) at the top would shadow and invalidate all rules beneath it.

---

## 5. Network Segmentation & Least Privilege

### 5.1 Network Segmentation
Segmentation divides a large flat network into isolated subnetworks (VLANs). For example, separating **Finance**, **HR**, and **Guest Wi-Fi** prevents a compromised guest laptop from pivoting laterally into sensitive accounting databases.

### 5.2 The Principle of Least Privilege
The core philosophy of firewall engineering is giving users, devices, and applications **only the minimum network access necessary** to perform their duties, and nothing more. Avoid lazy `any-to-any` rules and regularly audit rulesets for obsolete entries.

---

## 6. What to Remember & Document
* **Remember:** Order matters completely in ACLs; specific rules first, broad rules last.
* **Document:** Always record the business justification, owner, and expected traffic flow for every new firewall rule or exception added to production environments.
