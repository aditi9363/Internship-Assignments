import multiprocessing 
import time
import random
SENTINEL = None

def producer(queue, producer_id):
    for i in range(1, 6):
        time.sleep(random.uniform(0.5, 1.5))
        item = f"P{producer_id}-Item{i}"
        queue.put(item)
        print(f"[Producer {producer_id}] Put: {item}")

def consumer(queue, consumer_id):
    while True:
        item = queue.get()

        if item == SENTINEL:
            print(f"[Consumer {consumer_id}] Received SENTINEL. Exiting...")
            break

        print(f"[Consumer {consumer_id}] Got: {item}")
        time.sleep(random.uniform(0.5, 1.0))

if __name__ == "__main__":
    queue = multiprocessing.Queue(maxsize=10)
    producers = []
    consumers = []

    for i in range(1, 4):
        p = multiprocessing.Process(
            target=producer,
            args=(queue, i)
        )
        producers.append(p)
        p.start()

    for i in range(1, 3):
        c = multiprocessing.Process(
            target=consumer,
            args=(queue, i)
        )
        consumers.append(c)
        c.start()

    for p in producers:
        p.join()
    print("All producers finished.\n")

    queue.put(SENTINEL)
    queue.put(SENTINEL)

    for c in consumers:
        c.join()

    print("\nAll consumers finished.")
