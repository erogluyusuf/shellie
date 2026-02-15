import psutil
import json

# En çok bellek kullanan 5 işlemi getir
processes = []
for proc in psutil.process_iter(['pid', 'name', 'memory_info', 'cpu_percent']):
    try:
        processes.append(proc.info)
    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
        pass

# Bellek kullanımına göre sırala (büyükten küçüğe)
sorted_procs = sorted(processes, key=lambda p: p['memory_info'].rss, reverse=True)[:5]

final_list = []
for p in sorted_procs:
    mem_mb = p['memory_info'].rss / (1024 * 1024)
    final_list.append({
        "name": p['name'],
        "cpu": p['cpu_percent'],
        "memory": f"{mem_mb:.1f} MB"
    })

print(json.dumps(final_list))