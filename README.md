# Prueba Técnica Backend

Backend en Python con FastAPI, SQLAlchemy, PostgreSQL y un consumidor independiente, organizado con arquitectura hexagonal.

## Arquitectura
- `app/domain`: entidades, value objects y contratos de repositorio.
- `app/application`: casos de uso y puertos.
- `app/infrastructure`: PostgreSQL, logging, configuración y repositorios SQLAlchemy.
- `app/interfaces`: endpoints FastAPI, schemas y handlers de error.
- `consumer`: cliente externo que ejecuta requests, reintentos y trazas.

## Tecnologías
- Python 3.11
- FastAPI
- Pydantic v2
- SQLAlchemy 2
- PostgreSQL 16
- Docker y Docker Compose
- httpx, tenacity y structlog

## Requisitos cubiertos
- Crear, consultar y actualizar solicitudes.
- Validar catálogos, correo y campos obligatorios.
- Evitar duplicados por identificador externo.
- Exponer health checks `/health` y `/health/ready`.
- Consumidor independiente con reintentos solo para errores transitorios.
- Logs estructurados en JSON.
- Persistencia de PostgreSQL y logs.

## Estructura de carpetas
- `app/`
- `consumer/`
- `migrations/`
- `tests/`
- `docker-compose.yml`
- `Dockerfile`
- `consumer/Dockerfile`

## Variables de entorno
Las variables están documentadas en [.env.example](.env.example).

## Ejecución con Docker
La solución fue pensada para ejecutarse con:

```bash
docker compose up --build
```

Servicios expuestos:
- Backend: `http://localhost:8000`
- Swagger: `http://localhost:8000/docs`
- PostgreSQL: `localhost:5432`

## Endpoints
### Salud
- `GET /health`
- `GET /health/ready`

### Solicitudes
- `POST /api/v1/solicitudes`
- `GET /api/v1/solicitudes`
- `GET /api/v1/solicitudes/{id}`
- `PATCH /api/v1/solicitudes/{id}/estado`

## Ejemplos de consumo
### Crear solicitud
```bash
curl -X POST http://localhost:8000/api/v1/solicitudes \
  -H "Content-Type: application/json" \
  -d '{
    "external_identifier": "EXT-1001",
    "category": "soporte técnico",
    "requester_name": "Ana Perez",
    "requester_email": "ana@example.com",
    "description": "No puedo entrar a la plataforma",
    "priority": "alta"
  }'
```

### Consultar solicitudes
```bash
curl "http://localhost:8000/api/v1/solicitudes?status=recibida&category=soporte%20técnico&priority=alta"
```

### Consultar una solicitud
```bash
curl http://localhost:8000/api/v1/solicitudes/1
```

### Actualizar estado
```bash
curl -X PATCH http://localhost:8000/api/v1/solicitudes/1/estado \
  -H "Content-Type: application/json" \
  -d '{"status":"en proceso"}'
```

## Pruebas
La suite cubre:
- creación válida
- validación de correo
- duplicados
- consulta existente e inexistente
- actualización de estado
- health checks

Ejecuta las pruebas dentro del entorno con Python disponible o dentro de un contenedor de desarrollo.

## Decisiones técnicas
- FastAPI se usa como capa HTTP por su validación y OpenAPI nativos.
- SQLAlchemy queda aislado en infraestructura para no contaminar dominio y casos de uso.
- El consumidor no comparte código de persistencia con el backend.
- La base de datos se inicializa con script SQL para facilitar el arranque en Docker.
- La propuesta AWS usa Cognito como manejador de sesiones para el frontend, manteniendo el backend sin estado de autenticación.

## Limitaciones actuales
- La ruta `GET /api/v1/solicitudes/{id}` depende de la base real una vez que el contenedor backend arranque con PostgreSQL.

## Posibles mejoras
- Añadir Alembic como migración formal.
- Incorporar autenticación JWT y rate limiting.
- Añadir pruebas de integración con PostgreSQL real en Docker.
- Centralizar métricas y trazabilidad para una futura integración en AWS.
- Formalizar la integración con Cognito, incluyendo validación de JWKS y claims en cada backend.

## Documentación adicional
- Propuesta AWS: [docs/aws_proposal.md](docs/aws_proposal.md)
- Ejemplos y notas: [docs/examples.md](docs/examples.md)
