import os
import sys
import subprocess # nosec B404

REQUIREMENTS_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "requirements.txt")


def run_dependency_audit() -> bool:
    """Audits this project's declared dependencies (requirements.txt) for known vulnerabilities via pip-audit."""
    print("[*] Performing dependency vulnerability audit...")
    try:
        result = subprocess.run( # nosec B603
            [sys.executable, "-m", "pip_audit", "--format", "json", "-r", REQUIREMENTS_PATH],
            capture_output=True,
            text=True,
            check=False
        )
        if result.returncode == 0:
            print("[+] Dependency audit passed: No vulnerabilities found.")
            return True
        else:
            print("[!] Security vulnerabilities detected in dependencies!")
            print(result.stdout)
            return False
    except FileNotFoundError:
        print("[!] Warning: 'pip-audit' is not installed or not in PATH.")
        return False