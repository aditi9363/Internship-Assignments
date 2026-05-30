import sys
import hashlib

text = sys.stdin.readline().strip()
md5_hash = hashlib.md5(text.encode()).hexdigest()
print(md5_hash)