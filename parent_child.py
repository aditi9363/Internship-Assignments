from multiprocessing import Process
import os

def child():
    print("I am the child")
    print("Child PID:", os.getpid())
    print("Parent PPID:", os.getppid())

if __name__ == "__main__":
    proc = Process(target=child)
    proc.start()

    print("I am the parent")
    print("Parent PID :", os.getpid())
    print("Child PID  :", proc.pid)
    
    proc.join()
 
# Unlike Unix fork(), the child starts fresh.
# It does not continue execution from the line after start().
# Instead, it starts a new Python interpreter and runs the target function.