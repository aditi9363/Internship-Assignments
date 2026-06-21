import ctypes
import sys
from datetime import datetime

# Windows API
kernel32 = ctypes.windll.kernel32

# Mutex Name
MUTEX_NAME = "Global\\ROMS_LogMutex"

# Wait constants
WAIT_OBJECT_0 = 0
WAIT_ABANDONED = 0x80
WAIT_TIMEOUT = 258


def log_event(level, message):
    """
    Thread-safe logging using Windows Named Mutex
    """

    # Open/Create Named Mutex
    mutex = kernel32.CreateMutexW(
        None,
        False,
        MUTEX_NAME
    )

    if not mutex:
        print("Failed to create mutex", file=sys.stderr)
        return

    # Wait maximum 3000 ms
    result = kernel32.WaitForSingleObject(
        mutex,
        3000
    )

    # Success
    if result in (WAIT_OBJECT_0, WAIT_ABANDONED):

        try:
            timestamp = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )

            line = (
                f"[{timestamp}] "
                f"[{level}] "
                f"{message}\n"
            )

            with open(
                "roms.log",
                "a",
                encoding="utf-8"
            ) as logfile:
                logfile.write(line)

        finally:
            kernel32.ReleaseMutex(mutex)

    elif result == WAIT_TIMEOUT:
        print(
            "WARNING: Logger mutex timeout",
            file=sys.stderr
        )

    kernel32.CloseHandle(mutex)