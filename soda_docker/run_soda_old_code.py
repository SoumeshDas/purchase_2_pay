import subprocess
import sys
import os
from datetime import datetime

PROJECT_ROOT = "/jobs"

LOG_DIR = f"{PROJECT_ROOT}/soda_docker/logs"

os.makedirs(LOG_DIR, exist_ok=True)

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

log_file = f"{LOG_DIR}/soda_scan_{timestamp}.log"

cmd = [
    "soda",
    "scan",
    "-d",
    "parquet_data",
    "-c",
    f"{PROJECT_ROOT}/soda_docker/configuration.yml",
    f"{PROJECT_ROOT}/soda_docker/checks.yml",
]

with open(log_file, "w") as log:

    result = subprocess.run(cmd, stdout=log, stderr=subprocess.STDOUT, text=True)

print(f"Log saved : {log_file}")

sys.exit(result.returncode)
