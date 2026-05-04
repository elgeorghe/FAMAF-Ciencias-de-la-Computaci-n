#!/usr/bin/env python
# encoding: utf-8
"""
hget: un cliente HTTP simple

Escrito con fines didacticos por la catedra de
Redes y Sistemas Distribuidos,
FaMAF-UNC

El proposito de este codigo es mostrar con un ejemplo concreto las primitivas
basicas de comunicacion por sockets; no es para uso en produccion (para eso
esta el modulo urllib de la biblioteca estandar de python que contiene un
cliente HTTP mucho mas completo y correcto.
Revision 2019 (a Python 3): Pablo Ventura
Revision 2011: Eduardo Sanchez
Original 2009-2010: Natalia Bidart, Daniel Moisset

Constantes del modulo:

>>> PREFIX
'http://'
>>> HTTP_PORT
80
>>> HTTP_OK
'200'
>>> DNS_SERVER
'9.9.9.9'
>>> DNS_PORT
53
"""

from __future__ import annotations

import argparse
import random
import socket
import sys
import struct
from typing import Protocol

PREFIX: str = "http://"
HTTP_PORT: int = 80   # El puerto por convencion para HTTP,
# según http://tools.ietf.org/html/rfc1700
HTTP_OK: str = "200"  # El codigo esperado para respuesta exitosa.

# Cliente DNS: servidor Quad9 (9.9.9.9), puerto 53 (UDP)
DNS_SERVER: str = "9.9.9.9"
DNS_PORT: int = 53


class SocketLike(Protocol):
    """Protocolo para objetos con interfaz tipo socket (recv, send)."""

    def send(self, data: bytes) -> int:
        ...

    def recv(self, bufsize: int) -> bytes:
        ...


def parse_server(url: str) -> str:
    """
    Obtiene el server de una URL. Por ejemplo, si recibe como input
    "http://www.famaf.unc.edu.ar/carreras/computacion/computacion.html"
    devuelve "www.famaf.unc.edu.ar"

    Precondicion: url es un str, comienza con PREFIX
    Postcondicion: url comienza con PREFIX + resultado,
        '/' not in resultado, resultado es la cadena mas larga posible que cumple lo anterior

    >>> parse_server('http://docs.python.org/library/intro.html')
    'docs.python.org'
    >>> parse_server('http://google.com')
    'google.com'
    >>> parse_server('http://localhost:8080/')
    'localhost'
    >>> parse_server('http://a.b.c:9999/path/to/resource')
    'a.b.c'
    >>> parse_server('http://ejemplo.com/')
    'ejemplo.com'
    >>> parse_server('http://solo.host')
    'solo.host'
    >>> parse_server('http://1.2.3.4:80/')  # IP como hostname
    '1.2.3.4'
    >>> parse_server('google.com')  # Falta el prefijo, deberia fallar
    Traceback (most recent call last):
       ...
    AssertionError
    """
    assert url.startswith(PREFIX)
    # Removemos el prefijo:
    path = url[len(PREFIX):]
    path_elements = path.split('/')
    result = path_elements[0]
    # Si la URL incluye puerto (ej. http://localhost:8080/), solo el hostname
    if ':' in result:
        result = result.split(':', 1)[0]

    assert url.startswith(PREFIX + path_elements[0])
    assert '/' not in result

    return result


def parse_port(url: str) -> int:
    """
    Obtiene el puerto de una URL. Si no se indica puerto, devuelve HTTP_PORT.

    >>> parse_port('http://localhost:8080/')
    8080
    >>> parse_port('http://www.ejemplo.com/')
    80
    >>> parse_port('http://host:443/')
    443
    >>> parse_port('http://host:3128/path')
    3128
    >>> parse_port('http://host/')
    80
    >>> parse_port('http://host/sin/puerto')
    80
    """
    assert url.startswith(PREFIX)
    path = url[len(PREFIX):]
    segment = path.split('/')[0]
    if ':' in segment:
        return int(segment.split(':', 1)[1])
    return HTTP_PORT


