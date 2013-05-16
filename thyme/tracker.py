from datetime import datetime

import win32ui

from .database import Entry


def track(session):
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
                session.flush()
