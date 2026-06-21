import random
import time
import threading

NUM_TABLES = 5
NUM_CHEFS = 3

total_participants = NUM_TABLES + NUM_CHEFS + 1 + 1 + 1

startup_barrier = threading.Barrier(total_participants)

def waiter_thread(waiter_id):
    print(f"Waiter {waiter_id} setting up...")
    time.sleep(random.uniform(0, 2))
    print(f"Waiter {waiter_id} ready")

    try:
        startup_barrier.wait()
    except threading.BrokenBarrierError:
        print(f"Waiter {waiter_id}: Barrier broken")
        return
    
    print(f"Waiter {waiter_id} started working")

def chef_thread(chef_id):
    print(f"Chef {chef_id} setting up...")
    time.sleep(random.uniform(0, 2))
    print(f"Chef {chef_id} ready")

    try:
        startup_barrier.wait()
    except threading.BrokenBarrierError:
        print(f"Chef {chef_id}: Barrier broken")
        return
    
    print(f"Chef {chef_id} started cooking")

def cashier_thread():
    print("Cashier setting up...")
    time.sleep(random.uniform(0, 2))
    print("Cashier ready")

    try:
        startup_barrier.wait()
    except threading.BrokenBarrierError:
        print("Cashier: Barrier broken")
        return
    
    print("Cashier started billing")

def manager_thread():
    print("Manager setting up...")
    time.sleep(random.uniform(0, 2))
    print("Manager ready")

    try:
        startup_barrier.wait()
    except threading.BrokenBarrierError:
        print("Manager: Barrier broken")
        return
    
    print("Manager started monitoring")

def main():
    threads = []

    #Start Waiters
    for i in range(NUM_TABLES):
        t = threading.Thread(
            target=waiter_thread,
            args=(i+1,)
        )
        t.start()
        threads.append(t)

    #Start Chefs
    for i in range(NUM_CHEFS):
        t = threading.Thread(
            target=chef_thread,
            args=(i+1,)
        )
        t.start()
        threads.append(t)

    #Cashier
    cashier = threading.Thread(
        target=cashier_thread
    )
    cashier.start()
    threads.append(cashier)

    #Manager
    manager = threading.Thread(
        target=manager_thread
    )
    manager.start()
    threads.append(manager)

    #Main thread also waits
    try:
        startup_barrier.wait()
        print("\nAll workers ready. Restaurant is OPEN!\n")
    except threading.BrokenBarrierError:
        print("Main thread: Barrier broken")

    for t in threads:
        t.join()

if __name__ == "__main__":
    main()

    