import mmap
import json
from models import MenuItem


def write_menu_mmap(filepath, menu_dict):

    json_bytes = json.dumps(
        menu_dict,
        indent=4
    ).encode("utf-8")

    with open(filepath, "wb") as f:
        f.write(b"\x00" * len(json_bytes))

    with open(filepath, "r+b") as f:

        mm = mmap.mmap(
            f.fileno(),
            len(json_bytes)
        )

        mm.seek(0)
        mm.write(json_bytes)
        mm.flush()
        mm.close()


def load_menu_mmap(filepath):

    with open(filepath, "rb") as f:

        mm = mmap.mmap(
            f.fileno(),
            0,
            access=mmap.ACCESS_READ
        )

        data = json.loads(
            mm.read().decode("utf-8")
        )

        mm.close()

    menu = []

    for item in data:
        menu.append(
            MenuItem(
                item["item_id"],
                item["name"],
                item["category"],
                item["price"],
                item["prep_time_sec"]
            )
        )
    return menu
