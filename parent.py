import subprocess
process = subprocess.Popen(
    ["python", "child.py"],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    text=True
)
output, _ = process.communicate("Hello World\n")
print("MD5 Hash:", output.strip())