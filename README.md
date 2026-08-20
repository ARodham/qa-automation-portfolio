# QA Automation Portfolio

[![QA Automation](https://github.com/ARodham/qa-automation-portfolio/actions/workflows/tests.yml/badge.svg)](https://github.com/ARodham/qa-automation-portfolio/actions/workflows/tests.yml)

A small, self-contained quality engineering project demonstrating how I approach **UI automation, REST API validation, regression design, CI/CD, maintainable test code, and release confidence**.

> **Portfolio note:** My professional automation work is contained within employer-owned repositories and cannot be shared publicly. This repository was created independently as a demonstration project and contains no employer code, test data, endpoints, credentials, architecture, or other proprietary information.

## What this project demonstrates

- Playwright browser automation with Python
- Page Object Model for maintainable UI tests
- REST API validation with reusable client helpers
- Positive, negative, smoke, and regression scenarios
- Clear separation between test intent and implementation details
- Environment-driven configuration
- Deterministic local test application to avoid third-party test instability
- Parallel-ready pytest execution
- HTML test reporting
- GitHub Actions CI
- Risk-based test selection and a documented test strategy

The aim is not to maximise test count. It is to show how a small regression pack can provide useful release confidence while remaining understandable and maintainable.

## Example quality problem

A manual regression pass might include:

1. Verify the application is available.
2. Confirm a valid user can sign in.
3. Confirm invalid credentials are rejected.
4. Verify inventory data is displayed correctly.
5. Verify search/filter behaviour.
6. Validate the corresponding API responses.
7. Check invalid API requests fail safely.

This project automates those repeatable checks so manual QA time can be focused on exploratory testing, usability, risk analysis, and new behaviour.

## Tech stack

- Python 3.11+
- Playwright
- pytest
- FastAPI
- requests
- pytest-xdist
- pytest-html
- GitHub Actions

## Project structure

```text
qa-automation-portfolio/
├── .github/workflows/tests.yml
├── demo_app/
│   └── app.py
├── pages/
│   ├── inventory_page.py
│   └── login_page.py
├── tests/
│   ├── api/
│   │   └── test_items_api.py
│   └── ui/
│       ├── test_inventory.py
│       └── test_login.py
├── utils/
│   ├── api_client.py
│   └── config.py
├── conftest.py
├── pytest.ini
├── requirements.txt
├── TEST_STRATEGY.md
└── ARCHITECTURE.md
```

## Run locally

### 1. Create a virtual environment

Windows:

```powershell
python -m venv .venv
.venv\Scripts\activate
```

macOS/Linux:

```bash
python -m venv .venv
source .venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
python -m playwright install chromium
```

### 3. Run the full suite

```bash
pytest
```

### 4. Run only smoke tests

```bash
pytest -m smoke
```

### 5. Run in parallel

```bash
pytest -n auto
```

### 6. Generate an HTML report

```bash
pytest --html=reports/report.html --self-contained-html
```

## Configuration

The default test target is the bundled local demo application:

```text
http://127.0.0.1:8000
```

Override it with:

```bash
QA_BASE_URL=http://127.0.0.1:8000 pytest
```

Browser headless mode can be controlled with:

```bash
QA_HEADLESS=false pytest
```


If your environment already provides Chromium in a custom location, you can optionally set:

```bash
QA_CHROMIUM_PATH=/path/to/chromium pytest
```

## CI

The GitHub Actions workflow:

1. checks out the repository;
2. installs Python dependencies;
3. installs Chromium;
4. executes the automated suite;
5. generates an HTML report;
6. uploads the report as a build artifact.

This creates a repeatable release-safety signal on every push and pull request.

## Test credentials

The bundled demo application intentionally uses non-secret credentials:

```text
Username: demo_user
Password: quality123
```

These credentials exist only for this deterministic demo application.

## Why use a local demo application?

Public demo sites are convenient, but they make a portfolio test suite dependent on somebody else's availability, data, rate limits, and UI changes. A small local target keeps the pipeline deterministic and allows the repository to demonstrate framework design rather than third-party instability.

In a production environment I would normally test deployed services and use mocks/stubs selectively where they improve isolation.

## Development note

This is a personal portfolio project. AI-assisted development tools may be used as part of the implementation and review workflow, reflecting an AI-first engineering approach. All code should be reviewed, understood, and explainable by the repository owner before being presented in an interview.

See [TEST_STRATEGY.md](TEST_STRATEGY.md) for the quality approach and [ARCHITECTURE.md](ARCHITECTURE.md) for design decisions.
