import argparse
import subprocess


def parser() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--user",
        type=str,
        help="User and server used to send the client or server directory.",
        required=True,
    )
    parser.add_argument(
        "--hostname",
        type=str,
        help="Hostname or IP and port used to send the client or server directory.",
        required=True,
    )
    parser.add_argument(
        "--client",
        action="store_true",
        help="Specify is the directory to send is the client directory.",
        required=True,
    )
    return parser.parse_args()


def main() -> None:
    args = parser()
    user: str = args.user
    hostname: str = args.hostname
    is_client: bool = args.client
    directory: str = "client" if is_client else "server"

    subprocess.run(
        [
            "/usr/bin/rsync",
            "-r",
            f"websocket_{directory}/",
            f"{user}@{hostname}:websocket_{directory}/",
        ],
        check=True,
    )


main()
