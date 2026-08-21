#!/usr/bin/env python3
"""
Verification script for Changeset project setup.
Tests that all requirements are met without requiring AWS credentials.
"""

import sys
import os
from pathlib import Path


def check_file_exists(filepath, description):
    """Check if a file exists and report status."""
    if Path(filepath).exists():
        print(f"✅ {description}: {filepath}")
        return True
    else:
        print(f"❌ {description} MISSING: {filepath}")
        return False


def check_python_version():
    """Verify Python version >= 3.10"""
    version = sys.version_info
    if version.major == 3 and version.minor >= 10:
        print(f"✅ Python version: {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"❌ Python version {version.major}.{version.minor} < 3.10")
        return False


def check_syntax(filepath):
    """Check if Python file has valid syntax."""
    try:
        with open(filepath, 'r') as f:
            compile(f.read(), filepath, 'exec')
        print(f"✅ Valid syntax: {filepath}")
        return True
    except SyntaxError as e:
        print(f"❌ Syntax error in {filepath}: {e}")
        return False


def main():
    print("=" * 60)
    print("Changeset Project Verification")
    print("=" * 60)
    print()

    checks = []

    print("1. Python Version")
    checks.append(check_python_version())
    print()

    print("2. Required Files")
    checks.append(check_file_exists("requirements.txt", "Dependencies file"))
    checks.append(check_file_exists("pyproject.toml", "Project metadata"))
    checks.append(check_file_exists("LICENSE", "MIT License"))
    checks.append(check_file_exists("README.md", "Documentation"))
    checks.append(check_file_exists(".gitignore", "Git ignore rules"))
    checks.append(check_file_exists(".env.example", "Environment template"))
    print()

    print("3. Package Structure")
    checks.append(check_file_exists("changeset/__init__.py", "Package init"))
    checks.append(check_file_exists("changeset/agent.py", "Agent implementation"))
    print()

    print("4. Python Syntax Validation")
    checks.append(check_syntax("changeset/__init__.py"))
    checks.append(check_syntax("changeset/agent.py"))
    print()

    print("5. Content Checks")
    
    with open("requirements.txt", 'r') as f:
        requirements = f.read()
        if "strands-agents>=1.0.0" in requirements:
            print("✅ strands-agents pinned correctly")
            checks.append(True)
        else:
            print("❌ strands-agents version not pinned")
            checks.append(False)
        
        if "strands-agents-tools>=0.2.0" in requirements:
            print("✅ strands-agents-tools pinned correctly")
            checks.append(True)
        else:
            print("❌ strands-agents-tools version not pinned")
            checks.append(False)
    
    with open("changeset/agent.py", 'r') as f:
        agent_code = f.read()
        if "from strands.vended_interventions.hitl import HumanInTheLoop" in agent_code:
            print("✅ HumanInTheLoop import path correct")
            checks.append(True)
        else:
            print("❌ HumanInTheLoop import path incorrect")
            checks.append(False)
        
        if "allowed_tools=['scan_site', 'draft_changeset']" in agent_code:
            print("✅ HITL configured with allowed_tools")
            checks.append(True)
        else:
            print("❌ HITL allowed_tools configuration missing")
            checks.append(False)
        
        if "@tool" in agent_code and "def scan_site" in agent_code:
            print("✅ scan_site tool defined")
            checks.append(True)
        else:
            print("❌ scan_site tool missing")
            checks.append(False)
        
        if "@tool" in agent_code and "def draft_changeset" in agent_code:
            print("✅ draft_changeset tool defined")
            checks.append(True)
        else:
            print("❌ draft_changeset tool missing")
            checks.append(False)
        
        if "@tool" in agent_code and "def publish_changeset" in agent_code:
            print("✅ publish_changeset tool defined")
            checks.append(True)
        else:
            print("❌ publish_changeset tool missing")
            checks.append(False)
    
    with open("LICENSE", 'r') as f:
        license_text = f.read()
        if "MIT License" in license_text:
            print("✅ MIT License detected")
            checks.append(True)
        else:
            print("❌ MIT License not detected")
            checks.append(False)
    
    with open(".env.example", 'r') as f:
        env_example = f.read()
        if "AWS_ACCESS_KEY_ID" in env_example and "AWS_SECRET_ACCESS_KEY" in env_example:
            print("✅ AWS credential placeholders present")
            checks.append(True)
        else:
            print("❌ AWS credential placeholders missing")
            checks.append(False)
    
    print()
    print("=" * 60)
    passed = sum(checks)
    total = len(checks)
    print(f"Results: {passed}/{total} checks passed")
    
    if passed == total:
        print("✅ ALL CHECKS PASSED - Project setup complete!")
        return 0
    else:
        print(f"❌ {total - passed} check(s) failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