def _dns_encode_name(hostname: str) -> bytes:
    """Codifica un hostname en formato QNAME (RFC 1035): etiquetas length+bytes.

    >>> _dns_encode_name('localhost')[:1] == b'\\x09'  # len('localhost')=9
    True
    >>> _dns_encode_name('a') == b'\\x01a\\x00'
    True
    >>> _dns_encode_name('a.b') == b'\\x01a\\x01b\\x00'
    True
    >>> _dns_encode_name('ejemplo.com.') == _dns_encode_name('ejemplo.com')
    True
    >>> _dns_encode_name('x.y.z').endswith(b'\\x00')
    True
    """
    parts = hostname.strip().rstrip('.').split('.')
    buf = bytearray()
    for part in parts:
        if part:
            buf.append(len(part))
            buf.extend(part.encode('ascii'))
    buf.append(0)
    return bytes(buf)


def _dns_build_query(hostname: str, query_id: int) -> bytes:
    """Construye un mensaje de consulta DNS tipo A (RFC 1035).

    >>> q = _dns_build_query('a.b', 12345)
    >>> len(q) >= 12  # header 12 bytes + question
    True
    >>> q[0:2] == (12345).to_bytes(2, 'big')
    True
    >>> q[2:4] == b'\\x01\\x00'  # RD=1
    True
    >>> _dns_build_query('x', 0)[:2] == b'\\x00\\x00'
    True
    """
    # Header: ID, FLAGS (0x0100 = recursion desired), counts
    header = struct.pack(
        ">HHHHHH",
        query_id,
        0x0100,  # Standard query, RD=1
        1, 0, 0, 0   # QDCOUNT=1, ANCOUNT, NSCOUNT, ARCOUNT=0
    )
    qname = _dns_encode_name(hostname)
    # QTYPE A=1, QCLASS IN=1
    question = qname + struct.pack(">HH", 1, 1)
    return header + question


def _dns_skip_name(data: bytes, pos: int) -> int:
    """Avanza pos sobre un nombre DNS (puede ser comprimido por puntero).

    >>> _dns_skip_name(b'\\x00', 0)
    1
    >>> _dns_skip_name(b'\\x03foo\\x00', 0)
    5
    >>> _dns_skip_name(b'\\x01a\\x01b\\x00', 0)
    5
    >>> _dns_skip_name(b'\\x01a\\x00', 0)
    3
    """
    while pos < len(data):
        if data[pos] & 0xC0:
            return pos + 2  # Puntero de compresion
        length = data[pos]
        if length == 0:
            return pos + 1
        pos += 1 + length
    return pos


def _dns_parse_one_rr(data: bytes, pos: int) -> tuple[str | None, int]:
    """Si el RR en pos es tipo A, devuelve (ip_str, pos_siguiente); si no, (None, pos_siguiente)."""
    if pos + 2 > len(data):
        return (None, pos)
    pos = _dns_skip_name(data, pos)
    if pos + 10 > len(data):
        return (None, pos)
    rtype, _rclass, _ttl, rdlength = struct.unpack(">HHIH", data[pos:pos+10])
    pos += 10
    if pos + rdlength > len(data):
        return (None, pos)
    if rtype == 1 and rdlength == 4:  # A record
        ip = data[pos:pos+4]
        return ("%d.%d.%d.%d" % (ip[0], ip[1], ip[2], ip[3]), pos + rdlength)
    return (None, pos + rdlength)


