import socket
import subprocess
import sys
import time
from pathlib import Path

import pytest
import requests
from playwright.sync_api import sync_playwright

from utils.config import base_url, chromium_path, headless


ROOT = Path(__file__).resolve().parent
SCREENSHOT_DIR = ROOT / "reports" / "screenshots"


def _port_is_open(host: str, port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(0.2)
        return sock.connect_ex((host, port)) == 0

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call":
        item.test_result = report

@pytest.fixture(scope="session", autouse=True)
def demo_server():
    target = base_url()

    # Only start the bundled server when using the default local target.
    if target != "http://127.0.0.1:8000":
        yield
        return

    if _port_is_open("127.0.0.1", 8000):
        yield
        return

    process = subprocess.Popen(
        [
            sys.executable,
            "-m",
            "uvicorn",
            "demo_app.app:app",
            "--host",
            "127.0.0.1",
            "--port",
            "8000",
        ],
        cwd=ROOT,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    deadline = time.time() + 10
    while time.time() < deadline:
        try:
            response = requests.get(f"{target}/api/health", timeout=0.5)
            if response.status_code == 200:
                break
        except requests.RequestException:
            time.sleep(0.2)
    else:
        process.terminate()
        raise RuntimeError("Demo application failed to start")

    try:
        yield
    finally:
        process.terminate()
        process.wait(timeout=5)


@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=headless(), executable_path=chromium_path())
        yield browser
        browser.close()


@pytest.fixture
def page(browser, request):
    context = browser.new_context()
    page = context.new_page()

    yield page

    test_result = getattr(request.node, "test_result", None)

    if test_result and test_result.failed:
        SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)
        screenshot_path = SCREENSHOT_DIR / f"{request.node.name}.png"
        page.screenshot(path=screenshot_path, full_page=True)

    context.close()
