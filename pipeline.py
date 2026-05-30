import subprocess
sentence = "hello world from python pipeline"

stage1 = subprocess.Popen(
    ["python", "stage1.py"],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    text=True
)


stage2 = subprocess.Popen(
    ["python", "stage2.py"],
    stdin=stage1.stdout,
    stdout=subprocess.PIPE,
    text=True
)
stage1.stdin.write(sentence)
stage1.stdin.close()
result = stage2.communicate()[0]
print("Word Count:", result.strip())