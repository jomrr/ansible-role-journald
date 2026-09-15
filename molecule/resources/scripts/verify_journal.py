"""Verify local journal ingestion, storage and priority filtering."""

import subprocess
import sys
import uuid


def main() -> None:
    """Emit known priorities and read them from the expected journal storage."""
    directory, *expected = sys.argv[1:]
    subprocess.run(
        ["systemctl", "is-active", "--quiet", "systemd-journald.service"],
        check=True,
    )
    tag = "molecule-journald-" + uuid.uuid4().hex
    for priority in ("debug", "warning"):
        subprocess.run(
            ["systemd-cat", "--identifier=" + tag, "--priority=" + priority],
            input=priority + "\n",
            text=True,
            check=True,
        )
    subprocess.run(["journalctl", "--sync"], check=True)
    result = subprocess.run(
        [
            "journalctl",
            "--directory=" + directory,
            "--identifier=" + tag,
            "--output=cat",
            "--quiet",
            "--no-pager",
        ],
        text=True,
        stdout=subprocess.PIPE,
        check=True,
    )
    actual = result.stdout.splitlines()
    assert sorted(actual) == sorted(expected), (directory, expected, actual)
    print("Verified journal messages:", directory, actual)


if __name__ == "__main__":
    main()
