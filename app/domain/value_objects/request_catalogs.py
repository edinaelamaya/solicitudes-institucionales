from enum import StrEnum


class RequestCategory(StrEnum):
    ACCESS_TO_PLATFORM = "acceso a plataforma"
    TECH_SUPPORT = "soporte técnico"
    ACADEMIC = "académica"
    ADMINISTRATIVE = "administrativa"


class RequestPriority(StrEnum):
    LOW = "baja"
    MEDIUM = "media"
    HIGH = "alta"


class RequestStatus(StrEnum):
    RECEIVED = "recibida"
    IN_PROGRESS = "en proceso"
    COMPLETED = "completada"
    REJECTED = "rechazada"
