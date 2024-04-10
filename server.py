import socket
import threading


def handle_client(client_socket, clients, client_address):
    client_name = client_socket.recv(1024).decode()  # Recebe o nome do cliente
    clients[client_socket] = client_name  # Adiciona o cliente à lista de clientes conectados
    print(f"{client_name} ({client_address}) conectado ao servidor.")

    while True:
        try:
            message = client_socket.recv(1024).decode()
            if not message:
                del clients[client_socket]  # Remove o cliente da lista quando ele desconectar
                client_socket.close()
                broadcast(f"{client_name} saiu do chat.", clients)
                break
            print(f"Mensagem recebida de {client_name}: {message}")
            broadcast(f"{client_name}: {message}", clients, sender_socket=client_socket)
        except Exception as e:
            print("Erro:", e)
            del clients[client_socket]
            client_socket.close()
            broadcast(f"{client_name} saiu do chat.", clients)
            break


def broadcast(message, clients, sender_socket):
    sender_name = clients[sender_socket]
    for client_socket, name in clients.items():
        if client_socket != sender_socket:
            try:
                client_socket.send(f"{sender_name}: {message}".encode())
            except:
                del clients[client_socket]
                client_socket.close()
                broadcast(f"{name} saiu do chat.", clients)


def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 5555))
    server_socket.listen(5)
    print("Servidor inicializado na porta 5555 🚀")

    clients = []

    while True:
        client_socket, addr = server_socket.accept()
        clients.append(client_socket)
        print("Nova conexão:", addr)

        client_handler = threading.Thread(target=handle_client, args=(client_socket, clients))
        client_handler.start()
