#!/usr/bin/env python
"""Quick start script for IT Support Assistant"""

import subprocess
import sys
import time

print("=" * 60)
print("🚀 IT Support Assistant - Quick Start")
print("=" * 60)

# Install dependencies
print("\n📦 Installing dependencies...")
deps = ["streamlit", "requests", "pandas", "streamlit-option-menu", "python-dotenv"]

for dep in deps:
    try:
        __import__(dep.replace("-", "_"))
        print(f"   ✓ {dep} already installed")
    except ImportError:
        print(f"   ⏳ Installing {dep}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", dep, "-q"])
        print(f"   ✓ {dep} installed")

print("\n" + "=" * 60)
print("✅ All dependencies installed!")
print("=" * 60)

print("\n🌐 Starting Streamlit app...")
print("   Opening: http://localhost:8501")
print("\n💡 Demo Credentials:")
print("   User: user@example.com / password123")
print("   Admin: admin@example.com / admin123")
print("\n⚠️  Note: Backend must be running on http://localhost:8000")
print("=" * 60 + "\n")

# Start Streamlit
subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"])
