# Day 23 — Part 3: Understand the Structure of a Sigma Rule

## Looking Inside a Sigma Rule Without Memorizing It Blindly

Now that I understand why Sigma exists and how it differs from writing a search directly in Splunk SPL, the next step is opening up an actual Sigma rule and seeing how it is put together. Sigma rules are written in **YAML**, which is human-readable structured text that relies on clean spacing (spaces rather than tab characters) to show hierarchy.

Here is a simplified example of what a basic Sigma rule looks like:

```yaml
title: Windows Failed Logon Event Observed
id: 929a690e-bef0-4204-a928-ef5e620d6fcc
status: experimental
description: Identifies a Windows Security event associated with a failed logon.
logsource:
    product: windows
    service: security
detection:
    selection:
        EventID: 4625
    condition: selection
level: low
```

Instead of memorizing this snippet line by line and copying it without thinking, I want to understand **what** each field does, **why** it is there, **how** to use it properly in practice, and **what** could go wrong if I get sloppy with it.

## 3.1 `title` — Naming What the Rule Actually Detects

### What It Is and Why It Matters
The `title` is a short name that sums up what the detection rule is looking for. In a busy SOC queue, a pull request review, or a detection dashboard, the title is often the very first thing a human reads. If the title is vague, an analyst wastes time just figuring out what the rule is supposed to catch.

### How to Write a Good `title`
A strong title should be **clear, specific, concise, and descriptive**—focused on the behavior or event being observed rather than generic alarm words.

* **Weak example:** `title: Suspicious Activity` (Too vague—tells another analyst almost nothing.)
* **Strong example:** `title: Windows Failed Logon Event Observed` (Clear, specific, and tells you immediately what event is in scope.)

## 3.2 `id` — Giving Every Rule a Unique Identity

### What It Is and Why It Matters
The `id` field holds a globally unique identifier—best practice is a **UUID version 4**—that uniquely identifies the rule. File names can be renamed, and two teams could write rules with similar titles, so a unique ID gives tools and tracking systems a reliable way to identify the rule.

### How to Generate an `id` Properly
I should **never** copy an `id` from an existing rule when creating a new one of my own. Every new independent rule needs its own freshly generated UUID.

In Python, I can generate one cleanly like this:

```python
import uuid

print(uuid.uuid4())
```

Or directly from the command line when I am working in my terminal:

```bash
python3 -c 'import uuid; print(uuid.uuid4())'
```

As a rule of thumb, I should generate a fresh UUID for each new rule I create (and if I ever make a major logic change that creates a distinct detection, generate a new one rather than reusing an old ID).

## 3.3 `status` — Being Honest About Rule Maturity

### What It Is and Why It Matters
The `status` field tells anyone reading or running the rule how mature and tested it is. A rule I just wrote for a lab exercise is not in the same state as a rule that has been vetted across production telemetry and tuned for noise.

### Common `status` Values

| Status | What It Means |
| :--- | :--- |
| `experimental` | Early-stage rule that still needs testing, validation, or refinement. |
| `test` | More mature rule, though it may still need environment-specific tuning or verification. |
| `stable` | Considered sufficiently mature for production use in appropriate environments. |
| `deprecated` | Replaced or no longer recommended (often tied to another rule). |
| `unsupported` | Cannot be used as-is in its current form (for example, due to missing field support or format constraints). |

### What I Will Use Today
For the rules I write in today's lab, I will use `status: experimental`. I am learning and testing against synthetic data, and **passing YAML syntax validation does not make a rule `stable`**. Labeling something `stable` before real testing and tuning would overstate what I have actually proven.

## 3.4 `description` — Explaining Context Clearly and Calmly

### What It Is and Why It Matters
The `description` explains the detection in plain language so another analyst or reviewer understands the context behind the matching condition.

### How to Write a Useful `description`
A good description should cover four practical things:

1. **What activity** the rule identifies.
2. **What event data** it relies on.
3. **What the analyst should investigate** when it triggers.
4. **Any important limitations** or caveats.

Notice in the example below that it does **not** automatically declare every matching event to be an attack:

```yaml
description: >
  Identifies Windows Security events associated with failed logon attempts.
  Repeated events should be reviewed alongside successful authentication records
  and relevant account context.
```

That distinction matters a lot in real investigations: a single failed logon can easily be a mistyped password, whereas patterns, sources, or context help tell a routine typo apart from something worth deeper investigation.

