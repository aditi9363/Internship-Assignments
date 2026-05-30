import socket
import threading

clients = []

def send_to_all(message):
    for client in clients:
        client.send(message)

def handle_client(client):
    while True:
        try:
            message = client.recv(1024)

            if not message:
                break
            print("Message:", message.decode())
            send_to_all(message)
        except:
            break
    clients.remove(client)
    client.close()
    print("A client disconnected")

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("localhost", 9000))
server.listen()
print("Server started...")

while True:
    client, address = server.accept()
    print("Connected:", address)
    clients.append(client)

    thread = threading.Thread(target=handle_client, args=(client,))
    thread.start()
