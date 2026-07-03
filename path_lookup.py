import os
import shutil

py_path = shutil.which("python")

if py_path is None:
    print("Python executable not found in PATH")
else:
    print("Python found at:", py_path)

    exit_code = os.spawnv(
        os.P_WAIT,
        py_path,
        ["python", "--version"]
    )

    print("Exit code:", exit_code)

    if exit_code == 0:
        print("Python executed successfully.")
    else:
        print("Python execution failed.")

# shutil.which("python") searches the system path & returns the full path 
# of python.exe.
# This is the portable way to locate an executable because different systems 
# & installations may store programs in different directories.
# Using the returned full path with os.spawnv() ensures the correct executable is 
# launched without hardcoding its location. 

