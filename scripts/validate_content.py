#!/usr/bin/env python3
"""Validate generated content shape, links, private assets, and required answer sections."""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"


def main() -> None:
    data = json.loads((ROOT / "data/site-content.json").read_text(encoding="utf-8"))
    chapters = data["chapters"]
    assert len(chapters) == 12, f"expected 12 chapters, found {len(chapters)}"
    questions = [question for chapter in chapters for question in chapter["questions"]]
    assert len(questions) == 36, f"expected 36 questions, found {len(questions)}"

    required = [
        "候选人澄清问题", "功能与非功能需求", "容量估算", "API 与数据模型", "高层架构",
        "关键机制", "扩展、故障与恢复", "核心权衡", "面试官追问", "评分点",
    ]
    for chapter in chapters:
        chapter_file = DOCS / "chapters" / f"{chapter['slug']}.md"
        text = chapter_file.read_text(encoding="utf-8")
        assert "<WalkthroughExplorer" in text and "<KnowledgeCheck" in text
        for question in chapter["questions"]:
            path = DOCS / "questions" / f"{question['slug']}.md"
            content = path.read_text(encoding="utf-8")
            missing = [name for name in required if name not in content]
            assert not missing, f"{path}: missing {missing}"
            assert "对应 DDIA 知识" in content

    public_pdfs = list((DOCS / "public").rglob("*.pdf"))
    assert not public_pdfs, f"private PDFs leaked into public: {public_pdfs}"

    deep_dive_requirements = {
        "ch01.md": ["Fault 不是 Failure", "tail latency amplification", "Maintainability"],
        "ch02.md": ["Object-relational mismatch", "Declarative", "Graph-like Data Models"],
        "ch03.md": ["SSTable 与 LSM-Tree", "B-Tree", "Column-oriented Storage"],
    }
    for filename, markers in deep_dive_requirements.items():
        source = ROOT / "content-src/chapters" / filename
        content = source.read_text(encoding="utf-8")
        assert len(content) >= 5_000, f"{source}: deep-dive content is unexpectedly thin"
        missing = [marker for marker in markers if marker not in content]
        assert not missing, f"{source}: missing deep-dive sections {missing}"

    link_pattern = re.compile(r"\]\((/[^)#]+)")
    for page in DOCS.rglob("*.md"):
        for link in link_pattern.findall(page.read_text(encoding="utf-8")):
            target = DOCS / (link.strip("/") + ".md")
            index = DOCS / link.strip("/") / "index.md"
            assert target.exists() or index.exists() or link == "/", f"dead link in {page}: {link}"

    print("Validated 12 walkthroughs, 36 questions, Ch1-3 deep dives, links, and private PDF boundary")


if __name__ == "__main__":
    main()
