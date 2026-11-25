"""Unit and integration tests for the GitHub Profile README automation pipeline."""

from __future__ import annotations

import xml.etree.ElementTree as ET
from pathlib import Path

import pytest

from scripts.config_loader import load_config
from scripts.generators.readme_generator import replace_marker_section, update_readme
from scripts.generators.svg_generator import write_all_svgs
from scripts.processors.stats_processor import (
    compute_monthly_contributions,
    compute_streaks,
    compute_top_languages,
    normalize_snapshot,
)


def test_compute_streaks_handles_trailing_zero_today() -> None:
    days = [
        {"date": "2026-11-21", "count": 0, "level": 0},
        {"date": "2026-11-22", "count": 2, "level": 1},
        {"date": "2026-11-23", "count": 4, "level": 2},
        {"date": "2026-11-24", "count": 1, "level": 1},
        {"date": "2026-11-25", "count": 0, "level": 0},
    ]
    streaks = compute_streaks(days)
    assert streaks["current_streak"] == 3
    assert streaks["longest_streak"] == 3
    assert streaks["active_days"] == 3


def test_compute_monthly_contributions_orders_chronologically() -> None:
    days = [
        {"date": "2026-09-10", "count": 5, "level": 1},
        {"date": "2026-10-01", "count": 10, "level": 2},
        {"date": "2026-10-02", "count": 4, "level": 1},
        {"date": "2026-11-15", "count": 8, "level": 2},
    ]
    monthly = compute_monthly_contributions(days, months=3)
    assert [m["month"] for m in monthly] == ["2026-09", "2026-10", "2026-11"]
    assert [m["count"] for m in monthly] == [5, 14, 8]


def test_compute_top_languages_sums_to_100() -> None:
    langs = compute_top_languages({"TypeScript": 600, "Python": 300, "CSS": 100}, limit=2)
    assert langs[0]["name"] == "TypeScript"
    assert langs[0]["percent"] == 60.0
    assert langs[-1]["name"] == "Other"
    assert sum(item["percent"] for item in langs) == pytest.approx(100.0)


def test_normalize_snapshot_preserves_cached_fallback_and_is_idempotent() -> None:
    raw_first = {
        "github": {
            "username": "PRAJEENS2024",
            "source": "github_rest_public",
            "public_repos": 20,
            "total_stars": 3,
            "total_forks": 1,
            "followers": 2,
            "total_contributions": 400,
            "languages_bytes": {"TypeScript": 1000, "Python": 500},
            "calendar_days": [{"date": "2026-11-24", "count": 3, "level": 2}],
            "recent_events": [],
        },
        "leetcode": {"username": "PRAJEEN24", "total_solved": 624, "easy": 352, "medium": 259, "hard": 13},
        "codechef": {"username": "prajeens", "total_solved": 503, "rating": 1053, "highest_rating": 1083, "stars": 1, "contests": 14},
        "skillrack": {"programs_solved": 1567, "bronze_medals": 539, "certificates": 17, "rank": 7855, "languages": {"C": 957}},
        "hackerrank": {"username": "prajeensenthilk1", "badges": [{"name": "Sql", "stars": 2, "solved": 15}]},
    }
    snap1, status1, changed1 = normalize_snapshot(raw_first, previous_snapshot=None)
    assert changed1 is True
    assert all(v == "live" for v in status1.values())

    # Second run with identical data is strictly idempotent
    snap2, _, changed2 = normalize_snapshot(raw_first, previous_snapshot=snap1)
    assert changed2 is False
    assert snap2["content_hash"] == snap1["content_hash"]
    assert snap2["last_updated"] == snap1["last_updated"]

    # Partial failure preserves previous valid LeetCode data
    raw_partial = dict(raw_first)
    raw_partial["leetcode"] = None
    snap3, status3, changed3 = normalize_snapshot(raw_partial, previous_snapshot=snap2)
    assert status3["leetcode"] == "cached_fallback"
    assert snap3["derived"]["coding"]["leetcode"]["total_solved"] == 624
    assert changed3 is False


def test_readme_marker_replacement_preserves_manual_content(tmp_path: Path) -> None:
    readme = tmp_path / "README.md"
    readme.write_text(
        "# Header\n\nManual intro\n\n"
        "<!-- AUTO-GENERATED-START: github-stats -->\nold\n<!-- AUTO-GENERATED-END: github-stats -->\n\n"
        "<!-- AUTO-GENERATED-START: coding-stats -->\nold\n<!-- AUTO-GENERATED-END: coding-stats -->\n\n"
        "<!-- AUTO-GENERATED-START: activity -->\nold\n<!-- AUTO-GENERATED-END: activity -->\n\n"
        "Manual footer\n",
        encoding="utf-8",
    )
    config = load_config()
    raw = {
        "github": {
            "username": "PRAJEENS2024",
            "source": "github_rest_public",
            "public_repos": 20,
            "total_stars": 0,
            "total_forks": 0,
            "followers": 0,
            "total_contributions": 397,
            "languages_bytes": {"TypeScript": 1000},
            "calendar_days": [{"date": "2026-11-24", "count": 2, "level": 1}],
            "recent_events": [{"date": "2026-11-20", "repo": "PRAJEENS2024/ECE-Connect", "action": "Pushed 1 commit(s)", "url": "https://github.com/PRAJEENS2024/ECE-Connect"}],
        },
        "leetcode": {
            "username": "PRAJEEN24",
            "total_solved": 624,
            "easy": 352,
            "medium": 259,
            "hard": 13,
            "streak": 366,
            "profile_ranking": 135681,
            "contest_rating": 1725,
            "contests_attended": 79,
            "top_percentage": 12.43,
            "recent_submissions": [{"title": "Zigzag Conversion", "slug": "zigzag-conversion", "url": "https://leetcode.com/problems/zigzag-conversion/", "date": "2026-11-24"}],
        },
        "codechef": {"username": "prajeens", "total_solved": 503, "rating": 1053, "highest_rating": 1083, "stars": 1, "contests": 14},
        "skillrack": {"programs_solved": 1567, "bronze_medals": 539, "certificates": 17, "rank": 7855, "languages": {"C": 957}},
        "hackerrank": {"username": "prajeensenthilk1", "badges": [{"name": "Sql", "stars": 2, "solved": 15}]},
    }
    snap, _, _ = normalize_snapshot(raw)
    svg_dir = tmp_path / "assets" / "svg"
    write_all_svgs(svg_dir, config, snap)

    # Validate all generated SVGs and logo icons are well-formed XML
    for name in ("hero-banner.svg", "github-stats.svg", "contribution-heatmap.svg", "coding-profiles.svg"):
        ET.fromstring((svg_dir / name).read_text(encoding="utf-8"))
    for logo_file in (svg_dir / "logos").glob("*.svg"):
        ET.fromstring(logo_file.read_text(encoding="utf-8"))

    changed = update_readme(readme, config, snap)
    assert changed is True
    text = readme.read_text(encoding="utf-8")
    assert "Manual intro" in text
    assert "Manual footer" in text
    assert "ECE-Connect" in text
    assert "Zigzag Conversion" in text

    # Second update with same snapshot must be a no-op
    assert update_readme(readme, config, snap) is False


def test_replace_marker_section_raises_if_missing() -> None:
    with pytest.raises(ValueError):
        replace_marker_section("no markers here", "github-stats", "body")
