import asyncio
import logging
from asyncio.exceptions import CancelledError

import websockets
from websockets.exceptions import (
    ConnectionClosed,
    ConnectionClosedError,
    ConnectionClosedOK,
)
from websockets.server import WebSocketServerProtocol


class WebSocketServer:
    def __init__(self, ip: str = "0.0.0.0", port: int = 8765) -> None:
        self.ip: str = ip
        self.port: int = port
        self.tasks: set = set()
        self.logger = logging.getLogger(__name__)

    async def send_ping(self, ws: WebSocketServerProtocol) -> None:
        try:
            while True:
                await ws.send("ping")
                self.logger.info("Mensaje enviado")
                await asyncio.sleep(5)
        except (ConnectionClosedOK, ConnectionClosedError, ConnectionClosed):
            self.logger.info("La conexión se cerró mientras se enviaba un ping.")

    async def handler(self, ws: WebSocketServerProtocol) -> None:
        client_address = ws.remote_address[0]
        self.logger.info("Cliente conectado: %s", client_address)

        ping_task = asyncio.create_task(self.send_ping(ws))
        self.tasks.add(ping_task)

        ping_task.add_done_callback(self.tasks.discard)

        async for message in ws:
            self.logger.info("Mensaje recibido: %s", message)

    async def run(self) -> None:
        try:
            async with websockets.serve(
                self.handler,
                "0.0.0.0",
                8765,
            ) as server:
                self.logger.info("Servidor Websocket iniciado en ws://0.0.0.0:8765")
                await server.serve_forever()

        except CancelledError:
            self.logger.error("Cancelado a petición del usuario.")


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] - %(message)s",
        handlers=[
            logging.FileHandler("server_websocket.log"),
            logging.StreamHandler(),
        ],
    )
    logging.getLogger("websockets.server").setLevel(logging.WARNING)
    logging.getLogger("websockets.client").setLevel(logging.WARNING)
    logging.getLogger("websockets.protocol").setLevel(logging.WARNING)
    logging.getLogger("websockets.legacy.server").setLevel(logging.WARNING)
    logging.getLogger("websockets.legacy.client").setLevel(logging.WARNING)

    server = WebSocketServer()
    asyncio.run(server.run())
