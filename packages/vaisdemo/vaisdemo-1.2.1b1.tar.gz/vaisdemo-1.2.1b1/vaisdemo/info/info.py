import sys
import os
import ctypes

def get_registry_value(key, subkey, value):
    if sys.platform != 'win32':
        raise OSError("get_registry_value is only supported on Windows")

    import winreg as _winreg
    key = getattr(_winreg, key)
    handle = _winreg.OpenKey(key, subkey)
    (value, type) = _winreg.QueryValueEx(handle, value)
    return value

class SystemInformation:
    def __init__(self):
        self.os = self._os_version().strip()
        self.cpu = self._cpu().strip()
        self.browsers = self._browsers()
        self.totalRam, self.availableRam = self._ram()
        self.totalRam = self.totalRam / (1024*1024)
        self.availableRam = self.availableRam / (1024*1024)
        self.hdFree = self._disk_c() / (1024*1024*1024)

    def _os_version(self):
        def get(key):
            return get_registry_value(
                "HKEY_LOCAL_MACHINE",
                "SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion",
                key)
        os = get("ProductName")
        sp = get("CSDVersion")
        build = get("CurrentBuildNumber")
        return "%s %s (build %s)" % (os, sp, build)

    def _cpu(self):
        return get_registry_value(
            "HKEY_LOCAL_MACHINE",
            "HARDWARE\\DESCRIPTION\\System\\CentralProcessor\\0",
            "ProcessorNameString")

    def _firefox_version(self):
        try:
            version = get_registry_value(
                "HKEY_LOCAL_MACHINE",
                "SOFTWARE\\Mozilla\\Mozilla Firefox",
                "CurrentVersion")
            version = (u"Mozilla Firefox", version)
        except WindowsError:
            version = None
        return version

    def _iexplore_version(self):
        try:
            version = get_registry_value(
                "HKEY_LOCAL_MACHINE",
                "SOFTWARE\\Microsoft\\Internet Explorer",
                "Version")
            version = (u"Internet Explorer", version)
        except WindowsError:
            version = None
        return version

    def _browsers(self):
        browsers = []
        firefox = self._firefox_version()
        if firefox:
            browsers.append(firefox)
        iexplore = self._iexplore_version()
        if iexplore:
            browsers.append(iexplore)

        return browsers

    def _ram(self):
        kernel32 = ctypes.windll.kernel32
        c_ulong = ctypes.c_ulong
        class MEMORYSTATUS(ctypes.Structure):
            _fields_ = [
                ('dwLength', c_ulong),
                ('dwMemoryLoad', c_ulong),
                ('dwTotalPhys', c_ulong),
                ('dwAvailPhys', c_ulong),
                ('dwTotalPageFile', c_ulong),
                ('dwAvailPageFile', c_ulong),
                ('dwTotalVirtual', c_ulong),
                ('dwAvailVirtual', c_ulong)
            ]

        memoryStatus = MEMORYSTATUS()
        memoryStatus.dwLength = ctypes.sizeof(MEMORYSTATUS)
        kernel32.GlobalMemoryStatus(ctypes.byref(memoryStatus))
        return (memoryStatus.dwTotalPhys, memoryStatus.dwAvailPhys)

    def _disk_c(self):
        drive = unicode(os.getenv("SystemDrive"))
        freeuser = ctypes.c_int64()
        total = ctypes.c_int64()
        free = ctypes.c_int64()
        ctypes.windll.kernel32.GetDiskFreeSpaceExW(drive,
                                        ctypes.byref(freeuser),
                                        ctypes.byref(total),
                                        ctypes.byref(free))
        return freeuser.value

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
        data += [s.os, s.s_cpu, s.totalRam]
    except Exception as e:
        pass
    if sh:
        sh.insert_rows(row=1, values=data)
