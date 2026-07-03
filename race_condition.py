import threading
import time

counter = 0

def increment():
    global counter

    #Each thread increments counter 1000 times
    for _ in range(1000):
        #Read the current value
        temp = counter
        time.sleep(0)
        temp = temp + 1
        counter = temp

threads = []

for i in range(100):
    thread = threading.Thread(target=increment)
    threads.append(thread)

for thread in threads:
    thread.start()

for thread in threads:
    thread.join()

print("Expected Counter Value :", 100 * 1000)
print("Actual Counter Value  :", counter)

# Why does this happen?
# Incrementing a shared variable is not a single (atomic) operation.
# It happens in three steps: Read the value, Modify it, & Write it back.
# If two threads read the same value at the same time, one thread's update
# can overwrite the other's update, causing some increments to be lost.
# The Global Interpreter Lock(GIL) does not make this entire read-modify-write
# sequence atomic, so race conditions can still occur.
