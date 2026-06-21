from mmap_menu import load_menu_mmap

menu = load_menu_mmap("menu.mmap")

print("Reader 1")

for item in menu:
    print(item.item_id, item.name, item.price)