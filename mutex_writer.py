import ctypes
mutex = ctypes.windll.kernel32.CreateMutexW(None, False, "MyMutex")
print("Writer waiting...")

ctypes.windll.kernel32.WaitForSingleObject(mutex, -1)
print("Writer started writing")

with open("data.txt", "a") as file:
    file.write("Hello from writer\n")

print("Writing completed")

ctypes.windll.kernel32.ReleaseMutex(mutex)
print("Writer released mutex")