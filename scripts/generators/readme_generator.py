"""Safe marker-based README section generator."""

from __future__ import annotations

import re
from html import escape
from pathlib import Path
from typing import Any


def replace_marker_section(content: str, section_name: str, body: str) -> str:
    """Replace content strictly between AUTO-GENERATED-START/END markers for section_name."""
    start_tag = f"<!-- AUTO-GENERATED-START: {section_name} -->"
    end_tag = f"<!-- AUTO-GENERATED-END: {section_name} -->"
    pattern = re.compile(
        rf"({re.escape(start_tag)})(.*?)({re.escape(end_tag)})",
        flags=re.DOTALL,
    )
    if not pattern.search(content):
        raise ValueError(f"Markers for section '{section_name}' not found in README")

    replacement = f"{start_tag}\n{body.strip()}\n{end_tag}"
    return pattern.sub(lambda _: replacement, content, count=1)


def render_github_stats_section(snapshot: dict[str, Any]) -> str:
    """Render the auto-generated GitHub Statistics & Contribution Calendar section."""
    updated = snapshot.get("last_updated", "")
    gh = snapshot["derived"]["github"]
    source_label = "GitHub GraphQL API" if gh.get("source") == "github_graphql" else "GitHub REST & Public Calendar"
    return (
        '<p align="center">\n'
        '  <img src="./assets/svg/github-stats.svg" alt="GitHub Telemetry and Language Footprint" width="100%" />\n'
        '</p>\n'
        '<p align="center">\n'
        '  <img src="./assets/svg/contribution-heatmap.svg" alt="GitHub 52-Week Contribution Calendar" width="100%" />\n'
        '</p>\n'
        f'<p align="center"><sub>Source: {escape(source_label)} · Last data change: {escape(updated)}</sub></p>'
    )


def render_coding_stats_section(config: dict[str, Any], snapshot: dict[str, Any]) -> str:
    """Render Competitive Programming Dashboard with logo-linked profiles."""
    coding = snapshot["derived"]["coding"]
    lc = coding.get("leetcode") or {}
    sr = coding.get("skillrack") or {}
    cc = coding.get("codechef") or {}
    hr = coding.get("hackerrank") or {}
    gfg_url = config["platforms"]["geeksforgeeks"]["profile_url"]

    lc_url = f"https://leetcode.com/u/{lc.get('username', config['platforms']['leetcode']['username'])}"
    sr_url = sr.get(
        "profile_url",
        f"https://www.skillrack.com/faces/resume.xhtml?id={config['platforms']['skillrack']['id']}&key={config['platforms']['skillrack']['key']}",
    )
    cc_url = cc.get("profile_url", f"https://www.codechef.com/users/{config['platforms']['codechef']['username']}")
    hr_url = hr.get("profile_url", f"https://www.hackerrank.com/profile/{config['platforms']['hackerrank']['username']}")

    total_verified = coding.get("verified_solved_total", 0)
    return (
        '<p align="center">\n'
        '  <img src="./assets/svg/coding-profiles.svg" alt="Competitive Programming Metrics" width="100%" />\n'
        '</p>\n\n'
        '<p align="center">\n'
        f'  <strong>Verified Solved Total:</strong> <code>{total_verified:,}+</code><br/><br/>\n'
        f'  <a href="{escape(lc_url)}" title="LeetCode"><img src="./assets/svg/logos/leetcode.svg" width="34" height="34" alt="LeetCode" /></a>&nbsp;&nbsp;\n'
        f'  <a href="{escape(sr_url)}" title="SkillRack"><img src="./assets/svg/logos/skillrack.svg" width="34" height="34" alt="SkillRack" /></a>&nbsp;&nbsp;\n'
        f'  <a href="{escape(cc_url)}" title="CodeChef"><img src="./assets/svg/logos/codechef.svg" width="34" height="34" alt="CodeChef" /></a>&nbsp;&nbsp;\n'
        f'  <a href="{escape(hr_url)}" title="HackerRank"><img src="./assets/svg/logos/hackerrank.svg" width="34" height="34" alt="HackerRank" /></a>&nbsp;&nbsp;\n'
        f'  <a href="{escape(gfg_url)}" title="GeeksforGeeks"><img src="./assets/svg/logos/geeksforgeeks.svg" width="34" height="34" alt="GeeksforGeeks" /></a>\n'
        '</p>\n'
        '<p align="center"><sub>LeetCode, SkillRack, CodeChef, and HackerRank sync automatically. GeeksforGeeks renders client-side without a public API, so its logo links directly to the live profile.</sub></p>'
    )


def render_activity_section(snapshot: dict[str, Any]) -> str:
    """Render recent GitHub activity and recent LeetCode accepted submissions."""
    gh_events = snapshot["derived"]["github"].get("recent_events") or []
    lc_recent = (snapshot["derived"]["coding"].get("leetcode") or {}).get("recent_submissions") or []

    gh_lines = [
        f"| `{ev['date']}` | [{ev['repo'].split('/')[-1]}]({ev['url']}) | {ev['action']} |"
        for ev in gh_events[:5]
    ]
    if not gh_lines:
        gh_lines = ["| — | No recent public events recorded | — |"]

    lc_lines = [
        f"| `{sub['date']}` | [{sub['title']}]({sub['url']}) |"
        for sub in lc_recent[:5]
    ]
    if not lc_lines:
        lc_lines = ["| — | No recent submissions available |"]

    return "\n".join(
        [
            "#### Recent GitHub Activity",
            "",
            "| Date | Repository | Event |",
            "| :--- | :--- | :--- |",
            *gh_lines,
            "",
            "#### Recent LeetCode Accepted",
            "",
            "| Date | Problem |",
            "| :--- | :--- |",
            *lc_lines,
        ]
    )


def update_readme(readme_path: Path, config: dict[str, Any], snapshot: dict[str, Any]) -> bool:
    """Update only auto-generated marker sections in README.md. Returns True if file changed."""
    original = readme_path.read_text(encoding="utf-8")
    updated = original
    updated = replace_marker_section(updated, "github-stats", render_github_stats_section(snapshot))
    updated = replace_marker_section(updated, "coding-stats", render_coding_stats_section(config, snapshot))
    updated = replace_marker_section(updated, "activity", render_activity_section(snapshot))

    if updated == original:
        return False

    readme_path.write_text(updated, encoding="utf-8")
    return True
