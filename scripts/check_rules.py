#!/usr/bin/env python3
"""Check repo-root Clash *.list files, main.ini, and README mentions.

Scans *.list in the repository root (not subdirectories) for:
  1. Duplicate rule lines, case-insensitive (comments and blank lines ignored)
  2. Rule types outside the cross-client allowlist (e.g. PROCESS-NAME-WILDCARD,
     which makes Mihomo < v1.19.19 reject the whole profile)
  3. IP-CIDR / IP-CIDR6 rules missing ,no-resolve or with an invalid network
  4. Dangerous DOMAIN-SUFFIX values that over-capture
  5. README.md mentioning each existing *.list filename and main.ini

Checks main.ini for:
  6. ruleset= / []references pointing at undefined proxy groups
  7. Logical rules ([]AND / []OR / []NOT) that subconverter mangles
  8. Local ruleset URLs pointing at missing files, and local lists never loaded
  9. A 4th comma field after interval,timeout,tolerance (silently dropped)

Comments starting with # are allowed. Exit 1 if any finding is reported.
"""

from __future__ import annotations

import ipaddress
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
README_PATH = ROOT / "README.md"
MAIN_INI = "main.ini"
LOCAL_PREFIX = "https://raw.githubusercontent.com/Banezzz/private_clash_rules/main/"

ALLOWED_TYPES = {
    "DOMAIN",
    "DOMAIN-SUFFIX",
    "DOMAIN-KEYWORD",
    "IP-CIDR",
    "IP-CIDR6",
    "PROCESS-NAME",
}

DANGEROUS_SUFFIXES = {
    "googleapis.com",
    "googleusercontent.com",
    "goog",
    "stripe.com",
    "challenges.cloudflare.com",
    "us-west-2.amazonaws.com",
    "apple.com",
    "icloud.com",
    "itunes.apple.com",
}

BUILTIN_TARGETS = {"DIRECT", "REJECT", "REJECT-DROP", "PASS"}
LOGICAL_TYPES = {"AND", "OR", "NOT"}


def is_ignorable(line: str) -> bool:
    stripped = line.strip()
    return not stripped or stripped.startswith("#")


def check_cidr(kind: str, value: str) -> str | None:
    try:
        net = ipaddress.ip_network(value, strict=True)
    except ValueError as exc:
        return f"invalid network ({exc})"
    if kind == "IP-CIDR" and net.version != 4:
        return "IPv6 network under IP-CIDR (use IP-CIDR6)"
    if kind == "IP-CIDR6" and net.version != 6:
        return "IPv4 network under IP-CIDR6 (use IP-CIDR)"
    return None


def scan_list(path: Path) -> list[str]:
    findings: list[str] = []
    seen: dict[str, list[int]] = defaultdict(list)

    for lineno, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if is_ignorable(raw):
            continue
        rule = raw.strip()
        # Mihomo matches domains and process names case-insensitively.
        seen[rule.lower()].append(lineno)

        kind, _, rest = rule.partition(",")
        kind = kind.strip().upper()
        parts = [p.strip() for p in rest.split(",")]
        where = f"{path.name}:{lineno}"

        if kind not in ALLOWED_TYPES:
            findings.append(f"{where}: non-portable rule type {kind}: {rule}")
            continue

        if not parts or not parts[0]:
            findings.append(f"{where}: empty rule value: {rule}")
            continue

        if kind in {"IP-CIDR", "IP-CIDR6"}:
            if "no-resolve" not in parts[1:]:
                findings.append(f"{where}: {kind} missing ,no-resolve: {rule}")
            problem = check_cidr(kind, parts[0])
            if problem:
                findings.append(f"{where}: {kind} {problem}: {rule}")

        if kind == "DOMAIN-SUFFIX" and parts[0].lower() in DANGEROUS_SUFFIXES:
            findings.append(f"{where}: dangerous DOMAIN-SUFFIX ({parts[0]}): {rule}")

        if kind == "PROCESS-NAME" and any(ch in parts[0] for ch in "*?"):
            findings.append(f"{where}: wildcard in PROCESS-NAME is not portable: {rule}")

    for rule, lines in sorted(seen.items(), key=lambda item: item[1][0]):
        if len(lines) > 1:
            loc = ", ".join(f"L{n}" for n in lines)
            findings.append(f"{path.name}: duplicate rule ({loc}): {rule}")

    return findings


def check_main_ini(list_files: list[Path]) -> list[str]:
    path = ROOT / MAIN_INI
    if not path.is_file():
        return [f"{MAIN_INI}: file is missing"]

    findings: list[str] = []
    groups: set[str] = set()
    references: list[tuple[int, str]] = []
    loaded_local: set[str] = set()

    for lineno, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = raw.strip()
        where = f"{MAIN_INI}:{lineno}"

        if line.startswith("ruleset="):
            group, _, source = line[len("ruleset="):].partition(",")
            references.append((lineno, group))
            if source.startswith("[]"):
                inline_type = source[2:].split(",", 1)[0].strip().upper()
                if inline_type in LOGICAL_TYPES:
                    findings.append(
                        f"{where}: logical rule {inline_type} is mangled by subconverter: {line}"
                    )
            elif source.startswith(LOCAL_PREFIX):
                name = source[len(LOCAL_PREFIX):]
                loaded_local.add(name)
                if not (ROOT / name).is_file():
                    findings.append(f"{where}: local ruleset {name} does not exist")

        elif line.startswith("custom_proxy_group="):
            fields = line[len("custom_proxy_group="):].split("`")
            groups.add(fields[0])
            for field in fields[2:]:
                if field.startswith("[]"):
                    references.append((lineno, field[2:]))
            group_type = fields[1] if len(fields) > 1 else ""
            if group_type in {"url-test", "fallback", "load-balance"}:
                times = fields[-1]
                if times.count(",") > 2:
                    findings.append(
                        f"{where}: extra field after interval,timeout,tolerance is ignored: {times}"
                    )

    for lineno, name in references:
        if name not in groups and name not in BUILTIN_TARGETS:
            findings.append(f"{MAIN_INI}:{lineno}: reference to undefined group: {name}")

    for list_path in list_files:
        if list_path.name not in loaded_local:
            findings.append(f"{MAIN_INI}: local list {list_path.name} is never loaded")

    return findings


def check_readme(list_files: list[Path]) -> list[str]:
    if not README_PATH.is_file():
        return ["README.md: file is missing"]

    text = README_PATH.read_text(encoding="utf-8")
    required = [MAIN_INI] + [p.name for p in list_files]
    missing = [name for name in required if not re.search(rf"`{re.escape(name)}`", text)]
    if missing:
        return ["README.md: does not mention required filename(s): " + ", ".join(missing)]
    return []


def main() -> int:
    list_files = sorted(p for p in ROOT.glob("*.list") if p.is_file())
    print(f"Scanning {len(list_files)} list file(s) in {ROOT}")
    for path in list_files:
        print(f"  - {path.name}")
    print()

    findings: list[str] = []
    for path in list_files:
        findings.extend(scan_list(path))
    findings.extend(check_main_ini(list_files))
    findings.extend(check_readme(list_files))

    if findings:
        print(f"Found {len(findings)} issue(s):")
        for item in findings:
            print(f"  [FAIL] {item}")
        return 1

    print("OK: lists, main.ini references, and README mentions are clean.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
