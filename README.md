
# Saucedemo E2E (Playwright + Pytest, Python 3.11)

End‑to‑end tests for `https://www.saucedemo.com/v1/` with Allure reports, parallel runs, Docker, and GitHub Actions.

---

## What’s covered by tests

- **[smoke] Login → Logout** — successful login with the standard user and logout via the menu (v1).
- **[smoke] Add to cart + header badge** — add 2 items, verify the header counter and cart contents.
- **[regression] Catalog sorting by price** — verify `Price (low → high)` and `Price (high → low)` comparing the UI order to `sorted(...)`.
- **[regression] Full checkout flow** — Cart → Checkout Step One (data generated with **Faker**) → Overview → Complete (“THANK YOU…”).
- **[regression] Locked user login error** — error message is shown for the locked user.
---

## Tech stack

- **Python 3.11**
- **Pytest** — test runner
- **Playwright (sync API)** — browser E2E (Chromium)
- **Allure** (`allure-pytest`) — results / HTML report
- **pytest-xdist** — parallelization (`-n auto`)
- **pytest-rerunfailures** — flaky retries
- **Faker** — first/last/zip data for checkout
- **python-dotenv** — configuration via `.env`
- **Docker / docker-compose** — containerized runs
- **GitHub Actions** — CI (smoke/regression matrix), artifacts, optional Allure deploy to Pages (demo workflow included)

---

## How to run

### 1) Docker / Docker Compose

Build & run everything:
```bash
docker compose up --build --exit-code-from e2e
```

**Smoke only**:

- **PowerShell**
  ```powershell
  $env:TEST_SUITE="smoke"
  docker compose up --build --exit-code-from e2e
  ```
- **CMD**
  ```cmd
  set TEST_SUITE=smoke && docker compose up --build --exit-code-from e2e
  ```
- **Bash**
  ```bash
  TEST_SUITE=smoke docker compose up --build --exit-code-from e2e
  ```

**Regression** (also includes smoke), headed + filter:
```bash
TEST_SUITE=regression PYTEST_ARGS="--headed -k backpack" docker compose up --build --exit-code-from e2e
```

Artifacts are mapped to the host:
- `./allure-results` — Allure results
- `./traces` — Playwright traces

---

### 2) GitHub Actions (CI/CD)

1. Repo → **Settings → Actions → General → Allow all actions**.  
2. (For public report) Repo → **Settings → Pages → Build and deployment → Source: GitHub Actions**.  
3. Workflow lives at `.github/workflows/ci.yml`. On push/PR, two jobs run: `smoke` and `regression`.

You’ll get:
- Artifacts: `allure-results-*`, `traces-*`, `allure-report-html`.
- (Optional) Allure HTML deployed to **GitHub Pages** — link shown in `Deploy Allure to GitHub Pages` job.

---

## Configuration

`tests/conftest.py` (important):
- CLI flags `--headed/--headless` override `.env`.
- Hook `pytest_collection_modifyitems`: every `@pytest.mark.smoke` is also marked as `regression` → running `-m regression` automatically includes smoke.

---


