from pathlib import Path

import pytest

from sigmaforge.converter import SUPPORTED_TARGETS, convert_rule

EXAMPLES_DIR = Path(__file__).parent.parent / "examples" / "rules"


@pytest.mark.parametrize("target", SUPPORTED_TARGETS)
def test_convert_ssh_failed_password(target: str):
    queries = convert_rule(EXAMPLES_DIR / "ssh_failed_password.yml", target)
    assert len(queries) >= 1
    assert all(isinstance(q, str) and q for q in queries)


@pytest.mark.parametrize("target", SUPPORTED_TARGETS)
def test_convert_web_scanner(target: str):
    queries = convert_rule(EXAMPLES_DIR / "web_scanner_useragent.yml", target)
    assert len(queries) >= 1
