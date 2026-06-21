import socket
import json
import random

MENU = [
    ("Burger", 200, 2),
    ("Pizza", 350, 3),
    ("Pasta", 250, 2),
    ("Fries", 100, 1)
]
items = []

for _ in range(random.randint(1, 3)):
    name, price, prep = random.choice(MENU)

    items.append({
        "name": name,
        "price": price,
        "prep_time": prep
    })

order = {
    "order_id": "TCP-120",
    "table_no": 8,
    "items": [
        {
            "item_id": "M001",
            "name": "Pasta",
            "category": "Main",
            "price": 250,
            "prep_time": 2
        }
    ]
}

client = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)
client.connect(("localhost", 5000))
client.sendall(
    json.dumps(order).encode()
)

response = client.recv(4096)

print("Raw Response:")
print("Decoded Response:", (response.decode()))

client.close()