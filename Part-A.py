#Ans 1
import threading
counter = 0
lock = threading.Lock()

def increment_with_lock():
    global counter

    for i in range(1000):
        with lock:
            counter += 1

threads = []

for i in range(10):
    t = threading.Thread(target=increment_with_lock)
    threads.append(t)
    t.start()

for t in threads:
    t.join()

print("Final counter value WITH lock:", counter)

#-------------WITHOUT Lock---------------
counter = 0
def increment_without_lock():
    global counter

    for i in range(1000):
        counter += 1

threads = []

for i in range(10):
    t = threading.Thread(target=increment_without_lock)
    threads.append(t)
    t.start()

for t in threads:
    t.join()

print("Final counter value WITHOUT lock:", counter)
#The unprotected version fails because Without a lock,multiple threads update the counter at the same time,causing some increments to be lost.
#This is called a race condition.
#A mutex(lock) prevents this by allowing only one thread to access the counter at a time.


#Ans 2
#mutex_writer.py
import ctypes
mutex = ctypes.windll.kernel32.CreateMutexW(None, False, "MyMutex")
print("Writer waiting...")

ctypes.windll.kernel32.WaitForSingleObject(mutex, -1)
print("Writer started writing")

with open("data.txt", "a") as file:
    file.write("Hello from writer\n")

print("Writing completed")

ctypes.windll.kernel32.ReleaseMutex(mutex)
print("Writer released mutex")


#mutex_reader.py
import ctypes
mutex = ctypes.windll.kernel32.CreateMutexW(None, False, "MyMutex")
print("Reader Waiting...")

ctypes.windll.kernel32.WaitForSingleObject(mutex, -1)
print("Reader started reading")

try:
    with open("data.txt", "r") as file:
        print(file.read())
except FileNotFoundError:
    print("File not found")
print("Reading completed")

ctypes.windll.kernel32.ReleaseMutex(mutex)
print("Reader released mutex")


#Ans 3
import threading
import time
mutex = threading.Lock()
def worker():
    print("Worker thread trying to acquire lock... ")
    mutex.acquire()
    print("Worker thread acquired lock")
    time.sleep(8)
    print("Worker thread releasing lock")
    mutex.release()

t = threading.Thread(target=worker)
t.start()

time.sleep(1)
print("Main thread trying to acquire lock with 3-second timeout...")
result = mutex.acquire(timeout=3)
if result:
    print("Main thread acquired lock")
    mutex.release()
else:
    print("Could not acquire mutex - skipping task")
t.join()
print("Program finished")


#Ans 4
import threading
import time
import random

semaphore = threading.Semaphore(3)

def use_database(thread_number):
    print(f"Thread {thread_number} is waiting for a database connection...")
    semaphore.acquire()
    print(f"Thread {thread_number} CONNECTED to database")
    time.sleep(random.randint(1,2))
    print(f"Thread {thread_number} DISCONNECTED from database")
    semaphore.release()

threads = []
for i in range(1, 11):
    t = threading.Thread(target=use_database, args=(i,))
    threads.append(t)
    t.start()

for t in threads:
    t.join()
print("\nAll database tasks completed.")


#Ans 5
import threading
counter = 0
semaphore = threading.Semaphore(1)
def increment_with_semaphore():
    global counter
    for i in range(1000):
        semaphore.acquire()
        counter += 1
        semaphore.release()

threads = []
for i in range(10):
    t = threading.Thread(target=increment_with_semaphore)
    threads.append(t)
    t.start()

for t in threads:
    t.join()
print("Final Counter Value with Semaphore:", counter)

#--------------WITHOUT Semaphore---------------
import threading
counter2 = 0
def increment_without_semaphore():
    global counter2
    for i in range(1000):
        counter2 += 1

threads = []
for i in range(10):
    t = threading.Thread(target=increment_without_semaphore)
    threads.append(t)
    t.start()

for t in threads:
    t.join()
print("Final Counter Value without Semaphore:", counter2)
#Mutex has ownership: only the locking thread can unlock it.
#Binary Semaphore has no ownership: any thread can release it.


#Ans 6
import multiprocessing
import time
import os
def worker(semaphore, process_num):
    print(f"Process {process_num} is waiting to enter")
    semaphore.acquire()
    print(f"Process {process_num} ENTERED critical section"
          f"(PID: {os.getpid()})")
    time.sleep(3)
    print(f"Process {process_num} LEAVING critical section"
          f"(PID: {os.getpid()})")
    semaphore.release()


