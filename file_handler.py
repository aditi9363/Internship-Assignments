import ctypes
from ctypes import wintypes
import os
from datetime import datetime

kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)

GENERIC_READ = 0x80000000
GENERIC_WRITE = 0x40000000

FILE_SHARE_READ = 0x00000001
CREATE_ALWAYS = 2
OPEN_EXISTING = 3

FILE_ATTRIBUTE_NORMAL = 0x00000080

INVALID_HANDLE_VALUE = wintypes.HANDLE(-1).value

MOVEFILE_REPLACE_EXISTING = 0x00000001

MOVEFILE_COPY_ALLOWED = 0x00000002

FILE_ATTRIBUTE_DIRECTORY = 0x10

FILE_ATTRIBUTE_READONLY = 0x01

GetFileExInfoStandard = 0

#CreateFileW
kernel32.CreateFileW.argtypes = [
    wintypes.LPCWSTR,
    wintypes.DWORD,
    wintypes.DWORD,
    wintypes.LPVOID,
    wintypes.DWORD,
    wintypes.DWORD,
    wintypes.HANDLE
]

kernel32.CreateFileW.restype = wintypes.HANDLE

#ReadFile
kernel32.ReadFile.argtypes = [
    wintypes.HANDLE,
    wintypes.LPVOID,
    wintypes.DWORD,
    ctypes.POINTER(wintypes.DWORD),
    wintypes.LPVOID
]

kernel32.ReadFile.restype = wintypes.BOOL

#WriteFile
kernel32.WriteFile.argtypes = [
    wintypes.HANDLE,
    wintypes.LPVOID,
    wintypes.DWORD,
    ctypes.POINTER(wintypes.DWORD),
    wintypes.LPVOID
]

kernel32.WriteFile.restype = wintypes.BOOL

#CloseHandle
kernel32.CloseHandle.argtypes = [
    wintypes.HANDLE
]

kernel32.CloseHandle.restype = wintypes.BOOL

#CopyFileW
kernel32.CopyFileW.argtypes = [
    wintypes.LPCWSTR,
    wintypes.LPCWSTR,
    wintypes.BOOL
]

kernel32.CopyFileW.restype = wintypes.BOOL

#MoveFileExW
kernel32.MoveFileExW.argtypes = [
    wintypes.LPCWSTR,
    wintypes.LPCWSTR,
    wintypes.DWORD
]

kernel32.MoveFileExW.restype = wintypes.BOOL

#DeleteFileW
kernel32.DeleteFileW.argtypes = [
    wintypes.LPCWSTR
]

kernel32.DeleteFileW.restype = wintypes.BOOL

print("ctype bindings set up successfully")

def _raise(msg):
    err = ctypes.get_last_error()
    raise OSError(
        f"{msg}\nError code: {err}\nReason: {ctypes.FormatError(err)}"
    )

class FILETIME(ctypes.Structure):
    _fields_ = [
        ("dwLowDateTime", wintypes.DWORD),
        ("dwHighDateTime", wintypes.DWORD),
    ]

class WIN32_FILE_ATTRIBUTE_DATA(ctypes.Structure):
    _fields_ = [
        ("dwFileAttributes", wintypes.DWORD),
        ("ftCreationTime", FILETIME),
        ("ftLastAccessTime", FILETIME),
        ("ftLastWriteTime", FILETIME),
        ("nFileSizeHigh", wintypes.DWORD),
        ("nFileSizeLow", wintypes.DWORD),
    ]

kernel32.GetFileAttributesExW.argtypes = [
    wintypes.LPCWSTR,
    wintypes.INT,
    ctypes.POINTER(WIN32_FILE_ATTRIBUTE_DATA)
]

kernel32.GetFileAttributesExW.restype = wintypes.BOOL

# Why declaring the prototypes matters ?
# Declaring argtypes and restype tells Python the correct parameter
# types and return type of the Win32 function.
# A HANDLE is a pointer. On 64-bit Python, if restype is not set to
# wintypes.HANDLE, the returned handle may be truncated, making it
# invalid and causing Win32 API calls to fail.

