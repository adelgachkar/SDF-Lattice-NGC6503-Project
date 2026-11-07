"""Check in-text citation coverage against References/08_References.bib.

Every bibliography entry must be cited with an [@key] marker somewhere in the
manuscript, and every [@key] marker must resolve to a bibliography entry.

Usage:
    python Scripts/check_citations.py            # report + exit status
    python Scripts/check_citations.py --list     # also list keys per document

Exit status is 0 only when the bibliography has no uncited entry and the
manuscript has no undefined key.
"""

from __future__ import annotations

import argparse
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
BIB = ROOT / "References" / "08_References.bib"
DOCS = [
    "00_Master_Paper.md",
    "01_Abstract_Keywords.md",
    "02_Introduction.md",
    "03_Theoretical_BaseLayer.md",
    "03_radial_unfreezing_dynamics.md",
    "04_Data_and_Pipeline.md",
    "05_Empirical_Audits.md",
    "06_Discussion_Comparative.md",
    "07_Conclusion.md",
    "Equations_Snippets/03_radial_unfreezing_dynamics.md",
]

ENTRY_RE = re.compile(r"^@(?!preamble)(\w+)\{\s*([^,\s]+)\s*,", re.MULTILINE)
CITE_RE = re.compile(r"@([A-Za-z][A-Za-z0-9_:\-]*)")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--list", action="store_true", help="list keys per document")
    args = parser.parse_args(argv)

    if not BIB.is_file():
        print(f"missing bibliography: {BIB}", file=sys.stderr)
        return 2

    bib_text = BIB.read_text(encoding="utf-8")
    entries = [key for _kind, key in ENTRY_RE.findall(bib_text)]
    preambles = len(re.findall(r"^@preamble\{", bib_text, re.MULTILINE))

    per_doc: dict[str, list[str]] = {}
    for name in DOCS:
        path = ROOT / name
        if not path.is_file():
            print(f"missing document: {name}", file=sys.stderr)
            return 2
        per_doc[name] = CITE_RE.findall(path.read_text(encoding="utf-8"))

    cited = {key for keys in per_doc.values() for key in keys}
    uncited = [key for key in entries if key not in cited]
    undefined = sorted(cited - set(entries))

    print(f"bibliography entries      : {len(entries)} (+{preambles} @preamble)")
    print(f"entries cited in the text : {len(set(entries) & cited)}")
    print(f"undefined keys in text    : {len(undefined)}")
    print(f"uncited entries           : {len(uncited)}")

    if args.list:
        for name, keys in per_doc.items():
            print(f"  {name:44s} {len(keys):3d} markers, {len(set(keys)):2d} unique")

    if undefined:
        print("\nundefined: " + ", ".join(undefined))
    if uncited:
        print("\nuncited: " + ", ".join(uncited))

    if undefined or uncited:
        return 1
    print("\nOK: every entry is cited and every marker resolves.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
