import threading
import time
from bounded_queue import BoundedQueue

queue = BoundedQueue(maxsize=10)

def producer(pid):
    count = 1

    while True:
        item = f"P{pid}-{count}"
        print(f"Producer {pid} trying to add {item}")
        queue.put(item)
        print(f"Producer {pid} added {item}")
        count += 1
        time.sleep(0.2)              #Fast producer

def consumer(cid):
    while True:
        item = queue.get()
        print(f"Consumer {cid} processed {item}")
        time.sleep(2)               #Slow consumer

#5 Producers
for i in range(1, 6):
    threading.Thread(
        target=producer,
        args=(i,),
        daemon=True
    ).start()

#2 Consumers
for i in range(1, 3):
    threading.Thread(
        target=consumer,
        args=(i,),
        daemon=True
    ).start()

while True:
    time.sleep(1)

