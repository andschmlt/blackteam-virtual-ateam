"""
Shared environment loader for Paradise Media scripts.

Reads variables from ~/.keys/.env and respects os.environ precedence
so that Cloud Run (or any runtime injecting secrets as env vars) wins
over the local file.
"""

import os


def load_env(env_file=None, precedence_keys=None):
    """Load config from ~/.keys/.env with os.environ taking precedence.

    Parameters
    ----------
    env_file : str | None
        Path to the env file. Defaults to ``~/.keys/.env``.
    precedence_keys : list[str] | None
        Explicit list of env-var names where ``os.environ`` should override
        the file value.  When *None* (the default) **every** key found in
        ``os.environ`` takes precedence — which is the safest behaviour for
        Cloud Run where secrets are injected as env vars.

    Returns
    -------
    dict
        Merged key/value map (file values + env-var overrides).
    """
    if env_file is None:
        env_file = os.path.expanduser("~/.keys/.env")

    env_vars = {}

    # 1. Read the file (if it exists)
    if os.path.exists(env_file):
        with open(env_file) as f:
            for line in f:
                line = line.strip()
                if line and "=" in line and not line.startswith("#"):
                    key, value = line.split("=", 1)
                    env_vars[key] = value

    # 2. Cloud Run / runtime env vars take precedence
    if precedence_keys is not None:
        for key in precedence_keys:
            if key in os.environ:
                env_vars[key] = os.environ[key]
    else:
        # Default: every key loaded from the file can be overridden
        for key in list(env_vars.keys()):
            if key in os.environ:
                env_vars[key] = os.environ[key]

    return env_vars
