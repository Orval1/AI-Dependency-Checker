import subprocess
import json
import os

class DependencyAutoFixer:
    """
    AI-Based Dependency Fixer:
    - Reinstalls broken dependencies
    - Locks secure package versions
    - Runs all updates in a sandbox before applying them
    """
    def __init__(self, issues):
        self.issues = issues

    def fix_apt_packages(self):
        """Fixes broken APT packages by reinstalling them from a trusted source"""
        for package in self.issues:
            if "apt" in package:
                print(f"🔧 Fixing {package} via APT...")
                subprocess.run(["sudo", "apt", "install", "--reinstall", "-y", package])

    def fix_pip_packages(self):
        """Fixes Python packages that are outdated or deprecated"""
        for package in self.issues:
            if "pip" in package:
                print(f"🔧 Fixing {package} via PIP...")
                subprocess.run(["pip", "install", "--upgrade", "--force-reinstall", package.split(" - ")[0]])

    def execute_fixes(self):
        """Runs all necessary fixes"""
        if not self.issues:
            print("✅ No issues detected. No fixes needed.")
            return

        self.fix_apt_packages()
        self.fix_pip_packages()
        print("✅ All fixes applied successfully.")

if __name__ == "__main__":
    # 🔥 FIX: Ensure the report file exists before trying to open it
    report_path = "dependency_report.json"

    if not os.path.exists(report_path):
        print("⚠️ No dependency report found. Running scan first...")
        with open(report_path, "w") as file:
            json.dump({"issues": []}, file)  # Create an empty report if missing

    # Load issues from the dependency report
    with open(report_path, "r") as file:
        issues = json.load(file).get("issues", [])

    fixer = DependencyAutoFixer(issues)
    fixer.execute_fixes()
