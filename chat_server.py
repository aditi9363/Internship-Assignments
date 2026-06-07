import socket
import threading
import ctypes
import signal
import queue
from datetime import datetime
from rwlock import RWLock

SENTINEL = None

#Create users dictionary
users = {}
users_lock = threading.Lock()

class Room:
    def __init__(self, name):
        self.name = name
        self.members = []
        self.lock = threading.Lock()

        # Q12
        self.msg_queue = queue.Queue()

        # Q14
        self.condition = threading.Condition()

rooms_rwlock = RWLock()

rooms = {
    "General": Room("General"),
    "Tech": Room("Tech"),
    "Random": Room("Random")
}

startup_barrier = threading.Barrier(
    len(rooms) + 1
)

shutdown_event = threading.Event()

MAX_CLIENTS = 5
client_semaphore = threading.Semaphore(MAX_CLIENTS)

IDLE_TIMEOUT = 600

connected_clients = []
clients_lock = threading.Lock()

def signal_handler(signum, frame):
    print("\nServer shutting down...")
    log_event(
        "Server shutting down"
    )
    shutdown_event.set()
    with clients_lock:
        for client in connected_clients:
            print("Sending shutdown message")
            try:
                client.send(
                    "Server is shutting down. Goodbye.".encode()
                )
                print("Message sent")
            except Exception as e:
                print("Send fail:", e)
                pass

            try:
                client.close()
            except:
                pass

        for room in rooms.values():
            room.msg_queue.put(SENTINEL)
            with room.condition:
                room.condition.notify_all()

def broadcast_worker(room):
    print(f"{room.name} worker ready")
    startup_barrier.wait()
    print(f"{room.name} worker running")
    while not shutdown_event.is_set():
        with room.condition:
            while(
                room.msg_queue.empty()
                and not shutdown_event.is_set()
            ):
                room.condition.wait(timeout=1)
            if shutdown_event.is_set():
                break
            message = room.msg_queue.get()
        if message is SENTINEL:
            break
        log_event(
            f"Broadcast in {room.name}: {message}"
        )
        
        with room.lock:
            members_snapshot = list(
                room.members
            )
            disconnected = []
            for member in members_snapshot:
                try:
                    member.send(
                        message.encode()
                    )
                except Exception:
                    disconnected.append(
                        member
                    )
            
            for member in disconnected:
                if member in room.members:
                    room.members.remove(
                        member
                    )
            print(
                f"Broadcast worker stopped "
                f"for {room.name}"
            )
        
broadcast_workers = []
for room in rooms.values():
    worker = threading.Thread(
        target=broadcast_worker,
        args=(room,),
        daemon=True
    )
    worker.start()
    broadcast_workers.append(worker)
startup_barrier.wait()
print("All broadcast workers ready - server opening")

def kick_client(client_socket):
    print("IDLE TIMEOUT TRIGGERED")
    try:
        client_socket.send(
            "Disconnected: idle timeout".encode()
        )
    except:
        pass

    try:
        client_socket.close()
    except:
        pass

def log_event(message):
    mutex = ctypes.windll.kernel32.CreateMutexW(
        None,
        False,
        "ChatServerLog"
    )
    ctypes.windll.kernel32.WaitForSingleObject(
        mutex,
        0xFFFFFFFF
    )
    try:
        timestamp = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )
        
        with open(
            "server.log",
            "a",
            encoding="utf-8"
        ) as log_file:
            
            log_file.write(
                f"[{timestamp}] {message}\n"
            )

    finally:
        ctypes.windll.kernel32.ReleaseMutex(
            mutex
        )

