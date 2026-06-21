import socket
import threading
import json
import models

from models import Order
from models import MenuItem

print(models.__file__)

def handle_client(conn, addr, order_queue):
    print(f"Connected from {addr}")
    try:
        data = conn.recv(4096)
        print("Received:", data)

        order_dict = json.loads(data.decode())
        print("Decoded:", order_dict)

        items = []

        for item in order_dict["items"]:
            import inspect
            print("MenuItem source:")
            print(inspect.signature(MenuItem))

            print("TCP item:", item)
            menu_item = MenuItem(
                item["item_id"],
                item["name"],
                item["category"],
                item["price"],
                item["prep_time"]
            )
               
            items.append(menu_item)

        print(
            f"Creating Order: "
            f"{order_dict['order_id']} "
            f"Table={order_dict['table_no']}" 
        )
        order = Order(
            order_dict["order_id"],
            order_dict["table_no"],
            items
        )
        order_queue.put(order)
        print(f"TCP Order Received: {order.order_id}")


        response = {
            "status": "accepted",
            "order_id": order.order_id
        }


        response_json = json.dumps(response)
        print("Sending:", response_json)
        conn.sendall(response_json.encode())
        print("Response sent successfully:")
    except Exception as e:
        print("Send error:", e)
    finally:
        conn.close()

def start_order_server(
        host,
        port,
        order_queue,
        shutdown_event
):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen()
    server.settimeout(1)

    print(f"TCP Server running on {host}:{port}")

    try:
        while not shutdown_event.is_set():
            try:
                conn, addr = server.accept()

                threading.Thread(
                    target=handle_client,
                    args=(conn, addr, order_queue),
                    daemon=True
                ).start()

            except socket.timeout:
                continue

    
    finally:
        server.close()
        print("TCP Server closed.")