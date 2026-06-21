import json
import win32pipe
import win32file

PIPE_NAME = r'\\.\pipe\KitchenDisplay'

def create_kds_server(pipe_name=PIPE_NAME):
    """
    Create named pipe server
    """

    pipe = win32pipe.CreateNamedPipe(
        pipe_name,
        win32pipe.PIPE_ACCESS_DUPLEX,
        win32pipe.PIPE_TYPE_MESSAGE |
        win32pipe.PIPE_READMODE_MESSAGE |
        win32pipe.PIPE_WAIT,
        1,          # max instances
        65536,      # out buffer
        65536,      # in buffer
        0,
        None
    )

    print("KDS Server: Waiting for display connection...")
    win32pipe.ConnectNamedPipe(pipe, None)

    print("KDS Server: Display connected!")

    return pipe

def write_to_kds(pipe_handle, order):

    order_data = {
        "order_id": order.order_id,
        "table_no": order.table_no,
        "items": [item.name for item in order.items],
        "status": str(order.status)
    }

    message = json.dumps(order_data)

    result = win32file.WriteFile(
        pipe_handle,
        message.encode()
    )

    if result[0] == 0:
        print(f"KDS SENT: {order.order_id}") 
        
def kds_reader(pipe_name=PIPE_NAME):
    """
    KDS Client
    """

    print("KDS Display starting...")

    pipe = win32file.CreateFile(
        pipe_name,
        win32file.GENERIC_READ,
        0,
        None,
        win32file.OPEN_EXISTING,
        0,
        None
    )

    print("Connected to KDS Server")

    while True:
        try:
            result = win32file.ReadFile(pipe, 65536)

            data = result[1].decode()

            order = json.loads(data)

            print(
                f"\nORDER READY: {order['order_id']} "
                f"| Table {order['table_no']} "
                f"| Items: {order['items']}"
            )

        except Exception as e:
            print("KDS Error:", e)
            break

if __name__ == "__main__":
    kds_reader()