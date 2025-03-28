from pymem import Pymem, exception
import ctypes
import re

def scan_memory(pattern):
    try:
        class MEMORY_BASIC_INFORMATION(ctypes.Structure):
            _fields_ = [
                ("BaseAddress", ctypes.c_void_p),
                ("AllocationBase", ctypes.c_void_p),
                ("AllocationProtect", ctypes.c_ulong),
                ("RegionSize", ctypes.c_size_t),
                ("State", ctypes.c_ulong),
                ("Protect", ctypes.c_ulong),
                ("Type", ctypes.c_ulong)
            ]
        mbi = MEMORY_BASIC_INFORMATION()
        address = 0
        while ctypes.windll.kernel32.VirtualQueryEx(
            pm.process_handle, 
            ctypes.c_void_p(address), 
            ctypes.byref(mbi), 
            ctypes.sizeof(mbi)
        ):
            if mbi.Protect == 4:
                try:
                    memory = pm.read_bytes(mbi.BaseAddress, mbi.RegionSize)
                    for match in re.finditer(re.escape(pattern), memory):
                        return mbi.BaseAddress + match.start()
                except:
                    pass
            address += mbi.RegionSize        
        return None
    except Exception:
        pass

if __name__ == "__main__":
    try:
        pm = Pymem("Minecraft.Windows.exe")
        pattern = b"\x00\x00\x80\x3F\x00\x00\x00\x3F\x6F\x12\x83\x3A\x00"
        address = scan_memory(pattern)

        if address:
            pm.write_float(address, 100.0)
            print(f"It worked! ({hex(address)})")
        else:
            print("Address not found!\n- Make sure that your brightness is set to 100.")

    except (exception.ProcessNotFound):
        print("Game not found.")
        pass