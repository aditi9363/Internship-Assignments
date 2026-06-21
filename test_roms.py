import unittest
import threading
import time

from models import MenuItem, Order, Status
from models import Bill
from rwlock import RWLock
from bounded_queue import BoundedQueue
from kitchen import waiter_thread, chef_thread, cashier_thread, completed_orders


# ==================================================
# TEST 1 : DATA LAYER
# ==================================================

class TestDataLayer(unittest.TestCase):

    def test_order_and_bill(self):
        item1 = MenuItem(
            1,
            "Soup",
            "Starter",
            100,
            10
        )

        item2 = MenuItem(
            2,
            "Burger",
            "Main",
            150,
            15
        )

        item3 = MenuItem(
            3,
            "Ice Cream",
            "Dessert",
            50,
            5
        )

        # Create order
        order = Order(
            "T1-001",
             1,
            [item1, item2, item3]
        )

        # Initial status
        self.assertEqual(
            order.status,
            Status.PENDING
        )

        # Move to COOKING
        order.advance_status()
        self.assertEqual(
            order.status,
            Status.COOKING
        )

        # Move to READY
        order.advance_status()
        self.assertEqual(
            order.status,
            Status.READY
        )

        # Create Bill (must be READY)
        bill = Bill(
            "B001",
            order
        )

        # Verify bill fields
        self.assertEqual(
            bill.bill_id,
            "B001"
        )

        self.assertEqual(
            bill.order,
            order
        )

        self.assertEqual(
            bill.subtotal,
            300
        )

        self.assertEqual(
            bill.tax,
            24.0
        )

        self.assertEqual(
            bill.total,
            324.0
        )

        # Move to BILLED
        order.advance_status()

        self.assertEqual(
            order.status,
            Status.BILLED
        )

        # Verify order data
        self.assertEqual(
            order.total_price(),
            300
        )

        self.assertEqual(
            order.estimated_wait(),
            30
        )

        self.assertEqual(
            len(order.items),
            3
        )

# ==================================================
# TEST 2 : CONCURRENCY
# ==================================================

class TestConcurrency(unittest.TestCase):

    def test_kitchen_system(self):
        stop_event = threading.Event()

        rwlock = RWLock()

        order_queue = BoundedQueue(maxsize=20)
        ready_queue = BoundedQueue(maxsize=20)

        bill_counter = [0]
        bill_lock = threading.Lock()

        order_timers = {}

        menu = [
            MenuItem(1, "Soup", "Starter", 100, 1),
            MenuItem(2, "Burger", "Main", 150, 1),
            MenuItem(3, "Ice Cream", "Dessert", 50, 1)
        ]

        waiters = [
            threading.Thread(
                target=waiter_thread,
                args=(
                    i + 1,
                    menu,
                    order_queue,
                    stop_event,
                    rwlock,
                    order_timers
                )
            )
            for i in range(2)
        ]

        chefs = [
            threading.Thread(
                target=chef_thread,
                args=(
                    i + 1,
                    order_queue,
                    ready_queue,
                    stop_event,
                    rwlock,
                    order_timers,
                    [None]
                )
            )
            for i in range(2)
        ]

        cashier = threading.Thread(
            target=cashier_thread,
            args=(
                ready_queue,
                bill_counter,
                bill_lock,
                stop_event
            )
        )

        for t in waiters + chefs:
            t.start()

        cashier.start()

        time.sleep(10)

        stop_event.set()

        for t in waiters + chefs:
            t.join()

        cashier.join()

        self.assertGreater(
            len(completed_orders),
            0
        )

        self.assertGreater(
            bill_counter[0],
            0
        )

        for order in completed_orders:
            self.assertIn(
                order.status,
                list(Status)
            )

# ==================================================
# TEST 3 : RWLOCK
# ==================================================

class TestRWLock(unittest.TestCase):

    def test_rwlock(self):

        rwlock = RWLock()

        shared_counter = 0

        WRITERS = 3
        INCREMENTS = 1000

        def reader():
            for _ in range(100):
                with rwlock.read_lock_context():
                    _ = shared_counter

        def writer():
            nonlocal shared_counter

            for _ in range(INCREMENTS):
                with rwlock.write_lock_context():
                    shared_counter += 1

        readers = [
            threading.Thread(target=reader)
            for _ in range(10)
        ]

        writers = [
            threading.Thread(target=writer)
            for _ in range(WRITERS)
        ]

        for t in readers + writers:
            t.start()

        for t in readers + writers:
            t.join()

        expected = WRITERS * INCREMENTS

        self.assertEqual(shared_counter, expected)


# ==================================================
# TEST 4 : BOUNDED QUEUE
# ==================================================

class TestBoundedQueue(unittest.TestCase):

    def test_queue_blocks(self):

        queue = BoundedQueue(maxsize=3)

        # Fill queue completely
        queue.put(1)
        queue.put(2)
        queue.put(3)

        producer_finished = threading.Event()

        start_time = 0
        end_time = 0

        def producer():
            nonlocal start_time, end_time

            start_time = time.time()

            queue.put(4)

            end_time = time.time()

            producer_finished.set()

        producer_thread = threading.Thread(
            target=producer
        )

        producer_thread.start()

        # Wait 1 second before freeing slot
        time.sleep(1)

        queue.get()

        producer_finished.wait()

        producer_thread.join()

        block_time = end_time - start_time

        self.assertGreaterEqual(block_time, 1)


if __name__ == "__main__":
    unittest.main()