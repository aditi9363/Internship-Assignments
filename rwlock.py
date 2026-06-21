import threading
import time
import contextlib

class RWLock:
    def __init__(self):
        self.read_count = 0
        self.read_lock = threading.Lock()
        self.write_lock = threading.Lock()

    def acquire_read(self):
        with self.read_lock:
            self.read_count += 1
            if self.read_count == 1:
                self.write_lock.acquire()

    def release_read(self):
        with self.read_lock:
            self.read_count -= 1
            if self.read_count == 0:
                self.write_lock.release()

    def acquire_write(self):
        self.write_lock.acquire()

    def release_write(self):
        self.write_lock.release()

    @contextlib.contextmanager
    def read_lock_context(self):
        self.acquire_read()
        try:
            yield
        finally:
            self.release_read()

    @contextlib.contextmanager
    def write_lock_context(self):
        self.acquire_write()
        try:
            yield
        finally:
            self.release_write()


rwlock = RWLock()

#Reader thread function
def reader():
    with rwlock.read_lock_context():
        print(f"{time.strftime('%H:%M:%S')} {threading.current_thread().name} acquired READ lock")
        time.sleep(0.5)
        print(f"{time.strftime('%H:%M:%S')} {threading.current_thread().name} released READ lock")

#Writer thread function
def writer():
    with rwlock.write_lock_context():
        print(f"{time.strftime('%H:%M:%S')} {threading.current_thread().name} acquired WRITE lock")
        time.sleep(0.3)
        print(f"{time.strftime('%H:%M:%S')} {threading.current_thread().name} released WRITE lock")

if __name__ == "__main__":
    threads = []
    for i in range(5):
        t = threading.Thread(target=reader, name=f"Reader-{i+1}")
        threads.append(t)

    for i in range(2):
        t = threading.Thread(target=writer, name=f"Writer-{i+1}")
        threads.append(t)

    for t in threads:
        t.start()

    for t in threads:
        t.join()

    print("\nAll threads completed")