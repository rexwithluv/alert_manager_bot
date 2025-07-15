import asyncio
import logging
import os
import socket

import websockets


class WebSocketClient:
    def __init__(self, url: str) -> None:
        self.url: str = url
        self.hostname: str = socket.gethostname()
        self.logger = logging.getLogger(__name__)

    async def run(self) -> None:
        async with websockets.connect(self.url) as ws:
            self.logger.info("Conectado al servidor WS en %s", self.url)
            await ws.send(self.hostname)

            async for _ in ws:
                await ws.send("pong")


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

    ws_server_url = os.getenv("WS_SERVER_URL")

    client = WebSocketClient(ws_server_url)
    asyncio.run(client.run())
