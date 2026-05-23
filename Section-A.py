import os
print("Current Process ID (PID):", os.getpid())
print("Parent Process ID (PPID):", os.getpid())
#PID -> Unique ID given to the currently running process
#PPID -> ID of the process that started this process


#Ans 2
import subprocess
import os
import time
child = subprocess.Popen(
    ["python", "-c",
     "import os, time;"
     "print('I am the child');"
     "print('Child PID:', os.getpid());"
     "time.sleep(2)"]
)
print("I am the parent")
print("Parent PID:", os.getpid())
print("Child PID from parent:", child.pid)
child.wait()
print("Parent process finished")


#Ans 3
import subprocess
import time
child = subprocess.Popen(
    ["python", "-c",
     "import time;"
     "print('Child process started');"
     "time.sleep(2);"
     "print('Child done')"]
)
print("Parent is waiting for child to finish...")
status = child.wait()
print("Child process finished")
print("Child exit status:", status)
#If wait() is removed, the parent process will not wait for the child process to finish.
#The parent may terminate earlier while the child continues running in the background.
#Since the parent does not collect the child's exit status, the child process may temporarily become a zombie process.


#Ans 4
import subprocess
import os
children = []
for i in range(1, 4):
    child = subprocess.Popen(
        ["python", "-c",
         f"import os, time;"
         f"print('Child {i} running');"
         f"print('Child PID:', os.getpid());"
         f"time.sleep(2)"
         ]
    )
    children.append(child)
for child in children:
    child.wait()
    print("Parent collected child with PID:", child.pid)
print("All child processes finished")


#Ans 5
import subprocess
import os
child = subprocess.Popen(
    ["cmd", "/c", "dir"]
)
child.wait()
print("Child process finished")


#Ans 10
import subprocess
result = subprocess.run(
    "dir",
    capture_output=True,
    text=True,
    shell=True
)

print("Output of 'dir' command:\n")
print(result.stdout)

if result.returncode == 0:
    print("Command executed successfully")
else:
    print("Command failed")
    
failed_result = subprocess.run(
    "wrongcommand",
    capture_output=True,
    text=True,
    shell=True
)

if failed_result.returncode != 0:
    print("\nFailing command detected")
    print("Error message:")
    print(failed_result.stderr)
    
    
 #Ans 11
import subprocess
result = subprocess.run(
    ["more"],
    input="hello\n",
    text=True,
    capture_output=True,
    shell=True
)
print("Output from more command:")
print(result.stdout)
pipeline = subprocess.run(
    "echo hello",
    shell=True,
    text=True,
    capture_output=True
)
print("Output from shell command:")
print(pipeline.stdout)
#Security Risk of shell=True
#shell=True can be dangerous with untrusted input.
#If user input is directly added into the command,malicious commands may also get executed.
#So avoid shell=True when possible.


#Ans 12
import subprocess
import time
process = subprocess.Popen(
    ["timeout", "/T", "3"],
    shell=True
)

print("Process started, doing other work...")

for i in range(1, 6):
    print("Working...", i)
    time.sleep(1)

process.wait()

print("Process finished")
print("Return code:", process.returncode)
#why Popen() is useful vs run() for background tasks
#subprocess.run() 
#run() is blocking. 
#The program waits until the command finishes. 
#No other code executes during that time.
#subprocess.Popen()
#Popen() is non-blocking.
#The process starts in the background.
#Python can continue doing other tasks at the same time.


#Ans 13
import subprocess
popen_obj = subprocess.Popen(
    ["python", "-c",
     "import sys; print(sys.stdin.read().upper())"],
     stdin=subprocess.PIPE,
     stdout=subprocess.PIPE,
     stderr=subprocess.PIPE
)

stdout_data, stderr_data = popen_obj.communicate(
    input=b"hello world"
)

print("Output from child process:")
print(stdout_data.decode())

print("Return code:", popen_obj.returncode)
#Difference between communicate() and wait()
#communicate()                                 wait()       
#Sends input to the process                    Does NOT send input
#Captures stdout/stderr                        Does NOT capture output
#Waits for process to finish                   Only waits for process
#Returns output and errors                     Returns only return code
#Used when pipes are involved                  Used when only waiting is needed


#Ans 14
from multiprocessing import Process
import os
def worker():
    print("Worker process is running")
    print("Worker PID:", os.getpid())

if __name__ == "__main__":
    p = Process(target=worker)
    p.start()
    p.join()
    print("Main process done")
    print("Main Process PID:", os.getpid())


#Ans 15
import multiprocessing
import time
def task(name, duration):
    print(f"{name} started")

    time.sleep(duration)

    print(f"{name} finished after {duration} seconds")

if __name__ == "__main__":
    p1 = multiprocessing.Process(target=task, args=("Process 1", 3))
    p2 = multiprocessing.Process(target=task, args=("Process 2", 2))
    p3 = multiprocessing.Process(target=task, args=("Process 3", 1))
    
    p1.start()
    p2.start()
    p3.start()
    
    p1.join()
    p2.join()
    p3.join()
print("Main program finished")


#Ans 16
import multiprocessing
import time
def worker():
    print("Child process started")
    time.sleep(4)
    print("Child process finished")

if __name__ == "__main__":
    p = multiprocessing.Process(target=worker)
    p.start()
    print("Immediately after start():", p.is_alive())
    time.sleep(1)
    print("After 1 second:", p.is_alive())
    p.join()
    print("After join():", p.is_alive())
    print("Main process done")
#Understanding Process Lifecycle
#Stage                           Process State
#Before start()                  Process created but not running
#After start()                   Running(is_alive() = True)
#During sleep()                  Still alive/running
#After join()                    Finished(is_alive() = False)


#Ans 17
import multiprocessing
import time
def square(n):
    return n * n

if __name__ == "__main__":
    numbers = [1,2,3,4,5,6,7,8,9,10]
    start_time = time.time()
    normal_result = []
    for num in numbers:
        normal_result.append(square(num))
    end_time = time.time()
    print("Result using normal for loop:")
    print(normal_result)
    print("Time taken by normal for loop:",
          end_time - start_time, "seconds")
    
    start_time = time.time()
    with multiprocessing.Pool(processes=4) as pool:
        pool_result = pool.map(square, numbers)
    end_time = time.time()
    print("\nResult using Pool.map():")
    print(pool_result)
    print("Time taken by Pool.map():",
          end_time - start_time, "seconds")
    

#Ans 18
#Zombie Process
from multiprocessing import Process
import time
import os
def child_task():
    print("Child process started")
    print("Child PID:", os.getpid())
    print("Child process exiting")

if __name__ == "__main__":
    p = Process(target=child_task)
    p.start()
    print("\nParent process is sleeping WITHOUT join()")
    print("Parent PID:", os.getpid())
    time.sleep(10)
    print("\nNow parent calls join()")
    p.join()
    print("Child process cleaned successfully")

#Orphan Process
from multiprocessing import Process
import time
import os
def child_task():
    print("Child process started")
    print("Child PID:", os.getpid())
    for i in range(10):
        print("Child running...", i + 1)
        time.sleep(1)
    print("Child process finished")

if __name__ == "__main__":
    p = Process(target=child_task)
    p.start()
    print("Parent process exiting immediately")
    print("Parent PID:", os.getpid())