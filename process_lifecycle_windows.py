import subprocess
import multiprocessing
import time

def worker():
    print("Child process started...")
    time.sleep(5)           #Keep child alive for 5 seconds
    print("Child process finished.")

if __name__ == "__main__":
    print("========== PART 1 ==========")
    print("Detached process example")

    detached = subprocess.Popen(
        ["python", "-c", "import time; time.sleep(15)"],
        creationflags=subprocess.DETACHED_PROCESS
    )

    print("Detached child started with PID:", detached.pid)
    print("This child will continue running independently.")
    print()

    #-------------------------------------------------------------
    print("========== PART 2 ==========")
    print("Multiprocessing cleanup example")

    p = multiprocessing.Process(target=worker)
    p.start()

    print("\nActive chidren after start():")
    print(multiprocessing.active_children())

    time.sleep(2)

    print("\nChild is still running because join() has not been called.")

    p.join()

    print("\njoin() completed.")

    print("Active children after join():")
    print(multiprocessing.active_children())

    print("\nMain program finished.")

# Why Unix-style zombies do not occur on Windows:
# Windows automatically cleans up a child process after it exits.
# Therefore, Windows does not create "zombie" processes like Unix/Linux.

# Why you should still use join()/wait() children:
# Even though Windows does not create zombie processes,
# the parent process should still call join() (or wait())
# to wait for the child process to finish.
# This ensures proper program execution & resource cleanup.

# Observe running processes using Task Manager
# or the command: tasklist | findstr python