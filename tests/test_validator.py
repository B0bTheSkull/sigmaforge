from pathlib import Path

from sigmaforge.validator import validate_rule

EXAMPLES_DIR = Path(__file__).parent.parent / "examples" / "rules"


def test_ssh_failed_password_valid():
    result = validate_rule(EXAMPLES_DIR / "ssh_failed_password.yml")
    assert result.valid, f"errors: {result.errors}"
    assert result.rules[0]["title"].startswith("Failed SSH")


def test_suspicious_sudo_valid():
    result = validate_rule(EXAMPLES_DIR / "suspicious_sudo.yml")
    assert result.valid, f"errors: {result.errors}"


def test_web_scanner_valid():
    result = validate_rule(EXAMPLES_DIR / "web_scanner_useragent.yml")
    assert result.valid, f"errors: {result.errors}"


def test_invalid_yaml(tmp_path: Path):
    bad = tmp_path / "bad.yml"
    bad.write_text("title: missing\ndetection:\n  condition: nothing_to_match\n")
    result = validate_rule(bad)
    assert not result.valid
