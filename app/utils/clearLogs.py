import os

MAX_FILE_SIZE_DEBUG = 500000
MAX_FILE_SIZE_AUDIT = 200000


def clear_debug_logs():
    if os.path.exists("logs/debug.log"):
        if os.path.getsize("logs/debug.log") >= MAX_FILE_SIZE:
            os.remove("logs/debug.log")
    else:
        print("The debug file does not exist")


def clear_audit_logs():
    if os.path.exists("logs/audit.log"):
        if os.path.getsize("logs/audit.log") >= MAX_FILE_SIZE_AUDIT:
            os.remove("logs/audit.log")
    else:
        print("The audit file does not exist")
