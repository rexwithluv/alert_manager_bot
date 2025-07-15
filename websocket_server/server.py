import asyncio
import logging
import os
from asyncio.exceptions import CancelledError

import websockets
from telegram import Bot
from telegram.error import TelegramError
from websockets.exceptions import (
    ConnectionClosed,
    ConnectionClosedError,
    ConnectionClosedOK,
)
from websockets.server import WebSocketServerProtocol


class TelegramBot:
    def __init__(self, api_key: str, chat_id: str) -> None:
        self.api_key = api_key
        self.chat_id = chat_id

    async def send_message(self, message: str) -> None:
        try:
            bot = Bot(self.api_key)

            await bot.send_message(chat_id=self.chat_id, text=message)
            WebSocketServer.logger.info("Mensaje de telegram enviado: %s", message)
        except TelegramError as e:
            WebSocketServer.logger.error("No se pudo mandar el mensaje: %s", e)


class WebSocketServer:
    logger = logging.getLogger(__name__)

    def __init__(
        self,
        ip: str = "0.0.0.0",
        port: int = 8765,
        bot: TelegramBot = None,
    ) -> None:
        self.ip: str = ip
        self.port: int = port
        self.tasks: set = set()
        self.bot: TelegramBot = bot

    async def send_ping(
        self,
        ws: WebSocketServerProtocol,
        client_hostname: str,
    ) -> None:
        try:
            while True:
                await ws.send("ping")
                self.logger.info("Mensaje enviado")
                await asyncio.sleep(5)
        except (ConnectionClosedOK, ConnectionClosedError, ConnectionClosed):
            self.logger.info("Ha fallado el ping con: %s", client_hostname)

    async def handler(self, ws: WebSocketServerProtocol) -> None:
        try:
            client_hostname = await ws.recv()
            self.logger.info("Cliente conectado: %s", client_hostname)
            await self.bot.send_message(f"Cliente conectado: {client_hostname}")

            ping_task = asyncio.create_task(self.send_ping(ws, client_hostname))
            self.tasks.add(ping_task)
            ping_task.add_done_callback(self.tasks.discard)

            async for message in ws:
                self.logger.info("Mensaje recibido: %s", message)

        except (ConnectionClosedOK, ConnectionClosedError, ConnectionClosed):
            close_message: str = f"Se cerró la conexión con: {client_hostname}"
            self.logger.info(close_message)
            await self.bot.send_message(close_message)

    async def run(self) -> None:
        try:
            async with websockets.serve(
                self.handler,
                "0.0.0.0",
                8765,
            ) as server:
                init_message: str = "Servidor Websocket iniciado en ws://0.0.0.0:8765"
                self.logger.info(init_message)
                await self.bot.send_message(init_message)
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

    telegram_api_key = os.getenv("TELEGRAM_API_KEY")
    telegram_chat_id = os.getenv("TELEGRAM_CHAT_ID")

    bot = TelegramBot(telegram_api_key, telegram_chat_id)
    server = WebSocketServer("0.0.0.0", 8765, bot)
    asyncio.run(server.run())
