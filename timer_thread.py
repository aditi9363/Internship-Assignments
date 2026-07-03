import threading
import time

def message(text):
    print(text)

print("======Example 1: Starting and Cancelling a Timer======")

timer = threading.Timer(3,message, args=("Timer executed!",))

timer.start()

print("Timer started, doing other work...")

for i in range(3):
    print("Main thread working...", i + 1)
    time.sleep(0.5)

timer.cancel()

print("Timer cancelled before it could run.")

time.sleep(3)

print("\n======Example 2: Two Timers Running======")

timer1 = threading.Timer(2, message, args=("Timer 1 fired after 2 seconds.",))
timer2 = threading.Timer(4, message, args=("Timer 2 fired after 4 seconds.",))

timer1.start()
timer2.start()

print("Both timers started...")

timer1.join()
timer2.join()

print("Program finished.")