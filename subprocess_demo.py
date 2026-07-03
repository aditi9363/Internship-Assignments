import subprocess
import os

#Launch a simple command using subprocess.run()
print("Running a simple command...\n")
subprocess.run(["cmd", "/c", "echo", "hello"])
print("\nSimple command finished")

custom_env = {
    **os.environ,
    "MY_VAR": "hello"
}
print("\nRunning command with custom environment...\n")

#Run command & capture its output
result = subprocess.run(
    ["cmd", "/c", "set", "MY_VAR"],
    env=custom_env,
    capture_output=True,
    text=True
)
print("Captured Output:")
print(result.stdout)

# subprocess is the recommended modern replacement
# for both os.spawn* and the Unix fork+exec pattern.
# It is simpler, safer, and supports custom environments
# using the env parameter.