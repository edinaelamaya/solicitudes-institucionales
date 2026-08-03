from __future__ import annotations

import time
from typing import Any

import structlog

from consumer.client import ConsumerApiClient, ConsumerPayload, NonRetryableRequestError, RetryableRequestError
from consumer.logging_config import configure_logging
from consumer.settings import get_consumer_settings


logger = structlog.get_logger("consumer")


def _log_result(action: str, payload: dict[str, Any], **extra: Any) -> None:
    logger.info(action, **payload, **extra)


def run() -> None:
    settings = get_consumer_settings()
    configure_logging(settings.log_level, settings.consumer_log_file_path)

    client = ConsumerApiClient(
        base_url=settings.backend_base_url,
        timeout_seconds=settings.request_timeout_seconds,
        max_attempts=settings.max_retry_attempts,
    )

    payloads = [
        ConsumerPayload("EXT-1001", "soporte técnico", "Ana Perez", "ana@example.com", "No puedo entrar", "alta"),
        ConsumerPayload("EXT-1002", "administrativa", "Luis Gomez", "luis@example.com", "Solicitud de certificado", "media"),
        ConsumerPayload("EXT-1001", "soporte técnico", "Ana Perez", "ana@example.com", "Duplicado intencional", "alta"),
    ]

    created_ids: list[int] = []
    for index, payload in enumerate(payloads, start=1):
        start = time.perf_counter()
        try:
            response = client.create_request(payload)
            created_ids.append(response["id"])
            _log_result(
                "request_created",
                response,
                service="consumer",
                request_identifier=payload.external_identifier,
                endpoint="POST /api/v1/solicitudes",
                http_status=201,
                elapsed_ms=round((time.perf_counter() - start) * 1000, 2),
                attempt=index,
            )
        except NonRetryableRequestError as exc:
            logger.warning(
                "request_rejected",
                service="consumer",
                request_identifier=payload.external_identifier,
                endpoint="POST /api/v1/solicitudes",
                error=str(exc),
                attempt=index,
            )
        except RetryableRequestError as exc:
            logger.error(
                "request_failed_transiently",
                service="consumer",
                request_identifier=payload.external_identifier,
                endpoint="POST /api/v1/solicitudes",
                error=str(exc),
                attempt=index,
            )

    for request_id in created_ids:
        start = time.perf_counter()
        try:
            response = client.get_request(request_id)
            _log_result(
                "request_fetched",
                response,
                service="consumer",
                request_identifier=str(request_id),
                endpoint=f"GET /api/v1/solicitudes/{request_id}",
                http_status=200,
                elapsed_ms=round((time.perf_counter() - start) * 1000, 2),
                attempt=1,
            )

            updated = client.update_status(request_id, "en proceso")
            _log_result(
                "request_status_updated",
                updated,
                service="consumer",
                request_identifier=str(request_id),
                endpoint=f"PATCH /api/v1/solicitudes/{request_id}/estado",
                http_status=200,
                elapsed_ms=round((time.perf_counter() - start) * 1000, 2),
                attempt=1,
            )
        except NonRetryableRequestError as exc:
            logger.warning(
                "request_flow_rejected",
                service="consumer",
                request_identifier=str(request_id),
                error=str(exc),
            )
        except RetryableRequestError as exc:
            logger.error(
                "request_flow_failed_transiently",
                service="consumer",
                request_identifier=str(request_id),
                error=str(exc),
            )


if __name__ == "__main__":
    run()
