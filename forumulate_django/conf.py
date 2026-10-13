"""Settings: ``FORUMULATE = {"ORG": "...", "SPACE": "..."}`` in settings.py.

Read on every call rather than once at import, so ``override_settings`` in a
test (or a settings change in a long-lived shell) is honoured.
"""
import hashlib
from typing import Any, Dict

from django.conf import settings
from django.core.cache import caches

from .core import ContentClient, resolve


def config() -> Dict[str, Any]:
    return resolve(getattr(settings, "FORUMULATE", {}))


def _safe_key(key: str) -> str:
    # memcached refuses keys over 250 chars or with spaces; a URL can be both.
    return "forumulate:" + hashlib.sha256(key.encode("utf-8")).hexdigest()


def client() -> ContentClient:
    cfg = config()
    cache = caches[cfg.get("CACHE_ALIAS") or "default"]
    return ContentClient(
        cfg,
        cache_get=lambda key: cache.get(_safe_key(key)),
        cache_set=lambda key, value, ttl: cache.set(_safe_key(key), value, ttl),
    )
