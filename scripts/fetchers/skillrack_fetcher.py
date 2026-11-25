"""SkillRack public resume parser."""

from __future__ import annotations

import re
from typing import Any

from bs4 import BeautifulSoup

from scripts.fetchers.http_client import request_with_retry


def fetch_skillrack_stats(config: dict[str, Any]) -> dict[str, Any]:
    """Fetch SkillRack programs solved, medals, rank, certificates, and languages."""
    sr_cfg = config["platforms"]["skillrack"]
    auto_cfg = config["automation"]
    timeout = max(int(auto_cfg.get("request_timeout_seconds", 15)), 20)
    max_retries = int(auto_cfg.get("max_retries", 3))

    url = f"https://www.skillrack.com/faces/resume.xhtml?id={sr_cfg['id']}&key={sr_cfg['key']}"
    resp = request_with_retry(
        "GET",
        url,
        headers={
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
        },
        timeout=timeout,
        max_retries=max_retries,
    )
    soup = BeautifulSoup(resp.text, "html.parser")

    text = re.sub(r"\s+", " ", soup.get_text(" ", strip=True))

    def _extract_int(pattern: str) -> int | None:
        m = re.search(pattern, text, re.IGNORECASE)
        return int(m.group(1).replace(",", "")) if m else None

    rank = _extract_int(r"([\d,]+)\s+RANK\b")
    gold = _extract_int(r"(\d+)\s+GOLD\b")
    silver = _extract_int(r"(\d+)\s+SILVER\b")
    bronze = _extract_int(r"(\d+)\s+BRONZE\b")
    programs_solved = _extract_int(r"([\d,]+)\s+PROGRAMS\s+SOLVED\b")
    certificates = _extract_int(r"(\d+)\s+CERTIFICATE\(S\)")

    if programs_solved is None:
        raise RuntimeError("Could not parse SkillRack programs solved count")

    # Language breakdown near CERTIFICATE(S) block
    languages: dict[str, int] = {}
    for lang_label in ("C", "Java", "CPP23", "Python3", "SQL", "CPP"):
        m = re.search(rf"\b(\d+)\s+{re.escape(lang_label)}\b", text)
        if m:
            languages[lang_label] = int(m.group(1))

    return {
        "rank": rank,
        "programs_solved": programs_solved,
        "gold_medals": gold or 0,
        "silver_medals": silver or 0,
        "bronze_medals": bronze or 0,
        "certificates": certificates or 0,
        "languages": languages,
        "profile_url": url,
    }
