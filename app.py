import os, json, re, tempfile, subprocess
from pathlib import Path
import requests
import streamlit as st

API_URL = os.getenv("NEBIUS_BASE_URL", "https://api.tokenfactory.nebius.com/v1/chat/completions")
DEFAULT_MODEL = os.getenv("NEBIUS_MODEL", "nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B")

st.set_page_config(page_title="FixLoop — AI Repair Engineer", page_icon="🔧", layout="wide")
st.markdown("""
<style>
.block-container{max-width:1200px;padding-top:1.5rem}
.hero{padding:1.4rem;border:1px solid #354052;border-radius:18px;background:linear-gradient(120deg,#182235,#10151e)}
.hero h1{margin:0;font-size:2.6rem}.hero p{color:#b9c4d7;margin-bottom:0}
.pill{display:inline-block;border:1px solid #526079;border-radius:999px;padding:.2rem .65rem;margin-right:.4rem;font-size:.8rem}
</style>
<div class="hero"><span class="pill">Coding agent</span><span class="pill">Nemotron + Nebius Token Factory</span>
<h1>🔧 FixLoop</h1><p>An AI repair engineer that investigates a bug, proposes a patch, and checks it against real tests.</p></div>
""", unsafe_allow_html=True)

DEMO_SOURCE = """def calculate_total(items, discount=0):
    'Return the total price after applying a discount percentage.'
    subtotal = sum(item["price"] * item["quantity"] for item in items)
    # BUG: discount is a percentage, but this subtracts the raw number.
    return subtotal - discount
"""
DEMO_TESTS = """from calculator import calculate_total

def test_total_without_discount():
    assert calculate_total([{"price": 10, "quantity": 2}]) == 20

def test_percentage_discount():
    assert calculate_total([{"price": 100, "quantity": 1}], discount=10) == 90

def test_discount_on_larger_subtotal():
    assert calculate_total([{"price": 200, "quantity": 1}], discount=10) == 180

def test_zero_discount():
    assert calculate_total([{"price": 7, "quantity": 3}], discount=0) == 21
"""
BUG_REPORT = "The discount argument is a percentage. A subtotal of 200 with discount=10 should return 180. Diagnose the bug and propose the smallest correct patch."

with st.sidebar:
    st.header("Configuration")
    api_key = st.text_input("Nebius Token Factory API key", type="password", value=os.getenv("NEBIUS_API_KEY", ""))
    model = st.text_input("Model ID", value=DEFAULT_MODEL)
    st.caption("The model ID must be available in your Token Factory account.")
    st.divider()
    st.caption("Safety: only the built-in demo project can be test-run. Custom snippets are analyzed but not executed.")

c1,c2,c3 = st.columns(3)
c1.metric("Workflow","Inspect → Patch → Verify")
c2.metric("Model","NVIDIA Nemotron")
c3.metric("Patch policy","Human review")
tab1,tab2,tab3 = st.tabs(["Try the demo bug","Analyze your code","About"])

def call_model(prompt):
    if not api_key:
        raise ValueError("Enter your Nebius Token Factory API key in the sidebar.")
    body = {"model": model, "messages":[{"role":"user","content":prompt}], "temperature":0.1, "max_tokens":1800}
    r = requests.post(API_URL, headers={"Authorization":f"Bearer {api_key}","Content-Type":"application/json"}, json=body, timeout=90)
    if not r.ok:
        raise RuntimeError(f"Token Factory HTTP {r.status_code}: {r.text[:1000]}")
    return r.json()["choices"][0]["message"]["content"]

def parse_response(raw):
    cleaned = re.sub(r"^```(?:json)?\s*|\s*```$", "", raw.strip(), flags=re.I)
    a,b = cleaned.find("{"),cleaned.rfind("}")
    if a >= 0 and b > a:
        cleaned = cleaned[a:b+1]
    return json.loads(cleaned)

def report(result):
    st.markdown("### Repair report")
    st.write(result.get("summary",""))
    st.markdown("**Root cause**")
    st.write(result.get("root_cause","Not provided"))
    st.markdown("**Proposed patch**")
    st.code(result.get("patch",""), language="python")
    st.markdown("**Suggested regression tests**")
    st.code(result.get("tests_to_add",""), language="python")
    st.markdown("**Risks / assumptions**")
    st.write(result.get("risks","None stated"))