def client_handler(client_socket, client_address):
    print(f"Client handler started for {client_address}")
    print(f"Active threads: {threading.active_count()}")

    current_timer = None
    try:
        joined_rooms = set()
        username = None

        current_timer = threading.Timer(
            IDLE_TIMEOUT,
            kick_client,
            args=[client_socket]
        )
        current_timer.start()
        print(f"Idle timer started for {client_address}")

        while True:
            data = client_socket.recv(1024)
            if not data:
                print(f"Client disconnected: {client_address}")
                log_event(f"Client disconnected: {client_address}")
                break

            message = data.decode()
            print(
                f"{datetime.now().strftime('%H:%M:%S')} "
                f"Message received: {message}"
            )

            current_timer.cancel()
            print(
                f"{datetime.now().strftime('%H:%M:%S')} "
                f"Old timer cancelled"
            )

            current_timer = threading.Timer(
                IDLE_TIMEOUT,
                kick_client,
                args=(client_socket,)
            )
            current_timer.start()
            print(
                f"{datetime.now().strftime('%H:%M:%S')}"
                f"New timer started"
            )
            #-----------------Name-----------------

            if message.startswith("/name "):
                username = message.split(maxsplit=1)[1]
                with users_lock:
                    users[username] = client_socket
                print(f"Username registered: {username}")
                client_socket.send(
                    f"Username set to {username}".encode()
                )
                continue

            #-----------------Join-------------------

            if message.startswith("/join "):
                room_name = message.split(maxsplit=1)[1]
                rooms_rwlock.acquire_read()

                try:
                    if room_name not in rooms:
                        client_socket.send(
                            f"Room '{room_name}' does not exist".encode()
                        )
                        continue
                    room = rooms[room_name]
                finally:
                    rooms_rwlock.release_read()
                with room.lock:
                    if client_socket not in room.members:
                        room.members.append(client_socket)
                joined_rooms.add(room_name)

                joined_rooms.add(room_name)
                log_event(
                    f"{username} joined room {room_name}"
                )
                client_socket.send(
                    f"You joined room: {room_name}".encode()
                )
                continue

            #------------Leave----------------

            if message.startswith("/leave"):
                room_name = message.split(maxsplit=1)[1]
                if room_name not in joined_rooms:
                    client_socket.send(
                        f"You are not in {room_name}".encode()
                    )
                    continue
                rooms_rwlock.acquire_read()

                try:
                    room = rooms[room_name]
                finally:
                    rooms_rwlock.release_read()
                with room.lock:
                    if client_socket in room.members:
                        room.members.remove(client_socket)

                joined_rooms.remove(room_name)
                log_event(
                    f"{username} left room {room_name}"
                )
                client_socket.send(
                    f"You left room: {room_name}".encode()
                )
                continue
            
            #---------------------Room-------------------------
            if message == "/rooms":
                rooms_rwlock.acquire_read()
                try:
                    room_info = ""
                    for room_name, room in rooms.items():
                        with room.lock:
                            count = len(room.members)
                        room_info += (
                            f"{room_name} : "
                            f"{count} members\n"
                        )
                finally:
                    rooms_rwlock.release_read()
                client_socket.send(
                    room_info.encode()
                )
                continue

            #--------------/msg<room><text>-----------------
            if message.startswith("/msg "):
                parts = message.split(maxsplit=2)
                if len(parts) < 3:
                    client_socket.send(
                        "Usage: /msg <room> <message>".encode()
                    )
                    continue

                room_name = parts[1]
                message_text = parts[2]

                #Check if client joined this room
                if room_name not in joined_rooms:
                    client_socket.send(
                        f"You are not in {room_name}".encode()
                    )
                    continue
                rooms_rwlock.acquire_read()

                try:
                    if room_name not in rooms:
                        client_socket.send(
                            "Room not found".encode()
                        )
                        continue
                    room = rooms[room_name]
                finally:
                    rooms_rwlock.release_read()

                log_event(
                    f"Room={room_name}, "
                    f"Sender={username}, "
                    f"Message={message_text[:50]}"
                )
                formatted_message = (
                    f"[{room_name}] "
                    f"{username}: "
                    f"{message_text}"
                )
                room.msg_queue.put(
                    formatted_message
                )

                with room.condition:
                    room.condition.notify()
                client_socket.send(
                    "Message queued".encode()
                )
                continue

            if message == "/quit":
                log_event(
                    f"{username} disconnected: quit"
                )

                current_timer.cancel()
                print(f"Client requested quit: "
                      f"{client_address}"
                )
                break

            #---------------Normal Message-----------------

            #Current timestamp
            current_time = datetime.now().strftime("%H:%M:%S")

            #Print on server console
            print(
                f"[{current_time}] "
                f"[{client_address}] "
                f"{message}"
            )

            #Echo back to client
            if current_room is None:
                client_socket.send(
                    "Join a room first using /join <room>".encode()
                )
                continue
            broadcast_message = (
                f"[{client_address}] {message}"
            )
        
            with current_room.lock:
                for member in current_room.members:
                    if member != client_socket:
                        member.send(
                            broadcast_message.encode()
                        )
        
    except OSError:
        print(
            f"Client timed out: "
            f"{client_address}"
        )
        
    except Exception as e:
        log_event(
            f"{client_address} disconnected: error ({e})"
        )
        print(f"Error with {client_address}:{e}")
    finally:
        try:
            if current_timer is not None:
                current_timer.cancel()
        except:
            pass

        #Remove client from all joined rooms
        for room_name in joined_rooms:
            rooms_rwlock.acquire_read()
            try:
                room = rooms[room_name]
            finally:
                rooms_rwlock.release_read()
            with room.lock:
                if client_socket in room.members:
                    room.members.remove(client_socket)

        client_socket.close()

        with clients_lock:
            if client_socket in connected_clients:
                connected_clients.remove(client_socket)
            print(f"Connected clients: "
                  f"{len(connected_clients)}"
            )
        
        #Released one time slot
        client_semaphore.release()

        print(f"Handler thread ended for {client_address}")
        print(f"Active threads: {threading.active_count()}")

def connection_acceptor(server_socket):
    print("Connection Acceptor Thread started")

    while not shutdown_event.is_set():
      try:
          client_socket, client_address = server_socket.accept()
      except socket.timeout:
          continue

      if not client_semaphore.acquire(blocking=False):
          print("Server full - rejecting client")
          client_socket.send("Server full - try again later".encode())
          continue
      
      with clients_lock:
          connected_clients.append(client_socket)
          print(f"Connected clients: {len(connected_clients)}")
      
      print(f"New client connected : {client_address}") 
      log_event(
          f"Client connected: {client_address}"
      )

      handler_thread = threading.Thread(
          target=client_handler,
          args=(client_socket, client_address)
      )
      handler_thread.start()

signal.signal(signal.SIGINT, signal_handler)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_socket.bind(("localhost", 9000))
server_socket.listen(1)
server_socket.settimeout(1)
print("Server started on localhost:9000")
log_event("Server started")

acceptor_thread = threading.Thread(
    target=connection_acceptor,
    args=(server_socket,)
)
acceptor_thread.start()
acceptor_thread.join()
for worker in broadcast_workers:
    worker.join()
    print(
        f"{worker.name} joined"
    )
    print(
        f"Active Threads: "
        f"{threading.active_count()}"
    )

server_socket.close()

