import threading
import queue
import random
import time
import ctypes
from rwlock import RWLock
from itertools import count
from bounded_queue import BoundedQueue
import signal
from tcp_terminal import start_order_server
from order_board import create_board, update_board
from mmap_menu import load_menu_mmap
from kds_pipe import create_kds_server
from kds_pipe import write_to_kds
from logger import log_event
import win32file

from models import MenuItem, Order, Bill, Status

import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(message)s",
    handlers=[
        logging.FileHandler("roms.log"),
        logging.StreamHandler()
    ]
)

kitchen_semaphore = threading.Semaphore(3)
shutdown_event = threading.Event()

stats_lock = threading.Lock()

total_submitted = 0
total_completed = 0
total_cancelled = 0
total_revenue = 0.0

active_orders = {}
order_timers = {}

rwlock = RWLock()

stop_event = threading.Event()

completed_orders = []

RUN_DURATION = 60

def setup_order_timeout(order, rwlock, timeout_sec):
    def timeout_callback(order):
        with rwlock.write_lock_context():

            #Check if order is still waiting
            if order.status.name == "PENDING":
                order.cancel()
                
                print(
                    f"Timeout: Order {order.order_id} cancelled"
                )

    timer = threading.Timer(
        timeout_sec,
        timeout_callback,
        args=(order,)
    )
    timer.start()
    return timer

def chef_thread(chef_id, order_queue, ready_queue, stop_event, rwlock, order_timers, kds_pipe_handle):
    while not stop_event.is_set() or not order_queue.empty():
        
        try:
            order = order_queue.get(timeout=1)

            print(f"Chef {chef_id}: waiting for kitchen slot...")
            print(f"[Before Acquire] Available slots: {kitchen_semaphore._value}")

            acquired = kitchen_semaphore.acquire(timeout=1)
            if not acquired:
                if stop_event.is_set():
                    break
                continue

            print(f"[After Acquire] Chef {chef_id} entered kitchen. "
                  f"Available slots: {kitchen_semaphore._value}")
            
            try:
                # PENDING -> COOKING
                with rwlock.write_lock_context():
                    if order.status == Status.CANCELLED:
                        print(
                            f"Chef {chef_id}: skipping cancelled order {order.order_id}"
                        )
                        continue
                    timer = order_timers.pop(order.order_id, None)
                    if timer:
                        timer.cancel()
                    order.advance_status()      #PENDING -> COOKING
                    log_event(
                        "INFO",
                         f"Chef {chef_id}: cooking {order.order_id}"
                    )

                stop_event.wait(1)
                
                for item in order.items:
                    if stop_event.is_set():
                        break
                    stop_event.wait(item.prep_time_sec / 10)
                        

                 # COOKING -> READY
                with rwlock.write_lock_context():
                    if order.status == Status.COOKING:
                        order.advance_status()   #COOKING -> READY
                        if kds_pipe_handle[0] is not None:
                            write_to_kds(
                                kds_pipe_handle[0],
                                order
                            )
                        
                        ready_queue.put(order)
                        
                    else:
                        print(f"Chef {chef_id}: order {order.order_id} was cancelled")
                    

            finally:
                kitchen_semaphore.release()
                print(f"[Release] Chef {chef_id} left kitchen. "
                      f"Available slots: {kitchen_semaphore._value}")
        except TimeoutError:
            continue

        except Exception as e:
            print(f"Chef {chef_id} Error: {e}")
            
    print(f"Chef {chef_id} exited.")

def cashier_thread(ready_queue, bill_counter, bill_lock, stop_event):
    global completed_orders
    while not stop_event.is_set() or not ready_queue.empty():
        
        try:
            order = ready_queue.get(timeout=1)

            if order.status != Status.READY:
                print(
                    f"Cashier: skipping {order.order_id} "
                    f"(status={order.status.value})"
                )
                
                continue

            with bill_lock:
                bill_counter[0] += 1
                completed_orders.append(order)
                bill_id = f"BILL-{bill_counter[0]:03d}"

            bill = Bill(bill_id, order)
            bill.print_receipt()

            with rwlock.write_lock_context():
                time.sleep(10)
                order.advance_status()      #READY -> BILLED

            global total_completed
            global total_revenue

            with stats_lock:
                total_completed += 1
                total_revenue += order.total_price()
                
            log_event(
                "INFO",
                f"Cashier: billed {order.order_id}"
            )

            
        except (TimeoutError,queue.Empty):
            continue
    print("Cashier exited.")


