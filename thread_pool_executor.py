from concurrent.futures import ThreadPoolExecutor
import time

def fetch(n):
    print(f"Task {n} started")
    time.sleep(0.5)
    print(f"Task {n} finished")
    return n * n

#---------------Sequential Execution----------------
print("Sequential Execution")

start = time.time()

sequential_results = []

for i in range(10):
    sequential_results.append(fetch(i))

end = time.time()

print("Sequential Results:", sequential_results)
print("Sequential Time:", round(end - start, 2), "seconds")

#-----------------ThreadPoolExecutor-----------------
print("\nThreadPoolExecutor Execution")

start = time.time()

with ThreadPoolExecutor(max_workers=4) as executor:
    results = list(executor.map(fetch, range(10)))

end = time.time()

print("ThreadPool Results:", results)
print("ThreadPool Time:", round(end - start, 2), "seconds")

# ThreadPoolExecutor is better than creating threads manually because it
# automatically creates, reuses, and manages a fixed number of threads.
# It reduces code complexity, avoids creating too many threads, and is
# ideal for running many independent tasks concurrently, especially
# I/O-bound tasks like file handling, network requests, or database operations.