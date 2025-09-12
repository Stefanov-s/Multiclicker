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
    print("🚀 Building Advanced Autoclicker AppImage...")
    
    # Check if we're on Linux
    if sys.platform != "linux":
        print("❌ AppImage can only be built on Linux")
        return False
    
    # Create build directory
    build_dir = Path("appimage-build")
    app_dir = build_dir / "AdvancedAutoclicker.AppDir"
    
    if build_dir.exists():
        shutil.rmtree(build_dir)
    
    app_dir.mkdir(parents=True)
    
    print("📦 Setting up AppDir structure...")
    
    # Create directory structure
    (app_dir / "usr" / "bin").mkdir(parents=True)
    (app_dir / "usr" / "lib").mkdir(parents=True)
    (app_dir / "usr" / "share" / "applications").mkdir(parents=True)
    (app_dir / "usr" / "share" / "icons" / "hicolor" / "256x256" / "apps").mkdir(parents=True)
    (app_dir / "usr" / "lib" / "x86_64-linux-gnu").mkdir(parents=True)
    
    # Copy main application
    shutil.copy2("autoclicker.py", app_dir / "usr" / "bin" / "autoclicker.py")
    
    # Create desktop file
    desktop_content = """[Desktop Entry]
Type=Application
Name=Advanced Autoclicker
Comment=Multi-clicker and click recorder automation tool
Exec=autoclicker
Icon=autoclicker
Categories=Utility;
Terminal=false
"""
    
    with open(app_dir / "AdvancedAutoclicker.desktop", "w") as f:
        f.write(desktop_content)
    
    with open(app_dir / "usr" / "share" / "applications" / "AdvancedAutoclicker.desktop", "w") as f:
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
export LD_LIBRARY_PATH="${HERE}/usr/lib:${HERE}/usr/lib/x86_64-linux-gnu:${LD_LIBRARY_PATH}"
export PYTHONPATH="${HERE}/usr/lib/python3/site-packages:${PYTHONPATH}"

# Set up X11 environment
export DISPLAY="${DISPLAY:-:0}"

# Ensure xdotool can find libraries
export LD_LIBRARY_PATH="${HERE}/usr/lib/x86_64-linux-gnu:${LD_LIBRARY_PATH}"

# Check if we have bundled xdotool
if [ -f "${HERE}/usr/bin/xdotool" ]; then
    chmod +x "${HERE}/usr/bin/xdotool"
    echo "Using bundled xdotool"
else
    echo "Warning: xdotool not bundled, may need system installation"
fi

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
    
    # Install Python dependencies
    if not run_command(f"pip3 install --target {python_lib_dir} pynput==1.7.6"):
        print("❌ Failed to install pynput")
        return False
    
    print("📦 Bundling system dependencies...")
    
    # Bundle xdotool binary and its dependencies
    try:
        # Find xdotool binary
        result = subprocess.run(['which', 'xdotool'], check=True, capture_output=True, text=True)
        xdotool_path = result.stdout.strip()
        
        # Copy xdotool to AppImage
        shutil.copy2(xdotool_path, app_dir / "usr" / "bin" / "xdotool")
        print("✅ Bundled xdotool binary")
        
        # Find and copy xdotool dependencies
        ldd_result = subprocess.run(['ldd', xdotool_path], capture_output=True, text=True)
        if ldd_result.returncode == 0:
            lib_dir = app_dir / "usr" / "lib" / "x86_64-linux-gnu"
            for line in ldd_result.stdout.split('\n'):
                if '=>' in line and '/lib' in line:
                    parts = line.strip().split('=>')
                    if len(parts) == 2:
                        lib_path = parts[1].strip().split()[0]
                        if os.path.exists(lib_path) and not lib_path.startswith('/lib64/ld-'):
                            lib_name = os.path.basename(lib_path)
                            try:
                                shutil.copy2(lib_path, lib_dir / lib_name)
                                print(f"  📚 Bundled library: {lib_name}")
                            except Exception as e:
                                print(f"  ⚠️  Could not copy {lib_name}: {e}")
        
    except subprocess.CalledProcessError:
        print("⚠️  xdotool not found on system - installing from package...")
        
        # Try to install xdotool temporarily to bundle it
        temp_install_dir = build_dir / "temp_install"
        temp_install_dir.mkdir(exist_ok=True)
        
        # Download and extract xdotool package
        if not run_command(f"apt download xdotool", cwd=temp_install_dir):
            print("❌ Could not download xdotool package")
        else:
            # Extract the .deb package
            deb_files = list(temp_install_dir.glob("xdotool*.deb"))
            if deb_files:
                deb_file = deb_files[0]
                extract_dir = temp_install_dir / "extracted"
                extract_dir.mkdir(exist_ok=True)
                
                if run_command(f"dpkg-deb -x {deb_file} {extract_dir}", cwd=temp_install_dir):
                    # Find and copy xdotool binary
                    xdotool_bins = list(extract_dir.rglob("xdotool"))
                    if xdotool_bins:
                        shutil.copy2(xdotool_bins[0], app_dir / "usr" / "bin" / "xdotool")
                        print("✅ Bundled xdotool from package")
    
    except Exception as e:
        print(f"⚠️  Could not bundle xdotool: {e}")
        print("   AppImage will work but may need system xdotool for full functionality")
    
    # Bundle essential X11 libraries if available
    x11_libs = [
        '/usr/lib/x86_64-linux-gnu/libX11.so.6',
        '/usr/lib/x86_64-linux-gnu/libXtst.so.6',
        '/usr/lib/x86_64-linux-gnu/libXext.so.6',
        '/usr/lib/x86_64-linux-gnu/libXfixes.so.3',
        '/usr/lib/x86_64-linux-gnu/libXi.so.6'
    ]
    
    lib_dir = app_dir / "usr" / "lib" / "x86_64-linux-gnu"
    for lib_path in x11_libs:
        if os.path.exists(lib_path):
            try:
                shutil.copy2(lib_path, lib_dir / os.path.basename(lib_path))
                print(f"  📚 Bundled X11 library: {os.path.basename(lib_path)}")
            except Exception as e:
                print(f"  ⚠️  Could not copy {os.path.basename(lib_path)}: {e}")
    
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
    if not run_command(f"./{appimagetool_path} {app_dir} AdvancedAutoclicker-x86_64.AppImage"):
        print("❌ Failed to build AppImage")
        return False
    
    # Make the AppImage executable
    if os.path.exists("AdvancedAutoclicker-x86_64.AppImage"):
        os.chmod("AdvancedAutoclicker-x86_64.AppImage", 0o755)
        print("✅ AppImage built successfully: AdvancedAutoclicker-x86_64.AppImage")
        print("📦 You can now distribute this single file to any Linux system!")
        print("")
        print("🎯 Usage:")
        print("   sudo usermod -a -G input $USER  # One-time setup")
        print("   # Log out and log back in")
        print("   ./AdvancedAutoclicker-x86_64.AppImage")
        return True
    else:
        print("❌ AppImage file not found after build")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
