#Ans 19
import os
import threading
import multiprocessing
def thread_function():
    print("\n---Inside Thread---")
    print("Thread PID:", os.getpid())
def process_function():
    print("\n---Inside Child Process---")
    print("Child Process PID:", os.getpid())
if __name__ == "__main__":
    print("---Main Program---")
    print("Main Process PID:", os.getpid())
    t = threading.Thread(target=thread_function)
    t.start()
    t.join()
    p = multiprocessing.Process(target=process_function)
    p.start()
    p.join()
    print("\nProgram Finished")

#-------Process VS Thread---------
#+---------------------+--------------------------------+----------------------------------+
#|  Feature            |       Process                  |      Thread                      |
#+---------------------+--------------------------------+----------------------------------+
#| Memory space        |       Separate memory          |     Shared memory                |
#| PID                 |       Different PID            |      Same PID as parent process  |
#| Creation Cost       |       Higher                   |      Lower                       |
#| Communication       |       Harder(IPC needed)       |      Easier(shared data)         |
#+---------------------+--------------------------------+----------------------------------+

#Ans 20
import threading
def worker():
    print("Hello from worker thread")
    print("Current Thread Name:", threading.current_thread().name)
t = threading.Thread(target=worker)
t.start()
t.join()
print("Main thread done")


#Ans 21
import threading
import time
def download(url, duration):
    print(f"Starting download from {url}")
    time.sleep(duration)
    print(f"Finished download from {url} in {duration} seconds")
start_time = time.time()
t1 = threading.Thread(target=download, args=("https://site1.com", 3))
t2 = threading.Thread(target=download, args=("https://site2.com", 5))
t3 = threading.Thread(target=download, args=("https://site3.com", 2))
t1.start()
t2.start()
t3.start()
t1.join()
t2.join()
t3.join()
end_time = time.time()
total_time = end_time - start_time
print("\nAll downloads completed")
print(f"Total elapsed time: {total_time:.2f} seconds")


#Ans 22
import threading
import time
def worker():
    print("Thread started")
    time.sleep(3)
    print("Thread finished")
t = threading.Thread(target=worker)
t.start()
print("1.Is thread alive after start()? :", t.is_alive())
time.sleep(1)
print("2.Is thread alive after 1 second? :", t.is_alive())
t.join()
print("3.Is thread alive after join()? :", t.is_alive())
print("\n---Using join(timeout=1) Example---")
t2 = threading.Thread(target=worker)
t2.start()
t2.join(timeout=1)
print("4.Is second thread still alive after join(timeout=1)? :", t2.is_alive())
t2.join()
print("Main thread done")


#Ans 23
#---------Daemon Thread------------
import threading
import time
def worker():
    count = 1
    while True:
        print("Daemon thread counter:", count)
        count += 1
        time.sleep(1)
t = threading.Thread(target=worker, daemon=True)
t.start()
time.sleep(4)
print("Main thread exiting")

#---------------Non-Daemon Thread---------------
import threading
import time
def worker():
    count = 1
    while True:
        print("Normal thread counter:", count)
        count == 1
        time.sleep(1)

t = threading.Thread(target=worker, daemon=False)
t.start()
print("Main thread started")
time.sleep(4)
print("Main thread exiting")



#Ans 24
import threading
import time
import random
def worker(thread_number):
    print(f"Thread {thread_number} started")
    sleep_time = random.uniform(0.5, 2)
    time.sleep(sleep_time)
    print(f"Thread {thread_number} finished after {sleep_time:.2f} seconds")
threads = []
start_time = time.time()
for i in range(1, 11):
    t = threading.Thread(target=worker, args=(i,))
    threads.append(t)
for t in threads:
    t.start()
for t in threads:
    t.join()
end_time = time.time()
print(f"\nTotal time taken: {end_time - start_time:.2f} seconds")
#Using two separate loops for start() and join() is better because all threads start executing concurrently before the main program waits for completion.This improves performance and reduces total execution time. 
#If start() and join() are used together in the same loop, each thread completes before the next one starts,resulting in sequential execution and slower performance. 


#Ans 25
import threading
counter = 0
def increment():
    global counter
    for i in range(1000):
        counter += 1

threads = []
for i in range(100):
    t = threading.Thread(target=increment)
    threads.append(t)

for t in threads:
    t.start()

for t in threads:
    t.join()
print("Final counter value:", counter)
print("Execution Time:", end_time - start_time, "seconds")
#Why does Race Condition happen?
#Multiple threads try to modify the same variable simultaneously.
#counter += 1 is NOT atomic (not done in one single step,internally it happens it 3 steps-1.Read current counter value  2.Add 1  3.Write updated value back).
#So threads interfere with each other and some increments are lost.


#Ans 26
import threading
import time
counter = 0
lock = threading.Lock()
def increment():
    global counter
    for i in range(1000):
        with lock:
            counter += 1
threads = []
start_time = time.time()

for i in range(100):
    t = threading.Thread(target=increment)
    threads.append(t)

for t in threads:
    t.start()
for t in threads:
    t.join()
end_time = time.time()
print("Final Counter Value:", counter)
print("Execution Time:", end_time - start_time, "seconds")


