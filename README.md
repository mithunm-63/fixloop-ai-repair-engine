# FixLoop — Complete Prototype

FixLoop turns a bug report into a likely cause, investigation steps, a proposed patch, and regression-test ideas.

## Implemented
- Streamlit UI with Guided Demo, Analyze a Bug, and About & Setup tabs.
- Offline heuristic mode that works without an API key or payment card.
- Optional Nebius Token Factory integration using an OpenAI-compatible chat-completions endpoint.
- Model ID and endpoint configurable through environment variables or Streamlit secrets.
- JSON response parsing and clearer errors for common API failures.
- Built-in before/after calculator example and regression-test runner.
- Downloadable Markdown analysis report.
- Custom pasted code is treated as text and never executed.
- API keys are not stored in source code.
- Basic automated syntax/feature checks and GitHub Actions workflow.

## Important limitations
This is a complete prototype, not yet an autonomous repository-editing agent. It does not clone repositories, create branches, apply patches, commit changes, or run user-submitted code. Demo mode is heuristic, not a live LLM. Live model operation requires authorized Nebius access, available credits, and a model identifier enabled for your account. The default model identifier is only a starting value, not a guarantee of availability.

## Requirements
Python 3.10+ (Python 3.12 recommended). Internet is needed to install packages. Live mode also needs an authorized Nebius API key.

## Run on Windows / VS Code
Open this folder in VS Code. In Terminal → New Terminal, run each command:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

If PowerShell blocks activation, run this in the same terminal and retry:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

You can also skip activation and run `python -m pip install -r requirements.txt`, then `python -m streamlit run app.py`.

## Optional live Nebius configuration
Set environment variables or configure them in Streamlit Community Cloud → App settings → Secrets:

```toml
NEBIUS_API_KEY = "your-authorized-key"
NEBIUS_BASE_URL = "https://api.tokenfactory.nebius.com/v1"
NEBIUS_MODEL = "exact-model-id-from-your-account"
```

Optional environment variables: `NEBIUS_TIMEOUT` (default 90 seconds) and `MAX_CODE_CHARS` (default 18000). Never commit a real key or `.streamlit/secrets.toml`. Confirm the model ID in the catalog available to your account; the default may not be enabled for you.

## Deploy the offline demo
1. Upload/push the project to a GitHub repository.
2. Sign in at https://share.streamlit.io/.
3. Create an app from the repository, branch `main`, main file path `app.py`.
4. Deploy. Offline mode requires no secrets.
5. Only add a live API key through the host Secrets UI if you have authorized access.

Official guide: https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app

## Safety
- Code is sent to the configured provider only when live mode is selected and Analyze is clicked. Avoid sensitive code or secrets in a public demo.
- User-pasted code is never executed.
- The built-in runner only accepts the hard-coded calculator sample and runs a fixed test harness in a temporary directory.
- Model output is untrusted. Patches are displayed, not automatically applied.
- A human should review and test patches before use.

## Test and CI
Run `python -m compileall -q app.py tests demo_project` and `pytest -q`. The example project's calculator tests are intentionally expected to fail against the buggy function; this is part of the demonstration, not a CI failure. CI checks the app's syntax and key features instead.

## Hackathon demo flow
1. Show the incorrect discount behavior.
2. Run the built-in tests against the buggy sample.
3. Inspect the proposed diff.
4. Validate the fixed built-in sample.
5. Show the offline bug-report analysis.
6. If authorized API access is available, demonstrate live model mode and identify the actual model used.

## Next milestones
- Confirm card-free or sponsored live Nemotron access.
- Add controlled repository import and patch review.
- Add isolated container sandbox for tests on untrusted repositories.
- Add run history, rate limits, audit logs, and evaluation examples.
