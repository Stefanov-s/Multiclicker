#!/usr/bin/env python3
"""
Build script to create AppImage for Multi-Clicker Autoclicker
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def run_command(cmd, cwd=None):
    """Run a command and return success status"""
    print(f"Running: {cmd}")
    try:
        result = subprocess.run(cmd, shell=True, check=True, cwd=cwd, 
                              capture_output=True, text=True)
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        print(f"Stdout: {e.stdout}")
        print(f"Stderr: {e.stderr}")
        return False

def main():
    print("🚀 Building Multi-Clicker Autoclicker AppImage...")
    
    # Check if we're on Linux
    if sys.platform != "linux":
        print("❌ AppImage can only be built on Linux")
        return False
    
    # Create build directory
    build_dir = Path("appimage-build")
    app_dir = build_dir / "MultiClickerAutoclicker.AppDir"
    
    if build_dir.exists():
        shutil.rmtree(build_dir)
    
    app_dir.mkdir(parents=True)
    
    print("📦 Setting up AppDir structure...")
    
    # Create directory structure
    (app_dir / "usr" / "bin").mkdir(parents=True)
    (app_dir / "usr" / "lib").mkdir(parents=True)
    (app_dir / "usr" / "share" / "applications").mkdir(parents=True)
    (app_dir / "usr" / "share" / "icons" / "hicolor" / "256x256" / "apps").mkdir(parents=True)
    
    # Copy main application
    shutil.copy2("autoclicker.py", app_dir / "usr" / "bin" / "autoclicker.py")
    
    # Create desktop file
    desktop_content = """[Desktop Entry]
Type=Application
Name=Multi-Clicker Autoclicker
Comment=Advanced multi-clicker automation tool
Exec=autoclicker
Icon=autoclicker
Categories=Utility;
Terminal=false
"""
    
    with open(app_dir / "MultiClickerAutoclicker.desktop", "w") as f:
        f.write(desktop_content)
    
    with open(app_dir / "usr" / "share" / "applications" / "MultiClickerAutoclicker.desktop", "w") as f:
        f.write(desktop_content)
    
    # Create a simple icon (text-based for now)
    icon_content = """<?xml version="1.0" encoding="UTF-8"?>
<svg width="256" height="256" xmlns="http://www.w3.org/2000/svg">
  <rect width="256" height="256" fill="#212121"/>
  <rect x="32" y="32" width="192" height="192" fill="#2b2b2b" stroke="#1f538d" stroke-width="4"/>
  <text x="128" y="140" font-family="Arial" font-size="48" font-weight="bold" 
        text-anchor="middle" fill="#ffffff">MC</text>
  <text x="128" y="180" font-family="Arial" font-size="16" 
        text-anchor="middle" fill="#b0b0b0">Autoclicker</text>
</svg>"""
    
    with open(app_dir / "autoclicker.svg", "w") as f:
        f.write(icon_content)
    
    with open(app_dir / "usr" / "share" / "icons" / "hicolor" / "256x256" / "apps" / "autoclicker.svg", "w") as f:
        f.write(icon_content)
    
    # Create AppRun script
    apprun_content = """#!/bin/bash
HERE="$(dirname "$(readlink -f "${0}")")"
export APPDIR="$HERE"
export PATH="${HERE}/usr/bin:${PATH}"
export LD_LIBRARY_PATH="${HERE}/usr/lib:${LD_LIBRARY_PATH}"
export PYTHONPATH="${HERE}/usr/lib/python3/site-packages:${PYTHONPATH}"

cd "${HERE}/usr/bin"
exec python3 autoclicker.py "$@"
"""
    
    with open(app_dir / "AppRun", "w") as f:
        f.write(apprun_content)
    
    # Make AppRun executable
    os.chmod(app_dir / "AppRun", 0o755)
    
    # Install Python dependencies into the AppImage
    print("📦 Installing Python dependencies...")
    
    python_lib_dir = app_dir / "usr" / "lib" / "python3" / "site-packages"
    python_lib_dir.mkdir(parents=True)
    
    # Install pynput
    if not run_command(f"pip3 install --target {python_lib_dir} pynput==1.7.6"):
        print("❌ Failed to install pynput")
        return False
    
    print("🔧 Downloading appimagetool...")
    
    # Download appimagetool if not exists
    appimagetool_path = "appimagetool-x86_64.AppImage"
    if not os.path.exists(appimagetool_path):
        if not run_command(f"wget -O {appimagetool_path} https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"):
            print("❌ Failed to download appimagetool")
            return False
        
        os.chmod(appimagetool_path, 0o755)
    
    print("🏗️ Building AppImage...")
    
    # Build the AppImage
    if not run_command(f"./{appimagetool_path} {app_dir} MultiClickerAutoclicker-x86_64.AppImage"):
        print("❌ Failed to build AppImage")
        return False
    
    # Make the AppImage executable
    if os.path.exists("MultiClickerAutoclicker-x86_64.AppImage"):
        os.chmod("MultiClickerAutoclicker-x86_64.AppImage", 0o755)
        print("✅ AppImage built successfully: MultiClickerAutoclicker-x86_64.AppImage")
        print("📦 You can now distribute this single file to any Linux system!")
        return True
    else:
        print("❌ AppImage file not found after build")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
