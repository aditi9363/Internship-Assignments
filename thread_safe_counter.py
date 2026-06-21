import threading
import time

bill_counter = 0

bill_lock = threading.Lock()
INCREMENTS = 4

#---------------------WITHOUT Lock----------------------
def cashier_without_lock():
    global bill_counter

    for i in range(INCREMENTS):
        temp = bill_counter     # Read current value
        time.sleep(0)           # Force thread switching
        temp = temp + 1         # Increment
        bill_counter = temp      # Write back

#---------------------WITH Lock-------------------------
def cashier_with_lock():
    global bill_counter

    for i in range(INCREMENTS):
        with bill_lock:          #Only one thread enters at a time
            temp = bill_counter
            time.sleep(0)
            temp = temp + 1
            bill_counter = temp

#------------------Testing WITHOUT Lock-----------------
bill_counter = 0
threads = []

for i in range(5):
    t = threading.Thread(target=cashier_without_lock)
    threads.append(t)
    t.start()

for t in threads:
    t.join()

print("WITHOUT Lock - Expected: 20, Got:", bill_counter)

#-------------------Testing WITH Lock---------------------
bill_counter = 0
threads = []

for i in range(5):
    t = threading.Thread(target=cashier_with_lock)
    threads.append(t)
    t.start()

for t in threads:
    t.join()

print("WITH Lock - Expected: 20, Got:", bill_counter)


