import threading

def worker():
    print("Hello from the worker thread!")
    print("Current Thread Name:", threading.current_thread().name)

if __name__ == "__main__":
    thread = threading.Thread(target=worker)
    thread.start()
    thread.join()
    print("Main thread done")