class FileHandler:
    
    def __init__(self, path):
        self.path = path
        self.handle = None

    #---------------Create a New file-----------------
    def create(self):
        self.handle = kernel32.CreateFileW(
            self.path,
            GENERIC_READ | GENERIC_WRITE,
            FILE_SHARE_READ,
            None,
            CREATE_ALWAYS,
            FILE_ATTRIBUTE_NORMAL,
            None
        )

        if self.handle == INVALID_HANDLE_VALUE:
            _raise("Unable to Create File")

        print("File Created Successfully")

    #-------------------Open Existing----------------------
    def open(self, access="rw"):
        desired_access = 0

        if "r" in access:
            desired_access |= GENERIC_READ

        if "w" in access:
            desired_access |= GENERIC_WRITE

        self.handle = kernel32.CreateFileW(
            self.path,
            desired_access,
            FILE_SHARE_READ,
            None,
            OPEN_EXISTING,
            FILE_ATTRIBUTE_NORMAL,
            None
        )

        if self.handle == INVALID_HANDLE_VALUE:
            _raise("Unable to Open File")

        print("File Opened Successfully")

    # Difference between CREATE_ALWAYS(create) and OPEN_EXISTING(open)
    # CREATE_ALWAYS creates a new file. If the file already exists,
    # it overwrites (truncates) the existing file.
    
    # OPEN_EXISTING opens an existing file only.
    # If the file does not exist, the operation fails.

    #----------------Write Data into File-------------------
    def write(self, data):

        #Convert string into bytes
        if isinstance(data, str):
            data = data.encode("utf-8")

        #Variable to store number of bytes written
        written = wintypes.DWORD()

        #Call WriteFile
        success = kernel32.WriteFile(
            self.handle,
            data,
            len(data),
            ctypes.byref(written),
            None
        )

        if success == 0:
            _raise("Unable to Write File")

        print(f"{written.value} bytes written successfully")
        return written.value

    #-----------------Read Data from File--------------------
    def read(self, size=None):
        # If size is not given,determine complete the file size
        if size is None:
            file_size = ctypes.c_longlong()

            success = kernel32.GetFileSizeEx(
                self.handle,
                ctypes.byref(file_size)
            )
            if success == 0:
                _raise("Unable to Get File Size")

            size = file_size.value

        buffer = ctypes.create_string_buffer(size)

        bytes_read = wintypes.DWORD()

        success = kernel32.ReadFile(
            self.handle,
            buffer,
            size,
            ctypes.byref(bytes_read),
            None
        )

        if success == 0:
            _raise("Unable to Read File")

        return buffer.raw[:bytes_read.value].decode("utf-8")

    #--------------------Close File-------------------------
    def close(self):
        if self.handle is not None:
            success = kernel32.CloseHandle(self.handle)

            if success == 0:
                _raise("Unable to Close File")

            self.handle = None
            print("File Closed Successfully") 

    #------------------Context Manager Support------------------
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    # Why leaking handles is a problem(resource exhaustion; the file stays locked)
    # Every opened file creates a Windows HANDLE.
    # If the handle is not closed, it remains in use.
    # This can waste system resources and keep the file locked,
    # preventing other programs from accessing or modifying it.
    # Always close the handle after finishing file operations.

    #-----------------------Copy File--------------------------
    def copy(self, dest, overwrite=False):
        bFailIfExists = not self.write

        success = kernel32.CopyFileW(
            self.path,
            dest,
            bFailIfExists
        )

        if success == 0:
            self._raise("Failed to copy file")
        return dest
    
    #----------------------Move File-------------------------
    def move(self, dest):
        flags = MOVEFILE_REPLACE_EXISTING | MOVEFILE_COPY_ALLOWED

        success = kernel32.MoveFileExW(
            self.path,
            dest,
            flags
        )

        if success == 0:
            self._raise("Failed to move file")

        self.path = dest

        return self.path
    
    #----------------Rename the file------------------------
    def rename(self, new_name):
        directory = os.path.dirname(self.path)

        new_name = os.path.join(directory, new_name)

        return self.move(new_name)
    
    # Why on Windows a rename is just a move (both are MoveFile*)
    #On Windows, renaming a file is actually a special case of moving a file.
    #Both operations use the same Windows API function (MoveFile or MoveFileEx).

    #If the source and destination are in the same folder but have different names,
    #the file is renamed.
    #If the destination is a different folder, the file is moved.

    #Therefore, a rename operation is simply a move operation where only the file
    #name changes and the folder remains the same.
    
    #-------Converts Windows FILETIME to Python datetime-------
    def _filetime_to_datetime(self, filetime):
        ticks = (
            (filetime.dwHighDateTime << 32)
            | filetime.dwLowDateTime
        )

        #Converts FILETIME into unix timestamp
        unix_time = ticks / 10000000 - 11644473600

        return datetime.fromtimestamp(unix_time)
    
    #-----------------get_file_info----------------------
    def get_file_info(self):
        data = WIN32_FILE_ATTRIBUTE_DATA()

        success = kernel32.GetFileAttributesExW(
            self.path,
            GetFileExInfoStandard,
            ctypes.byref(data)
        )

        if success == 0:
            self._raise("Failed to get file information")

        #Calculate the complete file size
        size = (data.nFileSizeHigh << 32) | data.nFileSizeLow

        #Check whether the path is a directory
        is_directory = bool(
            data.dwFileAttributes & FILE_ATTRIBUTE_DIRECTORY
        )

        #Check whether the file is read-only
        read_only = bool(
            data.dwFileAttributes & FILE_ATTRIBUTE_READONLY
        )

        #Convert FILETIME into datetime
        created = self._filetime_to_datetime(
            data.ftCreationTime
        )

        modified = self._filetime_to_datetime(
            data.ftLastWriteTime
        )

        #Returns all information
        return {
            "path": self.path,
            "size_bytes": size,
            "is_directory": is_directory,
            "read_only": read_only,
            "created": created,
            "modified": modified
        }
    
    #-----------------Delete the File---------------------
    def delete(self):
        self.close()

        success = kernel32.DeleteFileW(self.path)

        if success == 0:
            self._raise("Failed to Delete File")

        return True
    

if __name__ == "__main__":
    print("\n----------CREATE----------")
    fh = FileHandler("demo.txt")
    fh.create()

    print("\n----------WRITE----------")
    fh.write("Hello World from Win32 API!")
    fh.close()

    print("\n----------OPEN----------")
    fh.open()

    print("\n----------READ----------")
    text = fh.read()
    print("File Content:")
    print(text)
    fh.close()

    print("\n----------CONTEXT MANAGER----------")
    with FileHandler("demo.txt") as file:
        file.open("r")
        print(file.read())

    print("\n----------COPY----------")
    fh = FileHandler("demo.txt")
    new_file = fh.copy("copy_demo.txt")
    print("Copied to:", new_file)

    print("\n----------MOVE----------")
    new_path = fh.move("moved_demo.txt")
    print("Moved to:", new_path)

    print("\n----------RENAME----------")
    new_file = fh.rename("renamed_demo.txt")
    print("Renamed to:", new_file)

    print("\n----------FILE INFO----------")

    info = fh.get_file_info()

    for key, value in info.items():
        print(f"{key}: {value}")


    print("\n----------DELETE----------")
    result = fh.delete()
    print("File Deleted:", result)



