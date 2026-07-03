import subprocess
import sys
import time

proc = subprocess.Popen([
    'python',
    '-c',
    'import time; time.sleep(3)'
])
print("Process started,doing other work...")

#Simulate some work in parent process
for i in range(1, 6):
    print("Working...", i)
    time.sleep(0.5)

proc.wait()

print("Process finished")
print("Return code:", proc.returncode)

# Popen() is useful because it lets the parent process
# continue doing other work while the child process runs in the background.
# Unlike subprocess.run(), it does not block immediately.



