import os
import time

print("Current Process ID(PID):", os.getpid())

print("Parent Process ID(PPID):", os.getppid())
#PID is the unique ID assigned to the currently running process.
#PPID is the ID of the parent process that started the current process.

#time.sleep(20)