if __name__ == "__main__":
    semaphore = multiprocessing.Semaphore(2)
    processes = []
    for i in range(1, 4):
        p = multiprocessing.Process(target=worker, args=(semaphore, i))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()
    print("All processes completed")


#Ans 7
import threading
import time
event = threading.Event()
def worker(worker_id):
    print(f"Worker {worker_id} is waiting...")
    event.wait()
    print(f"Worker {worker_id} is running")

print("--------FIRST ROUND--------")
threads = []
for i in range(5):
    t= threading.Thread(target=worker, args=(i+1,))
    threads.append(t)
    t.start()

print("Main thread preparing...")
time.sleep(3)
print("Main thread gives START signal")
event.set()

for t in threads:
    t.join()

event.clear()
print("\nEvent cleared\n")

print("--------SECOND ROUND--------")
threads = []
for i in range(5):
    t= threading.Thread(target=worker, args=(i+1,))
    threads.append(t)
    t.start()

print("Main thread preparing again...")
time.sleep(3)
print("Main thread gives START signal again")
event.set()

for t in threads:
    t.join()
print("\nAll workers finished")


#Ans 8
import threading
import time
event = threading.Semaphore(0)
def worker(worker_id):
    print(f"Worker {worker_id} is waiting...")
    event.acquire()
    print(f"Worker {worker_id} received the token and is running")

threads = []
for i in range(1, 6):
    t = threading.Thread(target=worker, args=(i,))
    threads.append(t)
    t.start()

for i in range(1, 6):
    time.sleep(1)
    print(f"\nMain thread released Token {i}")
    event.release()
for t in threads:
    t.join()
print("\nAll worker threads finished")


#Ans 9
import threading
import time
shared_list = []
lock = threading.Lock()
def add_items(thread_number):
    for i in range(50):
        lock.acquire()
        shared_list.append(f"Thread-{thread_number} Item-{i}")
        lock.release()

threads = []
start_time = time.time()

for i in range(20):
    t = threading.Thread(target=add_items, args=(i,))
    threads.append(t)
    t.start()
for t in threads:
    t.join()
end_time = time.time()
print("Total items in list:", len(shared_list))
if len(shared_list) == 1000:
    print("List is consistent.")
else:
    print("List is NOT consistent.")
print("Total time taken:", end_time - start_time, "seconds")


#Ans 10
import threading
import time
import ctypes
NUM_THREADS = 50
INCREMENTS = 10000
#------------------Version A------------------
counter_lock = 0 
lock = threading.Lock()
def increment_with_lock():
    global counter_lock

    for i in range(INCREMENTS):
        lock.acquire()
        counter_lock += 1
        lock.release()
start_time_lock = time.time()
threads = []

for i in range(NUM_THREADS):
    t = threading.Thread(target=increment_with_lock)
    threads.append(t)
    t.start()
for t in threads:
    t.join()
end_time_lock = time.time()
lock_time = end_time_lock - start_time_lock

#------------------Version B--------------------
counter_mutex = 0
kernel32 = ctypes.windll.kernel32
mutex = kernel32.CreateMutexW(None, False, "Global\\MyMutex")
def increment_with_mutex():
    global counter_mutex
    for i in range(INCREMENTS):
        kernel32.WaitForSingleObject(mutex, 0xFFFFFFFF)
        counter_mutex += 1
        kernel32.ReleaseMutex(mutex)
start_time_mutex = time.time()
threads = []
for i in range(NUM_THREADS):
    t = threading.Thread(target=increment_with_mutex)
    threads.append(t)
    t.start()

for t in threads:
    t.join()
end_time_mutex = time.time()
mutex_time = end_time_mutex - start_time_mutex

print("Final Counter using Lock :", counter_lock)
print("Time using Lock :", lock_time, "seconds")
print()
print("Final Counter using Mutex :", counter_mutex)
print("Time using Mutex :", mutex_time, "seconds")


#Ans 11
import threading
import time
buffer = []
MAX_SIZE = 5
TOTAL_ITEMS = 20
condition = threading.Condition()
def producer():
    for item in range(1, TOTAL_ITEMS + 1):
        with condition:
            while len(buffer) == MAX_SIZE:
                print("Buffer Full -> Producer Waiting")
                condition.wait()
            buffer.append(item)
            print(f"{time.strftime('%H:%M:%S')} Produced : {item}")
            condition.notify_all()
        time.sleep(0.5)

