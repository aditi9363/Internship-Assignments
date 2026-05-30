import mmap
import json
data = {
    "name": "Virat",
    "age": 23,
    "city": "Pune"
}

json_text = json.dumps(data)
with open("shared_data.bin", "wb") as file:
    file.write(b"\0" * 512)

with open("shared_data.bin", "r+b") as file:
    mm = mmap.mmap(file.fileno(), 512)

    mm.seek(0)
    mm.write(json_text.encode())

    mm.flush()
    mm.close()

open("ready.flag", "w").close()
print("Data written successfully.")