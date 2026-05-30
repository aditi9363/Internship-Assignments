import socket
import time
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ("localhost", 9001)
for i in range(1, 6):
    message = f"PING {i}"
    start = time.time()
    client.sendto(message.encode(), server_address)
    data, address = client.recvfrom(1024)
    end = time.time()
    latency = (end - start) * 1000

    print("Sent:", message)
    print("Reply:", data.decode())
    print("Latency:", round(latency, 2), "ms")
    print()
client.close()