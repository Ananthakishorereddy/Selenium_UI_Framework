# AE UI Automation Framework

Enterprise-grade Selenium + Pytest UI automation framework targeting [automationexercise.com](https://automationexercise.com).

---

## Tech Stack

| Layer | Tool |
|---|---|
| Language | Python 3.9+ |
| Browser Automation | Selenium WebDriver 4.x |
| Test Framework | Pytest |
| Design Pattern | Page Object Model (POM) |
| Reporting | pytest-html / Allure |
| Logging | Python `logging` module |
| Driver Management | webdriver-manager |
| Parallel Execution | pytest-xdist |
| Auto-retry | pytest-rerunfailures |

---

## Project Structure

```
AE_UI_Framework/
│
├── tests/
│   ├── test_login.py       # Login & logout scenarios
│   ├── test_signup.py      # User registration scenarios
│   ├── test_product.py     # Product listing & search
│   └── test_cart.py        # Cart add/remove scenarios
│
├── pages/
│   ├── base_page.py        # Shared Selenium actions
│   ├── home_page.py        # Navigation, subscription
│   ├── login_page.py       # Login + signup initiation
│   ├── signup_page.py      # Full registration form
│   ├── product_page.py     # Product listing & detail
│   └── cart_page.py        # Cart management
│
├── utils/
│   ├── driver_factory.py   # WebDriver initialization (Chrome/Firefox/Edge)
│   ├── config_reader.py    # YAML config loader
│   ├── logger.py           # Centralized logging
│   ├── waits.py            # Explicit wait wrappers
│   └── helpers.py          # Test data loader, random generators, screenshots
│
├── config/
│   └── config.yaml         # Environment configs (qa, staging, headless_ci)
│
├── test_data/
│   └── test_data.json      # Credentials, user data, search keywords
│
├── reports/                # Auto-generated (gitignored)
│   ├── report.html
│   ├── screenshots/
│   └── logs/
│
├── .github/
│   └── workflows/
│       └── ui_tests.yml    # GitHub Actions CI pipeline
│
├── conftest.py             # Fixtures, CLI options, screenshot-on-failure hook
├── pytest.ini              # Pytest configuration
└── requirements.txt        # Python dependencies
```

---

## Setup

### 1. Clone the repository
```bash
git clone <your-repo-url>
cd AE_UI_Framework
```

### 2. Create and activate a virtual environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Update test credentials
Open `test_data/test_data.json` and replace `valid_user.email` and `valid_user.password`
with a real account registered at [automationexercise.com](https://automationexercise.com).

---

## Running Tests

### All tests (default Chrome, headed)
```bash
pytest
```

### Specific test file
```bash
pytest tests/test_login.py -v
```

### Specific test class or function
```bash
pytest tests/test_login.py::TestLoginPage::test_valid_login -v
```

### By marker
```bash
pytest -m smoke -v
pytest -m "login or signup" -v
pytest -m regression -v
```

### Headless mode
```bash
pytest --headless
```

### Different browser
```bash
pytest --browser=firefox
pytest --browser=edge
```

### Different environment
```bash
pytest --env=staging
```

### Parallel execution
```bash
# auto-detect CPU count
pytest -n auto

# fixed 4 workers
pytest -n 4
```

### Auto-retry flaky tests
```bash
pytest --reruns=2 --reruns-delay=3
```

### Full CI-style command
```bash
pytest --browser=chrome --headless --env=headless_ci -n auto --reruns=2 -v
```

---

## Reporting

### HTML Report
Generated automatically at `reports/report.html` after each run (configured in `pytest.ini`).

Open it in any browser:
```bash
start reports/report.html        # Windows
open reports/report.html         # macOS
```

### Allure Report
```bash
# Run with Allure data collection
pytest --alluredir=reports/allure-results

# Generate and open the report (requires Allure CLI installed)
allure serve reports/allure-results
```

---

## Test Markers

| Marker | Purpose |
|---|---|
| `smoke` | Fast, critical path tests |
| `regression` | Full regression suite |
| `login` | Login/auth tests |
| `signup` | Registration tests |
| `product` | Product page tests |
| `cart` | Cart tests |

---

## Framework Architecture

### Page Object Model
Each page is a Python class that:
- Declares locators as class-level tuples `(By.X, "selector")`
- Exposes readable action methods (`login()`, `search_product()`)
- Inherits shared Selenium helpers from `BasePage`

Test files contain **only** test logic and assertions — never raw Selenium calls.

### Fixtures (conftest.py)
- `config` — session-scoped; reads `config.yaml` once per run
- `driver` — function-scoped; fresh browser per test, auto-quits after
- `pytest_runtest_makereport` hook — attaches pass/fail result to fixture teardown

### Screenshot on Failure
Automatically triggered in the `driver` fixture teardown. Saved to `reports/screenshots/FAIL_<test_name>_<timestamp>.png`.

### Logging
Dual-channel: `INFO` to console, `DEBUG` to `reports/logs/test_run_<date>.log`.

---

## CI/CD — GitHub Actions

The workflow in `.github/workflows/ui_tests.yml`:
- Triggers on push to `main`/`develop`, PRs, and weekday schedule (06:00 UTC)
- Runs tests in headless Chrome with parallel workers and auto-retry
- Uploads HTML report, screenshots, and logs as artifacts

---

## Extending the Framework

| Goal | How |
|---|---|
| Add a new page | Create `pages/new_page.py` extending `BasePage` |
| Add a new test module | Create `tests/test_new_feature.py` |
| Add a new environment | Add a block in `config/config.yaml` |
| Add test data | Extend `test_data/test_data.json` |
| Cross-browser matrix | Extend `matrix.browser` in `ui_tests.yml` |
| API + UI combined | Add `requests` to `requirements.txt` and create `api/` layer |