def waiter_thread(table_no, menu, order_queue, stop_event, rwlock, order_timers):
    order_counter = count(1)
    while not stop_event.is_set():
        if stop_event.is_set():
            print(f"Waiter {table_no}: shutting down...")
            break

        time.sleep(random.randint(1, 2))

        if stop_event.is_set():
            break

        #Randomly choose 1 to 3 items
        num_items = random.randint(1, 3)
        selected_items = random.sample(menu, num_items)

        # Generate unique order ID
        order_id = f"T{table_no}-{next(order_counter):03d}"

        order = Order(
            order_id=order_id,
            table_no=table_no,
            items=selected_items
        )

        with rwlock.write_lock_context():
            active_orders[order_id] = order

        #Start timeout timer
        order_timers[order.order_id] = setup_order_timeout(
            order,
            rwlock,
            15
        )
     
        #Put order into the queue
        order_queue.put(order)

        #Print info
        log_event(
            "INFO",
            f"Waiter {table_no}: submitted order"
        )
        global total_submitted
        with stats_lock:
            total_submitted += 1
    print(f"Waiter {table_no} exited.")

def manager_thread(stop_event):
    while not stop_event.is_set():

        #Read active orders safely
        with rwlock.read_lock_context():
            summary = {
                "PENDING": 0,
                "COOKING": 0,
                "READY": 0,
                "BILLED": 0,
                "CANCELLED": 0
            }
            for order in active_orders.values():
                summary[order.status.value] += 1

        print("\n---------Manager Summary---------")
        for status,count in summary.items():
            print(f"{status} : {count}")
        print("-------------------------\n")

        time.sleep(1)

def board_updater(shm, active_orders, rwlock, stop_event):

    while not stop_event.is_set():

        update_board(
            shm,
            active_orders,
            rwlock
        )

        time.sleep(2)
    print("Board updater exited.")

def start_kds_server(pipe_holder):

    pipe_holder[0] = create_kds_server()

def drain_order_queue(order_queue):
    global total_cancelled

    while True:
        try:
            order = order_queue.get(timeout=0)

            order.status = Status.CANCELLED

            with stats_lock:
                total_cancelled += 1

            print(f"Cancelled: {order.order_id}")

        except (TimeoutError, queue.Empty):
            break

def drain_ready_queue(ready_queue):
    global total_completed
    global total_revenue

    while True:
        try:
            order = ready_queue.get_nowait()

            print(f"Final billing: {order.order_id}")

            bill = Bill(f"FINAL-{order.order_id}", order)
            bill.print_receipt()

            with stats_lock:
                total_completed += 1
                total_revenue += order.total_price()

        except queue.Empty:
            break

def cancel_pending_orders():
    global total_cancelled

    with rwlock.write_lock_context():

        for order in active_orders.values():

            if order.status == Status.PENDING:
                order.cancel()

                with stats_lock:
                    total_cancelled += 1

                print(
                    f"Shutdown cancel: {order.order_id}"
                )

def print_final_summary():
    print("\n" + "=" * 50)
    print("FINAL SYSTEM SUMMARY")
    print("=" * 50)

    print(f"Total Submitted : {total_submitted}")
    print(f"Total Completed : {total_completed}")
    print(f"Total Cancelled : {total_cancelled}")
    print(f"Total Revenue   : ${total_revenue:.2f}")

    print("=" * 50)

