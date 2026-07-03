import os

comspec = os.environ["COMSPEC"]

#Run the command: cmd /c dir C:\Windows
#P_WAIT makes the parent wait until the child process finishes
exit_code = os.spawnv(
    os.P_WAIT,
    comspec,
    ["cmd", "/c", "dir", "C:\\Windows" ]
)

print("Exit Code:", exit_code)

print("Done!")

# On Windows, os.spawnv() always creates a brand-new child process (new PID).
# Unlike Unix's exec(), it does not replace the current process image.