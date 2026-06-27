import json
import sys
from pathlib import Path

REPORT_FILE = Path("/jobs/output/quality_report.json")


def main():

    print("=" * 60)
    print("Purchase2Pay Pipeline Validation")
    print("=" * 60)

    # -------------------------------------------------
    # Report exists?
    # -------------------------------------------------

    if not REPORT_FILE.exists():
        print(f"ERROR: Report not found: {REPORT_FILE}")
        sys.exit(1)

    # -------------------------------------------------
    # Load report
    # -------------------------------------------------

    try:
        with open(REPORT_FILE) as f:
            report = json.load(f)
    except Exception as e:
        print(f"ERROR: Unable to read report")
        print(e)
        sys.exit(1)

    # -------------------------------------------------
    # Print Summary
    # -------------------------------------------------

    print(f"Pipeline      : {report.get('pipeline')}")
    print(f"Status        : {report.get('status')}")
    print(f"Execution     : {report.get('execution_time')}")
    print(f"Duration      : {report.get('duration_seconds')} sec")

    print()

    print("Quality Summary")
    print("---------------------------")
    print(f"Total Checks  : {report.get('total_checks')}")
    print(f"Passed        : {report.get('passed')}")
    print(f"Failed        : {report.get('failed')}")
    print(f"Warnings      : {report.get('warnings')}")

    print()

    # -------------------------------------------------
    # Failed Checks
    # -------------------------------------------------

    failed_checks = [
        check
        for check in report.get("checks", [])
        if check["status"] == "FAILED"
    ]

    if failed_checks:

        print("Failed Checks")
        print("---------------------------")

        for check in failed_checks:

            print(f"❌ {check['name']}")

            if "actual" in check:
                print(f"   Actual Value : {check['actual']}")

        print()

    # -------------------------------------------------
    # Final Decision
    # -------------------------------------------------

    if report["status"] == "FAILED":

        print("=" * 60)
        print("Purchase2Pay Pipeline FAILED")
        print("=" * 60)

        sys.exit(1)

    print("=" * 60)
    print("Purchase2Pay Pipeline PASSED")
    print("=" * 60)

    sys.exit(0)


if __name__ == "__main__":
    main()