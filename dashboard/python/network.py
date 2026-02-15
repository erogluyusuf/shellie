import psutil
import json
import time

old_value = psutil.net_io_counters()
time.sleep(1)
new_value = psutil.net_io_counters()

bytes_sent = new_value.bytes_sent - old_value.bytes_sent
bytes_recv = new_value.bytes_recv - old_value.bytes_recv

def get_speed(bytes):
    # Mbps cinsinden hesapla
    bits = bytes * 8
    mbps = bits / (1024 * 1024)
    return f"{mbps:.1f}"

data = {
    "upload": get_speed(bytes_sent),
    "download": get_speed(bytes_recv)
}

print(json.dumps(data))