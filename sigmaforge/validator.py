"""Sigma rule validation backed by pySigma."""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml
from sigma.collection import SigmaCollection
from sigma.exceptions import SigmaError


@dataclass
class ValidationResult:
    valid: bool
    rules: list[dict[str, Any]] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)


def _summarize_logsource(logsource: dict) -> str:
    parts = [f"{k}={v}" for k, v in logsource.items()]
    return ", ".join(parts) if parts else "(none)"


def _summarize_detection(detection: dict) -> str:
    selections = [k for k in detection if k != "condition"]
    condition = detection.get("condition", "(missing)")
    return f"{len(selections)} selection(s), condition: {condition}"


def validate_rule(path: Path) -> ValidationResult:
    """Validate a single Sigma rule YAML file."""
    text = path.read_text()
    try:
        SigmaCollection.from_yaml(text)
    except SigmaError as e:
        return ValidationResult(valid=False, errors=[str(e)])
    except yaml.YAMLError as e:
        return ValidationResult(valid=False, errors=[f"YAML parse error: {e}"])

    raw = yaml.safe_load(text)
    rules_raw = raw if isinstance(raw, list) else [raw]
    summaries: list[dict[str, Any]] = []
    for r in rules_raw:
        summaries.append(
            {
                "id": r.get("id", "(no id)"),
                "title": r.get("title", "(untitled)"),
                "status": r.get("status", "(no status)"),
                "logsource": _summarize_logsource(r.get("logsource", {})),
                "detection_summary": _summarize_detection(r.get("detection", {})),
            }
        )
    return ValidationResult(valid=True, rules=summaries)
