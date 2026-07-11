#!/usr/bin/env python3
"""Split the local DDIA source PDF using verified physical PDF page ranges."""

from __future__ import annotations

import json
from pathlib import Path

import fitz


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "private/books/ddia/original.pdf"
OUTPUT = ROOT / "private/books/ddia/parts"
MANIFEST = ROOT / "data/ddia-chapters.json"

SEGMENTS = [
    ("00-front-matter", 1, 24, 0, "前言与全书导读", "Front Matter", "front"),
    ("01-reliable-scalable-maintainable", 25, 48, 1, "可靠、可扩展与可维护", "Reliable, Scalable, and Maintainable Applications", "foundations"),
    ("02-data-models-query-languages", 49, 90, 2, "数据模型与查询语言", "Data Models and Query Languages", "foundations"),
    ("03-storage-retrieval", 91, 132, 3, "存储与检索", "Storage and Retrieval", "foundations"),
    ("04-encoding-evolution", 133, 166, 4, "编码与演化", "Encoding and Evolution", "foundations"),
    ("05-replication", 167, 220, 5, "复制", "Replication", "distributed-data"),
    ("06-partitioning", 221, 242, 6, "分区", "Partitioning", "distributed-data"),
    ("07-transactions", 243, 294, 7, "事务", "Transactions", "distributed-data"),
    ("08-trouble-with-distributed-systems", 295, 342, 8, "分布式系统的麻烦", "The Trouble with Distributed Systems", "distributed-data"),
    ("09-consistency-consensus", 343, 406, 9, "一致性与共识", "Consistency and Consensus", "distributed-data"),
    ("10-batch-processing", 407, 460, 10, "批处理", "Batch Processing", "derived-data"),
    ("11-stream-processing", 461, 510, 11, "流处理", "Stream Processing", "derived-data"),
    ("12-future-of-data-systems", 511, 574, 12, "数据系统的未来", "The Future of Data Systems", "derived-data"),
    ("99-glossary-index", 575, 613, 99, "术语表与索引", "Glossary and Index", "back"),
]


def main() -> None:
    if not SOURCE.exists():
        raise SystemExit(f"Missing source PDF: {SOURCE}")

    document = fitz.open(SOURCE)
    if document.page_count != 613:
        raise SystemExit(f"Expected 613 pages, found {document.page_count}")

    OUTPUT.mkdir(parents=True, exist_ok=True)
    manifest = []
    covered: list[int] = []

    for slug, start, end, chapter, title_zh, title_en, part in SEGMENTS:
        target = OUTPUT / f"{slug}.pdf"
        split = fitz.open()
        split.insert_pdf(document, from_page=start - 1, to_page=end - 1)
        split.save(target, garbage=4, deflate=True)
        split.close()

        page_count = end - start + 1
        with fitz.open(target) as check:
            if check.page_count != page_count:
                raise RuntimeError(f"Page count mismatch for {target.name}")

        covered.extend(range(start, end + 1))
        manifest.append({
            "chapterId": f"ch{chapter:02d}" if chapter not in (0, 99) else slug,
            "chapter": chapter,
            "order": len(manifest),
            "part": part,
            "slug": slug[3:] if chapter not in (0, 99) else slug,
            "titleZh": title_zh,
            "titleEn": title_en,
            "sourcePages": {"start": start, "end": end},
            "pageCount": page_count,
            "privatePdf": f"private/books/ddia/parts/{target.name}",
        })
        print(f"{target.name}: {start}-{end} ({page_count} pages)")

    expected = list(range(1, document.page_count + 1))
    if covered != expected:
        raise RuntimeError("Segments contain a gap, overlap, or ordering error")

    MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Verified {len(covered)} pages across {len(SEGMENTS)} segments")


if __name__ == "__main__":
    main()
