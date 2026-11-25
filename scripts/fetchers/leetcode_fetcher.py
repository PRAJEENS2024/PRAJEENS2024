"""LeetCode GraphQL statistics fetcher."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from scripts.fetchers.http_client import request_with_retry

LEETCODE_GRAPHQL_URL = "https://leetcode.com/graphql"

LEETCODE_QUERY = """
query getUserProfile($username: String!) {
  matchedUser(username: $username) {
    username
    profile {
      ranking
      reputation
    }
    submitStatsGlobal {
      acSubmissionNum {
        difficulty
        count
        submissions
      }
    }
    userCalendar {
      streak
      totalActiveDays
    }
  }
  userContestRanking(username: $username) {
    attendedContestsCount
    rating
    globalRanking
    topPercentage
  }
  recentAcSubmissionList(username: $username, limit: 5) {
    title
    titleSlug
    timestamp
  }
}
"""


def fetch_leetcode_stats(config: dict[str, Any]) -> dict[str, Any]:
    """Fetch live LeetCode problem solving, contest rating, streak, and recent submissions."""
    username = config["platforms"]["leetcode"]["username"]
    auto_cfg = config["automation"]
    timeout = int(auto_cfg.get("request_timeout_seconds", 15))
    max_retries = int(auto_cfg.get("max_retries", 3))

    resp = request_with_retry(
        "POST",
        LEETCODE_GRAPHQL_URL,
        headers={
            "Content-Type": "application/json",
            "Referer": f"https://leetcode.com/u/{username}/",
        },
        json_payload={"query": LEETCODE_QUERY, "variables": {"username": username}},
        timeout=timeout,
        max_retries=max_retries,
    )
    payload = resp.json()
    if payload.get("errors"):
        raise RuntimeError(f"LeetCode GraphQL errors: {payload['errors']}")

    data = payload.get("data", {})
    matched = data.get("matchedUser")
    if not matched:
        raise RuntimeError(f"LeetCode user '{username}' not found")

    counts: dict[str, int] = {}
    for row in matched.get("submitStatsGlobal", {}).get("acSubmissionNum", []):
        counts[row["difficulty"]] = int(row["count"])

    contest = data.get("userContestRanking") or {}
    cal = matched.get("userCalendar") or {}
    profile = matched.get("profile") or {}

    recent_ac: list[dict[str, str]] = []
    for item in data.get("recentAcSubmissionList") or []:
        ts = item.get("timestamp")
        date_str = ""
        if ts and str(ts).isdigit():
            date_str = datetime.fromtimestamp(int(ts), tz=timezone.utc).strftime("%Y-%m-%d")
        recent_ac.append(
            {
                "title": item.get("title", ""),
                "slug": item.get("titleSlug", ""),
                "url": f"https://leetcode.com/problems/{item.get('titleSlug', '')}/",
                "date": date_str,
            }
        )

    return {
        "username": username,
        "total_solved": counts.get("All", 0),
        "easy": counts.get("Easy", 0),
        "medium": counts.get("Medium", 0),
        "hard": counts.get("Hard", 0),
        "profile_ranking": int(profile.get("ranking") or 0),
        "streak": int(cal.get("streak") or 0),
        "total_active_days": int(cal.get("totalActiveDays") or 0),
        "contests_attended": int(contest.get("attendedContestsCount") or 0),
        "contest_rating": round(float(contest["rating"])) if contest.get("rating") is not None else None,
        "contest_global_ranking": int(contest["globalRanking"]) if contest.get("globalRanking") is not None else None,
        "top_percentage": round(float(contest["topPercentage"]), 2) if contest.get("topPercentage") is not None else None,
        "recent_submissions": recent_ac,
    }
