# Architecture & Design Decisions

## 1. Page Objects

UI selectors and common interactions live in `pages/` instead of directly inside test cases.

This keeps tests focused on intent:

```python
login_page.login_as("demo_user", "quality123")
assert inventory_page.item_names() == [...]
```

rather than implementation:

```python
page.locator("#username").fill(...)
```

If a selector changes, the update can usually be made in one place.

## 2. API client wrapper

`utils/api_client.py` centralises base URL handling and common HTTP operations.

For a larger framework this is where I would consider adding:

- authentication/session management;
- retry policy where appropriate;
- structured request/response logging;
- correlation IDs;
- schema helpers;
- timing/telemetry.

I would avoid hiding so much HTTP detail that test failures become difficult to diagnose.

## 3. Environment configuration

`utils/config.py` reads environment variables and applies safe defaults.

The same tests can therefore target different environments without hard-coded URLs in test files.

## 4. Deterministic application target

The demo FastAPI application is included only to make the portfolio reliable and self-contained.

Production automation should test the actual deployed application at appropriate layers. The local target is not intended to imply that QA should own production application code.

## 5. CI pipeline

The GitHub Actions workflow represents a basic release gate.

A production implementation could expand this with:

- pull-request smoke suite;
- post-deployment environment validation;
- parallel/sharded regression execution;
- test result publishing;
- flaky-test tracking;
- quality thresholds;
- deployment rollback or promotion gates.

## 6. Failure diagnostics

Assertions include expected behaviour and use clear test names. The framework deliberately avoids complex abstractions that would make a failed test harder to understand.

For a larger system I would add screenshots/traces for failed UI tests and structured service logs/correlation IDs for API failures.

## Interview talking points

Be prepared to explain:

- why API tests usually outnumber UI tests;
- why deterministic tests matter in CI;
- why Page Objects help but can also be over-abstracted;
- how you would decide what belongs in smoke vs regression;
- what you would do with a flaky test;
- how you would evolve this structure for multiple environments or services;
- why a green regression suite is only one input into release readiness.
