import socket
import threading


class Server:
    def __init__(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = {}

    def remove_from_chat(self, client_socket, client_name):
        del self.clients[client_name]
        client_socket.close()
        self.broadcast(f"{client_name} saiu do chat.")

    def handle_client(self, client_socket, client_address):
        client_name = client_address[0]
        self.clients[client_name] = (client_name, client_socket)

        while True:
            try:
                message = client_socket.recv(1024).decode()

                if not message:
                    self.remove_from_chat(client_socket, client_name)
                    break

                if message == "HELLO":
                    client_socket.send(b"SERVER")
                else:
                    print(f"Mensagem recebida de {client_name}: {message}")
                    self.broadcast(f"{client_name}: {message}", client_name)

            except Exception as e:
                print("Erro:", e)
                self.remove_from_chat(client_socket, client_name)
                break

    def broadcast(self, message, sender_socket=None):
        sender_name = None
        if sender_socket:
            sender_name = self.clients[sender_socket][0]
        for client_socket, (name, _) in self.clients.items():
            if client_socket != sender_socket:
                try:
                    client_socket.send(f"{sender_name}: {message}".encode())
                except:
                    self.remove_from_chat(client_socket, name)

    def start_server(self):
        self.server_socket.bind(('0.0.0.0', 5555))
        self.server_socket.listen()
        print("Servidor inicializado na porta 5555 🚀")

        while True:
            client_socket, client_address = self.server_socket.accept()
            print("Nova conexão: ", client_address[0])

            client_handler = threading.Thread(target=self.handle_client, args=(client_socket, client_address))
            client_handler.start()
