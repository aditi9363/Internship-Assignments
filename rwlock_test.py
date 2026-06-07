import threading
import time
from rwlock import RWLock

rwlock = RWLock()

shared_data = {"users": 0}

def reader(reader_id):
    rwlock.acquire_read()
    print(f"Reader {reader_id} reading: {shared_data}")
    time.sleep(2)
    rwlock.release_read()

def writer(writer_id):
    rwlock.acquire_write()
    shared_data["users"] += 1
    print(f"Writer {writer_id} updated data")
    time.sleep(2)
    rwlock.release_write()

for i in range(3):
    threading.Thread(target=reader, args=(i,)).start()

threading.Thread(target=writer, args=(1,)).start()