def _dns_parse_response(data: bytes, query_id: int) -> str:
    """Extrae la primera direccion A de la respuesta DNS. Raises gaierror si falla.

    >>> _dns_parse_response(bytes(12) + b'\\x00\\x00\\x01\\x00', 0)  # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
       ...
    gaierror: ...
    >>> _dns_parse_response(b'\\x00' * 11, 0)  # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
       ...
    gaierror: ...
    """
    if len(data) < 12:
        raise socket.gaierror(socket.EAI_NODATA, "Respuesta DNS demasiado corta")
    resp_id, flags = struct.unpack(">HH", data[0:4])
    if resp_id != query_id:
        raise socket.gaierror(socket.EAI_FAIL, "ID de respuesta DNS no coincide")
    if not (flags & 0x8000):  # QR bit
        raise socket.gaierror(socket.EAI_FAIL, "No es una respuesta DNS")
    rcode = flags & 0x000F
    if rcode != 0:
        raise socket.gaierror(socket.EAI_FAIL, "DNS RCODE %d" % rcode)
    ancount = struct.unpack(">H", data[6:8])[0]
    if ancount == 0:
        raise socket.gaierror(socket.EAI_NODATA, "Sin registros A en la respuesta")
    pos = 12
    pos = _dns_skip_name(data, pos)
    pos += 4  # QTYPE, QCLASS
    for _ in range(ancount):
        ip_str, pos = _dns_parse_one_rr(data, pos)
        if ip_str is not None:
            return ip_str
    raise socket.gaierror(socket.EAI_NODATA, "Sin registro A en la respuesta")


def dns_resolve(hostname: str) -> str:
    """
    Resuelve el hostname a una direccion IPv4 usando un cliente DNS por UDP.

    Se envia una consulta tipo A al servidor DNS de Quad9 (9.9.9.9) por UDP
    y se parsea la respuesta. No se permite usar socket.gethostbyname().

    Precondicion: hostname es un str (nombre de dominio o 'localhost').
    Postcondicion: devuelve una cadena 'x.y.z.w' con la IPv4.

    Para 'localhost' se devuelve '127.0.0.1' sin consultar DNS.

    >>> dns_resolve('localhost')
    '127.0.0.1'
    >>> dns_resolve('www.famaf.unc.edu.ar')  # doctest: +ELLIPSIS
    '...'
    """
    if hostname == 'localhost':
        return '127.0.0.1'
    # Pasos sugeridos (RFC 1035, consulta tipo A):
    # 1. Generar un query_id aleatorio (p. ej. random.randint) para asociar respuesta con consulta.
    # 2. Construir el mensaje de consulta con _dns_build_query(hostname, query_id).
    # 3. Crear socket UDP (AF_INET, SOCK_DGRAM), settimeout razonable, sendto(query, (DNS_SERVER, DNS_PORT)), recvfrom(512).
    # 4. Cerrar el socket y devolver _dns_parse_response(data, query_id) que extrae la IP del primer registro A.
    raise NotImplementedError("Implementar cliente DNS (UDP, Quad9 9.9.9.9, RFC 1035).")


def connect_to_server(server_name: str, port: int = HTTP_PORT) -> socket.socket:
    """
    Se conecta al servidor llamado server_name en el puerto indicado.

    Devuelve el socket conectado en caso de exito, o falla con una excepcion
    de socket.connect o de dns_resolve (gaierror si falla la resolucion DNS).

    >>> type(connect_to_server('www.famaf.unc.edu.ar')) # doctest: +ELLIPSIS
    <class 'socket.socket'>

    >>> connect_to_server('no.exis.te') # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
       ...
    gaierror: [Errno -5] No address associated with hostname

    >>> connect_to_server('localhost')
    Traceback (most recent call last):
       ...
    ConnectionRefusedError: [Errno 111] Connection refused
    """
    ip_user = dns_resolve(server_name)
    sys.stderr.write("Hostname: %s\n" % server_name)
    sys.stderr.write("IP resuelta: %s\n" % ip_user)
    socket_user = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_user.settimeout(10)
    socket_user.connect((ip_user, port))
    return socket_user
    # Obtener la direccion IP del servidor con el cliente DNS (UDP, Quad9 9.9.9.9)
    # COMPLETAR: implementar resolucion usando dns_resolve(server_name)
    # PROHIBIDO usar socket.gethostbyname()
    # Paso 1: resolver el nombre con dns_resolve(server_name) y guardar la IP en una variable.
    # Paso 2: imprimir en stderr "Hostname: ..." e "IP resuelta: ..." (el enunciado lo exige).
    # Paso 3: crear socket TCP (AF_INET, SOCK_STREAM), opcional settimeout, connect((ip_address, port)), devolver el socket.
    ...
    # NO MODIFICAR POR FUERA DE ESTA FUNCION


