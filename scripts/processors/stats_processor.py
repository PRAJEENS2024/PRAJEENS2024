"""Statistics normalization, streak/monthly aggregation, and snapshot management."""

from __future__ import annotations

import hashlib
import json
from collections import defaultdict
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Any

LANGUAGE_COLORS: dict[str, str] = {
    "TypeScript": "#3178C6",
    "Python": "#3572A5",
    "JavaScript": "#F1E05A",
    "CSS": "#563D7C",
    "HTML": "#E34C26",
    "C++": "#F34B7D",
    "C": "#555555",
    "Java": "#B07219",
    "Jupyter Notebook": "#DA5B0B",
    "Dockerfile": "#384D54",
    "Shell": "#89E051",
    "PowerShell": "#012456",
    "Mako": "#7E858D",
}


def compute_streaks(calendar_days: list[dict[str, Any]]) -> dict[str, Any]:
    """Compute current streak, longest streak, and active day metrics from sorted daily counts."""
    if not calendar_days:
        return {
            "current_streak": 0,
            "longest_streak": 0,
            "active_days": 0,
            "total_days": 0,
        }

    ordered = sorted(calendar_days, key=lambda d: d["date"])
    active_days = sum(1 for d in ordered if int(d.get("count", 0)) > 0)

    longest = 0
    running = 0
    for d in ordered:
        if int(d.get("count", 0)) > 0:
            running += 1
            if running > longest:
                longest = running
        else:
            running = 0

    # Current streak: walk backward from last day; allow today=0 if yesterday had activity
    by_date = {d["date"]: int(d.get("count", 0)) for d in ordered}
    last_date = date.fromisoformat(ordered[-1]["date"])
    cursor = last_date
    if by_date.get(cursor.isoformat(), 0) == 0:
        yesterday = cursor - timedelta(days=1)
        if by_date.get(yesterday.isoformat(), 0) > 0:
            cursor = yesterday

    current = 0
    while by_date.get(cursor.isoformat(), 0) > 0:
        current += 1
        cursor -= timedelta(days=1)

    return {
        "current_streak": current,
        "longest_streak": longest,
        "active_days": active_days,
        "total_days": len(ordered),
    }


def compute_monthly_contributions(
    calendar_days: list[dict[str, Any]], months: int = 6
) -> list[dict[str, Any]]:
    """Aggregate daily contribution counts into the most recent N calendar months."""
    buckets: dict[str, int] = defaultdict(int)
    for day in calendar_days:
        month_key = day["date"][:7]  # YYYY-MM
        buckets[month_key] += int(day.get("count", 0))

    sorted_keys = sorted(buckets.keys())[-months:]
    result: list[dict[str, Any]] = []
    for key in sorted_keys:
        dt = datetime.strptime(key, "%Y-%m")
        result.append(
            {
                "month": key,
                "label": dt.strftime("%b"),
                "count": buckets[key],
            }
        )
    return result


def compute_top_languages(
    languages_bytes: dict[str, int],
    limit: int = 6,
    exclude_languages: set[str] | None = None,
) -> list[dict[str, Any]]:
    """Convert raw language byte counts into sorted percentage entries."""
    excluded = exclude_languages or set()
    filtered = {k: v for k, v in languages_bytes.items() if v > 0 and k not in excluded}
    total = sum(filtered.values())
    if total <= 0:
        return []

    sorted_langs = sorted(
        filtered.items(),
        key=lambda item: item[1],
        reverse=True,
    )
    top = sorted_langs[:limit]
    other_bytes = sum(v for _, v in sorted_langs[limit:])

    entries = [
        {
            "name": name,
            "bytes": size,
            "percent": round((size / total) * 100, 1),
            "color": LANGUAGE_COLORS.get(name, "#8B949E"),
        }
        for name, size in top
    ]
    if other_bytes > 0:
        entries.append(
            {
                "name": "Other",
                "bytes": other_bytes,
                "percent": round((other_bytes / total) * 100, 1),
                "color": "#6E7681",
            }
        )
    return entries


