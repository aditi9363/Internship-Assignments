import win32file
pipe = win32file.CreateFile(
    r'\\.\pipe\AssignmentPipe',
    win32file.GENERIC_READ | win32file.GENERIC_WRITE,
    0, None,
    win32file.OPEN_EXISTING,
    0, None
)
message = input("Enter message: ")
win32file.WriteFile(pipe, message.encode())
result, data = win32file.ReadFile(pipe, 1024)
print("Server response:", data.decode())
win32file.CloseHandle(pipe)