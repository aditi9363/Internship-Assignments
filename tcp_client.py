import socket

client = socket.socket()

client.connect(("localhost", 9000))

msg = input("Enter message")

client.send(msg.encode())

reply = client.recv(1024).decode()

print("Server replied:", reply)

client.close()