#!/usr/bin/env python3
"""Validate repository Clash rule lists and subconverter wiring."""

from __future__ import annotations

import ipaddress
import re
import sys
from collections import defaultdict
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent.parent
README_PATH = ROOT / "README.md"
MAIN_INI_PATH = ROOT / "main.ini"

DOMAIN_RULES = {"DOMAIN", "DOMAIN-SUFFIX"}
PROCESS_RULES = {"PROCESS-NAME", "PROCESS-NAME-WILDCARD"}
SUPPORTED_RULES = DOMAIN_RULES | PROCESS_RULES | {
    "DOMAIN-KEYWORD",
    "IP-CIDR",
    "IP-CIDR6",
}
DOMAIN_RE = re.compile(
    r"^(?=.{1,253}\Z)(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)*"
    r"[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?$",
    re.IGNORECASE,
)
COUNT_RE = re.compile(r"^#\s*Count:\s*(\d+)\s*$", re.IGNORECASE)
ORDER_REQUIREMENTS = (
    ("android.list", "BanAD.list"),
    ("trading.list", "BanAD.list"),
    ("GoogleFCM.list", "GoogleCN.list"),
    ("tiktok.list", "ChinaDomain.list"),
    ("steam.list", "ChinaDomain.list"),
    ("apple.list", "ProxyMedia.list"),
)

