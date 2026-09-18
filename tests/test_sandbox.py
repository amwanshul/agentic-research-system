import pytest
from agentic_research.tools.sandbox import SafeSandbox


def test_safe_math_execution():
    code = """
x = 100
y = 25
growth_rate = (x - y) / y
result = round(growth_rate * 100, 2)
"""
    res = SafeSandbox.execute(code)
    assert res["success"] is True
    assert res["result"]["result"] == 300.0


def test_sandbox_blocks_imports():
    code = "import os; os.listdir('.')"
    res = SafeSandbox.execute(code)
    assert res["success"] is False
    assert "Imports are disabled" in res["error"]


def test_sandbox_blocks_forbidden_names():
    code = "f = open('test.txt', 'w')"
    res = SafeSandbox.execute(code)
    assert res["success"] is False
    assert "Forbidden symbol" in res["error"]
