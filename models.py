from enum import Enum
from datetime import datetime
import json

class Status(Enum):
    PENDING = "PENDING"
    COOKING = "COOKING"
    READY = "READY"
    BILLED = "BILLED"
    CANCELLED = "CANCELLED"
    
class MenuItem:
    Valid_Categories = {"Starter", "Main", "Dessert", "Drink"}

    def __init__(self, item_id, name, category, price, prep_time_sec):
        if price <= 0:
            raise ValueError("Price must be greater than 0")
        
        if prep_time_sec < 0:
            raise ValueError("Preparation time cannot be negative")
        
        if category not in MenuItem.Valid_Categories:
            raise ValueError(
                "Category must be one of Starter, Main, Dessert, Drink."
            )
        
        self.item_id = item_id
        self.name = name
        self.category = category
        self.price = price
        self.prep_time_sec = prep_time_sec

    def __repr__(self):
        return f"[{self.category}] {self.name} - ${self.price:.2f} ({self.prep_time_sec} s)"
    
#-----------------Status Enum------------------
class Status(Enum):
    PENDING = "PENDING"
    COOKING = "COOKING"
    READY = "READY"
    BILLED = "BILLED"
    CANCELLED = "CANCELLED"

#-----------------Order Class-------------------
class Order:
    STATUS_FLOW = [
        Status.PENDING,
        Status.COOKING,
        Status.READY,
        Status.BILLED,
        Status.CANCELLED
    ]

    def __init__(self, order_id, table_no, items):
        if len(items) == 0:
            raise ValueError("Order cannot be empty")
        self.order_id = order_id
        self.table_no = table_no
        self.items = items
        self.status = Status.PENDING
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def cancel(self):
        if self.status == Status.PENDING:
            self.status = Status.CANCELLED
            self.updated_at = datetime.now()
            print(f"Order {self.order_id} cancelled due to timeout.")
 
    

    
    def advance_status(self):
        if self.status == Status.PENDING:
            self.status = Status.COOKING
        elif self.status == Status.COOKING:
            self.status = Status.READY
        elif self.status == Status.READY:
            self.status = Status.BILLED
        else:
            print("No further status change possible")

        self.updated_at = datetime.now()

    def total_price(self):
        return sum(item.price for item in self.items)
    
    def estimated_wait(self):
        return sum(item.prep_time_sec for item in self.items)
    
    def __str__(self):
        return self.order_id

#---------------Bill Class-------------------
TAX_RATE = 0.08

class Bill:
        def __init__(self, bill_id, order):
             if order.status != Status.READY:
                  raise RuntimeError(
                       "Bill can only be generated for READY orders."
                  )
             
             self.bill_id = bill_id
             self.order = order

             self.subtotal = sum(item.price for item in order.items)

             self.subtotal = order.total_price()
             self.tax = self.subtotal * 0.08
             self.total = self.subtotal + self.tax

             self.issued_at = datetime.now()

        def print_receipt(self):
            print("=" * 44)
            print("             ROMS Restaurant - Receipt")
            print(f"Bill: {self.bill_id}")
            print(f"Table: {self.order.table_no}")
            print("=" * 44)

            for item in self.order.items:
                print(f"{item.name:<30} ${item.price:>8.2f}")

            print("-" * 44)
            print(f"{'Subtotal:':<32} ${self.subtotal:>8.2f}")
            print(f"{'Tax (8%):':<32} ${self.tax:>8.2f}")
            print(f"{'TOTAL:':<32} ${self.total:>8.2f}")
            print("=" * 44)
            print("Issued At:", self.issued_at.strftime("%d-%m-%Y %H:%M:%S"))
            print("=" * 44)
        
        #current_index = Order.STATUS_FLOW.index(self.status)
        #self.status = Order.STATUS_FLOW[current_index + 1]
        #self.updated_at = datetime.now()

def load_menu(filepath):
    try:
        with open(filepath, "r") as file:
            data = json.load(file)

        menu = {}

        for item in data:
            menu_item = MenuItem(
                item["item_id"],
                item["name"],
                item["category"],
                item["price"],
                item["prep_time_sec"]
            )
            menu[item["item_id"]] = menu_item

        return menu
    except FileNotFoundError:
        print("Error: Menu file not found")
        return {}
    
    except json.JSONDecodeError:
        print("Error: Invalid JSON format")
        return {}

def cancel(self):
    if self.status in [Status.PENDING, Status.COOKING]:
        self.updated_at = datetime.now()
    else:
        raise RuntimeError(
             "Order can only be cancelled when PENDING or COOKING"
        )
        
def total_price(self):
    total = 0
    for item in self.items:
        total += item.price
    return total
    
def estimated_wait(self):
    max_time = 0
    for item in self.items:
        if item.prep_time_sec > max_time:
            max_time = item.prep_time_sec
    return max_time
    
#----------------------Testing-------------------------
item1 = MenuItem("101", "Pizza", "Main", 250.0, 20)
item2 = MenuItem("102", "Coke", "Drink", 50.0, 5)

order = Order("T1-001", 1, [item1, item2])
print("Order", order.order_id, "created.")
print("Status:", order.status.value)

order.advance_status()
print("Advanced to:", order.status.value)

order.advance_status()
print("Advanced to:", order.status.value)

order.advance_status()
print("Advanced to:", order.status.value)

try:
    order.advance_status()
except RuntimeError as e:
    print("Caught expected error:", e)

print("Total Price:", order.total_price())
print("Estimated Wait Time:", order.estimated_wait(), "seconds")

def to_dict(self):
    return {
        "item_id" : self.item_id,
        "name" : self.name,
        "category" : self.category,
        "price" : self.price,
        "prep_time_sec" : self.prep_time_sec
    }
if __name__ == "__main__":
    item1 = MenuItem("S101", "Garlic Bread", "Starter", 4.50, 300)
    item2 = MenuItem("M101", "Grilled Chicken", "Main", 14.99, 900)
    item3 = MenuItem("D101", "Chocolate Mousse", "Dessert", 6.00, 120)
    item4 = MenuItem("DR101", "Lemonade", "Drink",  2.50, 30)

    #print(item1)
    #print(item2)
    #print(item3)
    #print(item4)