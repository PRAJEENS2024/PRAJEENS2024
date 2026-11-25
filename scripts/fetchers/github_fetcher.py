"""GitHub statistics, contribution calendar, language share, and activity fetcher."""

from __future__ import annotations

import logging
import re
from datetime import datetime
from typing import Any

from bs4 import BeautifulSoup

from scripts.fetchers.http_client import request_with_retry

logger = logging.getLogger(__name__)

GITHUB_API_BASE = "https://api.github.com"
GITHUB_GRAPHQL_URL = "https://api.github.com/graphql"

GRAPHQL_QUERY = """
query($login: String!) {
  user(login: $login) {
    login
    name
    followers { totalCount }
    following { totalCount }
    repositories(
      first: 100
      ownerAffiliations: OWNER
      privacy: PUBLIC
      orderBy: {field: UPDATED_AT, direction: DESC}
    ) {
      totalCount
      nodes {
        name
        isFork
        stargazerCount
        forkCount
        pushedAt
        url
        description
        homepageUrl
        primaryLanguage { name color }
        languages(first: 10, orderBy: {field: SIZE, direction: DESC}) {
          edges {
            size
            node { name color }
          }
        }
      }
    }
    contributionsCollection {
      totalCommitContributions
      totalIssueContributions
      totalPullRequestContributions
      totalPullRequestReviewContributions
      restrictedContributionsCount
      contributionCalendar {
        totalContributions
        weeks {
          contributionDays {
            date
            contributionCount
            contributionLevel
          }
        }
      }
    }
  }
}
"""

LEVEL_MAP = {
    "NONE": 0,
    "FIRST_QUARTILE": 1,
    "SECOND_QUARTILE": 2,
    "THIRD_QUARTILE": 3,
    "FOURTH_QUARTILE": 4,
}


