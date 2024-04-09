import socket
import threading


def handle_client(client_socket, clients):
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if not message:
                clients.remove(client_socket)
                client_socket.close()
                break
            print("Mensagem recebida:", message)
            broadcast(message, client_socket, clients)
        except Exception as e:
            print("Erro:", e)
            clients.remove(client_socket)
            client_socket.close()
            break


def broadcast(message, sender_socket, clients):
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message.encode())
            except:
                clients.remove(client)
                client.close()


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


start_server()
