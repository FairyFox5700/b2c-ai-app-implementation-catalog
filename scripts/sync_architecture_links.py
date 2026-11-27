#!/usr/bin/env python
"""Synchronize implementation links from the root catalog into app guides."""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "README.md"
ARCHITECTURES = ROOT / "docs" / "architectures"
APP_HEADING = re.compile(r"^##\s+(\d+)\.\s+(.+?)\s*$", re.MULTILINE)
REFERENCE_HEADING = re.compile(r"^(?:\*\*Reference architecture|### Reference architecture)", re.MULTILINE)
LINK = re.compile(r"^\[([^\]]+)\]\((.+)\)$")
BLOCK = re.compile(
    r"\n*<!-- implementation-links:auto:start -->.*?<!-- implementation-links:auto:end -->\n*",
    re.DOTALL,
)
MATCH_EXPLANATIONS = {
    "Exact": "implements the same scenario and is the closest starting point",
    "Adjacent": "implements a closely related domain or workflow that needs adaptation",
    "Base": "provides reusable technical building blocks rather than a finished domain app",
}


@dataclass(frozen=True)
class CatalogEntry:
    app_id: int
    name: str
    category: str
    category_anchor: str
    match_level: str
    azure_label: str
    azure_url: str
    alternative_label: str
    alternative_url: str


def anchor(value: str) -> str:
    value = value.lower().replace("&", "and")
    value = re.sub(r"[^a-z0-9\s-]", "", value)
    return re.sub(r"[\s-]+", "-", value).strip("-")


def parse_link(cell: str, context: str) -> tuple[str, str]:
    match = LINK.fullmatch(cell.strip())
    if not match:
        raise RuntimeError(f"Expected a Markdown link for {context}: {cell}")
    return match.group(1), match.group(2)


def parse_catalog() -> dict[int, CatalogEntry]:
    entries: dict[int, CatalogEntry] = {}
    category = ""
    for raw_line in CATALOG.read_text(encoding="utf-8").splitlines():
        if raw_line.startswith("## "):
            category = raw_line[3:].strip()
            continue
        if not re.match(r"^\|\s*\d+\s*\|", raw_line):
            continue

        cells = [cell.strip() for cell in raw_line.strip().strip("|").split("|")]
        if len(cells) != 5:
            raise RuntimeError(f"Unexpected catalog row shape: {raw_line}")
        app_id = int(cells[0])
        name = cells[1]
        match_level = cells[2].strip("*")
        if match_level not in MATCH_EXPLANATIONS:
            raise RuntimeError(f"Unknown match level for app {app_id}: {match_level}")
        azure_label, azure_url = parse_link(cells[3], f"app {app_id} Azure reference")
        alternative_label, alternative_url = parse_link(cells[4], f"app {app_id} alternative")
        if app_id in entries:
            raise RuntimeError(f"Duplicate app ID in catalog: {app_id}")
        entries[app_id] = CatalogEntry(
            app_id=app_id,
            name=name,
            category=category,
            category_anchor=anchor(category),
            match_level=match_level,
            azure_label=azure_label,
            azure_url=azure_url,
            alternative_label=alternative_label,
            alternative_url=alternative_url,
        )

    expected = set(range(1, 108))
    if set(entries) != expected:
        missing = sorted(expected - set(entries))
        extra = sorted(set(entries) - expected)
        raise RuntimeError(f"Catalog IDs do not equal 1..107; missing={missing}, extra={extra}")
    return entries


def implementation_block(entry: CatalogEntry) -> str:
    explanation = MATCH_EXPLANATIONS[entry.match_level]
    return (
        "<!-- implementation-links:auto:start -->\n"
        f"### Implementation references for {entry.name}\n\n"
        f"- **Azure / Microsoft ({entry.match_level} match):** "
        f"[{entry.azure_label}]({entry.azure_url}) — {explanation}.\n"
        f"- **LangChain / Vercel alternative:** "
        f"[{entry.alternative_label}]({entry.alternative_url}).\n"
        f"- **Catalog mapping:** "
        f"[App #{entry.app_id} in {entry.category}](../../README.md#{entry.category_anchor}).\n"
        "<!-- implementation-links:auto:end -->\n\n"
    )


def synchronize_document(path: Path, entries: dict[int, CatalogEntry]) -> tuple[str, list[int]]:
    original = path.read_text(encoding="utf-8")
    text = BLOCK.sub("\n\n", original)
    app_matches = list(APP_HEADING.finditer(text))
    if not app_matches:
        return text, []

    output: list[str] = []
    cursor = 0
    document_ids: list[int] = []
    for index, app_match in enumerate(app_matches):
        section_start = app_match.end()
        section_end = app_matches[index + 1].start() if index + 1 < len(app_matches) else len(text)
        section = text[section_start:section_end]
        reference = REFERENCE_HEADING.search(section)
        if not reference:
            raise RuntimeError(f"App {app_match.group(1)} has no Reference architecture section in {path}")

        app_id = int(app_match.group(1))
        title = app_match.group(2).strip()
        entry = entries.get(app_id)
        if not entry:
            raise RuntimeError(f"App {app_id} in {path} is absent from the root catalog")
        if title.casefold() != entry.name.casefold():
            raise RuntimeError(
                f"App {app_id} title mismatch: architecture={title!r}, catalog={entry.name!r}"
            )

        insertion = section_start + reference.start()
        output.append(text[cursor:insertion])
        output.append(implementation_block(entry))
        cursor = insertion
        document_ids.append(app_id)

    output.append(text[cursor:])
    return "".join(output), document_ids


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="fail when architecture links are stale")
    args = parser.parse_args()

    entries = parse_catalog()
    all_ids: list[int] = []
    stale: list[Path] = []
    documents = sorted(ARCHITECTURES.glob("[0-9][0-9]-*.md"))
    for path in documents:
        expected, document_ids = synchronize_document(path, entries)
        all_ids.extend(document_ids)
        current = path.read_text(encoding="utf-8")
        if current == expected:
            continue
        if args.check:
            stale.append(path)
        else:
            path.write_text(expected, encoding="utf-8", newline="\n")

    if sorted(all_ids) != list(range(1, 108)) or len(set(all_ids)) != 107:
        raise RuntimeError("Architecture document IDs do not equal unique range 1..107")
    if stale:
        listed = "\n".join(str(path.relative_to(ROOT)) for path in stale)
        raise RuntimeError(f"Implementation links are stale; run this script without --check:\n{listed}")

    action = "Verified" if args.check else "Synchronized"
    print(f"{action} implementation links for {len(all_ids)} apps across {len(documents)} documents")


if __name__ == "__main__":
    try:
        main()
    except RuntimeError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc
