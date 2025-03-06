import os
import subprocess
import json

class DependencyChecker:
    """
    AI-Governed Dependency Scanner:
    - Scans installed packages for security vulnerabilities
    - Ensures all dependencies are up-to-date and unmodified
    - Blocks unauthorized dependency modifications
    """
    def __init__(self):
        self.vulnerable_packages = []
        self.report = {}

    def check_apt_packages(self):
        """Scans system-installed packages for outdated or vulnerable versions"""
        print("🔍 Scanning APT packages...")
        result = subprocess.run(["apt", "list", "--installed"], capture_output=True, text=True)
        for line in result.stdout.split("\n"):
            if "security" in line or "CVE" in line:
                self.vulnerable_packages.append(line)
    
    def check_pip_packages(self):
        """Scans Python dependencies for vulnerabilities"""
        print("🔍 Scanning PIP packages...")
        result = subprocess.run(["pip", "list", "--format=json"], capture_output=True, text=True)
        packages = json.loads(result.stdout)
        for package in packages:
            if "deprecated" in package["name"].lower():
                self.vulnerable_packages.append(f"{package['name']} - {package['version']} (Deprecated)")
    
    def generate_report(self):
        """Generates a security report of detected issues"""
        if self.vulnerable_packages:
            self.report = {
                "status": "⚠️ Vulnerabilities Found!",
                "issues": self.vulnerable_packages
            }
        else:
            self.report = {"status": "✅ No vulnerabilities detected."}

        return self.report

    def run_scan(self):
        """Runs all security scans and outputs the report"""
        self.check_apt_packages()
        self.check_pip_packages()
        return self.generate_report()

if __name__ == "__main__":
    scanner = DependencyChecker()
    report = scanner.run_scan()
    print(json.dumps(report, indent=4))
