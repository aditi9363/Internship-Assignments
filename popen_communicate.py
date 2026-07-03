import subprocess

proc = subprocess.Popen(
    ['python', '-c', 'import sys; print(sys.stdin.read().upper())'],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE
)

output, error = proc.communicate(input=b'hello world')

print("Output from child process:")
print(output.decode())

#  communicate()                              wait()
# Sends input to the child process.           Does not send any input.
# Receives output from the child process.     Does not receive any output.
# Waits until the process finishes.           Only waits until the process finishes.
# Returns (stdout, stderr).                   Returns only the exitcode(returncode).