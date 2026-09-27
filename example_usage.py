import sys, json
from client import PersonalDigitalHoardingDeclutter

def main():
    print("Testing PersonalDigitalHoardingDeclutter...")
    declutter = PersonalDigitalHoardingDeclutter()
    res = declutter.run_benchmark_digital_declutter()
    print(json.dumps(res, indent=2))
    assert res["benchmark_status"] == "PASSED"
    assert res["reclaimable_mb"] > 600.0
    assert res["staged_delete_count"] >= 2
    print("All Personal Digital Hoarding Declutter tests passed successfully!")

if __name__ == "__main__":
    main()