def send_request(connection: SocketLike, url: str) -> None:
    """
    Envia por 'connection' un pedido HTTP de la URL dada (incluye header Host).

    Precondicion:
        connection es valido y esta conectado
        url.startswith(PREFIX)

    >>> class FakeConn:
    ...   def __init__(self):
    ...     self.sent = b''
    ...   def recv(self, n): return b''
    ...   def send(self, d): self.sent += d; return len(d)
    >>> c = FakeConn()
    >>> send_request(c, 'http://host/path')
    >>> c.sent == b'GET http://host/path HTTP/1.0\\r\\nHost: host\\r\\n\\r\\n'
    True
    >>> c2 = FakeConn()
    >>> send_request(c2, 'http://a.b/')
    >>> c2.sent.startswith(b'GET ')
    True
    >>> c2.sent.endswith(b'\\r\\n\\r\\n')
    True
    """
    host = parse_server(url)
    request_lines = "GET %s HTTP/1.0\r\nHost: %s\r\n\r\n" % (url, host)
    request_bytes = request_lines.encode()
    sys.stderr.write("Request enviada:\n%s---\n" % request_lines)
    connection.send(request_bytes)


def _read_until_newline_or_end(connection: SocketLike) -> tuple[bytes, bool]:
    """Lee bytes hasta '\\n' o fin; devuelve (bytes_leidos, hubo_error)."""
    result = b''
    error = False
    try:
        data = connection.recv(1)
    except Exception:
        error = True
        data = b''
    while not error and data != b'' and data != b'\n':
        result = result + data
        try:
            data = connection.recv(1)
        except Exception:
            error = True
            data = b''
    result += data
    return (result, error)


def read_line(connection: SocketLike) -> bytes:
    """
    Devuelve una linea leida desde 'connection`; hasta el siguiente '\\n'
    (incluido), o hasta que se terminen los datos.

    Si se produce un error, genera una excepcion.

    >>> class FakeConn:
    ...   def __init__(self, chunks):
    ...     self.chunks = iter(chunks)
    ...   def recv(self, n):
    ...     return next(self.chunks, b'')
    ...   def send(self, d): return len(d)
    >>> c = FakeConn([b'A', b'B', b'C', b'\\n'])
    >>> read_line(c)
    b'ABC\\n'
    >>> c2 = FakeConn([b'HTTP/1.0 200 OK', b'\\r', b'\\n'])
    >>> read_line(c2)
    b'HTTP/1.0 200 OK\\r\\n'
    >>> read_line(FakeConn([b'x']))
    b'x'
    >>> read_line(FakeConn([b'\\n']))
    b'\\n'
    """
    result, error = _read_until_newline_or_end(connection)
    if error:
        raise Exception("Error leyendo de la conexion!")
    return result


def check_http_response(header: bytes) -> bool:
    """
    Verifica que el encabezado de la respuesta este bien formado e indique
    éxito. Un encabezado de respuesta HTTP tiene la forma

    HTTP/<version> <codigo> <mensaje>

    Donde version tipicamente es 1.0 o 1.1, el codigo para exito es 200,
    y el mensaje es opcional y libre pero suele ser una descripcion del
    codigo.

    >>> check_http_response(b"HTTP/1.1 200 Ok")
    True
    >>> check_http_response(b"HTTP/1.1 200")
    True
    >>> check_http_response(b"HTTP/1.0 200 OK")
    True
    >>> check_http_response(b"HTTP/1.0 200 ")
    True
    >>> check_http_response(b"HTTP/1.1 301 Permanent Redirect")
    False
    >>> check_http_response(b"HTTP/1.1 404 Not Found")
    False
    >>> check_http_response(b"HTTP/1.1 500 Internal Server Error")
    False
    >>> check_http_response(b"Malformed")
    False
    >>> check_http_response(b"")
    False
    >>> check_http_response(b"200 HTTP/1.1")
    False
    >>> check_http_response(b"HTTP/1.1")
    False
    """
    header = header.decode()
    elements = header.split(' ', 3)
    return (len(elements) >= 2 and elements[0].startswith("HTTP/")
            and elements[1] == HTTP_OK)


