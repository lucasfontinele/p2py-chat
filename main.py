import sys
import server
import client

arguments = sys.argv

if len(arguments) > 1 and arguments[1] == "server":
    server.start_server()
else:
    client.start_client()

