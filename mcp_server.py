import sys, json
from client import PersonalDigitalHoardingDeclutter

def main():
    declutter = PersonalDigitalHoardingDeclutter()
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        print(json.dumps(declutter.run_benchmark_digital_declutter(), indent=2))
        return

    for line in sys.stdin:
        if not line.strip(): continue
        try:
            req = json.loads(line)
            method = req.get("method")
            params = req.get("params", {})
            rid = req.get("id")

            if method == "tools/list":
                res = {
                    "tools": [
                        {"name": "analyze_file_batch", "description": "Triage files into delete, archive, or keep pools."},
                        {"name": "calculate_revisit_probability", "description": "Estimate probability of file revisit based on decay."},
                        {"name": "run_benchmark_digital_declutter", "description": "Run decluttering test suite."}
                    ]
                }
            elif method == "tools/call":
                tname = params.get("name")
                args = params.get("arguments", {})
                if tname == "analyze_file_batch":
                    out = declutter.analyze_file_batch(args.get("file_list", []))
                elif tname == "calculate_revisit_probability":
                    out = {"probability": declutter.calculate_revisit_probability(args.get("days_since_last_access", 0), args.get("file_category", "GENERAL_DOCUMENT"))}
                elif tname == "run_benchmark_digital_declutter":
                    out = declutter.run_benchmark_digital_declutter()
                else:
                    out = {"error": f"Unknown tool {tname}"}
                res = {"content": [{"type": "text", "text": json.dumps(out)}]}
            else:
                res = {"error": "Unsupported method"}
            print(json.dumps({"jsonrpc": "2.0", "id": rid, "result": res}), flush=True)
        except Exception as e:
            print(json.dumps({"jsonrpc": "2.0", "error": {"code": -32603, "message": str(e)}}), flush=True)

if __name__ == "__main__":
    main()
