"""Online barcode product lookup.

Primary source: Open Food Facts — free, no API key, huge open database.
Fallback: barcodeNest.com (only when BARCODENEST_API_KEY is configured).

All lookups happen server-side so any API key stays out of the browser.
Results are cached in memory (per worker) for a day to avoid hammering the
free providers.
"""
from __future__ import annotations

import time
from typing import Any

import httpx

from app.config import get_settings

_OFF_URL = "https://world.openfoodfacts.org/api/v2/product/{code}.json"
_BARCODENEST_URL = "https://api.barcodenest.com/v1/products/{code}"
_HEADERS = {"User-Agent": "TotalSell/0.3 (self-hosted POS; +https://github.com/GrayHatAli/TotalSell)"}
_TIMEOUT = 8.0

_CACHE_TTL = 24 * 60 * 60  # seconds
_cache: dict[str, tuple[float, dict[str, Any] | None]] = {}


def _clean_category(raw: str) -> str | None:
    """Turn OFF/barcodeNest category text into one readable label."""
    parts = [p.strip() for p in raw.split(",") if p.strip()]
    if not parts:
        return None
    # Drop language prefixes ("en:", "pt:", ...) and replace dashes for display.
    readable = [p.split(":", 1)[-1].replace("-", " ").strip() for p in parts]
    readable = [p for p in readable if p]
    return readable[0][:120] if readable else None


def _lookup_openfoodfacts(code: str) -> dict[str, Any] | None:
    try:
        resp = httpx.get(_OFF_URL.format(code=code), headers=_HEADERS, timeout=_TIMEOUT)
        if resp.status_code != 200:
            return None
        data = resp.json()
    except Exception:
        return None
    if data.get("status") != 1:
        return None
    p = data.get("product") or {}
    name = (p.get("product_name") or p.get("generic_name") or "").strip()
    if not name:
        return None
    return {
        "name": name[:255],
        "brand": (p.get("brands") or "").strip()[:120] or None,
        "image_url": (p.get("image_front_url") or p.get("image_url") or "").strip() or None,
        "quantity": (p.get("quantity") or "").strip()[:60] or None,
        "category": _clean_category(p.get("categories") or ""),
        "source": "openfoodfacts",
    }


def _lookup_barcodenest(code: str, api_key: str) -> dict[str, Any] | None:
    try:
        resp = httpx.get(
            _BARCODENEST_URL.format(code=code),
            headers={**_HEADERS, "X-API-Key": api_key},
            timeout=_TIMEOUT,
        )
        if resp.status_code != 200:
            return None
        data = resp.json()
    except Exception:
        return None
    if not (data.get("found") and data.get("product")):
        return None
    p = data["product"]
    name = (p.get("name") or "").strip()
    if not name:
        return None
    raw_categories = p.get("categories") or []
    if isinstance(raw_categories, list):
        raw_categories = ", ".join(str(c) for c in raw_categories)
    return {
        "name": name[:255],
        "brand": (p.get("brand") or "").strip()[:120] or None,
        "image_url": (p.get("image_url") or "").strip() or None,
        "quantity": (p.get("quantity") or "").strip()[:60] or None,
        "category": _clean_category(raw_categories),
        "source": "barcodenest",
    }


def lookup_barcode_online(code: str) -> dict[str, Any] | None:
    """Return normalized product info for a barcode, or None when not found."""
    if not code or not code.strip():
        return None
    code = code.strip()
    now = time.time()
    cached = _cache.get(code)
    if cached and cached[0] > now:
        return cached[1]

    result = _lookup_openfoodfacts(code)
    if result is None:
        settings = get_settings()
        if settings.barcodenest_api_key:
            result = _lookup_barcodenest(code, settings.barcodenest_api_key)

    _cache[code] = (now + _CACHE_TTL, result)
    return result