import psutil
import json
import time
import platform
import socket
import math

def get_size(bytes, suffix="B"):
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.1f}{unit}{suffix}"
        bytes /= factor

# Uptime hesapla
boot_time_timestamp = psutil.boot_time()
bt = time.time() - boot_time_timestamp
uptime_days = int(bt // (24 * 3600))
uptime_hours = int((bt % (24 * 3600)) // 3600)
uptime_str = f"{uptime_days}g {uptime_hours}s"

# Disk Bilgileri (C: ve D: varsayımıyla, yoksa olanı alır)
partitions = psutil.disk_partitions()
disk_info = []
for partition in partitions:
    try:
        partition_usage = psutil.disk_usage(partition.mountpoint)
        disk_info.append({
            "device": partition.device,
            "total": get_size(partition_usage.total),
            "used": get_size(partition_usage.used),
            "percent": partition_usage.percent
        })
    except PermissionError:
        continue

# Hostname & IP
hostname = socket.gethostname()
ip_address = socket.gethostbyname(hostname)

data = {
    "cpu_percent": psutil.cpu_percent(interval=0.5),
    "cpu_freq": psutil.cpu_freq().current if psutil.cpu_freq() else 0,
    "ram_percent": psutil.virtual_memory().percent,
    "ram_used": get_size(psutil.virtual_memory().used),
    "ram_total": get_size(psutil.virtual_memory().total),
    "uptime": uptime_str,
    "hostname": hostname,
    "ip": ip_address,
    "disks": disk_info,
    "platform": platform.system() + " " + platform.release()
}

print(json.dumps(data))