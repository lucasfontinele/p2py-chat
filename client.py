import socket
import threading


def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode()
            print(message)
        except Exception as e:
            print("Error:", e)
            break


def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_ip = input("Enter server IP: ")
    server_port = 5555

    try:
        client_socket.connect((server_ip, server_port))
        print("Connected to server.")

        receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
        receive_thread.start()

        while True:
            message = input()
            client_socket.send(message.encode())
    except Exception as e:
        print("Error:", e)
        client_socket.close()


start_client()