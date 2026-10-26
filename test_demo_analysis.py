import ast
from pathlib import Path

APP = Path(__file__).resolve().parents[1] / "app.py"
SOURCE = APP.read_text(encoding="utf-8")

def test_app_syntax():
    ast.parse(SOURCE)

def test_expected_features_are_present():
    assert "Offline demo" in SOURCE
    assert "NEBIUS_API_KEY" in SOURCE
    assert "Download analysis as Markdown" in SOURCE
    assert "run_builtin_tests" in SOURCE
