import win32pipe
import win32file

pipe = win32pipe.CreateNamedPipe(
    r'\\.\pipe\AssignmentPipe',
    win32pipe.PIPE_ACCESS_DUPLEX,
    win32pipe.PIPE_TYPE_MESSAGE | win32pipe.PIPE_WAIT,
    1, 65536, 65536, 0, None
)
print("Waiting for client...")
win32pipe.ConnectNamedPipe(pipe, None)

result, data = win32file.ReadFile(pipe, 1024)

message = data.decode()
print("Client sent:", message)
response = message[::-1]
win32file.WriteFile(pipe, response.encode())
print("Response sent:", response)
win32file.CloseHandle(pipe)