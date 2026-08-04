from __future__ import annotations

import importlib
from pathlib import Path

import pytest
from fastapi.testclient import TestClient


@pytest.fixture()
def api_client(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> TestClient:
    monkeypatch.setenv("BACKEND_LOG_FILE_PATH", str(tmp_path / "backend.jsonl"))
    monkeypatch.setenv("APP_NAME", "Prueba Tecnica Backend")
    monkeypatch.setenv("APP_VERSION", "0.1.0")
    monkeypatch.setenv("API_V1_PREFIX", "/api/v1")

    app_main = importlib.import_module("app.main")
    monkeypatch.setattr(app_main, "initialize_database", lambda: None)

    with TestClient(app_main.app) as client:
        yield client
        client.app.dependency_overrides.clear()
