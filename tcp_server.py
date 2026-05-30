import socket

server = socket.socket()
server.bind(("localhost", 9000))
server.listen(1)

print("Server is waiting for connection...")

client, addr = server.accept()

msg = client.recv(1024).decode()

msg = msg.upper()

client.send(msg.encode())

client.close()
server.close()