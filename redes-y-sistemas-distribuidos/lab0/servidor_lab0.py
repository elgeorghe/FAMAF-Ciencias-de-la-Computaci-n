#!/usr/bin/env python
# encoding: utf-8
"""
Servidor HTTP mínimo para probar el cliente hget (Laboratorio 0).

Solo librería estándar de Python. Uso: ejecutar en una terminal y en otra
ejecutar hget contra http://localhost:8080/ (o el puerto indicado).

  python3 servidor_lab0.py [puerto]

Este script es únicamente para pruebas locales; el cliente hget debe
implementarse con sockets crudos y no usar este módulo.
"""
from __future__ import annotations

import sys
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse

PUERTO_POR_DEFECTO: int = 8080


class Handler(BaseHTTPRequestHandler):
    protocol_version: str = "HTTP/1.0"

    def do_GET(self) -> None:
        host = self.headers.get("Host", "(no enviado)")
        sys.stderr.write("Host recibido: %s\n" % host)

        query = parse_qs(urlparse(self.path).query)
        status_param = query.get("status", [None])[0]
        if status_param == "404":
            self.send_response(404)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(b"<html><body><h1>404 Not Found</h1></body></html>")
            return
        if status_param == "301":
            self.send_response(301)
            self.send_header("Location", "http://localhost:%d/" % self.server.server_port)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(b"<html><body><h1>301 Moved</h1></body></html>")
            return

        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(b"<html><body><h1>Lab0</h1><p>OK</p></body></html>")

    def log_message(self, format: str, *args: object) -> None:
        sys.stderr.write("%s - %s\n" % (self.log_date_time_string(), format % args))


def main() -> None:
    port = PUERTO_POR_DEFECTO
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    server = HTTPServer(("", port), Handler)
    sys.stderr.write("Servidor HTTP en http://localhost:%d/\n" % port)
    sys.stderr.write("Ejecute en otra terminal: python3 hget.py http://localhost:%d/\n" % port)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    server.server_close()


if __name__ == "__main__":
    main()
