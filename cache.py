"""Simple file-based caching utilities."""

import hashlib
import json
import pickle
import time
from pathlib import Path
from typing import Any, Callable


class FileCache:
    """Simple file-based cache with TTL support."""

    def __init__(self, cache_dir: str | Path = ".cache", default_ttl: int = 3600):
        """Initialize file cache.

        Args:
            cache_dir: Directory to store cache files
            default_ttl: Default time-to-live in seconds
        """
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.default_ttl = default_ttl

    def _get_path(self, key: str) -> Path:
        """Get cache file path for a key."""
        # Hash the key for safe filenames
        hashed = hashlib.sha256(key.encode()).hexdigest()[:16]
        return self.cache_dir / f"{hashed}.cache"

    def get(self, key: str) -> Any | None:
        """Get value from cache, or None if missing/expired."""
        path = self._get_path(key)
        if not path.exists():
            return None

        try:
            with open(path, "rb") as f:
                data = pickle.load(f)

            if data["expires_at"] and time.time() > data["expires_at"]:
                path.unlink()
                return None

            return data["value"]
        except Exception:
            return None

    def set(self, key: str, value: Any, ttl: int | None = None) -> None:
        """Store value in cache.

        Args:
            key: Cache key
            value: Value to store
            ttl: Time-to-live in seconds (None = use default)
        """
        if ttl is None:
            ttl = self.default_ttl

        path = self._get_path(key)
        data = {
            "value": value,
            "expires_at": time.time() + ttl if ttl > 0 else None,
            "created_at": time.time(),
        }

        with open(path, "wb") as f:
            pickle.dump(data, f)

    def delete(self, key: str) -> bool:
        """Delete a cache entry. Returns True if existed."""
        path = self._get_path(key)
        if path.exists():
            path.unlink()
            return True
        return False

    def clear(self) -> int:
        """Clear all cache entries. Returns count deleted."""
        count = 0
        for path in self.cache_dir.glob("*.cache"):
            path.unlink()
            count += 1
        return count

    def cleanup_expired(self) -> int:
        """Remove expired entries. Returns count deleted."""
        count = 0
        for path in self.cache_dir.glob("*.cache"):
            try:
                with open(path, "rb") as f:
                    data = pickle.load(f)
                if data["expires_at"] and time.time() > data["expires_at"]:
                    path.unlink()
                    count += 1
            except Exception:
                pass
        return count


def cached(
    cache: FileCache | None = None,
    ttl: int = 3600,
    key_func: Callable[..., str] | None = None,
) -> Callable:
    """Decorator for caching function results.

    Args:
        cache: FileCache instance (creates default if None)
        ttl: Time-to-live in seconds
        key_func: Function to generate cache key from args

    Returns:
        Decorated function
    """
    _cache = cache or FileCache()

    def decorator(func: Callable) -> Callable:
        def wrapper(*args, **kwargs) -> Any:
            # Generate cache key
            if key_func:
                key = key_func(*args, **kwargs)
            else:
                key = f"{func.__module__}.{func.__name__}:{args}:{kwargs}"

            # Try to get from cache
            result = _cache.get(key)
            if result is not None:
                return result

            # Compute and cache
            result = func(*args, **kwargs)
            _cache.set(key, result, ttl)
            return result

        return wrapper
    return decorator
