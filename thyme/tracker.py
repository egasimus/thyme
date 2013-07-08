from datetime import datetime
from multiprocessing import Process
from time import sleep

import win32api
import win32con
import win32process
import win32security
import win32ui

from .database import init_db, Entry
from .settings import POLL_INTERVAL


def get_exe_name(cwnd):
    # Get name of executable for window handle, via:
    # http://mail.python.org/pipermail/python-win32/2009-July/009381.html

    # Request privileges to enable "debug process", so we can later use
    # PROCESS_VM_READ, retardedly required to GetModuleFileNameEx()
    priv_flags = \
        win32security.TOKEN_ADJUST_PRIVILEGES | win32security.TOKEN_QUERY
    hToken = win32security.OpenProcessToken(
        win32api.GetCurrentProcess(), priv_flags)

    # enable "debug process"
    privilege_id = win32security.LookupPrivilegeValue(
        None, win32security.SE_DEBUG_NAME)
    win32security.AdjustTokenPrivileges(
        hToken, 0, [(privilege_id, win32security.SE_PRIVILEGE_ENABLED)])

    # Open the process, and query its filename
    tid, pid = win32process.GetWindowThreadProcessId(cwnd.GetSafeHwnd())
    access = win32con.PROCESS_QUERY_INFORMATION | win32con.PROCESS_VM_READ
    pshandle = win32api.OpenProcess(access, 0, pid)
    exename = win32process.GetModuleFileNameEx(pshandle, 0)

    # clean up
    win32api.CloseHandle(pshandle)
    win32api.CloseHandle(hToken)

    return exename


def track():
    session = init_db()
    entry = None
    while True:
        try:
            cwnd = win32ui.GetForegroundWindow()
        except win32ui.error:
            cwnd = None

        if cwnd is not None:
            # Get window title
            title = cwnd.GetWindowText()

            print(get_exe_name(cwnd))

            # Write entry to database
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
