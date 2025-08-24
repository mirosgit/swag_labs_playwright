import os
import uuid
import pathlib
import allure
import pytest
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

load_dotenv(override=True)

def env_bool(name: str, default: bool = True) -> bool:
    val = os.getenv(name)
    if val is None:
        return default
    return val.strip().lower() in ("1", "true", "yes", "on")

BASE_URL: str = os.getenv("BASE_URL", "https://www.saucedemo.com/v1")
HEADLESS_DEFAULT: bool = env_bool("HEADLESS", True)

def pytest_addoption(parser):
    parser.addoption(
        "--headed",
        action="store_true",
        default=False,
        help="Run browser in headed mode (overrides HEADLESS env)",
    )
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Run browser in headless mode (overrides HEADLESS env)",
    )

@pytest.fixture(scope="session")
def base_url():
    return BASE_URL

@pytest.fixture(scope="session")
def playwright_context(pytestconfig):
    headed_flag = pytestconfig.getoption("--headed")
    headless_flag = pytestconfig.getoption("--headless")

    if headed_flag:
        headless = False
    elif headless_flag:
        headless = True
    else:
        headless = HEADLESS_DEFAULT

    # print(f"[DEBUG] Running with headless={headless}")

    with sync_playwright() as pw:
        browser = pw.chromium.launch(
            headless=headless, args=["--disable-dev-shm-usage"]
        )
        context = browser.new_context(
            viewport={"width": 1366, "height": 768},
            timezone_id="UTC",
            locale="en-US",
        )
        yield context
        context.close()
        browser.close()

@pytest.fixture(scope="function")
def page(playwright_context):
    page = playwright_context.new_page()

    console_buffer = []
    setattr(page, "_console_buffer", console_buffer)

    def _on_console(msg):
        try:
            console_buffer.append(f"{msg.type.upper()}: {msg.text}")
        except Exception:
            pass

    page.on("console", _on_console)

    traces_dir = pathlib.Path("traces")
    traces_dir.mkdir(parents=True, exist_ok=True)
    trace_name = f"trace-{uuid.uuid4().hex}.zip"
    trace_path = str(traces_dir / trace_name)
    page.context.tracing.start(screenshots=True, snapshots=True, sources=True)

    setattr(page, "_trace_path", trace_path)

    yield page

    try:
        page.context.tracing.stop(path=page._trace_path)
    except Exception:
        pass

    page.close()

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call" and rep.failed:
        page = item.funcargs.get("page", None)
        if not page:
            return

        try:
            png = page.screenshot(full_page=False)
            allure.attach(png, name="screenshot", attachment_type=allure.attachment_type.PNG)
        except Exception:
            pass

        try:
            html = page.content()
            allure.attach(html, name="page.html", attachment_type=allure.attachment_type.HTML)
        except Exception:
            pass

        try:
            logs = "\n".join(getattr(page, "_console_buffer", []))
            if logs:
                allure.attach(logs, name="console.log", attachment_type=allure.attachment_type.TEXT)
        except Exception:
            pass

        try:
            trace_path = getattr(page, "_trace_path", None)
            if trace_path and os.path.exists(trace_path):
                with open(trace_path, "rb") as f:
                    allure.attach(
                        f.read(),
                        name=os.path.basename(trace_path),
                        attachment_type=allure.attachment_type.ZIP,
                    )
        except Exception:
            pass
