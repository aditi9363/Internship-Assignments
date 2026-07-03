import multiprocessing
import time

def child():
    time.sleep(2)
    print("Child done")

if __name__ == "__main__":
    proc = multiprocessing.Process(target=child)
    proc.start()
    print("Parent is waiting for the child...")
    proc.join()
    print("Child Exit Code:", proc.exitcode)

# join() blocks the parent process until the child finishes execution.
# Without join(), the parent may continue or terminate before the child completes, 
# and the child's exit code may not be available immediately.
# Therefore, join() should be used to synchronize processes and clean up resources.
