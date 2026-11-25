"""Shared resilient HTTP client with retry and rate-limit handling."""

from __future__ import annotations

import logging
import time
from typing import Any

import requests

logger = logging.getLogger(__name__)

DEFAULT_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
)


def request_with_retry(
    method: str,
    url: str,
    *,
    headers: dict[str, str] | None = None,
    json_payload: dict[str, Any] | None = None,
    timeout: int = 15,
    max_retries: int = 3,
) -> requests.Response:
    """Execute an HTTP request with exponential backoff and rate-limit awareness."""
    merged_headers = {"User-Agent": DEFAULT_USER_AGENT}
    if headers:
        merged_headers.update(headers)

    last_exc: Exception | None = None
    for attempt in range(1, max_retries + 1):
        try:
            response = requests.request(
                method=method.upper(),
                url=url,
                headers=merged_headers,
                json=json_payload,
                timeout=timeout,
            )
            if response.status_code in (429, 502, 503, 504):
                retry_after = response.headers.get("Retry-After")
                wait_seconds = (
                    min(int(retry_after), 30)
                    if retry_after and retry_after.isdigit()
                    else min(2**attempt, 16)
                )
                logger.warning(
                    "Transient HTTP %s from %s (attempt %d/%d); retrying in %ss",
                    response.status_code,
                    url,
                    attempt,
                    max_retries,
                    wait_seconds,
                )
                time.sleep(wait_seconds)
                continue

            if response.status_code == 403 and response.headers.get("X-RateLimit-Remaining") == "0":
                raise RuntimeError(f"API rate limit exhausted for {url}")

            response.raise_for_status()
            return response
        except requests.RequestException as exc:
            last_exc = exc
            if attempt < max_retries:
                wait_seconds = min(2**attempt, 12)
                logger.warning(
                    "Request error for %s (attempt %d/%d): %s; retrying in %ss",
                    url,
                    attempt,
                    max_retries,
                    exc,
                    wait_seconds,
                )
                time.sleep(wait_seconds)
            else:
                raise RuntimeError(f"Failed to fetch {url} after {max_retries} attempts: {exc}") from exc

    raise RuntimeError(f"Failed to fetch {url}: {last_exc}")
