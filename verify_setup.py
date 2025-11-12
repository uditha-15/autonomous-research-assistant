#!/usr/bin/env python3
"""Simple verification script to check if setup is correct."""
import os
import sys

def check_file(filename, description):
    """Check if a file exists."""
    if os.path.exists(filename):
        print(f"✅ {description}: {filename}")
        return True
    else:
        print(f"❌ {description}: {filename} - MISSING!")
        return False

def check_directory(dirname, description):
    """Check if a directory exists."""
    if os.path.isdir(dirname):
        print(f"✅ {description}: {dirname}/")
        return True
    else:
        print(f"❌ {description}: {dirname}/ - MISSING!")
        return False

print("=" * 60)
print("Verifying Project Setup")
print("=" * 60)
print()

all_good = True

# Check core files
print("Core Files:")
all_good &= check_file("app.py", "Flask web application")
all_good &= check_file("requirements.txt", "Python dependencies")
all_good &= check_file("Procfile", "Render Procfile")
all_good &= check_file("render.yaml", "Render configuration")
all_good &= check_file("runtime.txt", "Python version")
all_good &= check_file("config.py", "Configuration module")
all_good &= check_file("memory.py", "Memory module")
all_good &= check_file("research_assistant.py", "Main orchestrator")
all_good &= check_file("web_scraper.py", "Web scraper")
print()

# Check agent files
print("Agent Files:")
all_good &= check_directory("agents", "Agents directory")
all_good &= check_file("agents/__init__.py", "Agents init")
all_good &= check_file("agents/base_agent.py", "Base agent")
all_good &= check_file("agents/researcher.py", "Researcher agent")
all_good &= check_file("agents/planner.py", "Planner agent")
all_good &= check_file("agents/data_alchemist.py", "Data alchemist")
all_good &= check_file("agents/experimenter.py", "Experimenter agent")
all_good &= check_file("agents/reviewer.py", "Reviewer agent")
all_good &= check_file("agents/critic.py", "Critic agent")
print()

# Check web files
print("Web Interface Files:")
all_good &= check_directory("templates", "Templates directory")
all_good &= check_file("templates/index.html", "Web interface")
print()

# Check config files
print("Configuration Files:")
all_good &= check_file(".env.example", "Environment example")
all_good &= check_file(".gitignore", "Git ignore")
print()

# Check documentation
print("Documentation:")
all_good &= check_file("README.md", "README")
all_good &= check_file("HOSTING_GUIDE.md", "Hosting guide")
print()

print("=" * 60)
if all_good:
    print("✅ All files present! Project is ready for deployment.")
    print()
    print("Next steps:")
    print("1. Get Google Gemini API key from: https://makersuite.google.com/app/apikey")
    print("2. Push code to GitHub")
    print("3. Deploy on Render (see HOSTING_GUIDE.md)")
    sys.exit(0)
else:
    print("❌ Some files are missing. Please check above.")
    sys.exit(1)

