import ctypes
from ctypes import wintypes
import psutil

# 64-bit / 32-bit uyumlu Windows API tanımları
FILE_MAP_READ = 0x0004
kernel32 = ctypes.windll.kernel32

kernel32.OpenFileMappingW.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.LPCWSTR]
kernel32.OpenFileMappingW.restype = wintypes.HANDLE

kernel32.MapViewOfFile.argtypes = [
    wintypes.HANDLE,
    wintypes.DWORD,
    wintypes.DWORD,
    wintypes.DWORD,
    ctypes.c_size_t,
]
kernel32.MapViewOfFile.restype = ctypes.c_void_p

kernel32.UnmapViewOfFile.argtypes = [ctypes.c_void_p]
kernel32.CloseHandle.argtypes = [wintypes.HANDLE]


# Core Temp C-Struct Yapısı
class CoreTempSharedData(ctypes.Structure):
    _fields_ = [
        ("uiLoad", wintypes.DWORD * 256),
        ("uiTjMax", wintypes.DWORD * 128),
        ("uiCoreCnt", wintypes.DWORD),
        ("uiCPUCnt", wintypes.DWORD),
        ("fTemp", ctypes.c_float * 256),
        ("fVID", ctypes.c_float),
        ("fCPUSpeed", ctypes.c_float),
        ("fFSBSpeed", ctypes.c_float),
        ("fMultipier", ctypes.c_float),
        ("sCPUName", ctypes.c_char * 100),
        ("ucIsShutdown", ctypes.c_ubyte),
    ]


def get_cpu_temp():
    try:
        handle = kernel32.OpenFileMappingW(
            FILE_MAP_READ, False, "CoreTempMappingObject"
        )
        if not handle:
            return None

        ptr = kernel32.MapViewOfFile(handle, FILE_MAP_READ, 0, 0, 0)
        if not ptr:
            kernel32.CloseHandle(handle)
            return None

        data = CoreTempSharedData.from_address(ptr)
        core_count = data.uiCoreCnt

        # Mantıklı çekirdek sayısı sınırı (0 ile 256 arası)
        if 0 < core_count <= 256:
            temps = [data.fTemp[i] for i in range(core_count)]
            avg_temp = sum(temps) / len(temps)
        else:
            avg_temp = None

        kernel32.UnmapViewOfFile(ptr)
        kernel32.CloseHandle(handle)
        return avg_temp
    except Exception:
        return None


# CPU Kullanımı ve Sıcaklık Çıktısı
kullanim = psutil.cpu_percent(interval=1)
sicaklik = get_cpu_temp()

if sicaklik is not None:
    print(f"CPU: %{kullanim} | Sıcaklık: {sicaklik:.1f}°C")
else:
    print(f"CPU: %{kullanim} | Sıcaklık: Alınamadı")
