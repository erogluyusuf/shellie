import subprocess
import json

output = subprocess.check_output("sc query state= all", shell=True).decode()

services = []
for line in output.split("\n"):
    if "SERVICE_NAME:" in line:
        services.append({
            "name": line.split(":")[1].strip()
        })

print(json.dumps(services[:20]))
