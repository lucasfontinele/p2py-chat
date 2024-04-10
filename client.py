import socket
import threading
import time
import server


def discover_server():
    multicast_group = '224.0.0.1'
    port = 5555
    message = b"HELLO"

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.settimeout(2)

    try:
        client_socket.sendto(message, (multicast_group, port))

        servers = set()

        while True:
            try:
                data, addr = client_socket.recvfrom(1024)
                servers.add(addr[0])
            except socket.timeout:
                break

        client_socket.close()

        return servers.pop() if servers else None
    except Exception as e:
        print("Error during server discovery:", e)
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
    found_server = discover_server()

    # if found_server is None:
    #     raise Exception("Nenhum servidor encontrado")
    time.sleep(5)


    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_ip = str(found_server)
    server_port = 5555
    
    try:
        client_socket.connect((server_ip, server_port))
        print("Conectado ao servidor. 🚀")

        receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
        receive_thread.start()

        while True:
            time.sleep(2)

            message = input("Digite uma mensagem: ")
            client_socket.send(message.encode())
    except Exception as e:
        print("Erro:", e)
        client_socket.close()
