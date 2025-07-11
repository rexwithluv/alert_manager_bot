import datetime
import subprocess
import time

import requests
import schedule
from dotenv import dotenv_values

config = dotenv_values(".env")


class AlertManagerBot:
    def __init__(self) -> None:
        self.api_key = config.get("API_KEY")
        self.chat_id: str = config.get("PRIVATE_CHAT_ID")
        self.has_power: bool = None

    @staticmethod
    def format_actual_datetime() -> str:
        now = datetime.datetime.now()
        date = now.date()

        day = date.day
        month = date.month

        hour = now.hour
        minute = now.minute

        return f"{day:02d}/{month:02d} - {hour:02d}:{minute:02d}"

    def send_text(self, msg: str) -> requests.Response:
        url = f"https://api.telegram.org/bot{self.api_key}/sendMessage?chat_id={self.chat_id}&parse_mode=HTML&text={msg}"

        return requests.get(url, timeout=10)

    def change_power_status(self, powerReturn: bool) -> None:
        datetime: str = self.format_actual_datetime()
        text: str = "Respira tranquilo que la luz ha vuelto."

        if not powerReturn:
            text = "Oye, que no tengo conexión con tu casa, hazlo mirar."

        self.send_text(f"{datetime} | {text}")

    def check_if_has_power(self):
        try:
            subprocess.run(["ping", "-c", "1", "pikapi"], check=True)

            self.send_text("He hecho un ping, todo bien!")

            if not self.has_power:
                self.send_text("Respira tranquilo que la luz ha vuelto.")
                self.has_power = True
        except subprocess.CalledProcessError:
            if self.has_power:
                self.send_text("Oye, que no tengo conexión con tu casa, hazlo mirar.")
                self.has_power = False


if __name__ == "__main__":
    alert_manager = AlertManagerBot()

    schedule.every(5).seconds.do(lambda: alert_manager.check_if_has_power())

    while True:
        schedule.run_pending()
        time.sleep(1)
