#!/usr/bin/env python
import os
import sys
import subprocess

# Change to the app directory
app_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(app_dir)
sys.path.insert(0, app_dir)

# Run uvicorn
subprocess.run([sys.executable, "-m", "uvicorn", "app.app:app", "--reload", "--port", "8000"])