## 3.5 `references` — Backing Logic with Authoritative Sources

### What It Is and Why It Matters
The `references` field lists links or documentation supporting the detection. Detections should be grounded in documented platform behavior, vendor documentation, or security research rather than guesses or assumptions.

### Example

```yaml
references:
  - https://learn.microsoft.com/en-us/windows/security/threat-protection/auditing/event-4625
```

Citing official documentation like Microsoft's Event `4625` reference makes it much easier for me—and anyone reviewing my work later—to verify what the event actually represents.

## 3.6 `author` — Owning My Work Honestly

### What It Is and Why It Matters
The `author` field identifies who wrote the rule—such as my name or GitHub handle. Clear attribution makes it obvious who maintains a detection when questions come up.

### Integrity Rule
I should use my own identifier for original rules I write myself, and **never** claim an existing SigmaHQ rule or someone else's work as my own original rule. If I learn from an existing example or reference, I should give honest credit and keep my own work clearly attributed.

## 3.7 `date` and `modified` — Tracking Timelines Cleanly

### What They Are and Why They Matter
`date` records when the rule was created, and `modified` tracks when meaningful updates were made to it. Together, they give a clear history of how the detection evolved over time.

### How to Format and Maintain Them
I should use standard ISO calendar dates (`YYYY-MM-DD`), such as:

```yaml
date: 2026-11-08
modified: 2026-11-24
```

When I make a meaningful change to the rule's logic or definition, updating `modified` keeps the timeline accurate.

## 3.8 `logsource` — Defining What Logs the Rule Expects

### What It Is and Why It Matters
`logsource` is one of the most critical parts of a Sigma rule because it describes **what kind of log data** the rule is written for. A detection cannot catch events that were never collected or that come from an unrelated log source.

### Core `logsource` Attributes

* **`product`:** Identifies the product or platform generating the logs—for example, `windows`, `linux`, or `apache` (along with other supported products).
* **`service`:** Identifies a specific service or logging channel within a product. For example:
  ```yaml
  logsource:
    product: windows
    service: security
  ```
  This points specifically to Windows Security event data.
* **`category`:** Describes a logical category of events—such as `process_creation`, `network_connection`, `firewall`, or `webserver`. Categories can group similar event types across products/implementations.
* **`definition`:** Documents additional requirements or context about logging/auditing configuration (for instance, whether specific auditing settings need to be enabled).

### Why Telemetry Availability Comes First
Even the cleanest Sigma rule is useless if the required logs are not collected or the right auditing is not turned on. **A detection's effectiveness depends directly on the availability and quality of its underlying telemetry.**

## How This Applies in the Job Market & How I Will Practice It

In SOC analyst, detection engineer, and security engineering interviews—including at larger or global tech organizations—reviewers look closely at **engineering judgment and honesty**:

* Do you pick an honest maturity level (`experimental` vs. `stable`) instead of inflating status?
* Do you connect detection logic to **telemetry and auditing prerequisites** (`logsource`), knowing that missing logs mean blind spots?
* Do you write clear titles, descriptions, and references so a teammate can pick up your work without guessing?

To practice this properly, I will write small lab rules by hand, generate a fresh UUIDv4 for each one, keep `status: experimental`, verify `logsource` fields against what logs would actually exist, and document every design choice clearly in my notes.

## What to Document & What I Must Remember

* **Document in my Day 23 notes:** Each metadata field (`title`, `id`, `status`, `description`, `references`, `author`, `date`, `modified`) and each `logsource` attribute (`product`, `service`, `category`, `definition`) in my own words, plus a small example rule.
* **Remember:** Generate a fresh UUIDv4 per new rule, keep new lab rules `experimental`, use `YYYY-MM-DD` dates, and treat telemetry availability as prerequisite #1 for any detection.

## Reference Resources

* [Sigma Rules Specification](https://sigmahq.io/sigma-specification/specification/sigma-rules-specification.html)
* [SigmaHQ Rules Documentation](https://sigmahq.io/docs/basics/rules.html)
* [SigmaHQ Logsources Documentation](https://sigmahq.io/docs/basics/log-sources.html)
* [SigmaHQ Rule Conventions](https://github.com/SigmaHQ/sigma-specification/blob/main/sigmahq/sigmahq-rule-convention.md)