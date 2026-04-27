#!/usr/bin/env python3
"""
QA-Gated Deployment Script for my-cicd-project
Usage: python3 qa-deploy.py [--skip-qa] [--force]
"""

import requests
import json
import time
import sys
import os
import subprocess
from datetime import datetime

BASE_URL = os.getenv("API_URL", "http://localhost:5000")
REPORT_FILE = "/home/devuser/my-cicd-project/qa-report.json"

def color(text, c):
    colors = {"green":"\033[92m","red":"\033[91m","yellow":"\033[93m","blue":"\033[94m","bold":"\033[1m","end":"\033[0m"}
    return f"{colors.get(c,'')}{text}{colors['end']}"

def run_tests():
    print(color("="*60, "bold"))
    print(color("🔍 PHASE 1: QA TESTING", "bold"))
    print(color("="*60, "bold"))
    
    report = {
        "project": "my-cicd-project",
        "tested_at": datetime.utcnow().isoformat(),
        "base_url": BASE_URL,
        "tests": [],
        "summary": {"passed": 0, "failed": 0, "total": 0}
    }
    
    tests = [
        ("Root Endpoint", "GET", "/", 200, lambda r: r.json()["message"] == "Hello from CI/CD Deployed API!"),
        ("Health Check", "GET", "/health", 200, lambda r: r.json()["status"] == "healthy"),
        ("Deploy Info", "GET", "/deploy-info", 200, lambda r: ".NET" in r.json().get("framework","")),
        ("404 Handler", "GET", "/nonexistent", 404, None),
    ]
    
    for name, method, path, expected, validator in tests:
        try:
            start = time.time()
            resp = requests.request(method, f"{BASE_URL}{path}", timeout=10)
            duration = (time.time() - start) * 1000
            
            status_ok = resp.status_code == expected
            val_ok = True
            if validator and status_ok:
                try:
                    val_ok = validator(resp)
                except Exception as e:
                    val_ok = False
            
            passed = status_ok and val_ok
            report["tests"].append({"name":name,"passed":passed,"status":resp.status_code,"ms":round(duration,1)})
            report["summary"]["total"] += 1
            if passed:
                report["summary"]["passed"] += 1
                print(color(f"✅ {name} — {resp.status_code} ({duration:.0f}ms)", "green"))
            else:
                report["summary"]["failed"] += 1
                print(color(f"❌ {name} — {resp.status_code} ({duration:.0f}ms)", "red"))
        except Exception as e:
            report["tests"].append({"name":name,"passed":False,"error":str(e)})
            report["summary"]["failed"] += 1
            print(color(f"❌ {name} — ERROR: {e}", "red"))
    
    # Performance
    times = []
    for _ in range(5):
        s = time.time()
        requests.get(f"{BASE_URL}/", timeout=10)
        times.append((time.time()-s)*1000)
    report["performance"] = {"avg_ms": round(sum(times)/len(times),2), "samples": 5}
    
    with open(REPORT_FILE, "w") as f:
        json.dump(report, f, indent=2)
    
    print(f"\n{color('📊 Summary:', 'bold')} {report['summary']['passed']}/{report['summary']['total']} passed")
    print(f"{color('⚡ Performance:', 'bold')} Avg {report['performance']['avg_ms']}ms")
    
    return report["summary"]["failed"] == 0, report

def generate_markdown_report(report):
    lines = [
        "# 🔍 QA Report — my-cicd-project",
        f"**Tested:** {report['tested_at']}",
        f"**URL:** {report['base_url']}",
        "",
        "## Results",
        "| Test | Status | Response | Time |",
        "|------|--------|----------|------|",
    ]
    for t in report["tests"]:
        icon = "✅" if t["passed"] else "❌"
        status = t.get("status", "ERR")
        ms = t.get("ms", "—")
        lines.append(f"| {t['name']} | {icon} | {status} | {ms}ms |")
    
    lines.extend([
        "",
        f"**Pass Rate:** {report['summary']['passed']}/{report['summary']['total']} ({report['summary']['passed']/report['summary']['total']*100:.0f}%)",
        f"**Performance:** Avg {report['performance']['avg_ms']}ms (5 samples)",
        "",
        f"## 🏆 Verdict: {'PASS ✅' if report['summary']['failed']==0 else 'FAIL ❌'}",
    ])
    
    if report['summary']['failed'] == 0:
        lines.extend([
            "",
            "✅ **Ready for deployment!**",
            "",
            "Reply with `deploy` to proceed with production deployment.",
        ])
    else:
        lines.extend([
            "",
            "⚠️ **Issues found. Fix before deploying.**",
        ])
    
    return "\n".join(lines)

def deploy():
    print(color("\n" + "="*60, "bold"))
    print(color("🚀 PHASE 2: DEPLOYMENT", "bold"))
    print(color("="*60, "bold"))
    
    # Build
    print("📦 Building project...")
    result = subprocess.run(
        ["dotnet", "publish", "-c", "Release", "-o", "./publish"],
        cwd="/home/devuser/my-cicd-project/App",
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print(color("❌ Build failed:\n" + result.stderr, "red"))
        return False
    print(color("✅ Build successful", "green"))
    
    # Here you would add your actual deploy step:
    # - SCP to server
    # - Docker push + restart
    # - GitHub Actions trigger
    # - systemd restart
    
    print(color("✅ Deployment artifacts ready at ./App/publish/", "green"))
    print(color("📝 Next: Push to server or restart service manually", "yellow"))
    return True

def main():
    skip_qa = "--skip-qa" in sys.argv
    force = "--force" in sys.argv
    
    if not skip_qa:
        passed, report = run_tests()
        md = generate_markdown_report(report)
        
        with open("/home/devuser/my-cicd-project/qa-report.md", "w") as f:
            f.write(md)
        
        print(color("\n" + "="*60, "bold"))
        print(color("📋 QA REPORT (Discord Format)", "bold"))
        print(color("="*60, "bold"))
        print(md)
        
        if not passed and not force:
            print(color("\n❌ QA FAILED. Fix issues or use --force to deploy anyway.", "red"))
            sys.exit(1)
        
        if passed or force:
            print(color("\n✅ QA PASSED. Ready to deploy.", "green"))
            print(color("🤖 In Discord: Reply 'deploy' and I will execute deployment.", "blue"))
    else:
        print(color("⏩ Skipping QA (--skip-qa)", "yellow"))
        deploy()

if __name__ == "__main__":
    main()
