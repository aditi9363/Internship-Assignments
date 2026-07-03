import subprocess

result = subprocess.run(
    ['cmd', '/c', 'dir'],
    capture_output=True,
    text=True
)
print("Directory Listing:")
print(result.stdout)

#Check whether command succeeded
if result.returncode == 0:
    print("Command executed successfully")
else:
    print("Command failed")

#Run a command that intentionally fails
failed_result = subprocess.run(
    ['cmd', '/c', 'dir', '//nope'],
    capture_output=True,
    text=True
)

if failed_result.returncode != 0:
    print("The second command failed as expected.")
    print("Error message:")
    print(failed_result.stderr)

