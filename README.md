# FixLoop — AI Repair Engineer

An early-stage coding-agent prototype for the NVIDIA x Nebius Global AI Hackathon. FixLoop uses an NVIDIA Nemotron model through the Nebius Token Factory runtime API to diagnose bugs, propose patches, suggest regression tests, and run tests against a proposed patch for a fixed built-in demo project.

**Track:** Coding and Agentic Engineering  
**License:** MIT  
**Status:** Prototype, not production-safe autonomous software.

## Hackathon requirement fit

- Makes a real runtime call to Nebius Token Factory's OpenAI-compatible chat-completions API.
- Uses a configurable NVIDIA Nemotron model ID.
- Demonstrates bug report → model diagnosis → patch → actual test run → visible pass/fail result.
- Includes README, source code, demo fixture, requirements, and MIT license.

Verify the model identifier and availability in your Token Factory account before using the demo. The default model ID is configurable and may need to be changed to a model currently available to you.

## Run locally

Requires Python 3.10+.

```bash
python -m venv .venv
# macOS/Linux
source .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run app.py
```

Open the local Streamlit URL, enter your Nebius Token Factory API key in the sidebar, verify the model ID, then click **Investigate with Nemotron**.

Environment variables are also supported:

```bash
export NEBIUS_API_KEY="your_key"
export NEBIUS_MODEL="nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B"
streamlit run app.py
```

## Configuration

- `NEBIUS_API_KEY`: Token Factory API key.
- `NEBIUS_MODEL`: Model ID available to your account.
- `NEBIUS_BASE_URL`: API endpoint; defaults to `https://api.tokenfactory.nebius.com/v1/chat/completions`.

## Demo video outline

1. Show the seeded discount bug and its test file.
2. Run the Nemotron diagnosis through Token Factory.
3. Show root cause, patch, and suggested regression tests.
4. Run the demo tests and show the real output.
5. Explain that the app, not the model, determines test pass/fail.

## Safety and limitations

- The runner executes only the fixed built-in demo test suite in a temporary directory.
- Custom pasted code is analyzed as text and is not executed.
- Never commit API keys or secrets.
- Review generated patches before using them.
- Before supporting arbitrary repositories, implement a hardened isolated container/VM with no host mounts or secrets, restricted networking, resource limits, and strict timeouts.
- No GitHub cloning, commits, or pull requests are implemented yet.

## Roadmap

1. Add hardened ephemeral execution.
2. Add authorized repository import and safe file selection.
3. Add bounded iterative test → diagnose → patch cycles.
4. Show unified diffs and per-test output.
5. Add a small benchmark of seeded bugs.
6. Deploy with server-side secrets and request/error logging.

## Hackathon feedback

Before submitting, record genuine test observations: patch quality, diagnosis accuracy, latency, token usage, API errors, integration friction, and possible improvements. Do not fabricate feedback.
