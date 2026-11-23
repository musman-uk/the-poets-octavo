from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUTPUT_FILE = ROOT / f"{ROOT.name}-code.txt"

EXCLUDE_DIRS = {
    ".git",
    ".github",
    ".vscode",
    ".idea",
    "__pycache__",
    ".venv",
    "venv",
    "node_modules",
    "docs",
    "releases",
}

EXCLUDE_FILES = {
    OUTPUT_FILE.name,
    "bundle_code.py",
    ".DS_Store",
    "Thumbs.db",
}

ALLOWED_EXTENSIONS = {
    ".py",
    ".md",
    ".html",
    ".css",
    ".js",
    ".json",
    ".txt",
    ".yml",
    ".yaml",
}


def collect_files(base: Path) -> list[Path]:
    files = []
    for path in base.rglob("*"):
        if not path.is_file():
            continue
        if any(part in EXCLUDE_DIRS for part in path.relative_to(base).parts):
            continue
        if path.name in EXCLUDE_FILES or path.name.endswith("-code.txt"):
            continue
        if path.suffix.lower() not in ALLOWED_EXTENSIONS:
            continue
        files.append(path)

    return sorted(
        files,
        key=lambda p: (
            len(p.relative_to(base).parts) > 1,
            p.relative_to(base).as_posix(),
        ),
    )


def main() -> None:
    files = collect_files(ROOT)
    sections = [f"=== {ROOT.name} ==="]

    for path in files:
        rel_path = path.relative_to(ROOT).as_posix()
        content = path.read_text(encoding="utf-8").rstrip()
        sections.append(f"==> {rel_path} <==\n{content}")

    OUTPUT_FILE.write_text("\n\n".join(sections) + "\n", encoding="utf-8")
    print(f"Bundled {len(files)} files into {OUTPUT_FILE.name}")


if __name__ == "__main__":
    main()
