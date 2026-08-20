import os


def base_url() -> str:
    return os.getenv("QA_BASE_URL", "http://127.0.0.1:8000").rstrip("/")


def headless() -> bool:
    return os.getenv("QA_HEADLESS", "true").strip().lower() not in {"0", "false", "no"}


def chromium_path() -> str | None:
    return os.getenv("QA_CHROMIUM_PATH") or None
