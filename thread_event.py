import threading
import time

event = threading.Event()

def worker(worker_name):
    print(worker_name, "is waiting for the signal...")

    event.wait()

    print(worker_name, ":Signal received, starting work...")
    time.sleep(2)
    print(worker_name, ":Work completed.\n")

t1 = threading.Thread(target=worker, args=("Worker 1",))
t1.start()

print("Main thread is preparing...")   
time.sleep(3)

print("Main thread: Sending signal.\n")
event.set()

t1.join()

#--------------------Reuse the Event---------------------
event.clear()     
print("Event has been cleared.\n")

t2 = threading.Thread(target=worker, args=("Worker 2",))
t2.start()

print("Main thread is preparing again...")
time.sleep(3)

print("Main thread: Sending signal again.\n")
event.set()

t2.join()

print("Main thread finished.")
