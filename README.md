# AlertManager - Telegram Bot

El código consiste en un servidor websocket que corre sobre el equipo que tiene constante conexión a la red y eléctrica, y un cliente que corre sobre el equipo que puede verse afectado por la caída de red eléctrica o de conexión.

## Uso

### Levantar el servidor

```bash
cd websocket_server
docker compose up -d --build
```

### Levantar el cliente

```bash
cd websocket_client
docker compose up -d --build
```
