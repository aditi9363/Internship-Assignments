from multiprocessing import shared_memory
from datetime import datetime
import win32event

shm = shared_memory.SharedMemory(
    name="AppSharedMem",
    create=True,
    size=256
)

mutex = win32event.CreateMutex(
    None,
    False,
    "AppMutex"
)

win32event.WaitForSingleObject(
    mutex,
    win32event.INFINITE
)

message = str(datetime.now())

shm.buf[:len(message)] = message.encode()
print("Timestamp written:", message)

win32event.ReleaseMutex(mutex)
input("Run reader first, then press Enter...")

shm.close()
shm.unlink()
print("Shared memory deleted.")