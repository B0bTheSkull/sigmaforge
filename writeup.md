# SigmaForge — Building a Detection Engineer's Pocket Knife

> First post in what I hope becomes a series on detection engineering. This one's about why I built [SigmaForge](https://github.com/B0bTheSkull/sigmaforge), what Sigma rules actually are, and the specific gap in the existing tooling that pushed me to write yet another CLI.

---

## The problem

If you've ever sat in an interview for a SOC role, you know the question: "How would you write a detection for X?" The honest answer for most junior candidates is some version of "I'd grep for it." That answer is fine for a CTF. It's not a job.

The professional answer involves writing a portable, reviewable, version-controlled rule that fires on the right log event regardless of which SIEM the company happens to have purchased. That format, more or less, is **Sigma**.

Sigma rules are YAML. They describe a detection — what to look for, in which log source, and under what condition. They don't run anywhere on their own. Instead, you point a converter at them and out comes a Splunk SPL query, an Elastic Lucene string, a Sentinel KQL expression, or a Chronicle YARA-L block. Same rule, every backend.

That's the dream, anyway. The reality is messier.

## What I wanted to use, and why I didn't

The official tool is [`sigma-cli`](https://github.com/SigmaHQ/sigma-cli). It works. I'm not here to bash it. But I found two things while trying to make it part of my daily rule-authoring loop:

1. The output assumes you already know what you're looking at. If a rule fails to parse, you get an exception with a stack trace. Useful if you're a maintainer of pySigma. Less useful if you're trying to learn what makes a rule valid.
2. There's a lot of ceremony for "show me what this rule looks like in Splunk." Multiple flags, a pipeline name, a verbose-mode incantation. Fine if you're converting hundreds. Friction if you're iterating on one.

I wanted something that felt more like `git diff` — type the command, get the answer, get on with your day. So I wrote it.

## What SigmaForge does

Three subcommands. Each does one thing.

```bash
sigmaforge validate examples/rules/ssh_failed_password.yml
```

Tells you whether a rule parses, and if so, summarizes what's actually in it — title, status, log source, detection structure. Exit code 0 for valid, 1 for invalid, 2 for usage errors. Drop it in a pre-commit hook or a CI step that runs against every rule in your detection repo.

```bash
sigmaforge convert examples/rules/web_scanner_useragent.yml --target splunk
```

Spits out the Splunk SPL. No header noise, no required pipeline configuration for the simple case, no "did you mean to specify the dialect" prompts. If you want to pipe it into Splunk's REST API or paste it into a search bar, it's ready.

```bash
sigmaforge convert ... --target elastic
```

Same thing for Elastic Lucene. Chronicle YARA-L and Sentinel KQL are on the roadmap.

## Under the hood

SigmaForge isn't reinventing pySigma — it sits on top of it. The validator wraps `SigmaCollection.from_yaml()` and converts the exception types into something you can read. The converter is essentially:

```python
backend = SplunkBackend()  # or LuceneBackend()
return backend.convert(collection)
```

That's the entire core. The interesting part — the part that took the most thought — was figuring out what to *show* the user. A Sigma rule has dozens of optional fields. Most of them don't matter at the "is this rule structurally sound" stage. Picking the four or five that *do* matter (logsource, status, detection condition, rule ID for traceability) is the design decision.

## The example rules are doing more work than they look like

The three example rules in `examples/rules/` aren't placeholders. They mirror real detections from [LogHound](https://github.com/B0bTheSkull/loghound) — my own Python log analyzer — translated into portable Sigma. So if you run LogHound and SigmaForge side by side, you can see the same primitive ("failed SSH password," "sudo to a shell," "Nikto user-agent") expressed two ways: as ad-hoc Python detection logic, and as a portable rule that any SIEM can run.

That's the bridge I'm trying to demonstrate in this portfolio. Detection engineering isn't picking one over the other. It's knowing how to author a rule, validate it, convert it for whatever the customer is paying for, and ship it.

## What I learned

Two things I didn't expect.

**One:** pySigma's parser is strict in a useful way. It catches things like `condition` referencing a selection that doesn't exist, or two top-level keys that conflict. I was writing rules that "looked right" and the parser would tell me they weren't. That's exactly what you want from a tool that catches the bug before the rule reaches a real SIEM.

**Two:** Backend output varies a lot more than the spec implies. The same SSH-failed-password rule comes out of the Splunk backend and the Elastic backend looking completely different — different field names, different escaping, different operator syntax. Not a bug. Just a reminder that "portable" is doing a lot of work in "portable detection format."

## What's next

The roadmap in the README is real, not aspirational. The two I'll prioritize:

- **`test` subcommand** — take a rule and a sample log file, evaluate the rule against the log, show which lines matched. This closes the loop — author a rule, validate it parses, see it fire, then convert.
- **`template` subcommand** — paste in an example log line, get a starter Sigma rule. Lowering the activation energy for "I want a rule for this" is the next big leverage point.

If you're building something similar or have feedback, [open an issue](https://github.com/B0bTheSkull/sigmaforge/issues). If you find SigmaForge useful, star it.

— *Bob*
