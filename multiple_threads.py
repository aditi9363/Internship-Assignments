import threading
import random
import time

def worker(thread_number):
    print(f"Thread {thread_number} started")

    sleep_time = random.uniform(0.5, 2)
    time.sleep(sleep_time)

    print(f"Thread {thread_number} finished after {sleep_time:.2f} seconds")

if __name__ == "__main__":

    threads = []

    start_time = time.perf_counter()

    for i in range(1, 11):
        thread = threading.Thread(target=worker, args=(i,))
        threads.append(thread)

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    end_time = time.perf_counter()

    print("\nAll threads have finished.")
    print(f"Total execution time: {end_time - start_time:.2f} seconds")

# Why use two separate loops?
# First, we start all threads so they can run at the same time(concurrently).
# Then, we use a second loop with join() to wait for all threads to finish.
# If we use start() & join() together in the same loop,each thread is started &
# immediately waited on before the next thread starts.
# This makes the threads run one after another (almost like normal sequential execution),
# so we lose the benefit of concurrency & the program takes longer to complete.
