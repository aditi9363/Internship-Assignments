from multiprocessing.shared_memory import SharedMemory
import ctypes
import time

BOARD_NAME = "restaurant_board"

shm = SharedMemory(
    name=BOARD_NAME,
    create=False
)

counts = (ctypes.c_uint * 4).from_buffer(shm.buf)

try:

    previous = None

    while True:

        current = (
            counts[0],
            counts[1],
            counts[2],
            counts[3]
        )

        if current != previous:

            print("\n===== LIVE ORDER BOARD =====")

            print("Pending :", counts[0])
            print("Cooking :", counts[1])
            print("Ready   :", counts[2])
            print("Billed  :", counts[3])

            print("============================")

            previous = current

        if current == (0, 0, 0, 0):

            print("\nBoard reset detected.")
            print("Kitchen system stopped.")

            break

        time.sleep(2)

except KeyboardInterrupt:
    pass

finally:
    del counts
    shm.close()