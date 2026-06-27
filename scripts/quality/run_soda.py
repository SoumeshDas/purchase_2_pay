
import json
import re
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

PIPELINE_NAME="Purchase2Pay"
CONFIG_FILE="/jobs/soda_docker/configuration.yml"
CHECKS_FILE="/jobs/soda_docker/checks.yml"
OUTPUT_DIR=Path("/jobs/output")
LOG_DIR=Path("/jobs/logs")
REPORT_FILE=OUTPUT_DIR/"quality_report.json"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
LOG_DIR.mkdir(parents=True, exist_ok=True)

start=time.time()
ts=datetime.now().strftime("%Y%m%d_%H%M%S")
log_file=LOG_DIR/f"soda_scan_{ts}.log"

result=subprocess.run(
    ["soda","scan","-d","parquet_data","-c",CONFIG_FILE,CHECKS_FILE],
    capture_output=True,text=True
)
output=result.stdout+"\n"+result.stderr
log_file.write_text(output)

report={
 "pipeline":PIPELINE_NAME,
 "execution_time":datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
 "status":"SUCCESS" if result.returncode==0 else "FAILED",
 "duration_seconds":0,
 "exit_code":result.returncode,
 "total_checks":0,
 "passed":0,
 "failed":0,
 "warnings":0,
 "checks":[],
 "log_file":str(log_file)
}

current=None
for raw in output.splitlines():
    line=raw.strip()
    m=re.search(r"(\d+)/(\d+)\s+checks\s+PASSED",line)
    if m:
        report["passed"]=int(m.group(1)); report["total_checks"]=int(m.group(2)); continue
    m=re.search(r"(\d+)/(\d+)\s+checks\s+FAILED",line)
    if m:
        report["failed"]=int(m.group(1)); continue
    m=re.search(r"Oops!\s+\d+\s+failures\.\s+(\d+)\s+warnings",line)
    if m:
        report["warnings"]=int(m.group(1)); continue
    if "[PASSED]" in line:
        report["checks"].append({"name":line.split("[PASSED]")[0].strip(),"status":"PASSED"}); continue
    if "[FAILED]" in line:
        current={"name":line.split("[FAILED]")[0].strip(),"status":"FAILED"}
        report["checks"].append(current); continue
    if current and line.startswith("check_value:"):
        current["actual"]=line.split(":",1)[1].strip()
        current=None

report["duration_seconds"]=round(time.time()-start,2)
with open(REPORT_FILE,"w") as f:
    json.dump(report,f,indent=4)

print("Report:",REPORT_FILE)
print("Log:",log_file)
# Always continue so Airflow can generate report and send email
sys.exit(0)
