#!/usr/bin/env python
"""Render and verify the catalog's committed Mermaid SVG diagrams.

The published architecture pages reference committed SVG files instead of asking
GitHub to render 7-17 Mermaid blocks on one page. Editable Mermaid source lives
beside each SVG. Rendering is pinned and `--check` compares a fresh render with
the committed output, so stale diagrams fail CI.
"""

from __future__ import annotations

import argparse
import hashlib
import os
import re
import shutil
import subprocess
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARCHITECTURES = ROOT / "docs" / "architectures"
DIAGRAMS = ROOT / "docs" / "diagrams" / "mermaid"
PUPPETEER_CONFIG = ROOT / "scripts" / "puppeteer-config.json"
MERMAID_VERSION = "12.2.0"
MERMAID_PACKAGE = f"@mermaid-js/mermaid-cli@{MERMAID_VERSION}"
MERMAID_BLOCK = re.compile(r"```mermaid\s*\n(.*?)\n```", re.DOTALL)
IMAGE_LINK = re.compile(r"!\[[^\]]*\]\((\.\./diagrams/mermaid/[^)]+\.svg)\)")
SOURCE_LINK = re.compile(r"\[[^\]]*\]\((\.\./diagrams/mermaid/[^)]+\.mmd)\)")
SOURCE_HASH = re.compile(r"^<!-- source-sha256: ([0-9a-f]{64}); mermaid-cli: ([^ ]+) -->$")


def temporary_directory(prefix: str) -> tempfile.TemporaryDirectory[str]:
    override = os.environ.get("B2C_DIAGRAM_SCRATCH")
    if override:
        scratch = Path(override)
        scratch.mkdir(parents=True, exist_ok=True)
        return tempfile.TemporaryDirectory(prefix=prefix, dir=scratch)
    return tempfile.TemporaryDirectory(prefix=prefix)


def mermaid_command() -> list[str]:
    local_name = "mmdc.cmd" if os.name == "nt" else "mmdc"
    local = ROOT / "node_modules" / ".bin" / local_name
    if local.is_file():
        return [str(local)]

    npx = shutil.which("npx") or shutil.which("npx.cmd")
    if not npx:
        raise RuntimeError("Node.js and npx are required to render diagrams")
    return [npx, "--yes", MERMAID_PACKAGE]


def source_digest(source: Path) -> str:
    normalized = source.read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    return hashlib.sha256(normalized).hexdigest()


def normalized_svg(source: Path, rendered: Path) -> str:
    svg = rendered.read_text(encoding="utf-8").replace("\r\n", "\n").lstrip("\ufeff")
    metadata = f"<!-- source-sha256: {source_digest(source)}; mermaid-cli: {MERMAID_VERSION} -->"
    return metadata + "\n" + svg.rstrip() + "\n"


def render_category(category_dir: Path, destination: Path) -> int:
    sources = sorted((category_dir / "source").glob("*.mmd"))
    if not sources:
        raise RuntimeError(f"No Mermaid sources found under {category_dir / 'source'}")

    destination.mkdir(parents=True, exist_ok=True)
    with temporary_directory("mermaid-render-") as temp_name:
        temp = Path(temp_name)
        markdown = temp / f"{category_dir.name}.md"
        rendered_markdown = temp / f"{category_dir.name}-rendered.md"
        markdown.write_text(
            "\n\n".join(
                f"## {source.stem}\n\n```mermaid\n{source.read_text(encoding='utf-8').rstrip()}\n```"
                for source in sources
            )
            + "\n",
            encoding="utf-8",
            newline="\n",
        )

        subprocess.run(
            [
                *mermaid_command(),
                "-i",
                str(markdown),
                "-o",
                str(rendered_markdown),
                "-p",
                str(PUPPETEER_CONFIG),
            ],
            cwd=ROOT,
            check=True,
        )

        generated = sorted(
            temp.glob(f"{category_dir.name}-rendered-*.svg"),
            key=lambda path: int(path.stem.rsplit("-", 1)[1]),
        )
        if len(generated) != len(sources):
            raise RuntimeError(
                f"{category_dir.name}: rendered {len(generated)} SVGs from {len(sources)} sources"
            )

        for source, rendered in zip(sources, generated, strict=True):
            target = destination / f"{source.stem}.svg"
            target.write_text(normalized_svg(source, rendered), encoding="utf-8", newline="\n")

    return len(sources)


