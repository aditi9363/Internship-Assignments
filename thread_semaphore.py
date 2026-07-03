import threading
import time

semaphore = threading.Semaphore(3)

def worker(thread_number):
    print(f"Thread {thread_number} is waiting to enter...")

    semaphore.acquire()

    print(f"Thread {thread_number} entered the critical section.")

    time.sleep(1)

    print(f"Thread {thread_number} is leaving the critical section.")

    semaphore.release()

threads = []

for i in range(1, 11):
    t = threading.Thread(target=worker, args=(i,))
    threads.append(t)

for t in threads:
    t.start()

for t in threads:
    t.join()

print("All threads have finished.")

# Semaphore  VS  Lock

#   Semaphore                                # Lock
# Allows multiple threads(up to a limit).    Allows only one thread at a time. 
# Has a counter(eg: 3,5)                     Has only two states:Locked & Unlocked.
# Used when multiple resources are           Used to protect a single shared resource.
# available.     