def run_demo(patch):
    with tempfile.TemporaryDirectory(prefix="fixloop-") as tmp:
        p = Path(tmp)
        (p/"calculator.py").write_text(patch, encoding="utf-8")
        (p/"test_calculator.py").write_text(DEMO_TESTS, encoding="utf-8")
        try:
            result = subprocess.run(["python","-m","pytest","-q"], cwd=tmp, capture_output=True, text=True, timeout=12)
            return result.returncode == 0, (result.stdout+"\n"+result.stderr).strip()
        except subprocess.TimeoutExpired:
            return False, "Tests timed out after 12 seconds."
        except FileNotFoundError:
            return False, "pytest is missing. Install dependencies using pip install -r requirements.txt."

with tab1:
    st.markdown("### Reproducible demo")
    st.write("The built-in calculator has a percentage-discount bug. FixLoop asks Nemotron for a diagnosis and patch, then runs a fixed test suite against the proposed replacement file.")
    with st.expander("Show demo source and tests"):
        st.code(DEMO_SOURCE, language="python")
        st.code(DEMO_TESTS, language="python")
    bug = st.text_area("Bug report", BUG_REPORT, height=85)
    if st.button("Investigate with Nemotron", type="primary", use_container_width=True):
        prompt = f"""You are FixLoop, a careful software repair engineer. Return ONLY valid JSON with keys:
summary, root_cause, patch, tests_to_add, risks.
patch must be the complete replacement contents for calculator.py. Do not claim tests passed; the app will run them.
Bug report: {bug}
Source calculator.py:
{DEMO_SOURCE}
Existing tests:
{DEMO_TESTS}
"""
        with st.spinner("Calling Nemotron through Nebius Token Factory…"):
            try:
                raw = call_model(prompt)
                st.session_state["result"] = parse_response(raw)
                st.session_state["raw"] = raw
            except Exception as e:
                st.error(str(e))
    if "result" in st.session_state:
        result = st.session_state["result"]
        report(result)
        patch = result.get("patch","")
        if patch.strip() and st.button("Run demo tests against proposed patch", use_container_width=True):
            passed, output = run_demo(patch)
            st.success("All demo tests passed.") if passed else st.warning("Tests failed or could not run.")
            st.code(output or "(No output)", language="text")
        with st.expander("Raw model response"):
            st.code(st.session_state.get("raw",""))

with tab2:
    st.markdown("### Analyze a bug report")
    st.write("This mode provides a diagnosis and proposed patch from supplied text. It does not execute custom code.")
    issue = st.text_area("Bug description / stack trace", height=120, key="custom_issue")
    code = st.text_area("Relevant code", height=200, key="custom_code")
    lang = st.selectbox("Language", ["Python","JavaScript / TypeScript","Other"])
    if st.button("Generate diagnosis", type="primary", use_container_width=True):
        if not issue.strip() or not code.strip():
            st.warning("Enter both a bug description and relevant code.")
        else:
            prompt = f"""You are FixLoop, a careful software repair engineer. Return ONLY valid JSON with keys:
summary, root_cause, patch, tests_to_add, risks.
Do not claim code was executed or tests passed. Be clear about uncertainty.
Language: {lang}
Issue: {issue}
Code:
{code}
"""
            with st.spinner("Asking Nemotron…"):
                try:
                    report(parse_response(call_model(prompt)))
                except Exception as e:
                    st.error(str(e))

with tab3:
    st.markdown("""
### What this first model includes
- Real runtime calls to an NVIDIA Nemotron model through Nebius Token Factory.
- A built-in, reproducible bug and visible source/tests.
- Structured diagnosis, root cause, patch, regression-test suggestions, and risks.
- Actual test execution for the fixed built-in demo project.
- A separate code-snippet analysis flow.
- Human review: generated code is never automatically applied.

### Deliberate limitations
- No GitHub OAuth, repository cloning, or pull requests yet.
- Custom pasted code is not executed.
- The demo test runner is not a hardened arbitrary-code sandbox.
- Model slug availability must be confirmed in your Token Factory account.

### Hackathon fit
Track: **Coding and Agentic Engineering**. This app makes a runtime inference call to Nebius Token Factory and uses an NVIDIA Nemotron model. The next milestone is a hardened execution sandbox, repository-aware repair loops, deployment, and a public demo.
""")
st.divider()
st.caption("FixLoop prototype · Review AI-generated code before using it in a real project.")
