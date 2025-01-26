"""Load configuration from JSON, YAML, or environment variables."""

import json
import os
from pathlib import Path
from typing import Any

import yaml


def load_json(path: str | Path) -> dict:
    """Load config from JSON file."""
    with open(path) as f:
        return json.load(f)


def load_yaml(path: str | Path) -> dict:
    """Load config from YAML file."""
    with open(path) as f:
        return yaml.safe_load(f)


def load_env(prefix: str = "", strip_prefix: bool = True) -> dict:
    """Load config from environment variables.

    Args:
        prefix: Only include vars starting with this prefix
        strip_prefix: Remove the prefix from keys in result

    Returns:
        Dict of environment variables
    """
    result = {}
    for key, value in os.environ.items():
        if prefix and not key.startswith(prefix):
            continue
        new_key = key[len(prefix):] if strip_prefix and prefix else key
        result[new_key.lower()] = value
    return result


def load_config(path: str | Path | None = None, env_prefix: str = "") -> dict:
    """Load config from file and/or environment.

    Environment variables override file values.

    Args:
        path: Path to JSON or YAML file
        env_prefix: Prefix for environment variables

    Returns:
        Merged configuration dict
    """
    config = {}

    if path:
        path = Path(path)
        if path.suffix == ".json":
            config = load_json(path)
        elif path.suffix in (".yaml", ".yml"):
            config = load_yaml(path)
        else:
            raise ValueError(f"Unsupported config format: {path.suffix}")

    # Env vars override file config
    env_config = load_env(env_prefix)
    config.update(env_config)

    return config


def get_required(config: dict, key: str) -> Any:
    """Get a required config value, raising if missing."""
    if key not in config:
        raise KeyError(f"Missing required config key: {key}")
    return config[key]


def get_optional(config: dict, key: str, default: Any = None) -> Any:
    """Get an optional config value with a default."""
    return config.get(key, default)
