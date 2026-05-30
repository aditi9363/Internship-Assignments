import socket 

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server.bind(("localhost", 9001))

print("Server started...")

while True:
    data, address = server.recvfrom(1024)

    print("Client Address:", address)
    print("Message:", data.decode())

    reply = "PONG"
    server.sendto(reply.encode(), address)