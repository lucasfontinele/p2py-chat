import socket
import threading


class P2PChatNode:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connections = {}
        self.is_server = False

    def handle_connection(self, client_socket, client_address):
        print(f"Nova conexão de {client_address}")
        while True:
            try:
                message = client_socket.recv(1024).decode()
                if not message:
                    print(f"{client_address} desconectado.")
                    client_socket.close()
                    del self.connections[client_address]
                    self.broadcast(f"{client_address} saiu do chat.")
                    break
                print(f"Mensagem recebida de {client_address}: {message}")
                self.broadcast(f"{client_address}: {message}", client_address)
            except Exception as e:
                print(f"Erro ao lidar com a conexão de {client_address}: {e}")
                break

    def broadcast(self, message, sender_address=None):
        for address, socket in self.connections.items():
            if address != sender_address:
                try:
                    socket.sendall(message.encode())
                except Exception as e:
                    print(f"Erro ao enviar mensagem para {address}: {e}")
                    del self.connections[address]

    def start_server(self):
        self.server_socket.bind((self.ip, self.port))
        self.server_socket.listen()
        print(f"Node {self.ip}:{self.port} iniciado e escutando...")
        while True:
            client_socket, client_address = self.server_socket.accept()
            self.connections[client_address] = client_socket
            threading.Thread(target=self.handle_connection, args=(client_socket, client_address)).start()

    def connect_to_peer(self, peer_ip, peer_port):
        try:
            peer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            peer_socket.connect((peer_ip, peer_port))
            self.connections[(peer_ip, peer_port)] = peer_socket
            threading.Thread(target=self.handle_connection, args=(peer_socket, (peer_ip, peer_port))).start()
            print(f"Conectado ao peer {peer_ip}:{peer_port}")
        except Exception as e:
            print(f"Erro ao conectar ao peer {peer_ip}:{peer_port}: {e}")

    def check_for_server(self):
        try:
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.settimeout(2)
            server_socket.connect((self.ip, self.port))
            server_socket.close()
            return True
        except Exception as e:
            return False

    def start(self):
        if self.check_for_server():
            print("Servidor encontrado na rede.")
            self.connect_to_peer(self.ip, self.port)
        else:
            print("Nenhum servidor encontrado na rede. Este nó será o servidor.")
            self.is_server = True
            self.start_server()

    def send_message(self, message):
        if self.is_server:
            self.broadcast(f"Server: {message}")
        else:
            for socket in self.connections.values():
                try:
                    socket.sendall(f"{self.ip}:{self.port}: {message}".encode())
                except Exception as e:
                    print(f"Erro ao enviar mensagem para {address}: {e}")
                    del self.connections[address]


if __name__ == "__main__":
    node = P2PChatNode("127.0.0.1", 5000)
    node.start()

    while True:
        message = input("Digite uma mensagem: ")
        node.send_message(message)