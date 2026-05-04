#!/usr/bin/env python3
# encoding: utf-8
"""
hget-test: batería de tests para el cliente HTTP simple.

Escrito con fines didácticos por la cátedra de
Redes y Sistemas Distribuidos,
FaMAF-UNC

Amplía los doctests del cliente hget. Prueba funciones auxiliares
sin necesidad de conexiones de red reales.

Uso:
  pytest hget-test.py -v
  python3 -m pytest hget-test.py -v
  python3 hget-test.py -v
"""

from __future__ import annotations

import socket
import subprocess
import sys
import time
from pathlib import Path

import pytest

import hget


class FakeSocket:
    """
    Socket simulado con datos en memoria.
    Para testing sin conexiones reales.
    """

    def __init__(self, data: str | bytes = "") -> None:
        if isinstance(data, bytes):
            self._data = data
        else:
            self._data = data.encode()
        self._sent: bytearray = bytearray()

    def recv(self, count: int) -> bytes:
        chunk = self._data[:count]
        self._data = self._data[count:]
        return chunk

    def send(self, data: bytes) -> int:
        self._sent.extend(data)
        return len(data)

    def sent_data(self) -> bytes:
        return bytes(self._sent)


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


def test_send_request() -> None:
    sock = FakeSocket(b"")
    hget.send_request(sock, "http://host/path")
    assert sock.sent_data() == b"GET http://host/path HTTP/1.0\r\nHost: host\r\n\r\n"


def test_send_request_url_conservada() -> None:
    sock = FakeSocket(b"")
    hget.send_request(sock, "http://a.b:8080/foo/bar")
    assert b"http://a.b:8080/foo/bar" in sock.sent_data()
    assert b"Host: a.b" in sock.sent_data()


def test_read_line_completa() -> None:
    sock = FakeSocket(b"text line\r\nother line\r\n")
    assert hget.read_line(sock) == b"text line\r\n"
    assert hget.read_line(sock) == b"other line\r\n"
    assert hget.read_line(sock) == b""


def test_read_line_sin_newline() -> None:
    sock = FakeSocket(b"text line")
    assert hget.read_line(sock) == b"text line"


def test_read_line_solo_newline() -> None:
    sock = FakeSocket(b"\n")
    assert hget.read_line(sock) == b"\n"


def test_get_response_guarda_body(tmp_path: Path) -> None:
    response = (
        b"HTTP/1.0 200 OK\r\n"
        b"Encabezado: ignorado\r\n"
        b"Otro: tambien\r\n"
        b"\r\n"
        b"dato123456\n"
        b"7890"
    )
    out_file = tmp_path / "test.tmp"
    sock = FakeSocket(response)
    hget.get_response(sock, str(out_file))
    assert out_file.read_text() == "dato123456\n7890"


def test_get_response_status_ok(tmp_path: Path) -> None:
    sock = FakeSocket(b"HTTP/1.0 200 OK\r\n\r\nbody")
    out_file = tmp_path / "out.bin"
    assert hget.get_response(sock, str(out_file)) is True
    assert out_file.read_bytes() == b"body"


def test_get_response_status_no_ok(tmp_path: Path) -> None:
    sock = FakeSocket(b"HTTP/1.0 404 Not Found\r\n\r\n")
    out_file = tmp_path / "out.bin"
    assert hget.get_response(sock, str(out_file)) is False


def test_parse_server_y_puerto() -> None:
    assert hget.parse_server("http://localhost:8080/") == "localhost"
    assert hget.parse_port("http://localhost:8080/") == 8080


def test_check_http_response() -> None:
    assert hget.check_http_response(b"HTTP/1.0 200 OK") is True
    assert hget.check_http_response(b"HTTP/1.1 301 Moved") is False


# --- Tests para cobertura: helpers DNS y parse ---


def test_parse_server_varios() -> None:
    assert hget.parse_server("http://a.b/") == "a.b"
    assert hget.parse_server("http://host:99/path") == "host"


def test_parse_port_varios() -> None:
    assert hget.parse_port("http://host/") == 80
    assert hget.parse_port("http://host:443/") == 443


def test_dns_encode_name() -> None:
    assert hget._dns_encode_name("a") == b"\x01a\x00"
    assert hget._dns_encode_name("a.b") == b"\x01a\x01b\x00"
    assert hget._dns_encode_name("localhost").endswith(b"\x00")


def test_dns_build_query() -> None:
    q = hget._dns_build_query("x", 12345)
    assert len(q) >= 12
    assert q[:2] == (12345).to_bytes(2, "big")


def test_dns_skip_name() -> None:
    assert hget._dns_skip_name(b"\x00", 0) == 1
    assert hget._dns_skip_name(b"\x01a\x00", 0) == 3


def test_dns_parse_one_rr_a_record() -> None:
    # RR: name \x00, type=1, class=1, ttl=0, rdlength=4, rdata=1.2.3.4
    data = b"\x00\x00\x01\x00\x01\x00\x00\x00\x00\x00\x04" + bytes([1, 2, 3, 4])
    ip_str, next_pos = hget._dns_parse_one_rr(data, 0)
    assert ip_str == "1.2.3.4"
    assert next_pos == 1 + 10 + 4


def test_dns_parse_response_corta() -> None:
    import socket as s

    with pytest.raises(s.gaierror):
        hget._dns_parse_response(b"\x00" * 11, 0)


def test_dns_parse_response_valida() -> None:
    # Respuesta DNS mínima: header 12 bytes, question 5 bytes, 1 RR tipo A.
    query_id = 1
    header = (
        query_id.to_bytes(2, "big")
        + b"\x80\x00\x00\x01\x00\x01\x00\x00\x00\x00"
    )
    question = b"\x00\x00\x01\x00\x01"
    rr = b"\x00\x00\x01\x00\x01\x00\x00\x00\x00\x00\x04" + bytes([1, 2, 3, 4])
    data = header + question + rr
    assert hget._dns_parse_response(data, query_id) == "1.2.3.4"


def test_dns_resolve_localhost() -> None:
    assert hget.dns_resolve("localhost") == "127.0.0.1"


# ---------------------------------------------------------------------------
# Test de integración (servidor real)
# ---------------------------------------------------------------------------


@pytest.mark.integration
def test_download_integration_servidor_real(tmp_path: Path) -> None:
    """
    Arranca servidor_lab0.py en un subproceso, descarga con hget y comprueba
    el contenido. Excluir por defecto: pytest -m "not integration".
    """
    # Puerto libre
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("", 0))
        port = s.getsockname()[1]

    servidor_script = Path(__file__).resolve().parent / "servidor_lab0.py"
    proc = subprocess.Popen(
        [sys.executable, str(servidor_script), str(port)],
        cwd=servidor_script.parent,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    try:
        # Esperar a que el servidor escuche
        for _ in range(30):
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as c:
                    c.settimeout(0.3)
                    c.connect(("127.0.0.1", port))
                break
            except (OSError, socket.error):
                time.sleep(0.1)
        else:
            pytest.fail("El servidor no arrancó a tiempo")

        out_file = tmp_path / "downloaded.html"
        hget.download("http://localhost:%d/" % port, str(out_file))

        assert out_file.exists()
        content = out_file.read_text()
        assert "Lab0" in content and "OK" in content
    finally:
        proc.terminate()
        proc.wait(timeout=3)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
