import psutil
import time
from colorama import init, Fore, Style
import threading

# Initialize colorama
init(autoreset=True)

# Global toggle and stop signal
unit_is_mbps = True
stop_event = threading.Event()

def toggle_units():
    global unit_is_mbps
    while not stop_event.is_set():
        try:
            input("\n🔁 Press Enter to toggle units (MBps <-> Mbps)...\n")
            if stop_event.is_set():
                break
            unit_is_mbps = not unit_is_mbps
            print(f"✅ Toggled to: {'Mbps' if unit_is_mbps else 'MBps'}\n")
        except EOFError:
            break

def get_speed(interval=1):
    net_io_1 = psutil.net_io_counters()
    time.sleep(float(interval))
    net_io_2 = psutil.net_io_counters()

    if unit_is_mbps:
        # Convert to Megabits
        download_speed = (net_io_2.bytes_recv - net_io_1.bytes_recv) * 8 / (1024 * 1024 * interval)
        upload_speed = (net_io_2.bytes_sent - net_io_1.bytes_sent) * 8 / (1024 * 1024 * interval)
    else:
        # Convert to Megabytes
        download_speed = (net_io_2.bytes_recv - net_io_1.bytes_recv) / (1024 * 1024 * interval)
        upload_speed = (net_io_2.bytes_sent - net_io_1.bytes_sent) / (1024 * 1024 * interval)

    return download_speed, upload_speed

def get_color(speed):
    if speed >= 100:
        return Fore.GREEN
    elif speed >= 20:
        return Fore.GREEN
    else:
        return Fore.YELLOW

if __name__ == "__main__":
    print("📡 Real-Time Speed Monitor (Press Ctrl+C to stop)\n")

    # Start toggle thread
    toggle_thread = threading.Thread(target=toggle_units, daemon=True)
    toggle_thread.start()

    try:
        while not stop_event.is_set():
            down, up = get_speed(1)
            unit = "Mbps" if unit_is_mbps else "MBps"
            down_color = get_color(down)
            up_color = get_color(up)

            print(f"{down_color}↓ Download: {down:.2f} {unit}{Style.RESET_ALL} | "
                  f"{up_color}↑ Upload: {up:.2f} {unit}", end="\r")
    except KeyboardInterrupt:
        stop_event.set()