def _gh_headers(token: str) -> dict[str, str]:
    headers = {"Accept": "application/vnd.github+json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


def _fetch_via_graphql(
    username: str,
    token: str,
    exclude_forks: bool,
    exclude_language_repos: set[str],
    timeout: int,
    max_retries: int,
) -> dict[str, Any]:
    resp = request_with_retry(
        "POST",
        GITHUB_GRAPHQL_URL,
        headers=_gh_headers(token),
        json_payload={"query": GRAPHQL_QUERY, "variables": {"login": username}},
        timeout=timeout,
        max_retries=max_retries,
    )
    payload = resp.json()
    if payload.get("errors"):
        raise RuntimeError(f"GitHub GraphQL errors: {payload['errors']}")

    user = payload["data"]["user"]
    if not user:
        raise RuntimeError(f"GitHub user '{username}' not found via GraphQL")

    repos_all = user["repositories"]["nodes"]
    repos = [r for r in repos_all if not (exclude_forks and r["isFork"])]

    total_stars = sum(r["stargazerCount"] for r in repos)
    total_forks = sum(r["forkCount"] for r in repos)

    lang_totals: dict[str, int] = {}
    for repo in repos:
        if repo["name"] in exclude_language_repos:
            continue
        for edge in repo.get("languages", {}).get("edges", []):
            lang_name = edge["node"]["name"]
            lang_totals[lang_name] = lang_totals.get(lang_name, 0) + int(edge["size"])

    cc = user["contributionsCollection"]
    cal = cc["contributionCalendar"]
    days: list[dict[str, Any]] = []
    for week in cal["weeks"]:
        for day in week["contributionDays"]:
            days.append(
                {
                    "date": day["date"],
                    "count": int(day["contributionCount"]),
                    "level": LEVEL_MAP.get(day["contributionLevel"], 0),
                }
            )

    return {
        "source": "github_graphql",
        "username": username,
        "public_repos": len(repos),
        "total_stars": total_stars,
        "total_forks": total_forks,
        "followers": user["followers"]["totalCount"],
        "total_contributions": int(cal["totalContributions"]),
        "commits": int(cc["totalCommitContributions"]),
        "pull_requests": int(cc["totalPullRequestContributions"]),
        "issues": int(cc["totalIssueContributions"]),
        "reviews": int(cc["totalPullRequestReviewContributions"]),
        "languages_bytes": lang_totals,
        "calendar_days": days,
        "top_repos": [
            {
                "name": r["name"],
                "description": r["description"],
                "stars": r["stargazerCount"],
                "forks": r["forkCount"],
                "language": r["primaryLanguage"]["name"] if r["primaryLanguage"] else None,
                "pushed_at": r["pushedAt"],
                "url": r["url"],
                "homepage": r["homepageUrl"],
            }
            for r in repos[:6]
        ],
    }


def _parse_public_contributions(username: str, timeout: int, max_retries: int) -> tuple[int, list[dict[str, Any]]]:
    """Parse GitHub's public contributions calendar HTML as a tokenless fallback."""
    url = f"https://github.com/users/{username}/contributions"
    resp = request_with_retry("GET", url, timeout=timeout, max_retries=max_retries)
    soup = BeautifulSoup(resp.text, "html.parser")

    total_match = re.search(r"([\d,]+)\s+contributions?\s+in\s+the\s+last\s+year", resp.text)
    total_contributions = int(total_match.group(1).replace(",", "")) if total_match else 0

    tooltip_counts: dict[str, int] = {}
    for tip in soup.find_all("tool-tip"):
        for_id = tip.get("for")
        text = tip.get_text(strip=True)
        if not for_id:
            continue
        if text.startswith("No contributions"):
            tooltip_counts[for_id] = 0
        else:
            m = re.match(r"(\d+)\s+contribution", text)
            tooltip_counts[for_id] = int(m.group(1)) if m else 0

    days: list[dict[str, Any]] = []
    for td in soup.find_all("td", attrs={"data-date": True}):
        date_str = td.get("data-date")
        cell_id = td.get("id", "")
        level = int(td.get("data-level", "0") or 0)
        count = tooltip_counts.get(cell_id, level)
        days.append({"date": date_str, "count": count, "level": level})

    days.sort(key=lambda d: d["date"])
    if not total_contributions and days:
        total_contributions = sum(d["count"] for d in days)
    return total_contributions, days


def _fetch_via_rest(
    username: str,
    token: str,
    exclude_forks: bool,
    exclude_language_repos: set[str],
    timeout: int,
    max_retries: int,
) -> dict[str, Any]:
    headers = _gh_headers(token)
    user_resp = request_with_retry(
        "GET",
        f"{GITHUB_API_BASE}/users/{username}",
        headers=headers,
        timeout=timeout,
        max_retries=max_retries,
    ).json()

    repos_resp = request_with_retry(
        "GET",
        f"{GITHUB_API_BASE}/users/{username}/repos?per_page=100&sort=pushed",
        headers=headers,
        timeout=timeout,
        max_retries=max_retries,
    ).json()

    repos = [r for r in repos_resp if not (exclude_forks and r.get("fork"))]
    total_stars = sum(int(r.get("stargazers_count", 0)) for r in repos)
    total_forks = sum(int(r.get("forks_count", 0)) for r in repos)

    lang_totals: dict[str, int] = {}
    for repo in repos:
        if repo["name"] in exclude_language_repos:
            continue
        try:
            langs = request_with_retry(
                "GET",
                repo["languages_url"],
                headers=headers,
                timeout=timeout,
                max_retries=2,
            ).json()
            for k, v in langs.items():
                lang_totals[k] = lang_totals.get(k, 0) + int(v)
        except Exception as exc:
            logger.debug("Skipping languages for %s: %s", repo["name"], exc)

    total_contributions, days = _parse_public_contributions(username, timeout, max_retries)
    return {
        "source": "github_rest_public",
        "username": username,
        "public_repos": len(repos),
        "total_stars": total_stars,
        "total_forks": total_forks,
        "followers": int(user_resp.get("followers", 0)),
        "total_contributions": total_contributions,
        "commits": None,
        "pull_requests": None,
        "issues": None,
        "reviews": None,
        "languages_bytes": lang_totals,
        "calendar_days": days,
        "top_repos": [
            {
                "name": r["name"],
                "description": r.get("description"),
                "stars": int(r.get("stargazers_count", 0)),
                "forks": int(r.get("forks_count", 0)),
                "language": r.get("language"),
                "pushed_at": r.get("pushed_at"),
                "url": r.get("html_url"),
                "homepage": r.get("homepage"),
            }
            for r in repos[:6]
        ],
    }


def _fetch_recent_events(
    username: str, token: str, timeout: int, max_retries: int
) -> list[dict[str, str]]:
    """Fetch recent public GitHub events for the activity feed."""
    headers = _gh_headers(token)
    events = request_with_retry(
        "GET",
        f"{GITHUB_API_BASE}/users/{username}/events/public?per_page=20",
        headers=headers,
        timeout=timeout,
        max_retries=max_retries,
    ).json()

    summaries: list[dict[str, str]] = []
    seen_keys: set[tuple[str, str, str]] = set()
    for ev in events:
        ev_type = ev.get("type", "")
        repo_name = ev.get("repo", {}).get("name", "")
        created_raw = ev.get("created_at", "")
        date_label = created_raw[:10] if created_raw else ""
        try:
            dt = datetime.fromisoformat(created_raw.replace("Z", "+00:00"))
            date_label = dt.strftime("%Y-%m-%d")
        except ValueError:
            pass

        action_label = ""
        payload = ev.get("payload", {})
        if ev_type == "PushEvent":
            commits = payload.get("size") or len(payload.get("commits", []))
            action_label = f"Pushed {commits} commit(s)" if commits else "Pushed updates"
        elif ev_type == "CreateEvent":
            ref_type = payload.get("ref_type", "resource")
            action_label = f"Created {ref_type}"
        elif ev_type == "PullRequestEvent":
            action = payload.get("action", "updated")
            action_label = f"Pull request {action}"
        elif ev_type == "IssuesEvent":
            action = payload.get("action", "updated")
            action_label = f"Issue {action}"
        elif ev_type == "ReleaseEvent":
            action_label = "Published release"
        else:
            continue

        key = (date_label, repo_name, action_label)
        if key in seen_keys:
            continue
        seen_keys.add(key)
        summaries.append(
            {
                "date": date_label,
                "repo": repo_name,
                "action": action_label,
                "url": f"https://github.com/{repo_name}",
            }
        )
        if len(summaries) >= 6:
            break

    return summaries


def fetch_github_stats(config: dict[str, Any]) -> dict[str, Any]:
    """Fetch GitHub metrics using GraphQL when tokenized, falling back to REST + HTML."""
    gh_cfg = config["platforms"]["github"]
    auto_cfg = config["automation"]
    username = gh_cfg["username"]
    exclude_forks = bool(gh_cfg.get("exclude_forks", True))
    exclude_lang_repos = set(gh_cfg.get("exclude_language_repos", []))
    token = config.get("runtime", {}).get("github_token", "")
    timeout = int(auto_cfg.get("request_timeout_seconds", 15))
    max_retries = int(auto_cfg.get("max_retries", 3))

    data: dict[str, Any]
    recent_events: list[dict[str, str]] | None = None
    try:
        recent_events = _fetch_recent_events(username, token, timeout, max_retries)
    except Exception as exc:
        logger.warning("Failed to fetch recent GitHub events: %s", exc)

    if token:
        try:
            data = _fetch_via_graphql(
                username, token, exclude_forks, exclude_lang_repos, timeout, max_retries
            )
        except Exception as exc:
            logger.warning("GitHub GraphQL failed (%s); falling back to REST API", exc)
            data = _fetch_via_rest(
                username, token, exclude_forks, exclude_lang_repos, timeout, max_retries
            )
    else:
        data = _fetch_via_rest(
            username, token, exclude_forks, exclude_lang_repos, timeout, max_retries
        )

    data["recent_events"] = recent_events
    return data
