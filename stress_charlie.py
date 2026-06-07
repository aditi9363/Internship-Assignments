import socket
import time

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("localhost", 9000))

client.send("/name Charlie".encode())
print(client.recv(1024).decode())

client.send("/join General".encode())
print(client.recv(1024).decode())

for i in range(1, 34):
    msg = f"/msg General C{i}"
    client.send(msg.encode())
    time.sleep(0.05)

print("Charlie sent 33 messages")
input("Press Enter to close...")
client.close()
