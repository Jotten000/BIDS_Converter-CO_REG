import os
import sys
import tempfile

def _open_log_stream():
    try:
        if getattr(sys, "frozen", False):
            base_dir = os.path.dirname(sys.executable)
        else:
            base_dir = os.getcwd()

        log_path = os.path.join(base_dir, "BIDS_and_coreg_runtime.log")
        return open(log_path, "a", buffering=1, encoding="utf-8")
    except Exception:
        log_path = os.path.join(tempfile.gettempdir(), "BIDS_and_coreg_runtime.log")
        return open(log_path, "a", buffering=1, encoding="utf-8")

if sys.stderr is None:
    sys.stderr = _open_log_stream()
    sys.__stderr__ = sys.stderr

if sys.stdout is None:
    sys.stdout = sys.stderr
    sys.__stdout__ = sys.stdout

if sys.stdin is None:
    sys.stdin = open(os.devnull, "r")
    sys.__stdin__ = sys.stdin

    if sys.stdin is None:
        sys.stdin = open(os.devnull, "r", encoding="utf-8")
        sys.__stdin__ = sys.stdin