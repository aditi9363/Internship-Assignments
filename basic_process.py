from multiprocessing import Process, current_process
import os

def worker():
    print("Process Name:", current_process().name)
    print("Process PID:", os.getpid())

if __name__ == "__main__":
    print("Main Process PID:", os.getpid())

    process = Process(target=worker)

    process.start()

    process.join()

    print("Main process done")

#Why if __name__ == "__main__":  - mandatory on Windows?
#When a new process is created, Python imports the script again.
#Without this block, the script would execute from the beginning 
#inside every child process, causing endless process creation.
#The block ensures that only the original(main) process creates new child processes.
