#!/usr/bin/env python3
"""Extract repository context into a concise brand brief input file."""

from __future__ import annotations

import argparse
import collections
import pathlib
import re

SKIP_DIRS = {
    ".git",
    ".next",
    ".venv",
    "venv",
    "node_modules",
    "dist",
    "build",
    "coverage",
}
PRIORITY_FILES = [
    "README.md",
    "README.MD",
    "package.json",
    "pyproject.toml",
    "Cargo.toml",
]
TEXT_EXTENSIONS = {".md", ".txt", ".rst", ".json", ".toml", ".yaml", ".yml", ".ts", ".tsx", ".js", ".jsx", ".py"}
STOPWORDS = {
    "about", "after", "also", "because", "before", "being", "between", "build", "built", "could",
    "create", "from", "have", "into", "just", "more", "most", "other", "over", "project", "should",
    "some", "that", "their", "there", "these", "they", "this", "those", "under", "using", "what",
    "when", "where", "with", "your",
}


def is_text_candidate(path: pathlib.Path) -> bool:
    return path.suffix.lower() in TEXT_EXTENSIONS or path.name in PRIORITY_FILES


def iter_candidate_files(project_root: pathlib.Path, max_files: int) -> list[pathlib.Path]:
    files: list[pathlib.Path] = []

    for name in PRIORITY_FILES:
        candidate = project_root / name
        if candidate.exists() and candidate.is_file():
            files.append(candidate)

    docs_dir = project_root / "docs"
    if docs_dir.exists() and docs_dir.is_dir():
        for path in sorted(docs_dir.rglob("*")):
            if path.is_file() and is_text_candidate(path):
                if any(part in SKIP_DIRS for part in path.parts):
                    continue
                files.append(path)

    for path in sorted(project_root.rglob("*")):
        if len(files) >= max_files:
            break
        if not path.is_file():
            continue
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if not is_text_candidate(path):
            continue
        if path not in files:
            files.append(path)

    return files[:max_files]


def read_snippet(path: pathlib.Path, max_chars: int) -> str:
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return ""
    return text[:max_chars].strip()


def extract_keywords(text: str) -> list[str]:
    words = re.findall(r"[a-zA-Z][a-zA-Z0-9-]{3,}", text.lower())
    filtered = [word for word in words if word not in STOPWORDS]
    counts = collections.Counter(filtered)
    return [word for word, _ in counts.most_common(30)]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", default=".", help="Project root directory.")
    parser.add_argument("--output-file", required=True, help="Output markdown file path.")
    parser.add_argument("--max-files", type=int, default=30, help="Maximum files to scan.")
    parser.add_argument("--chars-per-file", type=int, default=1600, help="Max chars to keep per file.")
    args = parser.parse_args()

    project_root = pathlib.Path(args.project_root).resolve()
    output_file = pathlib.Path(args.output_file).resolve()

    files = iter_candidate_files(project_root, args.max_files)
    snippets: list[tuple[pathlib.Path, str]] = []
    combined_text = []
    for path in files:
        snippet = read_snippet(path, args.chars_per_file)
        if not snippet:
            continue
        snippets.append((path, snippet))
        combined_text.append(snippet)

    keywords = extract_keywords("\n".join(combined_text))
    lines: list[str] = [
        "# Repository Brand Context",
        "",
        "## Source Files",
    ]
    lines.extend([f"- `{path.relative_to(project_root)}`" for path, _ in snippets])
    lines.extend(["", "## Candidate Keywords", ", ".join(keywords) if keywords else "(none)", ""])

    for path, snippet in snippets:
        rel = path.relative_to(project_root)
        lines.extend(
            [
                f"## Extract: `{rel}`",
                "```text",
                snippet,
                "```",
                "",
            ]
        )

    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text("\n".join(lines), encoding="utf-8")
    print(f"[OK] Wrote context file: {output_file}")


if __name__ == "__main__":
    main()