DANGEROUS_SUFFIXES = {
    "akadns.net",
    "crashlytics.com",
    "edgesuite.net",
    "googleapis.com",
    "googleusercontent.com",
    "goog",
    "gvt1.com",
    "gvt2.com",
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
    lines = path.read_text(encoding="utf-8").splitlines()

    for lineno, raw in enumerate(lines, 1):
        if is_ignorable(raw):
            continue
        rule = rule_payload(raw)
        seen[rule].append(lineno)

        kind, separator, _ = rule.partition(",")
        kind = kind.strip().upper()
        if not separator or kind not in SUPPORTED_RULES:
            findings.append(
                f"{path.name}:{lineno}: unsupported or malformed rule: {rule}"
            )
            continue

        parts = [part.strip() for part in rule.split(",")]
        expected_parts = 3 if kind in {"IP-CIDR", "IP-CIDR6"} else 2
        if len(parts) != expected_parts or any(not part for part in parts):
            findings.append(
                f"{path.name}:{lineno}: {kind} expects {expected_parts} "
                f"comma-separated fields: {rule}"
            )
            continue

        payload = parts[1]
        if kind in DOMAIN_RULES and not DOMAIN_RE.fullmatch(payload):
            findings.append(
                f"{path.name}:{lineno}: invalid domain payload ({payload}): {rule}"
            )

        if kind == "PROCESS-NAME-WILDCARD":
            if "*" not in payload and "?" not in payload:
                findings.append(
                    f"{path.name}:{lineno}: wildcard rule has no wildcard: {rule}"
                )

        if kind in {"IP-CIDR", "IP-CIDR6"}:
            if "no-resolve" not in parts:
                findings.append(
                    f"{path.name}:{lineno}: {kind} missing ,no-resolve: {rule}"
                )
            try:
                network = ipaddress.ip_network(payload, strict=True)
            except ValueError as error:
                findings.append(
                    f"{path.name}:{lineno}: invalid {kind} network "
                    f"({error}): {rule}"
                )
            else:
                expected_version = 4 if kind == "IP-CIDR" else 6
                if network.version != expected_version:
                    findings.append(
                        f"{path.name}:{lineno}: {kind} contains IPv"
                        f"{network.version}: {rule}"
                    )

        if kind == "DOMAIN-SUFFIX":
            suffix = payload.lower()
            if suffix in DANGEROUS_SUFFIXES:
                findings.append(
                    f"{path.name}:{lineno}: dangerous DOMAIN-SUFFIX ({suffix}): {rule}"
                )

    for rule, rule_lines in sorted(seen.items(), key=lambda item: item[1][0]):
        if len(rule_lines) > 1:
            loc = ", ".join(f"L{n}" for n in rule_lines)
            findings.append(f"{path.name}: duplicate rule ({loc}): {rule}")

    declared_counts = [
        (lineno, int(match.group(1)))
        for lineno, raw in enumerate(lines, 1)
        if (match := COUNT_RE.fullmatch(raw.strip()))
    ]
    actual_count = sum(len(rule_lines) for rule_lines in seen.values())
    for lineno, declared_count in declared_counts:
        if declared_count != actual_count:
            findings.append(
                f"{path.name}:{lineno}: declared count {declared_count} "
                f"does not match {actual_count} rules"
            )

    return findings


def check_main_ini(list_files: list[Path]) -> list[str]:
    """Check local rule references and policy group definitions."""
    if not MAIN_INI_PATH.is_file():
        return ["main.ini: file is missing"]

    findings: list[str] = []
    ruleset_groups: list[tuple[int, str]] = []
    ruleset_sources: list[tuple[int, str]] = []
    defined_groups: set[str] = set()
    referenced_local_lists: dict[str, list[int]] = defaultdict(list)

    for lineno, raw in enumerate(
        MAIN_INI_PATH.read_text(encoding="utf-8").splitlines(), 1
    ):
        line = raw.strip()
        if not line or line.startswith(";"):
            continue

        if line.startswith("ruleset="):
            value = line.removeprefix("ruleset=")
            group, separator, source = value.partition(",")
            if not separator or not group.strip() or not source.strip():
                findings.append(f"main.ini:{lineno}: malformed ruleset: {line}")
                continue
            ruleset_groups.append((lineno, group.strip()))
            source = source.strip()
            ruleset_sources.append((lineno, source))
            if source.startswith("http://"):
                findings.append(
                    f"main.ini:{lineno}: remote ruleset must use HTTPS: {source}"
                )
            if "Banezzz/private_clash_rules/main/" in source:
                filename = Path(urlparse(source).path).name
                referenced_local_lists[filename].append(lineno)

        if line.startswith("custom_proxy_group="):
            value = line.removeprefix("custom_proxy_group=")
            group, separator, _ = value.partition("`")
            if not separator or not group.strip():
                findings.append(
                    f"main.ini:{lineno}: malformed custom_proxy_group: {line}"
                )
            else:
                defined_groups.add(group.strip())
            if "http://" in line:
                findings.append(
                    f"main.ini:{lineno}: health-check URL must use HTTPS"
                )

    for lineno, group in ruleset_groups:
        if group not in defined_groups:
            findings.append(
                f"main.ini:{lineno}: ruleset policy group is undefined: {group}"
            )

    for earlier_name, later_name in ORDER_REQUIREMENTS:
        earlier_lines = [
            line for line, source in ruleset_sources if source.endswith(earlier_name)
        ]
        later_lines = [
            line for line, source in ruleset_sources if source.endswith(later_name)
        ]
        if earlier_lines and later_lines and min(earlier_lines) >= min(later_lines):
            findings.append(
                f"main.ini: {earlier_name} must load before {later_name}"
            )

    expected_local_lists = {path.name for path in list_files}
    referenced_names = set(referenced_local_lists)
    for filename in sorted(expected_local_lists - referenced_names):
        findings.append(f"main.ini: local list is not referenced: {filename}")
    for filename in sorted(referenced_names - expected_local_lists):
        lines = ", ".join(f"L{line}" for line in referenced_local_lists[filename])
        findings.append(
            f"main.ini: references missing local list ({lines}): {filename}"
        )
    for filename, lines in sorted(referenced_local_lists.items()):
        if len(lines) > 1:
            locations = ", ".join(f"L{line}" for line in lines)
            findings.append(
                f"main.ini: local list referenced more than once "
                f"({locations}): {filename}"
            )

    return findings


def check_readme(list_files: list[Path]) -> list[str]:
    findings: list[str] = []
    if not README_PATH.is_file():
        return ["README.md: file is missing"]

    text = README_PATH.read_text(encoding="utf-8")
    required = [MAIN_INI_PATH.name] + [p.name for p in list_files]
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
    findings.extend(check_main_ini(list_files))
    findings.extend(check_readme(list_files))

    if findings:
        print(f"Found {len(findings)} issue(s):")
        for item in findings:
            print(f"  [FAIL] {item}")
        return 1

    print("OK: rule syntax, CIDRs, main.ini wiring, and documentation are valid.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
