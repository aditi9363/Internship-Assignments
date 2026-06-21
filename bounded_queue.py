import threading
import queue
import time
from collections import deque

class BoundedQueue:
    def __init__(self, maxsize):
        self.queue = deque()
        self.maxsize = maxsize
        self.condition = threading.Condition()

        self.total_put = 0
        self.total_get = 0
        self.total_wait_put = 0
        self.total_wait_get = 0

    def put(self, item, timeout=None):
        with self.condition:
            if len(self.queue) >= self.maxsize:
                self.total_wait_put += 1

            if timeout is None:
                self.condition.wait_for(
                    lambda: len(self.queue) < self.maxsize
                )

            else:
                success = self.condition.wait_for(
                    lambda: len(self.queue) < self.maxsize,
                    timeout=timeout
                )

                if not success:
                    raise TimeoutError("Queue full")

            self.queue.append(item)

            self.total_put += 1

            print(
                f"{threading.current_thread().name} "
                f"produced {getattr(item, 'order_id', item)} "
                f"(size={len(self.queue)})"
            )

            self.condition.notify_all()

    def get(self, timeout=None):
        with self.condition:
            if len(self.queue) == 0:
                self.total_wait_get += 1

            if timeout is None:
                self.condition.wait_for(
                    lambda: len(self.queue) > 0
                )

            else:
                success = self.condition.wait_for(
                    lambda: len(self.queue) > 0,
                    timeout=timeout
                )

                if not success:
                    raise TimeoutError("Queue empty")

            item = self.queue.popleft()

            self.total_get += 1

            print(
                f"{threading.current_thread().name} "
                f"consumed {item} "
                f"(size={len(self.queue)})"
            )

            self.condition.notify_all()

            return item
        
    def print_status(self):
        print("\n==========QUEUE STATISTICS==========")
        print(f"Total Put         :{self.total_put}")
        print(f"Total Get         :{self.total_get}")
        print(f"Producer waits    :{self.total_wait_put}")
        print(f"Consumer waits    :{self.total_wait_get}")
        print("======================================")

    def empty(self):
        with self.condition:
            return len(self.queue) == 0
        
    def qsize(self):
        with self.condition:
            return len(self.queue)
        
def producer(queue, stop_event):
    count = 1
    while not stop_event.is_set():
        queue.put(count)
        count += 1

        #Fast producer
        time.sleep(0.1)
    
def consumer(queue, stop_event):
    while not stop_event.is_set():
        queue.get()

        #Slow consumer
        time.sleep(0.5)

def main():
    q = BoundedQueue(maxsize=10)
    stop_event = threading.Event()
    threads = []

    # 3 Fast Producers
    for i in range(3):
        t = threading.Thread(
            target=producer,
            args=(q, stop_event),
            name=f"Producer-{i+1}"
        )
        t.start()
        threads.append(t)

    # 3 Slow Consumers
    for i in range(3):
        t = threading.Thread(
            target=consumer,
            args=(q, stop_event),
            name=f"Consumer-{i+1}"
        )
        t.start()
        threads.append(t)

    time.sleep(30)

    stop_event.set()

    for t in threads:
        t.join(timeout=1)
    q.print_status()

if __name__ == "__main__":
    main()

    