import os
import threading
import multiprocessing

def thread_function():
    print("\nInside Thread")
    print("Thread PID:", os.getpid())

def process_function():
    print("\nInside Process")
    print("Process PID:", os.getpid())
    
if __name__ == "__main__":
    print("Main Program PID:", os.getpid())

    thread = threading.Thread(target=thread_function)
    thread.start()
    thread.join()

    process = multiprocessing.Process(target=process_function)
    process.start()
    process.join()

# Process VS Thread
#+--------------------+----------------------+----------------------+
#| Feature            |Thread                | Process              |
#+--------------------+----------------------+----------------------+ 
#| Memory Space       | Shared               |  Separate            |
#| PID                | Same as parent       |  Different           |
#| Creation Cost      | Low                  |  High                |       
#| Communication      | Easy(shared data)    | IPC Required         |
#| GIL Impact         | Compete for one GIL  | Each has its own GIL |
#+--------------------+----------------------+----------------------+    
    