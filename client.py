import socket
import threading
import time
import server


def discover_new_server():
    udp_port = 5555

    discovery_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    discovery_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    discovery_socket.settimeout(20)

    try:
        discovery_socket.sendto(b"HELLO", ("<broadcast>", udp_port))

        servers = set()

        data, addr = discovery_socket.recvfrom(1024, 4)

        print(f"data received {data}")

        if data == b"SERVER":
            servers.add(addr[0])

        discovery_socket.close()

        if servers:
            return servers.pop()
        else:
            return None
    except Exception as e:
        print("Error during discovery:", e)
        return None


def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if not message:
                print("Lost connection to server. Attempting to become a server...")
                server.start_server()
                break
            print(f"Mensagem recebida: {message}")
        except ConnectionResetError:
            print("Lost connection to server. Attempting to become a server...")
            server.start_server()
            break
        except Exception as e:
            print("Error:", e)
            break


def start_client():
    server = discover_new_server()

    print(server, "Server")

    # if server is not None:



    # client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # server_ip = "192.168.1.3"
    # server_port = 5555
    #
    # try:
    #     client_socket.connect((server_ip, server_port))
    #     print("Conectado ao servidor. 🚀")
    #
    #     receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    #     receive_thread.start()
    #
    #     while True:
    #         time.sleep(2)
    #
    #         message = input("Digite uma mensagem: ")
    #         client_socket.send(message.encode())
    # except Exception as e:
    #     print("Erro:", e)
    #     client_socket.close()
