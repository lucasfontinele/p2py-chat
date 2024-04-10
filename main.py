import sys
from server import Server
import client

arguments = sys.argv

try:
    if len(arguments) > 1 and arguments[1] == "server":
        _server = Server()
        _server.start_server()
    else:
        client.start_client()
except KeyboardInterrupt:
    print("Desconectado")