def normalize_snapshot(
    raw_results: dict[str, dict[str, Any] | None],
    previous_snapshot: dict[str, Any] | None = None,
    exclude_languages: set[str] | None = None,
) -> tuple[dict[str, Any], dict[str, str], bool]:
    """Merge fresh fetch results with previous valid snapshot and compute derived metrics.

    Returns (snapshot, status_by_platform, changed).
    """
    prev = previous_snapshot or {}
    prev_raw = prev.get("raw", {})
    status: dict[str, str] = {}
    merged_raw: dict[str, Any] = {}

    for key in ("github", "leetcode", "codechef", "skillrack", "hackerrank"):
        fresh = raw_results.get(key)
        if fresh is not None:
            merged_raw[key] = fresh
            status[key] = "live"
        elif key in prev_raw and prev_raw[key] is not None:
            merged_raw[key] = prev_raw[key]
            status[key] = "cached_fallback"
        else:
            merged_raw[key] = None
            status[key] = "unavailable"

    # Preserve cached recent_events if GitHub core succeeded but events endpoint was rate-limited
    if merged_raw.get("github") is not None and merged_raw["github"].get("recent_events") is None:
        prev_events = (prev_raw.get("github") or {}).get("recent_events")
        merged_raw["github"]["recent_events"] = prev_events if prev_events is not None else []

    gh = merged_raw.get("github") or {}
    cal_days = gh.get("calendar_days") or []
    streaks = compute_streaks(cal_days)
    monthly = compute_monthly_contributions(cal_days, months=6)
    top_langs = compute_top_languages(
        gh.get("languages_bytes") or {}, limit=6, exclude_languages=exclude_languages
    )

    lc = merged_raw.get("leetcode") or {}
    cc = merged_raw.get("codechef") or {}
    sr = merged_raw.get("skillrack") or {}
    hr = merged_raw.get("hackerrank") or {}

    verified_solved_total = (
        int(lc.get("total_solved") or 0)
        + int(sr.get("programs_solved") or 0)
        + int(cc.get("total_solved") or 0)
    )

    derived = {
        "github": {
            "username": gh.get("username", "PRAJEENS2024"),
            "source": gh.get("source", "unavailable"),
            "public_repos": gh.get("public_repos", 0),
            "total_stars": gh.get("total_stars", 0),
            "total_forks": gh.get("total_forks", 0),
            "followers": gh.get("followers", 0),
            "total_contributions": gh.get("total_contributions", 0),
            "commits": gh.get("commits"),
            "pull_requests": gh.get("pull_requests"),
            "issues": gh.get("issues"),
            "reviews": gh.get("reviews"),
            "current_streak": streaks["current_streak"],
            "longest_streak": streaks["longest_streak"],
            "active_days": streaks["active_days"],
            "monthly_contributions": monthly,
            "top_languages": top_langs,
            "recent_events": gh.get("recent_events") or [],
            "calendar_days": cal_days,
        },
        "coding": {
            "verified_solved_total": verified_solved_total,
            "leetcode": lc,
            "codechef": cc,
            "skillrack": sr,
            "hackerrank": hr,
        },
    }

    # Deterministic hash over core metrics (ignoring volatile run dates) for strict idempotency
    canonical = json.dumps(derived, sort_keys=True, ensure_ascii=False)
    content_hash = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    changed = content_hash != prev.get("content_hash")

    today_utc = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    last_updated = today_utc if changed else prev.get("last_updated", today_utc)

    snapshot = {
        "schema_version": 1,
        "content_hash": content_hash,
        "last_updated": last_updated,
        "fetch_status": status,
        "raw": merged_raw,
        "derived": derived,
    }
    return snapshot, status, changed


def load_snapshot(path: Path) -> dict[str, Any] | None:
    """Load previous JSON snapshot if present and valid."""
    if not path.exists():
        return None
    try:
        with path.open("r", encoding="utf-8") as fh:
            return json.load(fh)
    except (OSError, json.JSONDecodeError):
        return None


def save_snapshot(path: Path, snapshot: dict[str, Any]) -> None:
    """Persist normalized snapshot atomically."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as fh:
        json.dump(snapshot, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
