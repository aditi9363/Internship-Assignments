import multiprocessing
import time

def worker():
    print("Child process started.")
    time.sleep(4)
    print("Child process finished.")

if __name__ == "__main__":
    proc = multiprocessing.Process(target=worker)
    print("Process created.")

    proc.start()

    print("Immediately after start(), is_alive():", proc.is_alive())

    time.sleep(1)
    print("After 1 second, is_alive():", proc.is_alive())

    proc.join()
    print("After join(), is_alive():", proc.is_alive())

    print("Process exit code:", proc.exitcode)