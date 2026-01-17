import os
import re

ROOT = "spec/0.1"
OUT = "linkcheck-report.txt"

LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")


def is_external(target: str) -> bool:
    return bool(re.match(r"^[a-zA-Z]+://", target)) or target.startswith("mailto:")


def main() -> int:
    md_files: list[str] = []
    for dirpath, _, filenames in os.walk(ROOT):
        for filename in filenames:
            if filename.endswith(".md"):
                md_files.append(os.path.join(dirpath, filename))

    broken: list[tuple[str, str, str, str]] = []

    for file_path in md_files:
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()

        base = os.path.dirname(file_path)
        for raw_target in LINK_RE.findall(text):
            target = raw_target.strip()
            if not target or target.startswith("#") or is_external(target):
                continue

            # Trim any accidental title part (not expected, but harmless)
            target = target.split()[0]
            path = target.split("#", 1)[0]
            if not path or path.startswith("data:"):
                continue

            resolved = os.path.normpath(os.path.join(base, path))

            if os.path.isdir(resolved):
                index_md = os.path.join(resolved, "index.md")
                if not os.path.exists(index_md):
                    broken.append((file_path, target, "dir missing index.md", resolved))
            else:
                if not os.path.exists(resolved):
                    broken.append((file_path, target, "missing", resolved))

    with open(OUT, "w", encoding="utf-8") as out:
        out.write(f"Checked {len(md_files)} markdown files\n")
        out.write(f"Broken links {len(broken)}\n")
        for file_path, target, why, resolved in broken:
            out.write(f"{file_path}: {target} -> {why} ({resolved})\n")

    print(OUT)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
