import os
import shutil

from file_handler import FileHandler

demo_folder = "_demo"

if not os.path.exists(demo_folder):
    os.mkdir(demo_folder)

#------------------File Path---------------------
file_path = os.path.join(demo_folder, "demo.txt")

#--------------Create FileHandler object--------------
fh = FileHandler(file_path)

print("\n========== CREATE ==========")
fh.create()

print("\n========== WRITE ==========")
fh.write("Hello World from Win32 API!")
fh.close()

print("\n========== OPEN ==========")
fh.open()

print("\n========== READ ==========")
text = fh.read()

print("File Content:")
print(text)

fh.close()

print("\n========== FILE INFO ==========")

info = fh.get_file_info()

for key, value in info.items():
    print(f"{key}: {value}")

print("\n========== COPY ==========")

copy_path = os.path.join(demo_folder, "copy_demo.txt")

fh.copy(copy_path)

print("Copied to:", copy_path)

print("\n========== RENAME ==========")

copy_handler = FileHandler(copy_path)

new_copy = copy_handler.rename("renamed_copy.txt")

print("Renamed to:", new_copy)

print("\n========== MOVE ==========")

# Create backup folder
backup_folder = os.path.join(demo_folder, "backup")

if not os.path.exists(backup_folder):
    os.mkdir(backup_folder)

# Destination path
destination = os.path.join(
    backup_folder,
    "renamed_copy.txt"
)

# Move the file
copy_handler.move(destination)

print("Moved to:", destination)

print("\n========== CONTEXT MANAGER ==========")

with FileHandler(file_path) as file:
    file.open("r")
    print("File Content:")
    print(file.read())

print("\n========== DELETE ==========")

# Delete original file
print("Deleting demo.txt...")
fh.delete()

# Delete moved file
backup_file = FileHandler(destination)

print("Deleting renamed_copy.txt...")
backup_file.delete()

print("Files deleted successfully.")

print("\n========== CLEANUP ==========")

# Remove backup folder
if os.path.exists(backup_folder):
    os.rmdir(backup_folder)
    print("Backup folder removed.")

# Remove demo folder
if os.path.exists(demo_folder):
    os.rmdir(demo_folder)
    print("Demo folder removed.")