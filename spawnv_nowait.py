import os
import sys

comspec = os.environ.get("COMSPEC")

#Start child process without waiting
child_pid = os.spawnv(
    os.P_NOWAIT,
    comspec,
    ["cmd", "/c", "echo", "Background process is running"]
)

print("Parent continues immediately.")

pid, status = os.waitpid(child_pid, 0)

print("Child PID:", pid)
print("Exit Status:", status)

#Verify a different PID using Python
python_path = sys.executable

print("\nParent PID : ", os.getpid())

child_pid2 = os.spawnv(
    os.P_NOWAIT,
    python_path,
    [
        python_path,
        "child_pid.py"
    ]
)
os.waitpid(child_pid2, 0)

#os.P_WAIT                                         os.P_NOWAIT
#Parent waits for the child to finish.             Parent continues immediately.
#Blocking call.                                    Non-blocking call.
#Returns the child's exit status.                  Returns the child's PID/handle immediately.
#Parent & child do not run at the same time.       Parent & child run concurrently.
#No need to call waitpid().                        Use waitpid() later if you want to wait for the child & get its exit status.
