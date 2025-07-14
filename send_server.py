import argparse
import subprocess


def parser() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--user_and_server",
        type=str,
        help="User and server used to send weboscket_server directory.",
    )
    return parser.parse_args()


def main() -> None:
    args = parser()
    user_and_server = args.user_and_server

    subprocess.run(
        [
            "/usr/bin/rsync",
            "-r",
            "websocket_server/",
            f"{user_and_server}:websocket_server/",
        ],
        check=True,
    )


main()
