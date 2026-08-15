#!/usr/bin/env python3
"""Validate the repository's Markdown knowledge-base structure.

This is intentionally a static V2 gate. It does not fetch external URLs or
validate the factual content of claims, builds, runtimes, or services.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote

try:
    import yaml
except ImportError:
    print(
        "ERROR: PyYAML is required for fail-closed frontmatter validation; "
        "install it in the validation environment.",
        file=sys.stderr,
    )
    raise SystemExit(2)


REPO_ROOT = Path(__file__).resolve().parents[1]
KB_ROOT = REPO_ROOT / "knowledge-base"
COMMON_REQUIRED = ("id", "type", "title", "status", "tags")

STATUS_BY_TYPE = {
    "index": {"active", "superseded", "deprecated"},
    "project-context": {"active", "superseded", "deprecated"},
    "profile-catalog": {"active", "superseded", "deprecated"},
    "governance": {"active", "superseded", "deprecated"},
    "catalog": {"active", "superseded", "deprecated"},
    "coverage-matrix": {"active", "superseded", "deprecated"},
    "reference-architecture": {"proposed", "accepted", "superseded", "deprecated"},
    "project-blueprint": {"proposed", "accepted", "superseded", "deprecated"},
    "ArchitectureDecision": {
        "proposed",
        "accepted",
        "rejected",
        "deferred",
        "superseded",
        "deprecated",
    },
    "tool-profile": {"observed", "superseded", "deprecated"},
    "execution-record": {"historical-snapshot"},
}

LINK_RE = re.compile(r"(?<!!)\[[^\]]*\]\(([^)]+)\)")
SCHEME_RE = re.compile(r"^[A-Za-z][A-Za-z0-9+.-]*:")


def relative(path: Path) -> str:
    return path.relative_to(REPO_ROOT).as_posix()


def split_frontmatter(path: Path, text: str) -> tuple[str, str]:
    lines = text.splitlines(keepends=True)
    if not lines or lines[0].strip() != "---":
        raise ValueError("missing opening YAML frontmatter delimiter")

    for index, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            return "".join(lines[1:index]), "".join(lines[index + 1 :])

    raise ValueError("missing closing YAML frontmatter delimiter")


def parse_frontmatter(path: Path, text: str) -> tuple[dict[str, object], str]:
    raw, body = split_frontmatter(path, text)
    try:
        data = yaml.safe_load(raw)
    except yaml.YAMLError as error:
        raise ValueError(f"invalid YAML frontmatter: {error}") from error
    if not isinstance(data, dict):
        raise ValueError("frontmatter must be a YAML mapping")
    return data, body


def link_target(raw_target: str) -> str:
    target = raw_target.strip()
    if target.startswith("<") and ">" in target:
        return target[1 : target.index(">")]
    # Repository links do not use spaces in paths. A suffix is a Markdown title.
    return target.split(maxsplit=1)[0]


def validate_links(path: Path, body: str) -> list[str]:
    errors: list[str] = []
    for match in LINK_RE.finditer(body):
        target = link_target(match.group(1))
        if not target or target.startswith("#") or SCHEME_RE.match(target):
            continue

        clean_target = unquote(target.split("#", 1)[0].split("?", 1)[0])
        if not clean_target:
            continue
        resolved = (path.parent / clean_target).resolve()
        try:
            resolved.relative_to(REPO_ROOT)
        except ValueError:
            errors.append(f"{relative(path)}: relative link escapes repository: {target}")
            continue
        if not resolved.exists():
            errors.append(f"{relative(path)}: missing relative link target: {target}")
    return errors


def main() -> int:
    errors: list[str] = []
    seen_ids: dict[str, Path] = {}
    markdown_paths = sorted(KB_ROOT.rglob("*.md"))

    for path in markdown_paths:
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as error:
            errors.append(f"{relative(path)}: cannot read as UTF-8: {error}")
            continue

        try:
            frontmatter, body = parse_frontmatter(path, text)
        except ValueError as error:
            errors.append(f"{relative(path)}: {error}")
            continue

        for field in COMMON_REQUIRED:
            if field not in frontmatter or frontmatter[field] in (None, "", []):
                errors.append(f"{relative(path)}: missing required frontmatter field: {field}")

        document_id = frontmatter.get("id")
        if isinstance(document_id, str) and document_id:
            if document_id in seen_ids:
                errors.append(
                    f"{relative(path)}: duplicate id {document_id!r}; "
                    f"first seen in {relative(seen_ids[document_id])}"
                )
            else:
                seen_ids[document_id] = path

        document_type = frontmatter.get("type")
        status = frontmatter.get("status")
        if document_type not in STATUS_BY_TYPE:
            errors.append(f"{relative(path)}: unsupported document type: {document_type!r}")
        elif status not in STATUS_BY_TYPE[document_type]:
            allowed = ", ".join(sorted(STATUS_BY_TYPE[document_type]))
            errors.append(
                f"{relative(path)}: status {status!r} is invalid for "
                f"type {document_type!r}; allowed: {allowed}"
            )

        if status == "superseded" and not frontmatter.get("superseded_by"):
            errors.append(f"{relative(path)}: superseded document requires superseded_by")

        tags = frontmatter.get("tags")
        if tags is not None and not isinstance(tags, list):
            errors.append(f"{relative(path)}: tags must be a YAML list")

        errors.extend(validate_links(path, body))

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        print(
            f"FAIL: {len(errors)} error(s) across {len(markdown_paths)} Markdown files",
            file=sys.stderr,
        )
        return 1

    print(
        f"PASS: {len(markdown_paths)} Markdown files; frontmatter, lifecycle, "
        "unique IDs, and relative links are valid"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
