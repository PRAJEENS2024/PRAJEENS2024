"""HackerRank public badges REST fetcher."""

from __future__ import annotations

from typing import Any

from scripts.fetchers.http_client import request_with_retry


def fetch_hackerrank_stats(config: dict[str, Any]) -> dict[str, Any]:
    """Fetch HackerRank badge stars and solved counts from the public REST API."""
    username = config["platforms"]["hackerrank"]["username"]
    auto_cfg = config["automation"]
    timeout = int(auto_cfg.get("request_timeout_seconds", 15))
    max_retries = int(auto_cfg.get("max_retries", 3))

    url = f"https://www.hackerrank.com/rest/hackers/{username}/badges"
    resp = request_with_retry("GET", url, timeout=timeout, max_retries=max_retries)
    payload = resp.json()

    badges = [
        {
            "name": b.get("badge_name", ""),
            "stars": int(b.get("stars") or 0),
            "solved": int(b.get("solved") or 0),
        }
        for b in payload.get("models", [])
        if (b.get("solved") or 0) > 0 or (b.get("stars") or 0) > 0
    ]

    return {
        "username": username,
        "badges": badges,
        "profile_url": f"https://www.hackerrank.com/profile/{username}",
    }
