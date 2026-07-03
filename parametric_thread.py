import threading
import time

def download(url, duration):
    print(f"Starting download from {url}")
    time.sleep(duration)
    print(f"Finished downloading from {url} in {duration} seconds")

if __name__ == "__main__":
    start_time = time.perf_counter()

    thread1 = threading.Thread(target=download, args=("www.google.com", 3))
    thread2 = threading.Thread(target=download, args=("www.github.com", 2))
    thread3 = threading.Thread(target=download, args=("www.python.org", 4))

    thread1.start()
    thread2.start()
    thread3.start()

    thread1.join()
    thread2.join()
    thread3.join()

    end_time = time.perf_counter()

    total_time = end_time - start_time

    print(f"Total elapsed time: {total_time:.2f} seconds")

