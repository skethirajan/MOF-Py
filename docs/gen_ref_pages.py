"""Generate the code reference pages and navigation."""
from __future__ import annotations

from pathlib import Path

import mkdocs_gen_files

nav = mkdocs_gen_files.Nav()  # pyright: ignore [reportPrivateImportUsage]

for path in sorted(Path("src").rglob(pattern="*.py")):
    module_path = path.relative_to("src").with_suffix(suffix="")
    doc_path = path.relative_to("src").with_suffix(suffix=".md")
    full_doc_path = Path("reference", doc_path)

    parts = tuple(module_path.parts)

    if parts[-1] == "__init__":
        parts = parts[:-1]
        doc_path = doc_path.with_name("index.md")
        full_doc_path = full_doc_path.with_name("index.md")
    elif parts[-1] == "__main__":
        continue

    nav[parts] = doc_path.as_posix()

    with mkdocs_gen_files.open(full_doc_path, "w") as fd:
        IDENT = ".".join(parts)
        fd.write(f"::: {IDENT}")

    mkdocs_gen_files.set_edit_path(full_doc_path, Path("../") / path)

with mkdocs_gen_files.open("reference/SUMMARY.md", "w") as nav_file:
    nav_file.writelines(nav.build_literate_nav())
