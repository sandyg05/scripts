import ctypes
import psutil

# DLL
kernel32 = ctypes.windll.kernel32

# CLIENT
CLIENT_NAME = "WarFare_x64.exe"

# PROCESS PERMISSIONS

PROCESS_QUERY_INFORMATION = 0x0400
PROCESS_VM_OPERATION = 0x0008
PROCESS_VM_READ = 0x0010
PROCESS_VM_WRITE = 0x0020

# WINDOWS API

OpenProcess = kernel32.OpenProcess
CloseHandle = kernel32.CloseHandle
GetLastError = kernel32.GetLastError
ReadProcessMemory = kernel32.ReadProcessMemory
WriteProcessMemory = kernel32.WriteProcessMemory


class ReadWriteMemory:

    def OpenProcess(self, process_name):
        dwDesiredAccess = (PROCESS_QUERY_INFORMATION |
                           PROCESS_VM_OPERATION |
                           PROCESS_VM_READ |
                           PROCESS_VM_WRITE)
        bInheritHandle = False

        process = filter(lambda process: process.name() == CLIENT_NAME, psutil.process_iter())
        client_process = None
        for p in process:
            client_process = p

        dwProcessId = client_process.pid

        hProcess = (dwDesiredAccess, bInheritHandle, dwProcessId)

        return hProcess

    def CloseHandle(self, hProcess):
        CloseHandle(hObject)

    def GetLastError(self):
        GetLastError()
        return GetLastError()

    def PointerOffset(self, lbBaseAddress):
        pass

    def ReadProcessMemory(self, hProcess, lpBaseAddress):
        try:
            lpBaseAddress = lpBaseAddress
            ReadBuffer = ctypes.c_uint()
            lpBuffer = ctypes.byref(ReadBuffer)
            nSize = ctypes.sizeof(ReadBuffer)
            lpNumberOfBytesRead = ctypes.c_ulong(0)

            ctypes.windll.kernel32.ReadProcessMemory(hProcess,lpBaseAddress,lpBuffer,nSize,lpNumberOfBytesRead)

            return ReadBuffer.value
        except (BufferError, ValueError, TypeError):
            self.CloseHandle(hProcess)
            e = 'Handle Closed, Error', hProcess, self.GetLastError()
            return e


    def WriteProcessMemory(self, hProcess, lpBaseAddress, Value):
        try:
            lpBaseAddress = lpBaseAddress
            Value = Value
            WriteBuffer = ctypes.c_uint(Value)
            lpBuffer = ctypes.byref(WriteBuffer)
            nSize = ctypes.sizeof(WriteBuffer)
            lpNumberOfBytesWritten = ctypes.c_ulong(0)

            ctypes.windll.kernel32.WriteProcessMemory(
                                                    hProcess,
                                                    lpBaseAddress,
                                                    lpBuffer,
                                                    nSize,
                                                    lpNumberOfBytesWritten
                                                    )
        except (BufferError, ValueError, TypeError):
            self.CloseHandle(hProcess)
            e = 'Handle Closed, Error', hProcess, self.GetLastError()
            return e




process = filter(lambda process: process.name() == CLIENT_NAME, psutil.process_iter())
for p in process:
    client_process = p

assert (client_process.status() == 'running')

print(client_process.pid)


