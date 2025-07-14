import asyncio
import logging
from asyncio.exceptions import CancelledError

import websockets
from dotenv import dotenv_values
from websockets.exceptions import ConnectionClosedError, ConnectionClosedOK


class WebSocketClient:
    logger = logging.getLogger(__name__)

    def __init__(self, url: str) -> None:
        self.url = url

    async def run(self) -> None:
        try:
            async with websockets.connect(self.url) as ws:
                self.logger.info("Conectado al servidor WS en %s", self.url)

                async for _ in ws:
                    await ws.send("pong")

        except ConnectionClosedOK:
            self.logger.error("Conexión cerrada con el servidor")
        except ConnectionClosedError:
            self.logger.error(
                "Error de conexión. Intentando reconectar en 5 segundos",
            )
            await asyncio.sleep(5)
        except ConnectionRefusedError:
            self.logger.error(
                "Conexión rechazada. ¿Está el server WS activo en %s?",
                self.url,
            )
        except CancelledError:
            self.logger.error("Cancelado a petición del usuario.")


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] - %(message)s",
        handlers=[
            logging.FileHandler("client_websocket.log"),
            logging.StreamHandler(),
        ],
    )
    logging.getLogger("websockets.server").setLevel(logging.WARNING)
    logging.getLogger("websockets.client").setLevel(logging.WARNING)
    logging.getLogger("websockets.protocol").setLevel(logging.WARNING)
    logging.getLogger("websockets.legacy.server").setLevel(logging.WARNING)
    logging.getLogger("websockets.legacy.client").setLevel(logging.WARNING)

    config = dotenv_values(".env")
    ws_server_url = config.get("WS_SERVER_URL")

    client = WebSocketClient(ws_server_url)
    asyncio.run(client.run())
