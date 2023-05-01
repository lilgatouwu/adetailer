from __future__ import annotations

import importlib.util
import subprocess
import sys
from importlib.metadata import version  # python >= 3.8

from packaging.version import parse


def is_installed(
    package: str, min_version: str | None = None, max_version: str | None = None
):
    try:
        spec = importlib.util.find_spec(package)
    except ModuleNotFoundError:
        return False

    if spec is None:
        return False

    if not min_version and not max_version:
        return True

    pkg_version = version(package)
    if not min_version:
        min_version = "0.0.0"
    if not max_version:
        max_version = "99999999.99999999.99999999"

    try:
        return parse(min_version) <= parse(pkg_version) <= parse(max_version)
    except Exception:
        return False


def run_pip(*args):
    subprocess.run([sys.executable, "-m", "pip", "install", *args])


def install():
    deps = [
        # requirements
        ("ultralytics", "8.0.87", None),
        ("mediapipe", "0.9.3.0", None),
        ("huggingface_hub", None, None),
        # mediapipe
        ("protobuf", "3.20.0", "3.20.9999"),
    ]

    for name, low, high in deps:
        if not is_installed(name, low, high):
            if low and high:
                cmd = f"{name}>={low},<={high}"
            elif low:
                cmd = f"{name}>={low}"
            elif high:
                cmd = f"{name}<={high}"
            else:
                cmd = name

            run_pip("-U", cmd)


try:
    from launch import skip_install
except ImportError:
    skip_install = False

if not skip_install:
    install()
