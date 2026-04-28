# SigmaForge

> **Sigma rule writer, validator, and multi-backend converter — for detection engineers who want to actually understand what their rules do.**

![Python](https://img.shields.io/badge/python-3.10%2B-blue?style=flat-square&logo=python)
![License](https://img.shields.io/badge/license-MIT-green?style=flat-square)
![Status](https://img.shields.io/badge/status-alpha-orange?style=flat-square)

---

## What It Does

SigmaForge wraps the [pySigma](https://github.com/SigmaHQ/pySigma) ecosystem in a CLI that's ergonomic enough to use during rule authoring, with output that's friendly to both humans and CI pipelines.

**Three jobs:**

- **Validate** — parse a Sigma rule against the official spec, surface syntax + structural errors before they hit prod.
- **Convert** — translate a rule to your SIEM's query language. Splunk SPL and Elastic Lucene are supported in v0.1, more on the roadmap.
- **Inspect** — show what a rule actually does (logsource, detection summary) without hand-reading the YAML.

---

## Installation

```bash
git clone https://github.com/B0bTheSkull/sigmaforge.git
cd sigmaforge
pip install -e .
```

Or, once published to PyPI:

```bash
pip install sigmaforge
```

---

## Usage

### Validate a rule

```bash
sigmaforge validate examples/rules/ssh_failed_password.yml
```

```
OK ssh_failed_password.yml — valid
  ID:         1a2b3c4d-5e6f-7890-abcd-ef1234567890
  Title:      Failed SSH Password Authentication
  Status:     experimental
  Logsource:  product=linux, service=auth
  Detection:  1 selection(s), condition: failed_password
```

Exit code is `0` for valid, `1` for invalid, `2` for usage errors. Drop it into a pre-commit hook or a CI step that runs against every rule in your detection repo.

### Convert a rule to Splunk SPL

```bash
sigmaforge convert examples/rules/web_scanner_useragent.yml --target splunk
```

```
=== web_scanner_useragent.yml -> splunk ===
cs-user-agent IN ("*Nikto*", "*sqlmap*", "*nuclei*", "*dirbuster*", "*gobuster*", "*wfuzz*", "*masscan*", "*Nmap Scripting Engine*")
```

### Convert to Elastic Lucene

```bash
sigmaforge convert examples/rules/suspicious_sudo.yml --target elastic
```

### List supported targets

```bash
sigmaforge list-targets
```

---

## Why I Built This

Sigma is the closest thing detection engineering has to a portable rule format — and the official `sigma-cli` is great, but I wanted something thinner and more conversational for the rule-authoring loop. SigmaForge is what I reach for when I'm iterating on a detection and want a fast "does this parse / what does it look like in Splunk?" turnaround.

It's also the natural next step in my detection portfolio after [LogHound](https://github.com/B0bTheSkull/loghound) and [HoneyNet](https://github.com/B0bTheSkull/honeynet) — moving from "find anomalies in logs" to "express anomalies as portable, reviewable detection logic."

---

## Example Rules

The `examples/rules/` directory contains three rules that mirror real detections from my other tools, so you can see the full pipeline:

| Rule | Mirrors | MITRE |
|------|---------|-------|
| `ssh_failed_password.yml` | LogHound auth-log brute force | [T1110.001](https://attack.mitre.org/techniques/T1110/001/) |
| `suspicious_sudo.yml` | LogHound sudo escalation | [T1548.003](https://attack.mitre.org/techniques/T1548/003/) |
| `web_scanner_useragent.yml` | LogHound web-log scanner detection | [T1595.002](https://attack.mitre.org/techniques/T1595/002/) |

---

## Roadmap

- [ ] Chronicle YARA-L backend
- [ ] Microsoft Sentinel KQL backend
- [ ] `test` subcommand: run a rule against a sample log file and report matches
- [ ] `template` subcommand: scaffold a new rule from an example log line
- [ ] Bulk directory validation (`sigmaforge validate rules/`)
- [ ] JSON output mode for SIEM-pipeline integration

---

## Contributing

Issues and PRs welcome. For new backends, please add a corresponding test in `tests/test_converter.py`.

---

## License

MIT — see [LICENSE](LICENSE)
