from __future__ import annotations

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("ai-baton-tool")
except PackageNotFoundError:
    # Running from a source checkout that was never `pip install`-ed.
    __version__ = "0.0.0+unknown"
