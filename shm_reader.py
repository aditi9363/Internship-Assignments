from multiprocessing import shared_memory
import win32event

shm = shared_memory.SharedMemory(
    name="AppSharedMem"
)

mutex = win32event.OpenMutex(
    0x1F0001,
    False,
    "AppMutex"
)

win32event.WaitForSingleObject(
    mutex,
    win32event.INFINITE
)
message = bytes(shm.buf[:256]).decode().strip('\x00')

print("Timestamp read:", message)

win32event.ReleaseMutex(mutex)
shm.close()