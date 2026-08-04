from __future__ import annotations

from app.interfaces.api import routes as api_routes


def test_health_endpoint_returns_ok(api_client) -> None:
    response = api_client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_health_ready_endpoint_returns_ready(api_client, monkeypatch) -> None:
    from app.interfaces.api.routes import health as health_module

    monkeypatch.setattr(health_module, "check_database_connection", lambda: True)

    response = api_client.get("/health/ready")

    assert response.status_code == 200
    assert response.json()["status"] == "ready"


def test_health_ready_endpoint_returns_unavailable(api_client, monkeypatch) -> None:
    from app.interfaces.api.routes import health as health_module

    def failing_check() -> bool:
        raise RuntimeError("db down")

    monkeypatch.setattr(health_module, "check_database_connection", failing_check)

    response = api_client.get("/health/ready")

    assert response.status_code == 503
