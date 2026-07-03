import time
import threading
import multiprocessing

def count_up(n):
    count = 0

    for i in range(n):
        count += 1

    return count

if __name__ == "__main__":
    #------------------Sequential Execution---------------------
    N = 50_000_000

    print("Sequential Execution Started...")

    start = time.perf_counter()

    count_up(N)
    count_up(N)

    end = time.perf_counter()

    print(f"Sequential Time: {end - start:.2f} seconds")

    #--------------------Thread Execution----------------------
    print("\nThread Execution Started...")

    thread1 = threading.Thread(target=count_up, args=(N,))
    thread2 = threading.Thread(target=count_up, args=(N,))

    start = time.perf_counter()

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()

    end = time.perf_counter()

    print(f"Thread Time : {end - start:.2f} seconds")

    #---------------------Process Execution------------------------
    print("\nProcess Execution Started...")

    process1 = multiprocessing.Process(target=count_up, args=(N,))
    process2 = multiprocessing.Process(target=count_up, args=(N,))

    start = time.perf_counter()

    process1.start()
    process2.start()

    process1.join()
    process2.join()

    end = time.perf_counter()

    print(f"Process Time : {end - start:.2f} seconds")

# GIL (Global Interpreter Lock) allows only one thread to execute Python bytecode
# at a time in a single process.

# Threads do not speed up CPU-bound work because only one thread can
# execute Python bytecode at a time due to the GIL.

# Use multiprocessing for CPU-bound tasks because each process has its own
# Python interpreter and GIL, allowing multiple CPU cores to work in parallel.

# On Windows, multiprocessing uses the "spawn" method.
# Each child process starts a fresh Python interpreter and re-imports the module,
# which adds startup overhead. Therefore, multiprocessing code must be placed
# inside 'if __name__ == "__main__":'.