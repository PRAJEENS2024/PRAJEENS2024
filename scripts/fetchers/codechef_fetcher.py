"""CodeChef public profile parser."""

from __future__ import annotations

import re
from typing import Any

from bs4 import BeautifulSoup

from scripts.fetchers.http_client import request_with_retry


def fetch_codechef_stats(config: dict[str, Any]) -> dict[str, Any]:
    """Fetch public CodeChef rating, stars, contest count, and solved count."""
    username = config["platforms"]["codechef"]["username"]
    auto_cfg = config["automation"]
    timeout = int(auto_cfg.get("request_timeout_seconds", 15))
    max_retries = int(auto_cfg.get("max_retries", 3))

    url = f"https://www.codechef.com/users/{username}"
    resp = request_with_retry("GET", url, timeout=timeout, max_retries=max_retries)
    html = resp.text
    soup = BeautifulSoup(html, "html.parser")

    rating_el = soup.select_one(".rating-number")
    rating = int(re.sub(r"\D", "", rating_el.get_text())) if rating_el else None

    stars_el = soup.select_one(".rating-star")
    stars = len(stars_el.find_all("span")) if stars_el else None

    highest_match = re.search(r"Highest Rating\s*(\d+)", html)
    solved_match = re.search(r"Total Problems Solved:\s*(\d+)", html)
    contests_match = re.search(r"Contests\s*\((\d+)\)", html)

    if rating is None and not solved_match:
        raise RuntimeError("Could not parse CodeChef profile metrics from HTML")

    return {
        "username": username,
        "rating": rating,
        "highest_rating": int(highest_match.group(1)) if highest_match else None,
        "stars": stars,
        "total_solved": int(solved_match.group(1)) if solved_match else None,
        "contests": int(contests_match.group(1)) if contests_match else None,
        "profile_url": url,
    }
