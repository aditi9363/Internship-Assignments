import multiprocessing
import os

def child(child_number):
    print(f"I am Child {child_number}")
    print(f"Child PID: {os.getpid()}")

if __name__ == "__main__":
    processes = []

    for i in range(1, 4):
        proc = multiprocessing.Process(target=child, args=(i,))
        processes.append(proc)

    for proc in processes:
        proc.start()

    for index, proc in enumerate(processes, start=1):
        proc.join()
        print(f"Parent: Child {index} finished with Exitcode = {proc.exitcode}")

    print("Active Children:", multiprocessing.active_children())
