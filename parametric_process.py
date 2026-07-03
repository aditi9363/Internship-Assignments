from multiprocessing import Process
import time

def task(name, duration):
    print(f"{name} started")
    time.sleep(duration)
    print(f"{name} finished after {duration} seconds")

if __name__ == "__main__":
    p1=Process(target=task, args=("Process 1", 2))
    p2=Process(target=task, args=("Process 2", 4))
    p3=Process(target=task, args=("Process 3", 3))

    p1.start()
    p2.start()
    p3.start()

    p1.join()
    p2.join()
    p3.join()
    
    print("All processes completed")
        
        


