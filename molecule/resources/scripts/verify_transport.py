"""Exercise authenticated reception, journal uploads, rotation and recovery."""

import base64
import json
import os
import ssl
import subprocess
import sys
import time
import uuid
from http.client import HTTPSConnection
from pathlib import Path


def read_entries(directory: str, tag: str) -> list[dict[str, str]]:
    """Read only the test's messages from the received journal."""
    result = subprocess.run(
        [
            "journalctl",
            "--directory=" + directory,
            "--identifier=" + tag,
            "--output=json",
            "--quiet",
            "--no-pager",
        ],
        check=True,
        text=True,
        capture_output=True,
    )
    return [json.loads(line) for line in result.stdout.splitlines()]


def wait_for_message(directory: str, tag: str, message: str, hostname: str) -> None:
    """Allow the upload service time to reconnect and deliver a message."""
    deadline = time.monotonic() + 90
    while time.monotonic() < deadline:
        entries = read_entries(directory, tag)
        if any(entry["MESSAGE"] == message for entry in entries):
            assert all(entry["_HOSTNAME"] == hostname for entry in entries), entries
            return
        time.sleep(1)
    raise AssertionError(
        f"Message {message!r} from {hostname} did not reach {directory}"
    )


def export_entry(tag: str, message: str) -> bytes:
    """Produce a remote event whose source differs from the collector."""
    return (
        f"__REALTIME_TIMESTAMP={time.time_ns() // 1000}\n"
        f"__MONOTONIC_TIMESTAMP={time.monotonic_ns() // 1000}\n"
        "_BOOT_ID=0123456789abcdef0123456789abcdef\n"
        "_HOSTNAME=remote-fixture\n"
        f"SYSLOG_IDENTIFIER={tag}\nPRIORITY=4\nMESSAGE={message}\n\n"
    ).encode()


def upload(port: int, data: bytes, *, authenticate: bool = True) -> int:
    """Send Journal Export Format over a verified TLS connection."""
    context = ssl.create_default_context(cafile="/etc/journald-molecule/ca.crt")
    if authenticate:
        context.load_cert_chain(
            "/etc/journald-molecule/client.crt",
            "/etc/journald-molecule/client.key",
        )
    connection = HTTPSConnection("localhost", port, context=context, timeout=30)
    try:
        connection.request(
            "POST",
            "/upload",
            data,
            {"Content-Type": "application/vnd.fdo.journal"},
        )
        response = connection.getresponse()
        response.read()
        return response.status
    finally:
        connection.close()


def emit(tag: str, message: str) -> None:
    """Emit a local message for the managed upload service to forward."""
    subprocess.run(
        ["systemd-cat", "--identifier=" + tag, "--priority=warning"],
        input=message + "\n",
        text=True,
        check=True,
    )
    subprocess.run(["journalctl", "--sync"], check=True)


def verify_reception(directory: str, port: int, tag: str) -> None:
    """Verify source metadata, required client authentication and rotation."""
    assert upload(port, export_entry(tag, "accepted")) == 202
    wait_for_message(directory, tag, "accepted", "remote-fixture")
    try:
        status = upload(port, export_entry(tag, "unauthenticated"), authenticate=False)
    except (ssl.SSLError, ConnectionResetError):
        pass
    else:
        assert status in (401, 403), status
    assert not any(
        entry["MESSAGE"] == "unauthenticated" for entry in read_entries(directory, tag)
    )
    payload = b"".join(
        export_entry(tag + "-rotation", base64.b64encode(os.urandom(65536)).decode())
        for _ in range(192)
    )
    assert upload(port, payload) == 202
    assert list(Path(directory).glob("*@*.journal")), "Receiver did not rotate"
    assert upload(port, export_entry(tag, "after-rotation")) == 202
    wait_for_message(directory, tag, "after-rotation", "remote-fixture")


def upload_state() -> str:
    """Identify an active upload invocation and its automatic restart count."""
    result = subprocess.run(
        [
            "systemctl",
            "show",
            "systemd-journal-upload.service",
            "--property=ActiveState,InvocationID,NRestarts",
        ],
        check=True,
        text=True,
        capture_output=True,
    )
    state = dict(line.split("=", 1) for line in result.stdout.splitlines())
    assert state["ActiveState"] == "active", state
    assert state["InvocationID"], state
    return result.stdout.strip()


def main() -> None:
    """Run a collector check, emit a source message or wait for its delivery."""
    action, *arguments = sys.argv[1:]
    if action == "receive":
        directory, port_text = arguments
        tag = "molecule-transport-" + uuid.uuid4().hex
        verify_reception(directory, int(port_text), tag)
        print("Verified TLS reception, source metadata and rotation:", directory)
    elif action == "emit":
        tag = "molecule-upload-" + uuid.uuid4().hex
        emit(tag, arguments[0])
        print(tag)
    elif action == "upload-state":
        print(upload_state())
    elif action == "wait":
        directory, tag, hostname, message = arguments
        wait_for_message(directory, tag, message, hostname)
        print("Verified delivery from", hostname, "of", message)
    else:
        raise ValueError(f"Unknown test action: {action}")


if __name__ == "__main__":
    main()