#Ans 27
import threading
import time
def worker(event, worker_name):
    print(f"{worker_name} is waiting for the signal...")
    event.wait()
    print(f"{worker_name}: Signal received, starting work")
    time.sleep(2)
    print(f"{worker_name}: Work completed")

event = threading.Event()
t1 = threading.Thread(target=worker, args=(event, "Worker-1"))
t1.start()
time.sleep(3)
print("\nMain thread: Sending signal using event.set()")
event.set()
t1.join()

print("\nResetting event using event.clear()")
event.clear()
t2 = threading.Thread(target=worker, args=(event, "Worker-2"))
t2.start()
time.sleep(3)
print("\nMain thread: Sending signal again")
event.set()
t2.join()
print("\nMain program finished")


#Ans 28
import threading
import time
semaphore = threading.Semaphore(3)
def worker(thread_number):
    print(f"Thread {thread_number} is waiting to acquire semaphore")
    semaphore.acquire()
    print(f"Thread {thread_number} acquired semaphore")
    print(f"Thread {thread_number} is doing work...")
    time.sleep(1)
    print(f"Thread {thread_number} finished work")
    semaphore.release()
    print(f"Thread {thread_number} released semaphore")
    threads = []

for i in range(1, 11):
    t = threading.Thread(target=worker, args=(i,))
    threads.append(t)
    t.start()
for t in threads:
    t.join()
print("All threads completed")


#Ans 29
import threading
import time
def task(name):
    print(f"{name} executed")

timer1 = threading.Timer(3, task, args=("Timer 1",))
timer1.start()
print("Timer started,doing other work...")

for i in range(3):
    print(f"Main thread working...{i+1}")
    time.sleep(1)

print("\nCreating another timer and cancelling before execution...")
timer2 = threading.Timer(5, task, args=("Cancelled Timer",))
timer2.start()
time.sleep(2)
timer2.cancel()
print("Timer 2 cancelled before execution")

print("\nStarting two timers with different delays...")
t1 = threading.Timer(2, task, args=("First Timer",))
t2 = threading.Timer(4, task, args=("Second Timer",))
t1.start()
t2.start()
time.sleep(5)
print("\nProgram finished")


#Ans 30
from concurrent.futures import ThreadPoolExecutor
import time
def fetch(n):
    print(f"Task {n} started")
    time.sleep(0.5)
    print(f"Task {n} completed")
    return n * n

#------------Thread Pool Execution-------------
start = time.time()
with ThreadPoolExecutor(max_workers=4) as executor:
    results = executor.map(fetch, range(10))
    results = list(results)
end = time.time()

print("\nResults using ThreadPoolExecutor:")
print(results)
print("ThreadPoolExecutor Time:", round(end - start, 2), "seconds")

#-------------------Sequential Execution-----------------
start = time.time()
sequential_results = []
for i in range(10):
    sequential_results.append(fetch(i))
end = time.time()
print("\nResults using Sequential Loop:")
print(sequential_results)
print("Sequential Time:", round(end - start, 2), "seconds")
#ThreadPoolExecutor is better than creating threads manually because it automatically manages threads, reuses them efficiently, and makes the code simpler and cleaner.We do not need to manually create,start,join and manage multiple threads.It is especially useful for I/O-bound tasks like file handling,API calls and network operations,where multiple tasks can run concurrently and reduce execution time.


#Ans 31
import time
import threading
import multiprocessing

def count_up(n):
    count = 0
    while count < n:
        count += 1
N = 50_00_000

#---------Sequential Execution----------
print("Running sequentially...")
start = time.time()
count_up(N)
count_up(N)
end = time.time()
print("Sequential Time:", end -start, "seconds")

#---------------Multithreading----------------
print("\nRunning with threads...")
start = time.time()
t1 = threading.Thread(target=count_up, args=(N,))
t2 = threading.Thread(target=count_up, args=(N,))
t1.start()
t2.start()
t1.join()
t2.join()
end = time.time()
print("Threading Time:", end - start, "seconds")

#--------------Multiprocessing---------------
if __name__ == "__main__":
    p1 = multiprocessing.Process(target=count_up, args=(N,))
    p2 = multiprocessing.Process(target=count_up, args=(N,))
    p1.start()
    p2.start()
    p1.join()
    p2.join()
    end = time.time()
    print("Multiprocessing Time:", end - start, "seconds")
#GIL(Global Interpreter Lock)
#In python, the GIL allows only one thread to execute python bytecode at a time.
#Even if multiple threads are created,only one thread can use the CPU for python execution at any moment.

#Why threads do not help for CPU-bound tasks:
#CPU-bound tasks mainly use the processor for calculations.
#Because of the GIL,threads take turns using the CPU instead of running truly in parallel.
#Therefore,multithreading usually does not improve performance for heavy CPU tasks and may even become slightly slower due to thread switching overhead.

#When to prefer multiprocessing over threading:
#Multiprocessing is preferred for CPU-bound tasks because each process has its own python interpreter and its own GIL.
#This allows multiple CPU cores to work simultaneously,giving true parallel execution and better performance.

#Threading is better for I/O-bound tasks such as file handling,network requests,or database operations where programs spend time waiting.