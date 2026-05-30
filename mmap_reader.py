import mmap
import json
import os
import time
while not os.path.exists("ready.flag"):
    time.sleep(1)

with open("shared_data.bin", "r+b") as file:
    mm = mmap.mmap(file.fileno(), 512)
    data_bytes = mm.read(512)

    json_text = data_bytes.decode().strip("\0")
    data = json.loads(json_text)

    print("Received Data:")
    print(data)

    mm.close()

os.remove("ready.flag")
print("Reading completed.")