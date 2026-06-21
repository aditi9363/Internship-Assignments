from multiprocessing.shared_memory import SharedMemory
import ctypes
from models import Status

def create_board(shm_name, size=16):
   
    shm = SharedMemory(
        name=shm_name,
        create=True,
        size=size
    )

    counts = (ctypes.c_uint * 4).from_buffer(shm.buf)

    counts[0] = 0  # pending
    counts[1] = 0  # cooking
    counts[2] = 0  # ready
    counts[3] = 0  # billed

    del counts
    
    return shm

def update_board(shm, active_orders, rwlock):

    pending = 0
    cooking = 0
    ready = 0
    billed = 0

    with rwlock.read_lock_context():

        for order in active_orders.values():

            if order.status == Status.PENDING:
                pending += 1

            elif order.status == Status.COOKING:
                cooking += 1

            elif order.status == Status.READY:
                ready += 1

            elif order.status == Status.BILLED:
                billed += 1

    counts = (ctypes.c_uint * 4).from_buffer(shm.buf)

    counts[0] = pending
    counts[1] = cooking
    counts[2] = ready
    counts[3] = billed

    del counts