#----------------------------Main Program----------------------------
def main():
    print("*************MAIN STARTED*************")

    menu = load_menu_mmap("menu.mmap")
    
    #Create queues
    order_queue = BoundedQueue(maxsize=10)

    ready_queue = queue.Queue()

    #Shared bill counter & lock
    bill_counter = [0]
    bill_lock = threading.Lock()

    print("Before create_board()")
    BOARD_NAME = "restaurant_board"
    shm = create_board(BOARD_NAME)
    print("After create_board()")
 
    kds_pipe_handle = [None]

    kds_thread = threading.Thread(
        target=start_kds_server,
        args=(kds_pipe_handle,),
        daemon=True
    )

    kds_thread.start()

    board_thread = threading.Thread(
        target=board_updater,
        args=(shm, active_orders, rwlock, stop_event),
        daemon=True
    )
    board_thread.start()

    #Create waiter thread
    waiters = []
    for table in range(1, 11):
        waiter = threading.Thread(
            target=waiter_thread,
            args=(table, menu, order_queue, stop_event, rwlock, order_timers),
            name=f"Waiter-{table}"
        )
        waiters.append(waiter)

    #Create chef thread
    chefs = []
    for chef_id in range(1, 4):
        chef = threading.Thread(
            target=chef_thread,
            args=(chef_id, order_queue, ready_queue, stop_event, rwlock, order_timers, kds_pipe_handle),
            name=f"Chef-{chef_id}"
        )
        chefs.append(chef)

    #Create cashier thread
    cashier = threading.Thread(
        target=cashier_thread,
        args=(ready_queue, bill_counter, bill_lock, stop_event)
    )

    manager = threading.Thread(
        target=manager_thread,
        args=(stop_event,),
        daemon=True
    )

    tcp_thread = threading.Thread(
        target=start_order_server,
        args=(
            "localhost",
            5000,
            order_queue,
            stop_event
        ),
        daemon=True
    )

    tcp_thread.start()
    
    for waiter in waiters:
        waiter.start()

    for chef in chefs:
        chef.start()

    cashier.start()
    manager.start()

    try:
        print(f"\nSystem running for {RUN_DURATION} seconds...")
        start_time = time.time()

        while time.time() - start_time < RUN_DURATION:
            time.sleep(1)
        print("\nRun duration reached.")

    except KeyboardInterrupt:
        print("\nCtrl+C detected.")

    finally:

        print("Step-1")
        print("A: Setting stop event...")
        stop_event.set()

        print("Step-2")
        for timer in order_timers.values():
            timer.cancel()
        order_timers.clear()

        print("Step-3")
        for waiter in waiters:
            waiter.join(timeout=10)
        print("All waiters finished.")
        print("Orders left in queue:", order_queue.qsize())

        #order_queue.join()
        #print("All orders cooked.")

        #ready_queue.join()
        #print("All orders billed.")

        print("Step-4")
        for chef in chefs:
            chef.join(timeout=10)
        print("All chefs finished")

        print("Step-5")
        cashier.join(timeout=10)
        if cashier.is_alive():
            print("Cashier still running")
        else:
            print("Cashier finished")

        print("Step-6")
        board_thread.join(timeout=10)

        print("Step-7")
        tcp_thread.join(timeout=10)

        print("Step-8")
        drain_order_queue(order_queue)

        print("Step-9")
        drain_ready_queue(ready_queue)

        print("Step-9.5")
        cancel_pending_orders()

        print("\nFINAL ORDER STATES")

        with rwlock.read_lock_context():
            for order_id, order in active_orders.items():
                print(
                    order_id,
                    order.status
                )

        if kds_pipe_handle[0]:
            win32file.CloseHandle(kds_pipe_handle[0])
            print("Named pipe closed.")
            
        update_board(shm, active_orders, rwlock)
        print("Cleaning shared memory...")

        counts = (ctypes.c_uint * 4).from_buffer(shm.buf)

        counts[0] = 0
        counts[1] = 0
        counts[2] = 0
        counts[3] = 0

        del counts

        shm.close()
        shm.unlink()
    
        throughput = total_completed / RUN_DURATION

        print(
            f"\nThroughput: {throughput:.2f} orders/sec"
        )
        
        print("Step-10")
        print_final_summary()
    
#Run the program
if __name__ == "__main__":
    main()