def get_response(connection: SocketLike, filename: str) -> bool:
    """
    Recibe de `connection' una respuesta HTTP, y si es valida la descarga
    en un archivo llamado `filename'.

    Devuelve True en caso de éxito, False en caso contrario.

    >>> import tempfile
    >>> class FakeConn:
    ...   def __init__(self, data):
    ...     self.buf = bytes(data)
    ...     self.pos = 0
    ...   def recv(self, n):
    ...     start = self.pos
    ...     self.pos = min(self.pos + n, len(self.buf))
    ...     return self.buf[start:self.pos]
    ...   def send(self, d): return len(d)
    >>> body = b"contenido del body"
    >>> raw = b"HTTP/1.0 200 OK\\r\\nX-Foo: bar\\r\\n\\r\\n" + body
    >>> with tempfile.NamedTemporaryFile(delete=False, suffix='.tmp') as f:
    ...     tmp = f.name
    >>> get_response(FakeConn(raw), tmp)
    True
    >>> open(tmp, 'rb').read() == body
    True
    >>> import os; os.remove(tmp)
    """
    BUFFER_SIZE = 4096

    # Status line
    header = read_line(connection)
    sys.stderr.write("Status line: %s" % header.decode())
    if not check_http_response(header):
        sys.stdout.write("Encabezado HTTP malformado: '%s'\n" % header.strip())
        return False
    else:
        # Leer y mostrar cada header hasta la linea en blanco
        sys.stderr.write("Headers:\n")
        line = read_line(connection)
        while line != b'\r\n' and line != b'':
            sys.stderr.write(line.decode())
            line = read_line(connection)
        sys.stderr.write("---\n")
        sys.stderr.write("Body: guardado en %s\n" % filename)

        # Descargar el body al archivo
        with open(filename, "wb") as output:
            data = connection.recv(BUFFER_SIZE)
            while data != b'':
                output.write(data)
                data = connection.recv(BUFFER_SIZE)
        return True


def download(url: str, filename: str) -> None:
    """
    Descarga por http datos desde `url` y los guarda en un nuevo archivo
    llamado `filename`
    """
    # Obtener server
    server = parse_server(url)
    sys.stderr.write("Contactando servidor '%s'...\n" % server)

    port = parse_port(url)
    try:
        connection = connect_to_server(server, port)
    except socket.gaierror:
        sys.stderr.write("No se encontro la direccion '%s'\n" % server)
        sys.exit(1)
    except socket.error:
        sys.stderr.write("No se pudo conectar al servidor HTTP en '%s:%d'\n"
                         % (server, port))
        sys.exit(1)

    # Enviar pedido, recibir respuesta
    try:
        sys.stderr.write("Enviando pedido...\n")
        send_request(connection, url)
        sys.stderr.write("Esperando respuesta...\n")
        result = get_response(connection, filename)
        if not result:
            sys.stderr.write("No se pudieron descargar los datos\n")
    except Exception:
        sys.stderr.write("Error al comunicarse con el servidor\n")
        # Descomentar la siguiente línea para debugging:
        # raise
        sys.exit(1)


def main() -> None:
    """Procesa los argumentos, y llama a download()"""
    parser = argparse.ArgumentParser(description="Cliente HTTP simple (hget).")
    parser.add_argument(
        "-o", "--output",
        default="download.html",
        help="Archivo de salida",
    )
    parser.add_argument("url", nargs="?", help="URL http:// a descargar")
    args = parser.parse_args()
    if args.url is None:
        sys.stderr.write("No se indico una URL a descargar\n")
        parser.print_help()
        sys.exit(1)

    url = args.url
    if not url.startswith(PREFIX):
        sys.stderr.write("La direccion '%s' no comienza con '%s'\n" % (url,
                                                                       PREFIX))
        sys.exit(1)

    download(url, args.output)


if __name__ == "__main__":
    main()
    sys.exit(0)
