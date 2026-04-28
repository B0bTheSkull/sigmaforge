"""Convert Sigma rules to target query languages via pySigma backends."""

from pathlib import Path

from sigma.backends.elasticsearch import LuceneBackend
from sigma.backends.splunk import SplunkBackend
from sigma.collection import SigmaCollection

SUPPORTED_TARGETS = ["splunk", "elastic"]


def _backend_for(target: str):
    if target == "splunk":
        return SplunkBackend()
    if target == "elastic":
        return LuceneBackend()
    raise ValueError(f"unsupported target: {target}")


def convert_rule(path: Path, target: str) -> list[str]:
    """Convert a Sigma rule file to the target query language.

    Returns a list of query strings (one per rule in the file — Sigma supports
    multi-document YAML).
    """
    text = path.read_text()
    collection = SigmaCollection.from_yaml(text)
    backend = _backend_for(target)
    return backend.convert(collection)
