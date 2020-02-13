import os
import structlog

MAX_FILE_SIZE_DEBUG = 500000
MAX_FILE_SIZE_AUDIT = 200000
logger = structlog.getLogger('audit')


def clear_debug_logs():
    if os.path.exists("logs/debug.log"):
        if os.path.getsize("logs/debug.log") >= MAX_FILE_SIZE_DEBUG:
            os.remove("logs/debug.log")
    else:
        logger.critical("Debug log file does not exist")


def clear_audit_logs():
    if os.path.exists("logs/audit.log"):
        if os.path.getsize("logs/audit.log") >= MAX_FILE_SIZE_AUDIT:
            os.remove("logs/audit.log")
    else:
        logger.critical("Audit log file does not exist")
