#!/usr/bin/env python3
"""Check repo-root Clash *.list files, main.ini wiring, and README mentions.

Scans *.list in the repository root (not subdirectories) for:
  1. Duplicate rule lines (comments and blank lines ignored)
  2. IP-CIDR / IP-CIDR6 rules missing ,no-resolve
  3. Dangerous DOMAIN-SUFFIX values that over-capture
  4. README.md mentioning each existing *.list filename and main.ini
  5. main.ini ordering invariants (first-match-wins):
     - trading.list must load before BanAD (exchange Android init hosts
       would otherwise be REJECT before PROCESS-NAME can save them)
     - tiktok.list must load before ChinaDomain / ChinaMedia (snssdk.com
       would otherwise be DIRECT)
     - every local <name>.list referenced by main.ini must exist, and every
       repo-root *.list must be referenced by main.ini (no orphans)

Cross-platform notes are reported as warnings (exit code stays 0):
  W1. PROCESS-NAME-WILDCARD is Mihomo-only; old Clash kernels skip the line.
  W2. A list with PROCESS-NAME but no Windows (.exe) / macOS (bare name) /
      Android (dotted package) entry may leave one platform uncovered.

Comments starting with # are allowed. Exit 1 if any finding is reported.
"""

from __future__ import annotations

import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
README_PATH = ROOT / "README.md"
MAIN_INI_PATH = ROOT / "main.ini"
MAIN_INI = "main.ini"

LOCAL_PREFIX = "Banezzz/private_clash_rules/main/"

DANGEROUS_SUFFIXES = {
    "googleapis.com",
    "googleusercontent.com",
    "goog",
    "stripe.com",
    "challenges.cloudflare.com",
    "us-west-2.amazonaws.com",
}

# (local list file, upstream marker that must appear earlier) — first match wins.
ORDERING_CONSTRAINTS = (
    ("trading.list", "BanAD"),
    ("tiktok.list", "ChinaDomain"),
    ("tiktok.list", "ChinaMedia"),
)


def is_ignorable(line: str) -> bool:
    stripped = line.strip()
    return not stripped or stripped.startswith("#")


def rule_payload(line: str) -> str:
    return line.strip()


def classify_process(value: str) -> str:
    """Classify a PROCESS-NAME value into windows / android / mac."""
    lowered = value.strip().lower()
    if lowered.endswith(".exe"):
        return "windows"
    if "." in value.strip():
        return "android"
    return "mac"


def scan_list(path: Path) -> tuple[list[str], list[str]]:
    findings: list[str] = []
    warnings: list[str] = []
    seen: dict[str, list[int]] = defaultdict(list)
    platforms: set[str] = set()
    has_process = False
    wildcard_lines: list[int] = []

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

        if kind == "PROCESS-NAME":
            has_process = True
            platforms.add(classify_process(rest.split(",", 1)[0]))
        elif kind == "PROCESS-NAME-WILDCARD":
            has_process = True
            platforms.add(classify_process(rest.split(",", 1)[0].rstrip("*")))
            wildcard_lines.append(lineno)

    for rule, lines in sorted(seen.items(), key=lambda item: item[1][0]):
        if len(lines) > 1:
            loc = ", ".join(f"L{n}" for n in lines)
            findings.append(f"{path.name}: duplicate rule ({loc}): {rule}")

    if wildcard_lines:
        loc = ", ".join(f"L{n}" for n in wildcard_lines)
        warnings.append(
            f"{path.name}: PROCESS-NAME-WILDCARD ({loc}) is Mihomo-only; "
            "old Clash kernels skip the line, so keep an exact "
            "PROCESS-NAME alongside it."
        )

    if has_process:
        missing = {"windows", "mac", "android"} - platforms
        if missing:
            warnings.append(
                f"{path.name}: PROCESS-NAME covers "
                f"{sorted(platforms)} but has no "
                f"{sorted(missing)} entry; that platform falls back to "
                "domain/IP rules only."
            )

    return findings, warnings


def check_main_ini(list_files: list[Path]) -> tuple[list[str], list[str]]:
    findings: list[str] = []
    warnings: list[str] = []
    if not MAIN_INI_PATH.is_file():
        return [f"{MAIN_INI}: file is missing"], warnings

    lines = MAIN_INI_PATH.read_text(encoding="utf-8").splitlines()
    rulesets = [
        line.strip() for line in lines if line.strip().startswith("ruleset=")
    ]

    def index_of(marker: str) -> int | None:
        for i, line in enumerate(rulesets):
            if marker in line:
                return i
        return None

    for local, upstream_marker in ORDERING_CONSTRAINTS:
        local_idx = index_of(local)
        upstream_idx = index_of(upstream_marker)
        if local_idx is None:
            findings.append(f"{MAIN_INI}: no ruleset references local {local}")
        elif upstream_idx is None:
            warnings.append(
                f"{MAIN_INI}: upstream marker {upstream_marker!r} not found; "
                f"cannot verify {local} loads first."
            )
        elif local_idx > upstream_idx:
            findings.append(
                f"{MAIN_INI}: {local} (ruleset #{local_idx}) must load before "
                f"{upstream_marker} (ruleset #{upstream_idx}); first match wins."
            )

    referenced = set(re.findall(r"main/(\S+\.list)", "\n".join(rulesets)))
    existing = {p.name for p in list_files}
    for name in sorted(referenced - existing):
        findings.append(f"{MAIN_INI}: references missing local file {name}")
    for name in sorted(existing - referenced):
        findings.append(f"{MAIN_INI}: local file {name} is not referenced")

    if any("ACL4SSR/master/Clash/Apple.list" in line for line in rulesets):
        findings.append(
            f"{MAIN_INI}: still references upstream Apple.list; "
            "use local apple.list (upstream has no PROCESS-NAME)."
        )

    return findings, warnings


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
    warnings: list[str] = []
    for path in list_files:
        file_findings, file_warnings = scan_list(path)
        findings.extend(file_findings)
        warnings.extend(file_warnings)
    ini_findings, ini_warnings = check_main_ini(list_files)
    findings.extend(ini_findings)
    warnings.extend(ini_warnings)
    findings.extend(check_readme(list_files))

    for item in warnings:
        print(f"  [WARN] {item}")
    if warnings:
        print()

    if findings:
        print(f"Found {len(findings)} issue(s):")
        for item in findings:
            print(f"  [FAIL] {item}")
        return 1

    print("OK: no duplicate rules, missing no-resolve flags,")
    print("    dangerous DOMAIN-SUFFIX values, main.ini wiring breaks,")
    print("    or README filename gaps.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
