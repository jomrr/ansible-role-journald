"""Create disposable certificates for journal transport integration tests."""

import os
import subprocess
import sys
from pathlib import Path


def openssl(*arguments: str) -> None:
    """Run OpenSSL without printing generated material."""
    subprocess.run(["openssl", *arguments], check=True, capture_output=True)


def main() -> None:
    """Issue a server and client certificate from the test CA."""
    os.umask(0o077)
    directory = Path(sys.argv[1])
    directory.mkdir(mode=0o700, exist_ok=True)
    os.chdir(directory)
    openssl(
        "req",
        "-x509",
        "-newkey",
        "rsa:2048",
        "-nodes",
        "-days",
        "2",
        "-subj",
        "/CN=Journal test CA",
        "-keyout",
        "ca.key",
        "-out",
        "ca.crt",
        "-addext",
        "basicConstraints=critical,CA:TRUE",
        "-addext",
        "keyUsage=critical,keyCertSign,cRLSign",
    )
    for name, usage in (("server", "serverAuth"), ("client", "clientAuth")):
        openssl(
            "req",
            "-new",
            "-newkey",
            "rsa:2048",
            "-nodes",
            "-subj",
            f"/CN={name}",
            "-keyout",
            f"{name}.key",
            "-out",
            f"{name}.csr",
        )
        Path(f"{name}.ext").write_text(
            "basicConstraints=critical,CA:FALSE\n"
            "keyUsage=critical,digitalSignature,keyEncipherment\n"
            f"extendedKeyUsage={usage}\n"
            "subjectAltName=DNS:localhost,DNS:journal-collector\n",
            encoding="utf-8",
        )
        openssl(
            "x509",
            "-req",
            "-in",
            f"{name}.csr",
            "-CA",
            "ca.crt",
            "-CAkey",
            "ca.key",
            "-CAcreateserial",
            "-days",
            "2",
            "-extfile",
            f"{name}.ext",
            "-out",
            f"{name}.crt",
        )


if __name__ == "__main__":
    main()
