import socket
import threading

def receive_messages():
    while True:
        try:
            message = client.recv(1024).decode()
            print(message)
        except:
            break

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("localhost", 9000))
print("Connected to server")

thread = threading.Thread(target=receive_messages)
thread.start()

while True:
    message = input("You: ")
    client.send(message.encode())