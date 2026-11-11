import os
import pytest

@pytest.fixture(autouse=True)
def set_ttd_ai_fixture_env(monkeypatch):
    """Ensure tests run in fixture mode by default."""
    monkeypatch.setenv("TTD_AI_FIXTURE", "1")
