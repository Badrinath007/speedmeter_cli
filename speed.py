import psutil
import time
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

def get_speed(interval=1):
    net_io_1 = psutil.net_io_counters()
    time.sleep(float(interval))
    net_io_2 = psutil.net_io_counters()

    download_speed = (net_io_2.bytes_recv - net_io_1.bytes_recv) * 8 / (1024 * 1024 * interval)
    upload_speed = (net_io_2.bytes_sent - net_io_1.bytes_sent) * 8 / (1024 * 1024 * interval)

    return download_speed, upload_speed

def get_color(speed):
    if speed >= 100:
        return Fore.GREEN
    elif speed >= 20:
        return Fore.GREEN
    else:
        return Fore.YELLOW

if __name__ == "__main__":
    print("📡 Internet Speed tracker (Press Ctrl+C to stop)\n")

    try:
        while True:
            down, up = get_speed(1)
            down_color = get_color(down)
            up_color = get_color(up)

            print(f"{down_color}↓ Download: {down:.2f} Mbps{Style.RESET_ALL} | "
                  f"{up_color}↑ Upload: {up:.2f} Mbps", end="\r")
    except KeyboardInterrupt:
        print("\nThank You!.")

