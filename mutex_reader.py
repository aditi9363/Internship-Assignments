import ctypes
mutex = ctypes.windll.kernel32.CreateMutexW(None, False, "MyMutex")
print("Reader Waiting...")

ctypes.windll.kernel32.WaitForSingleObject(mutex, -1)
print("Reader started reading")

try:
    with open("data.txt", "r") as file:
        print(file.read())
except FileNotFoundError:
    print("File not found")
print("Reading completed")

ctypes.windll.kernel32.ReleaseMutex(mutex)
print("Reader released mutex")        