def verify_references(expected_count: int) -> None:
    documents = sorted(ARCHITECTURES.glob("[0-9][0-9]-*.md"))
    live_blocks = sum(len(MERMAID_BLOCK.findall(path.read_text(encoding="utf-8"))) for path in documents)
    if live_blocks:
        raise RuntimeError(f"Found {live_blocks} live Mermaid blocks; published pages must use SVGs")

    references: list[Path] = []
    sources: list[Path] = []
    for document in documents:
        text = document.read_text(encoding="utf-8")
        references.extend((document.parent / relative).resolve() for relative in IMAGE_LINK.findall(text))
        sources.extend((document.parent / relative).resolve() for relative in SOURCE_LINK.findall(text))

    missing = [path for path in references + sources if not path.is_file()]
    if missing:
        raise RuntimeError("Missing diagram artifacts:\n" + "\n".join(map(str, missing)))
    if len(references) != expected_count or len(set(references)) != expected_count:
        raise RuntimeError(f"Found {len(references)} SVG references; expected {expected_count} unique links")
    if len(sources) != expected_count or len(set(sources)) != expected_count:
        raise RuntimeError(f"Found {len(sources)} Mermaid source links; expected {expected_count} unique links")


def verify_svg_metadata(expected_count: int) -> None:
    sources = sorted(DIAGRAMS.glob("*/source/*.mmd"))
    if len(sources) != expected_count:
        raise RuntimeError(f"Found {len(sources)} Mermaid sources; expected {expected_count}")

    errors: list[str] = []
    for source in sources:
        svg = source.parent.parent / f"{source.stem}.svg"
        if not svg.is_file():
            errors.append(f"missing: {svg.relative_to(ROOT)}")
            continue
        text = svg.read_text(encoding="utf-8")
        first_line = text.splitlines()[0] if text else ""
        match = SOURCE_HASH.fullmatch(first_line)
        if not match:
            errors.append(f"missing source metadata: {svg.relative_to(ROOT)}")
        elif match.group(1) != source_digest(source) or match.group(2) != MERMAID_VERSION:
            errors.append(f"stale: {svg.relative_to(ROOT)}")
        try:
            ET.fromstring("\n".join(text.splitlines()[1:]))
        except ET.ParseError as exc:
            errors.append(f"invalid SVG {svg.relative_to(ROOT)}: {exc}")

    if errors:
        raise RuntimeError("Diagram metadata validation failed:\n" + "\n".join(errors))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--check",
        action="store_true",
        help="freshly render all sources and verify committed SVG freshness without modifying files",
    )
    args = parser.parse_args()

    categories = sorted(path for path in DIAGRAMS.iterdir() if path.is_dir())
    if not categories:
        raise RuntimeError("No diagram source categories found")

    rendered_total = 0
    if args.check:
        source_count = sum(1 for _ in DIAGRAMS.glob("*/source/*.mmd"))
        verify_svg_metadata(source_count)
        with temporary_directory("mermaid-check-") as temp_name:
            check_root = Path(temp_name)
            for category in categories:
                rendered_total += render_category(category, check_root / category.name)
    else:
        for category in categories:
            rendered_total += render_category(category, category)

    verify_references(rendered_total)
    verify_svg_metadata(rendered_total)
    mode = "Verified" if args.check else "Rendered"
    print(f"{mode} {rendered_total} Mermaid diagrams across {len(categories)} categories")


if __name__ == "__main__":
    main()