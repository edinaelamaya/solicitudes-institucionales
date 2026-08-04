# Ejemplos de uso y evidencias

## Ejemplos de curl

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

### Consultar salud
```bash
curl http://localhost:8000/health
curl http://localhost:8000/health/ready
```

### Actualizar estado
```bash
curl -X PATCH http://localhost:8000/api/v1/solicitudes/1/estado \
  -H "Content-Type: application/json" \
  -d '{"status":"completada"}'
```

## Formato de logs esperado
Los logs del backend y del consumidor se escriben en JSONL dentro de `/logs` cuando se ejecutan en contenedor.

### Ejemplo backend
```json
{"event":"request_created","service":"backend","request_identifier":"EXT-1001","endpoint":"POST /api/v1/solicitudes","http_status":201,"elapsed_ms":12.8,"level":"info","timestamp":"2026-08-02T12:00:00Z"}
```

### Ejemplo consumer
```json
{"event":"request_created","service":"consumer","request_identifier":"EXT-1001","endpoint":"POST /api/v1/solicitudes","http_status":201,"elapsed_ms":20.4,"attempt":1,"level":"info","timestamp":"2026-08-02T12:00:01Z"}
```

## Evidencias recomendadas
- `docker compose up --build`
- `docker compose logs -f`
- captura del Swagger: [img\Backend-Swagger.png]
- captura de un request válido y uno inválido
- valido:[img\valido-request.png]
- invalido:[img\invalid-request.png]
- captura de la salida del consumidor:
 - captura de la salida del consumidor: ![Consumer output](docs/img/consumer_output.svg)
 - evidencia del login con Cognito y el uso posterior del access token en una llamada a la API
