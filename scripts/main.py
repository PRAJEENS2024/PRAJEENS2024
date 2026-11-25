"""Main CLI entry point for daily GitHub Profile README automation."""

from __future__ import annotations

import argparse
import logging
import os
import sys
from pathlib import Path
from typing import Any, Callable

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from scripts.config_loader import load_config
from scripts.fetchers.codechef_fetcher import fetch_codechef_stats
from scripts.fetchers.github_fetcher import fetch_github_stats
from scripts.fetchers.hackerrank_fetcher import fetch_hackerrank_stats
from scripts.fetchers.leetcode_fetcher import fetch_leetcode_stats
from scripts.fetchers.skillrack_fetcher import fetch_skillrack_stats
from scripts.generators.readme_generator import update_readme
from scripts.generators.svg_generator import write_all_svgs
from scripts.processors.stats_processor import (
    load_snapshot,
    normalize_snapshot,
    save_snapshot,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-7s | %(name)s | %(message)s",
)
logger = logging.getLogger("profile_updater")


def _safe_fetch(
    name: str,
    fetcher: Callable[[dict[str, Any]], dict[str, Any]],
    config: dict[str, Any],
) -> tuple[dict[str, Any] | None, str | None]:
    """Run a single platform fetcher safely so one outage never crashes the pipeline."""
    try:
        logger.info("Fetching %s metrics...", name)
        result = fetcher(config)
        logger.info("Fetched %s metrics successfully.", name)
        return result, None
    except Exception as exc:
        logger.error("Failed to fetch %s metrics: %s", name, exc)
        return None, str(exc)


def _write_step_summary(status: dict[str, str], errors: dict[str, str], changed: bool, readme_changed: bool) -> None:
    """Write an informative run summary to GitHub Actions step summary when available."""
    summary_path = os.getenv("GITHUB_STEP_SUMMARY")
    if not summary_path:
        return
    lines = [
        "### Profile README Automation Summary",
        "",
        f"- **Snapshot Changed:** `{changed}`",
        f"- **README Updated:** `{readme_changed}`",
        "",
        "| Platform | Status | Notes |",
        "| :--- | :--- | :--- |",
    ]
    for platform, st in status.items():
        note = errors.get(platform, "OK")
        lines.append(f"| `{platform}` | `{st}` | {note} |")
    with open(summary_path, "a", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")


def run_pipeline(config_path: str | None = None, dry_run: bool = False) -> int:
    """Execute data collection, normalization, SVG generation, and README update."""
    config = load_config(config_path)
    root = Path(config["runtime"]["root_dir"])
    auto_cfg = config["automation"]

    snapshot_path = root / auto_cfg["snapshot_path"]
    readme_path = root / auto_cfg["readme_path"]
    svg_dir = root / auto_cfg["svg_dir"]

    previous_snapshot = load_snapshot(snapshot_path)

    fetchers: dict[str, Callable[[dict[str, Any]], dict[str, Any]]] = {
        "github": fetch_github_stats,
        "leetcode": fetch_leetcode_stats,
        "codechef": fetch_codechef_stats,
        "skillrack": fetch_skillrack_stats,
        "hackerrank": fetch_hackerrank_stats,
    }

    raw_results: dict[str, dict[str, Any] | None] = {}
    errors: dict[str, str] = {}
    for name, fn in fetchers.items():
        data, err = _safe_fetch(name, fn, config)
        raw_results[name] = data
        if err:
            errors[name] = err

    if all(v is None for v in raw_results.values()) and previous_snapshot is None:
        logger.critical("All platform fetchers failed and no cached snapshot exists. Aborting.")
        return 1

    exclude_languages = set(config.get("platforms", {}).get("github", {}).get("exclude_languages", []))
    snapshot, status, data_changed = normalize_snapshot(
        raw_results, previous_snapshot, exclude_languages=exclude_languages
    )
    logger.info("Fetch status: %s | Data changed: %s", status, data_changed)

    if dry_run:
        logger.info("Dry-run enabled; skipping file writes.")
        return 0

    write_all_svgs(svg_dir, config, snapshot)
    readme_changed = update_readme(readme_path, config, snapshot)
    if data_changed or previous_snapshot is None:
        save_snapshot(snapshot_path, snapshot)

    _write_step_summary(status, errors, data_changed, readme_changed)
    logger.info("Completed successfully (readme_changed=%s).", readme_changed)
    return 0


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Update GitHub Profile README & SVGs.")
    parser.add_argument("--config", default=None, help="Optional path to profile.yml")
    parser.add_argument("--dry-run", action="store_true", help="Fetch and process without writing files")
    return parser.parse_args(argv)


if __name__ == "__main__":
    args = parse_args()
    raise SystemExit(run_pipeline(config_path=args.config, dry_run=args.dry_run))
