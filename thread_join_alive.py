import threading
import time

def worker():
    print("Thread started")
    print("Thread is working for 3 seconds...")
    time.sleep(3)
    print("Thread finished")

if __name__ == "__main__":

    print("========== PART 1 : Using is_alive() and join() ==========\n")

    thread1 = threading.Thread(target=worker)
    thread1.start()
    print("Immediately after start(), is thread alive?", thread1.is_alive())

    time.sleep(1)

    print("After 1 second, is thread alive?", thread1.is_alive())

    thread1.join()
    print("After join(), is thread alive?", thread1.is_alive())

    print("\n========== PART 2 : Using join(timeout=1) ==========\n")

    thread2 = threading.Thread(target=worker)
    thread2.start()

    print("Waiting for only 1 second using join(timeout=1)...")

    thread2.join(timeout=1)

    if thread2.is_alive():
        print("Thread is still running after timeout.")
    else:
        print("Thread has already finished.")

    thread2.join()

    print("Main thread done")



