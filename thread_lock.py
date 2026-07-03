import threading
import time

counter = 0

lock = threading.Lock()

def increment():
    global counter

    for _ in range(1000):
        lock.acquire()
        counter += 1
        lock.release()

threads = []

start_time = time.time()

for i in range(100):
    thread = threading.Thread(target=increment)
    threads.append(thread)

for thread in threads:
    thread.start()

for thread in threads:
    thread.join()

end_time = time.time()

print("Final Counter Value :", counter)
print("Expected Value   :", 100 * 1000)
print("Execution Time   :{:.6f} seconds".format(end_time - start_time))

# Using a Lock ensures only one thread updates the counter at a time.
# This prevents race conditions and guarantees the final value is always 100000.
# However, acquiring and releasing the lock adds a small overhead,
# so this version is usually a little slower than the version without a lock.

# -------------------- Alternative Method --------------------

# Instead of:
# lock.acquire()
# counter += 1
# lock.release()

# We can use:
#
# with lock:
#     counter += 1
#
# 'with lock:' automatically acquires and releases the lock.
# It is shorter, safer, and the recommended way in Python.