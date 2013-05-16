from datetime import datetime
from multiprocessing import Process
from time import sleep

import win32ui

from .database import init_db, Entry
from .settings import POLL_INTERVAL


def track():
    session = init_db()
    entry = None
    while True:
        try:
            hwnd = win32ui.GetForegroundWindow()
        except win32ui.error:
            hwnd = None

        if hwnd is not None:
            title = hwnd.GetWindowText()
            if entry is None or entry.title != title:
                entry = Entry(title=title,
                              time=datetime.now())
                session.add(entry)
                session.commit()
        sleep(POLL_INTERVAL)


def launch_tracker():
    p = Process(target=track)
    p.start()
    return p
