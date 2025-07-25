import datetime
import subprocess
import time

import requests
import schedule
from dotenv import dotenv_values

config = dotenv_values(".env")


class AlertManagerBot:
    def __init__(self) -> None:
        self.api_key: str = config.get("API_KEY")
        self.chat_id: str = config.get("PRIVATE_CHAT_ID")
        self.has_power: bool = None

    @staticmethod
    def format_actual_datetime() -> str:
        now = datetime.datetime.now(tz=datetime.UTC)
        date = now.date()

        day = date.day
        month = date.month

        hour = now.hour
        minute = now.minute

        return f"{day:02d}/{month:02d} - {hour:02d}:{minute:02d}"

    def send_text(self, msg: str) -> requests.Response:
        datetime = self.format_actual_datetime()
        text = f"{datetime} | {msg}"
        url = f"https://api.telegram.org/bot{self.api_key}/sendMessage?chat_id={self.chat_id}&parse_mode=HTML&text={text}"

        return requests.get(url, timeout=10)

    def check_if_has_power(self) -> None:
        hostname: str = config.get("PING_HOSTNAME_OR_IP")
        ping_count: str = config.get("PING_COUNT")
        timeout: int = int(config.get("PING_TIMEOUT"))

        try:
            subprocess.run(
                ["/bin/ping", "-c", ping_count, hostname],
                check=True,
                timeout=timeout,
                capture_output=True,
                text=True,
            )

            if self.has_power is None:
                self.send_text("---")
                self.send_text("Primera detección de luz. Todo bien.")

            if not self.has_power and self.has_power is not None:
                self.send_text("Respira tranquilo que la luz ha vuelto.")

            self.has_power = True
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as e:
            if self.has_power:
                self.send_text(f"Error! {e}")
                self.send_text(f"Stdout: {e.stdout}")
                self.send_text("Oye, que no tengo conexión con tu casa, hazlo mirar.")
                self.has_power = False


if __name__ == "__main__":
    alert_manager = AlertManagerBot()

    schedule.every(5).seconds.do(lambda: alert_manager.check_if_has_power())

    while True:
        schedule.run_pending()
        time.sleep(1)
