# Stores the current quota and date as a binary file so the program can keep track of it per use
from datetime import datetime
import struct

QUOTA_FORMAT = "L"
NEW_QUOTA_VALUE = 10000
TODAY = datetime.now().date()

def get_quota():
    content = None

    try:
        with open('quota', 'rb') as f:
            content = f.read()
    except FileNotFoundError:
        update_quota(NEW_QUOTA_VALUE)
        return NEW_QUOTA_VALUE

    date = content[:8].decode('utf-8')

    stored_date = datetime.strptime(date, "%d%m%Y").date()
    if TODAY > stored_date:
        update_quota(NEW_QUOTA_VALUE)
        return NEW_QUOTA_VALUE

    return struct.unpack(QUOTA_FORMAT, content[8:])[0]

def update_quota(current):
    today = datetime.now().date().strftime('%d%m%Y').encode('utf-8')
    current_in_bytes = struct.pack(QUOTA_FORMAT, current)

    with open('quota', 'wb') as f:
        f.write(today + current_in_bytes)