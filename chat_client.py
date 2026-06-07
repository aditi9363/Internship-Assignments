import socket
import threading

HOST = "localhost"
PORT = 9000
def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if not message:
                break
            print(f"\nServer: {message}")

        except:
            break

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(("localhost", 9000))

receiver_thread = threading.Thread(
    target=receive_messages,
    args=(client_socket,),
    daemon=True
)
receiver_thread.start()

print("Connected to server")
print("Type /quit to exit")

while True:
    message = input("You: ")

    client_socket.send(message.encode())
    if message == "/quit":
        break
    
client_socket.close()
