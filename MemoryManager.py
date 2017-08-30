import ctypes as c
from ctypes import wintypes as w
import win32ui
import win32process

k32 = c.windll.kernel32

OpenProcess = k32.OpenProcess
OpenProcess.argtypes = [w.DWORD,w.BOOL,w.DWORD]
OpenProcess.restype = w.HANDLE

ReadProcessMemory = k32.ReadProcessMemory
ReadProcessMemory.argtypes = [w.HANDLE,w.LPCVOID,w.LPVOID,c.c_size_t,c.POINTER(c.c_size_t)]
ReadProcessMemory.restype = w.BOOL

WriteProcessMemory = k32.WriteProcessMemory
WriteProcessMemory.argtypes = [w.HANDLE, w.LPVOID, w.LPCVOID, c.c_size_t, c.POINTER(c.c_size_t)]
WriteProcessMemory.restype = w.BOOL

GetLastError = k32.GetLastError
GetLastError.argtypes = None
GetLastError.restype = w.DWORD

CloseHandle = k32.CloseHandle
CloseHandle.argtypes = [w.HANDLE]
CloseHandle.restype = w.BOOL

def readFromProcessWithWindowTitle(title, address):

    PROCESS = getProcessForTitle(title)

    data = c.c_long()
    bytes_read = c.c_ulong()
    result = ReadProcessMemory(PROCESS, address, c.byref(data), c.sizeof(data), c.byref(bytes_read))
    e = GetLastError()

    print('result: {}, err code: {}, bytesRead: {}'.format(result, e, bytes_read.value))
    print('data: {:016X}'.format(data.value))

    return data.value


def writeToProcessWithWindowTitle(title, address):

    PROCESS = getProcessForTitle(title)

    new_val = c.create_string_buffer(4)
    new_val[0] = 0xE8
    new_val[1] = 0x03
    new_val[2] = 0x00
    new_val[3] = 0x00

    bytes_wrote = c.c_ulong()
    result = WriteProcessMemory(PROCESS, address, new_val, c.sizeof(new_val), bytes_wrote)
    e = GetLastError()

    print('result: {}, err code: {}, bytesWrote: {}'.format(result,e,bytes_wrote.value))



def getProcessForTitle(title):
    HWND = win32ui.FindWindow(None, title).GetSafeHwnd()
    PID = win32process.GetWindowThreadProcessId(HWND)[1]

    PROCESS_ALL_ACCESS = (0x000F0000 | 0x00100000 | 0xFFF)
    return OpenProcess(PROCESS_ALL_ACCESS, False, PID)