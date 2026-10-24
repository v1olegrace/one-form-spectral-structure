"""Build the reviewed canonical claim graph; fail on uncovered formal units.

The catalog contains human-reviewed scientific judgments. This generator only
resolves source locations, inventories the canonical claim surface, and checks
coverage/dependency integrity. It never infers proof from a passing test.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
STATUSES = {"PROVED", "PROVED_CONDITIONALLY", "CLASSICAL", "CHECKED", "CERTIFIED",
            "CHECKED_COMPATIBLE", "SUPPORTED_BY_LITERATURE", "OPEN", "UNRESOLVED", "RETRACTED"}
FILES = ("paper/paper.tex", "paper/appendix.tex")


def braced(text: str, offset: int) -> tuple[str, int]:
    depth, pos = 1, offset
    while depth and pos < len(text):
        depth += (text[pos] == "{") - (text[pos] == "}")
        pos += 1
    if depth:
        raise ValueError("unclosed source brace")
    return text[offset:pos - 1], pos


def inventory(sources: dict[str, str]) -> list[dict]:
    units = []
    for filename, source in sources.items():
        pattern = r"\\begin\{(theorem|proposition|lemma|hypothesis|definition|remark)\}"
        for count, match in enumerate(re.finditer(pattern, source), 1):
            kind = match.group(1)
            end = source.index(r"\end{" + kind + "}", match.end()) + len(kind) + 6
            content = source[match.start():end]
            label = re.search(r"\\label\{([^}]+)\}", content)
            key = label.group(1) if label else f"{kind}-{count}"
            units.append(dict(unit_id=f"{filename}#{key}", kind=kind, text=content,
                              line=source.count("\n", 0, match.start()) + 1))
        for match in re.finditer(r"\\paragraph\{", source):
            title, end = braced(source, match.end())
            # A paragraph unit ends at the next heading, formal environment or the end
            # of the text, so an anchor further on cannot mark it as covered.
            tail = re.search(r"\\(?:paragraph\{|(?:sub)*section\*?\{|begin\{(?:theorem|proposition|lemma"
                             r"|corollary|definition|hypothesis|remark)\}|bibliography\{|end\{document\})",
                             source[end:])
            stop = end + tail.start() if tail else len(source)
            units.append(dict(unit_id=f"{filename}#paragraph:{title}", kind="paragraph",
                              text=source[match.start():stop],
                              line=source.count("\n", 0, match.start()) + 1))
    return units


def build(root: Path = ROOT) -> dict:
    sources = {name: (root / name).read_text(encoding="utf-8") for name in FILES}
    catalog = json.loads((root / ".agent/claim_catalog.json").read_text(encoding="utf-8"))
    units = inventory(sources)
    claims = []
    ids = {entry["claim_id"] for entry in catalog["claims"]}
    if len(ids) != len(catalog["claims"]):
        raise ValueError("duplicate claim IDs")
    for entry in catalog["claims"]:
        item = dict(entry)
        filename, anchor = item.pop("source"), item.pop("anchor")
        source = sources[filename]
        if anchor not in source:
            raise ValueError(f"{item['claim_id']}: missing reviewed source anchor {anchor!r}")
        start = source.index(anchor)
        item["location"] = {"file": filename, "line": source.count("\n", 0, start) + 1,
                            "anchor": anchor}
        if item["status"] not in STATUSES:
            raise ValueError(f"{item['claim_id']}: invalid epistemic status")
        for dependency in item["depends_on"]["lemmas"]:
            if dependency not in ids:
                raise ValueError(f"{item['claim_id']}: unknown logical dependency {dependency}")
        claims.append(item)
    uncovered = [unit["unit_id"] for unit in units if not any(
        claim["location"]["file"] == unit["unit_id"].split("#")[0]
        and (claim["location"]["anchor"] in unit["text"]
             or unit["text"][:80] in claim["location"]["anchor"])
        for claim in claims)]
    if uncovered:
        raise ValueError("Unreviewed formal/paragraph source units: " + "; ".join(uncovered))
    ledger = re.search(r"## Claim ledger(.*?)## Status", (root / "README.md").read_text("utf-8"), re.S)
    advertised = set(re.findall(r"\| (C\d+) \|", ledger.group(1))) if ledger else set()
    projected = {item["readme_claim_id"] for item in claims if item.get("readme_claim_id")}
    if advertised - projected:
        raise ValueError("README claims absent from graph: " + str(sorted(advertised - projected)))
    # Prose in the abstract and discussion has a separate reviewed inventory.
    for surface in ("abstract", "discussion"):
        if not any(surface in c.get("surfaces", []) for c in claims):
            raise ValueError(f"No reviewed {surface} claims")
    return {
        "schema_version": 1,
        "review_started": "2026-10-22", "execution_continued": "2026-10-23",
        "baseline_head": "78b637cb6a2cf4d92691a3eb7e31312baf23ef32",
        "canonical_source_sha256": {name: hashlib.sha256(text.encode()).hexdigest()
                                    for name, text in sources.items()},
        "dependency_semantics": {"depends_on": "logical", "literature_precedent": "prior art, not a premise",
                                  "numerical_results": "illustration/check, never a proof premise unless certified and explicit",
                                  "historical_inspiration": "history only"},
        "coverage": {"formal_and_major_paragraph_units": len(units), "uncovered": uncovered,
                     "readme_claim_ids": sorted(advertised),
                     "abstract_and_discussion": "reviewed subclaims in catalog; open steps separated"},
        "claims": claims,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    graph = build()
    rendered = json.dumps(graph, indent=2, ensure_ascii=False) + "\n"
    path = ROOT / ".agent/claims.json"
    if args.check:
        if not path.exists() or path.read_text("utf-8") != rendered:
            raise SystemExit("Claim graph is stale; run python scripts/build_claim_graph.py")
    else:
        path.write_text(rendered, encoding="utf-8")
    print(f"{len(graph['claims'])} reviewed claims; {graph['coverage']['formal_and_major_paragraph_units']} source units; no uncovered units")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
