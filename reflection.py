import shutil

source = "demo.txt"
destination = "copy_demo.txt"

shutil.copy(source, destination)

print("File copied successfully.")

# Comparison:

# Win32 API uses more lines of code, while Python built-in functions use fewer.
# Win32 API is Windows-only, whereas Python built-in functions are portable
# across Windows, Linux, and macOS.
# Win32 API is useful for Windows-specific features such as sharing modes,
# special flags, and exact error codes. Python built-in functions are better
# for general file operations because they are simpler and portable.