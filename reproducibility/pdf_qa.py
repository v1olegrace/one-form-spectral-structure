"""Automated structural QA for the rendered manuscript PDF."""

from __future__ import annotations

import json
import re
import unicodedata
from pathlib import Path

import fitz


ROOT = Path(__file__).resolve().parents[1]
PDF_PATH = ROOT / "output" / "pdf" / "symmetry_resolved_positivity_audited.pdf"
REPORT_PATH = ROOT / "output" / "data" / "pdf_qa.json"


def normalized(text: str) -> str:
    value = unicodedata.normalize("NFKD", text)
    value = "".join(char for char in value if not unicodedata.combining(char)).lower()
    return re.sub(r"\s+", " ", value).strip()


def main() -> None:
    doc = fitz.open(PDF_PATH)
    all_text = "\n".join(page.get_text() for page in doc)
    plain = normalized(all_text)

    empty_pages: list[int] = []
    out_of_bounds: list[dict[str, object]] = []
    page_sizes: set[tuple[float, float]] = set()
    image_occurrences = 0

    for page_number, page in enumerate(doc, start=1):
        page_text = page.get_text().strip()
        if len(page_text) < 40:
            empty_pages.append(page_number)
        page_sizes.add((round(page.rect.width, 2), round(page.rect.height, 2)))
        image_occurrences += len(page.get_images(full=True))
        for block in page.get_text("blocks"):
            rectangle = fitz.Rect(block[:4])
            if not page.rect.contains(rectangle):
                tolerance = 1.0
                if (
                    rectangle.x0 < page.rect.x0 - tolerance
                    or rectangle.y0 < page.rect.y0 - tolerance
                    or rectangle.x1 > page.rect.x1 + tolerance
                    or rectangle.y1 > page.rect.y1 + tolerance
                ):
                    out_of_bounds.append(
                        {
                            "page": page_number,
                            "rectangle": [round(value, 2) for value in block[:4]],
                            "text": block[4][:100],
                        }
                    )

    forbidden_patterns = [
        r"(?<!\w)TODO(?!\w)",
        r"(?<!\w)TBD(?!\w)",
        r"(?<!\w)PLACEHOLDER(?!\w)",
        r"(?<!\w)undefined(?!\w)",
        r"(?<!\w)NaN(?!\w)",
        r"codex-file-citation",
        r"\{\{",
        r"\}\}",
    ]
    required_phrases = [
        "positividade espectral com simetrias de 1-forma",
        "teorema 6",
        "apendice d",
        "notas e referencias numeradas",
        "confianca das referencias",
    ]
    forbidden_hits = {
        pattern: len(re.findall(pattern, all_text)) for pattern in forbidden_patterns
    }
    required_hits = {phrase: phrase in plain for phrase in required_phrases}

    expected_a4_points = (595.28, 841.89)
    a4_ok = all(
        abs(width - expected_a4_points[0]) < 1.0
        and abs(height - expected_a4_points[1]) < 1.0
        for width, height in page_sizes
    )
    checks = {
        "pdf_exists": PDF_PATH.is_file(),
        "page_count_at_least_15": len(doc) >= 15,
        "all_pages_nonempty": not empty_pages,
        "all_pages_a4": a4_ok,
        "no_out_of_bounds_text_blocks": not out_of_bounds,
        "no_forbidden_placeholders": not any(forbidden_hits.values()),
        "all_required_sections_present": all(required_hits.values()),
        "at_least_two_embedded_image_occurrences": image_occurrences >= 2,
    }
    report = {
        "pdf": str(PDF_PATH.relative_to(ROOT)),
        "page_count": len(doc),
        "word_count_approx": len(re.findall(r"\b\w+\b", all_text)),
        "page_sizes_points": sorted(page_sizes),
        "empty_pages": empty_pages,
        "out_of_bounds_text_blocks": out_of_bounds,
        "image_occurrences": image_occurrences,
        "forbidden_pattern_hits": forbidden_hits,
        "required_phrase_hits": required_hits,
        "checks": checks,
        "all_checks_pass": all(checks.values()),
    }
    REPORT_PATH.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(report, ensure_ascii=False, indent=2))
    if not report["all_checks_pass"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
