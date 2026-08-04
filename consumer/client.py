from __future__ import annotations

from dataclasses import asdict, dataclass

import httpx
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential


class RetryableRequestError(Exception):
    """Raised when a request can be retried."""


class NonRetryableRequestError(Exception):
    """Raised when a request must not be retried."""


@dataclass(slots=True)
class ConsumerPayload:
    external_identifier: str
    category: str
    requester_name: str
    requester_email: str
    description: str
    priority: str


class ConsumerApiClient:
    def __init__(self, base_url: str, timeout_seconds: float, max_attempts: int) -> None:
        self._base_url = base_url.rstrip("/")
        self._timeout = httpx.Timeout(timeout_seconds)
        self._max_attempts = max_attempts

    def _request(self, method: str, path: str, json_body: dict | None = None) -> dict:
        try:
            with httpx.Client(base_url=self._base_url, timeout=self._timeout) as client:
                response = client.request(method, path, json=json_body)
        except httpx.RequestError as exc:
            raise RetryableRequestError(str(exc)) from exc

        if 500 <= response.status_code:
            raise RetryableRequestError(f"server error {response.status_code}")
        if 400 <= response.status_code:
            raise NonRetryableRequestError(f"client error {response.status_code}")

        return response.json()

    def _retry_config(self):
        return retry(
            retry=retry_if_exception_type(RetryableRequestError),
            stop=stop_after_attempt(self._max_attempts),
            wait=wait_exponential(multiplier=1, min=1, max=5),
            reraise=True,
        )

    def create_request(self, payload: ConsumerPayload) -> dict:
        @self._retry_config()
        def _create() -> dict:
            return self._request("POST", "/api/v1/solicitudes", json_body=asdict(payload))

        return _create()

    def get_request(self, request_id: int) -> dict:
        @self._retry_config()
        def _get() -> dict:
            return self._request("GET", f"/api/v1/solicitudes/{request_id}")

        return _get()

    def update_status(self, request_id: int, status: str) -> dict:
        @self._retry_config()
        def _update() -> dict: 
            return self._request("PATCH", f"/api/v1/solicitudes/{request_id}/estado", json_body={"status": status})

        return _update()
