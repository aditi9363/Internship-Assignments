import os

comspec = os.environ["COMSPEC"]
print("Parent process started")

#Run the command
# cmd /c echo Hello from spawnl!
exit_code = os.spawnl(
    os.P_WAIT,
    comspec,
    "cmd",
    "/c",
    "echo",
    "Hello from spawnl!"
)

print("Exit code:", exit_code)

print("spawnl() execution completed successfully.")

# spawnl() is used when the command line arguments are fixed & already known.
# Each argument is passed separately to the function.
# spawnv() is used when the arguments are built dynamically at runtime.
# All arguments are stored in a list & passed together.
# Use spawnl() for simple commands with a fixed set of arguments and
# Use spawnv() when the number or values of arguments may change during program execution. 