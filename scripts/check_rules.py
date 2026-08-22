#!/usr/bin/env python3
"""Check repo-root Clash *.list files and README mentions.

Scans *.list in the repository root (not subdirectories) for:
  1. Duplicate rule lines (comments and blank lines ignored)
  2. IP-CIDR / IP-CIDR6 rules missing ,no-resolve
  3. Dangerous DOMAIN-SUFFIX values that over-capture
  4. README.md mentioning each existing *.list filename and main.ini

Comments starting with # are allowed. Exit 1 if any finding is reported.
"""

from __future__ import annotations

import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
README_PATH = ROOT / "README.md"
MAIN_INI = "main.ini"

DANGEROUS_SUFFIXES = {
    "googleapis.com",
    "googleusercontent.com",
    "goog",
    "stripe.com",
    "challenges.cloudflare.com",
    "us-west-2.amazonaws.com",
}


def is_ignorable(line: str) -> bool:
    stripped = line.strip()
    return not stripped or stripped.startswith("#")


def rule_payload(line: str) -> str:
    return line.strip()


def scan_list(path: Path) -> list[str]:
    findings: list[str] = []
    seen: dict[str, list[int]] = defaultdict(list)

    for lineno, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if is_ignorable(raw):
            continue
        rule = rule_payload(raw)
        seen[rule].append(lineno)

        kind, _, rest = rule.partition(",")
        kind = kind.strip().upper()
        if kind in {"IP-CIDR", "IP-CIDR6"}:
            parts = [p.strip() for p in rest.split(",")]
            if "no-resolve" not in parts:
                findings.append(
                    f"{path.name}:{lineno}: {kind} missing ,no-resolve: {rule}"
                )

        if kind == "DOMAIN-SUFFIX":
            suffix = rest.split(",", 1)[0].strip().lower()
            if suffix in DANGEROUS_SUFFIXES:
                findings.append(
                    f"{path.name}:{lineno}: dangerous DOMAIN-SUFFIX ({suffix}): {rule}"
                )

    for rule, lines in sorted(seen.items(), key=lambda item: item[1][0]):
        if len(lines) > 1:
            loc = ", ".join(f"L{n}" for n in lines)
            findings.append(f"{path.name}: duplicate rule ({loc}): {rule}")

    return findings


def check_readme(list_files: list[Path]) -> list[str]:
    findings: list[str] = []
    if not README_PATH.is_file():
        return ["README.md: file is missing"]

    text = README_PATH.read_text(encoding="utf-8")
    required = [MAIN_INI] + [p.name for p in list_files]
    missing = [name for name in required if name not in text]
    if missing:
        findings.append(
            "README.md: does not mention required filename(s): " + ", ".join(missing)
        )
    return findings


def main() -> int:
    list_files = sorted(p for p in ROOT.glob("*.list") if p.is_file())
    print(f"Scanning {len(list_files)} list file(s) in {ROOT}")
    for path in list_files:
        print(f"  - {path.name}")
    print()

    findings: list[str] = []
    for path in list_files:
        findings.extend(scan_list(path))
    findings.extend(check_readme(list_files))

    if findings:
        print(f"Found {len(findings)} issue(s):")
        for item in findings:
            print(f"  [FAIL] {item}")
        return 1

    print("OK: no duplicate rules, missing no-resolve flags,")
    print("    dangerous DOMAIN-SUFFIX values, or README filename gaps.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
