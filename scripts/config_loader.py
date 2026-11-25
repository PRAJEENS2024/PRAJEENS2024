"""Configuration loader for profile automation."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import yaml

ROOT_DIR = Path(__file__).resolve().parent.parent
DEFAULT_CONFIG_PATH = ROOT_DIR / "config" / "profile.yml"


def load_config(config_path: Path | str | None = None) -> dict[str, Any]:
    """Load YAML configuration and merge runtime environment settings."""
    path = Path(config_path) if config_path else DEFAULT_CONFIG_PATH
    with path.open("r", encoding="utf-8") as fh:
        config: dict[str, Any] = yaml.safe_load(fh) or {}

    config.setdefault("runtime", {})
    config["runtime"]["root_dir"] = str(ROOT_DIR)
    config["runtime"]["github_token"] = (
        os.getenv("GH_STATS_TOKEN")
        or os.getenv("GITHUB_TOKEN")
        or ""
    ).strip()
    return config
