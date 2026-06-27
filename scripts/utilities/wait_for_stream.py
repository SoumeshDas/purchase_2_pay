import os
import time
import sys

OUTPUT = "/jobs/output/sales_stream"

timeout = 120
start = time.time()

while True:

    files = [f for f in os.listdir(OUTPUT) if f.startswith("part-")]

    if files:
        print("Output detected.")
        sys.exit(0)

    if time.time() - start > timeout:
        print("Timeout waiting for stream.")
        sys.exit(1)

    time.sleep(5)
