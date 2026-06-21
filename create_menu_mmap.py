import json
from mmap_menu import write_menu_mmap

with open("menu.json", "r") as f:
    menu_data = json.load(f)

write_menu_mmap(
    "menu.mmap",
    menu_data
)

print("menu.mmap created")