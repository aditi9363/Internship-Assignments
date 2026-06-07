import socket
import time

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("localhost", 9000))

client.send("/name Alice".encode())
print(client.recv(1024).decode())

client.send("/join General".encode())
print(client.recv(1024).decode())

for i in range(1, 35):
    msg = f"/msg General A{i}"
    client.send(msg.encode())
    time.sleep(0.05)

print("Alice sent 34 messages")
input("Press Enter to close...")
client.close()