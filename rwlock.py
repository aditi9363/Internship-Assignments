import threading

class RWLock:
    def __init__(self):
        self.readers = 0
        self.readers_lock = threading.Lock()
        self.resource_lock = threading.Lock()

    def acquire_read(self):
        with self.readers_lock:
            self.readers += 1

            if self.readers == 1:
                self.resource_lock.acquire()

    def release_read(self):
        with self.readers_lock:
            self.readers -= 1

            if self.readers == 0:
                self.resource_lock.release()

    def acquire_write(self):
        self.resource_lock.acquire()

    def release_write(self):
        self.resource_lock.release()