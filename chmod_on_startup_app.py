import os
import stat
import sys
from pathlib import Path

def ensure_executable(path: Path) -> None:
    if not path.exists():
        return

    current_mode = path.stat().st_mode

    path.chmod(
        current_mode
        | stat.S_IXUSR
        | stat.S_IXGRP
        | stat.S_IXOTH
    )

def get_bundle_dir() -> Path:
    if getattr(sys, "frozen", False):
        return Path(sys._MEIPASS)
    return Path(__file__).parent

def run_mac_startupp():
    bundle_dir = get_bundle_dir()

    deno_path = bundle_dir / "deno"
    dcm2niix_path = bundle_dir / "dcm2niix"

    ensure_executable(deno_path)
    ensure_executable(dcm2niix_path)