def consumer():
    for i in range(TOTAL_ITEMS):
        with condition:
            while len(buffer) == 0:
                print("Buffer Empty -> Consumer Waiting")
                condition.wait()
            item = buffer.pop(0)
            print(f"{time.strftime('%H:%M:%S')} Consumed : {item}")
            condition.notify_all()
        time.sleep(1)

producer_thread = threading.Thread(target=producer)
consumer_thread = threading.Thread(target=consumer)

producer_thread.start()
consumer_thread.start()

producer_thread.join()
consumer_thread.join()
print("Program Finished")


#Ans 12
import threading
import time
import random
class RWLock:
    def __init__(self):
        self.condition = threading.Condition()
        self.readers = 0
        self.writer = False

    def acquire_read(self):
        with self.condition:
            while self.writer:
                self.condition.wait()
            self.readers += 1

    def release_read(self):
        with self.condition:
            self.readers -= 1
            if self.readers == 0:
                self.condition.notify_all()

    def acquire_write(self):
        with self.condition:
            while self.readers > 0 or self.writer:
                self.condition.wait()
            self.writer = True

    def release_write(self):
        with self.condition:
            self.writer = False
            self.condition.notify_all()

#---------------Shared Resource----------------
shared_data = {"value": 0}
rwlock = RWLock()

def reader(reader_id):
    for i in range(3):
        rwlock.acquire_read()
        print(f"Reader {reader_id} is reading value:",
              shared_data["value"])
        time.sleep(random.uniform(0.5, 1))
        rwlock.release_read()
        time.sleep(random.uniform(0.5, 1))

def writer(writer_id):
    for i in range(2):
        rwlock.acquire_write()
        print(f"Writer {writer_id} is WRITING...")
        shared_data["value"] += 1
        print(f"Writer {writer_id} updated value to:",
              shared_data["value"])
        time.sleep(1)
        rwlock.release_write()
        time.sleep(random.uniform(1, 2))

threads = []
for i in range(6):
    t = threading.Thread(target=reader, args=(i + 1,))
    threads.append(t)

for i in range(2):
    t = threading.Thread(target=writer, args=(i + 1,))
    threads.append(t)
for t in threads:
    t.start()
for t in threads:
    t.join()
print("\nFinal Shared Data:", shared_data)


#Ans 13
import threading
import time
import random
from datetime import datetime
NUM_THREADS = 5
barrier = threading.Barrier(NUM_THREADS)
def current_time():
    return datetime.now().strftime("%H:%M:%S")
def worker(thread_id):
    for phase in range(1,4):
        print(f"[{current_time()}] Thread-{thread_id} started Phase-{phase}")
        work_time = random.uniform(0.5, 2)
        if thread_id == 1 and phase == 2:
           work_time = 5
           print(f"[{current_time()}] Thread-{thread_id} is VERY SLOW in Phase-{phase}")
        time.sleep(work_time)
        print(f"[{current_time()}] Thread-{thread_id} Finished Phase-{phase}")
        print(f"[{current_time()}] Thread-{thread_id} waiting at barrier after Phase-{phase}")
        barrier.wait()
        print(f"[{current_time()}] Thread-{thread_id} passed barrier for Phase-{phase}\n")

threads = []
for i in range(NUM_THREADS):
    t = threading.Thread(target=worker, args=(i + 1,))
    threads.append(t)
    t.start()

for t in threads:
    t.join()
print("All phases completed successfully")


#Ans 14
import threading
import time
import random
def timeout_handler():
    print("WATCHGDOG: task timed out")
def perform_task():
    work_time = random.randint(1, 10)
    print(f"Task started... will take {work_time} seconds")
    time.sleep(work_time)
    print("Task completed")
for i in range(5):
    print(f"\n--- Run {i+1} ---")
    timer = threading.Timer(5, timeout_handler)
    timer.start()
    start = time.time()
    perform_task()
    end = time.time()
    total_time =  end - start
    if total_time < 5:
        timer.cancel()
        print("Timer cancelled because task finished in time")
    print(f"Task time: {total_time:.2f} seconds")



