import subprocess


def main() -> None:
    subprocess.run(
        ["/usr/bin/docker", "compose", "down", "--rmi", "all"],
        check=False,
    )
    subprocess.run(
        ["/usr/bin/docker", "compose", "up", "-d"],
        check=False,
    )


main()
