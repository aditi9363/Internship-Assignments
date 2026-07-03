import threading
import time

running = True          #flag to stop daemon thread

def worker():
    count = 1
    while True:
        print(f"Daemon thread: {count}")

        count += 1

        time.sleep(1)

t = threading.Thread(target=worker, daemon=False)
t.start()

for i in range(4):
    print(f"Main thread : {i + 1}")
    time.sleep(1)

running = False     #Stop the daemon thread before exiting

time.sleep(0.2)

print("Main thread exiting...")
