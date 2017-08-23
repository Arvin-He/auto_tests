
import ast
import gevent.socket

_SERVER_ADDRESS = ("127.0.0.1", 21000)

_client = gevent.socket.socket(gevent.socket.AF_INET, gevent.socket.SOCK_DGRAM)


def _eval(script, timeout=5):
    _client.sendto(b"EVAL\n" + script.encode(), _SERVER_ADDRESS)
    with gevent.Timeout(timeout):
        result, address = _client.recvfrom(65536)
    assert address == _SERVER_ADDRESS
    if not result.startswith(b"OK\n"):
        if result.startswith(b"ERROR\n"):
            result = result[6:].decode()
        raise RuntimeError(result)
    return ast.literal_eval(result[3:].decode())


def _exec(script, timeout=5):
    _client.sendto(b"EXEC\n" + script.encode(), _SERVER_ADDRESS)
    with gevent.Timeout(timeout):
        result, address = _client.recvfrom(65536)
    assert address == _SERVER_ADDRESS
    if result != b"OK":
        if result.startswith(b"ERROR\n"):
            result = result[6:].decode()
        raise RuntimeError(result)
