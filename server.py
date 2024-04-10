import socket
import threading

class Server:
    def __init__(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind(("0.0.0.0", 5555))
        self.server_socket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
        self.MCAST_GRP = '224.0.0.1'
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = {}

        self.clients = {}

    def remove_from_chat(self, client_name):
        del self.clients[client_name]
        self.broadcast(f"{client_name} saiu do chat.")

    def handle_client(self, message, client_address):
        client_name = client_address[0]
        if client_name not in self.clients:
            self.clients[client_name] = (client_name, None)  # For UDP, client_socket is not needed

        if not message:
            self.remove_from_chat(client_name)
            return

        if message == "HELLO":
            self.server_socket.sendto(b"SERVER", client_address)
        else:
            print(f"Mensagem recebida de {client_name}: {message}")
            self.broadcast(f"{client_name}: {message}", client_name)

    def broadcast(self, message, sender_name=None):
        for name, _ in self.clients.values():
            if name != sender_name:
                self.server_socket.sendto(f"{sender_name}: {message}".encode(), (self.MCAST_GRP, 5555))

    def start_server(self):
        self.socket.bind(('0.0.0.0', 5555))
        self.socket.listen()
        print("Servidor inicializado na porta 5555 🚀")

        while True:
            message, client_address = self.socket.accept()
            print("Nova conexão: ", client_address[0])

            client_thread = threading.Thread(target=self.handle_client, args=(message, client_address))
            client_thread.start()