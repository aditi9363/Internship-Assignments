from models import MenuItem, Order, Bill

#-----------------Create MenuItems---------------
item1 = MenuItem(
    "M001",
    "Garlic Bread",
    "Starter",
    4.50,
    300
)
item2 = MenuItem(
    "M002",
    "Grilled Chicken",
    "Main",
    14.99,
    900
)

#------------------Create Order-----------------
order1 = Order(
    "ORD-001",
    1,
    [item1, item2]
)

order1.advance_status()
order1.advance_status()
print("Current Order Status:", order1.status.value)

#--------------Create Bill-----------------
bill1 = Bill(
    "BILL-001",
    order1
)

bill1.print_receipt()

#----------------Testing RuntimeError-----------------
print("\nTesting Bill creation for PENDING order:")

pending_order = Order(
    "ORD-002",
    2,
    [item1]
)

try:
    wrong_bill = Bill(
        "BILL-002",
        pending_order
    )
except RuntimeError as e:
    print("Error:", e)

#--------------------Test Menu Loader----------------------
from models import load_menu

menu = load_menu("menu.json")
print(f"\nLoaded {len(menu)} menu items.")

for item in menu.values():
    print(item)