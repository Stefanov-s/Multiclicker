# Advanced Autoclicker

A cross-platform Python autoclicker application with multiple modes and advanced automation features.

## Features

### 🎯 Multi-Clicker Mode
- **3 Independent Clickers**: Each can be configured and enabled separately
- **Coordinate-Based Clicking**: Set specific screen coordinates for each clicker
- **Flexible Timing**: Configure minutes, seconds, and milliseconds for each clicker
- **Real-time Status**: See click counts and current status for each clicker
- **Test Functionality**: Test coordinates before starting
- **Reset Options**: Reset individual clickers or all at once

### 🎬 Click Recorder Mode
- **Record Click Sequences**: Record exact coordinates and timing of your clicks
- **Precise Replay**: Replay sequences with original timing preserved
- **Multiple Replays**: Set how many times to repeat the sequence
- **Real-time Feedback**: See recording progress and replay status
- **Sequence Management**: Clear recordings and start fresh

### 🎮 Global Controls
- **Hotkeys**: F9 (Multi-Clicker), F10 (Record/Stop Recording)
- **Cross-Platform**: Works on Windows and Linux
- **Tabbed Interface**: Easy switching between modes

## Requirements

- Python 3.6 or higher
- pip (Python package installer)

## Quick Start Options

### 🚀 Option 1: AppImage (Linux - Recommended)
**Self-contained AppImage** for instant use on any Linux distribution:

#### ✨ **Why AppImage?**
- ✅ **Zero dependencies** - includes Python, tkinter, pynput, xdotool, X11 libraries
- ✅ **Works everywhere** - any Linux distro (Ubuntu, Fedora, Arch, Mint, etc.)
- ✅ **Single file** - no installation, no package management
- ✅ **Portable** - run from USB stick, share easily
- ✅ **Out-of-window clicking** - bundled xdotool for Linux clicking outside app
- ✅ **Always works** - no dependency conflicts or missing packages

#### 📦 **How to Build AppImage:**
```bash
# 1. Clone this repository
git clone https://github.com/yourusername/autoclicker
cd autoclicker

# 2. Build the AppImage (requires Linux)
python3 build_appimage.py

# 3. Make executable
chmod +x AdvancedAutoclicker-x86_64.AppImage
```

#### 🎯 **How to Use AppImage:**
```bash
# 1. One-time setup: Add user to input group (required for mouse control)
sudo usermod -a -G input $USER

# 2. Log out and log back in (or reboot)

# 3. Run the AppImage
./AdvancedAutoclicker-x86_64.AppImage
```

#### 🔧 **AppImage Features:**
- **Bundled xdotool**: Clicks work outside app window on Ubuntu/Linux
- **All libraries included**: X11, tkinter, pynput - no system packages needed
- **Cross-distro**: Works on Ubuntu, Fedora, Arch, openSUSE, Mint, etc.
- **Version independent**: Works regardless of system Python version

### 📝 Option 2: Manual Installation
If you prefer to install from source, follow the installation instructions below.

## Installation

### Windows

1. **Clone or download this repository**
2. **Open Command Prompt or PowerShell as Administrator** (required for global hotkeys)
3. **Navigate to the project directory**:
   ```cmd
   cd path\to\Autoclicker
   ```
4. **Install dependencies**:
   ```cmd
   pip install -r requirements.txt
   ```
5. **Run the application**:
   ```cmd
   python autoclicker.py
   ```

### Linux

1. **Clone or download this repository**
2. **Install Python, pip, and required system packages**:
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip python3-venv python3-tk xdotool
   ```
   
   **For other distributions:**
   ```bash
   # CentOS/RHEL/Fedora
   sudo dnf install python3-tkinter python3-pip xdotool
   
   # Arch Linux
   sudo pacman -S tk python-pip xdotool
   
   # OpenSUSE
   sudo zypper install python3-tk python3-pip xdotool
   ```
   
   **Note**: `xdotool` is needed for clicking outside the application window on Linux.
3. **Navigate to the project directory**:
   ```bash
   cd /path/to/Autoclicker
   ```
4. **Choose ONE of these methods to install dependencies**:

   **Method 1: Virtual Environment (Recommended)**
   ```bash
   # Create virtual environment
   python3 -m venv autoclicker-env
   
   # Activate it
   source autoclicker-env/bin/activate
   
   # Install dependencies
   pip install -r requirements.txt
   
   # Run the application
   python autoclicker.py
   ```
   
   **Method 2: User Install (Alternative)**
   ```bash
   pip3 install --user -r requirements.txt
   python3 autoclicker.py
   ```
   
   **Method 3: System Package (If available)**
   ```bash
   sudo apt install python3-pynput
   python3 autoclicker.py
   ```
   
   **Method 4: Override Protection (Not recommended)**
   ```bash
   pip3 install --break-system-packages -r requirements.txt
   python3 autoclicker.py
   ```

5. **Add your user to the input group** (for mouse control):
   ```bash
   sudo usermod -a -G input $USER
   ```
6. **Log out and log back in** for group changes to take effect
7. **Run the application** (use method from step 4)

## Building AppImage (Linux Only)

To create a portable AppImage that works on any Linux distribution:

```bash
# On Linux, run the build script
python3 build_appimage.py

# Or use the shell script (if available)
./build_appimage.sh
```

This creates `AdvancedAutoclicker-x86_64.AppImage` - a single file that:
- ✅ **Complete package**: Python, pynput, tkinter, xdotool, X11 libraries
- ✅ **Universal compatibility**: Works on any Linux distribution
- ✅ **Out-of-window clicking**: Bundled xdotool handles Ubuntu/Linux restrictions  
- ✅ **No installation needed**: Just make executable and run
- ✅ **Portable**: Copy to USB stick, share with others
- ⚠️ **One requirement**: User must be in input group: `sudo usermod -a -G input $USER`

### AppImage Build Requirements:
- Linux system (Ubuntu, Fedora, etc.)
- Python 3 and pip installed
- Internet connection (downloads dependencies)
- About 100MB free space for build process

## Usage

The application has two modes accessible via tabs:

### 🎯 Multi-Clicker Mode

#### Basic Operation:
1. **Enable Clickers**: Check "Enable" for clickers you want to use
2. **Set Timing**: Configure minutes, seconds, milliseconds for each clicker  
3. **Choose Coordinates**: Click "Choose Coordinates" and click where you want each clicker to click
4. **Test Coordinates**: Use "Test" button to verify click positions
5. **Start Clicking**: Press **F9** or click "Start All"
6. **Stop Clicking**: Press **F9** again or click "Stop All"

#### Features:
- **Coordinate-based**: Clicks at specific screen positions (not mouse cursor)
- **Independent timing**: Each clicker can have different intervals
- **Test functionality**: Verify coordinates before starting
- **Reset options**: Reset individual clickers or all at once

### 🎬 Click Recorder Mode

#### Recording:
1. **Switch to "Click Recorder" tab**
2. **Start Recording**: Click "Start Recording" or press **F10**
3. **Perform Clicks**: Click anywhere on screen - coordinates and timing recorded
4. **Stop Recording**: Press **F10** again or click "Stop Recording"

#### Replaying:
1. **Set Replay Count**: Enter how many times to repeat the sequence
2. **Start Replay**: Click "Start Replay" 
3. **Watch**: Sequence replays with original timing and coordinates
4. **Stop Early**: Click "Stop Replay" if needed

#### Features:
- **Exact reproduction**: Records precise coordinates and timing
- **Multiple replays**: Repeat sequences any number of times
- **Real-time feedback**: See recording progress and replay status
- **Sequence management**: Clear and re-record as needed

### 🎮 Global Hotkeys
- **F9**: Start/Stop Multi-Clicker mode
- **F10**: Start/Stop Recording in Recorder mode
- Work system-wide even when app is not focused

### 💡 Example Scenarios

**Multi-Clicker Example:**
- Enable Clicker 1: Set to click at (100, 200) every 5 seconds
- Enable Clicker 2: Set to click at (300, 400) every 10 seconds
- Press F9 - both click at their coordinates simultaneously

**Recorder Example:**
- Press F10 to start recording
- Click through a sequence: login → navigate → submit → etc.
- Press F10 to stop
- Set replay count to 10
- Click "Start Replay" - sequence repeats 10 times exactly

## Troubleshooting

### Windows Issues

**"Access Denied" or hotkeys not working:**
- Run Command Prompt or PowerShell as Administrator
- Some antivirus software may block global hotkey functionality

**Mouse clicks not registering:**
- Ensure no other applications are blocking mouse input
- Try running as Administrator

### Linux Issues

**"Permission denied" errors:**
- Make sure you're in the input group: `groups $USER`
- If not, run: `sudo usermod -a -G input $USER` and log out/in
- For some distributions, you might need to install additional packages:
  ```bash
  sudo apt install python3-tk python3-dev
  ```

**Global hotkeys not working:**
- **Most common issue**: Add user to input group: `sudo usermod -a -G input $USER` then log out/in
- **Wayland users**: Global hotkeys may not work due to security restrictions - switch to X11 session
- **Alternative**: Install xdotool: `sudo apt install xdotool`
- **Fallback**: Use the GUI buttons instead of F9 hotkey
- Try running from terminal to see error messages

**Clicking doesn't work outside app window:**
- **Install xdotool**: `sudo apt install xdotool` (most important)
- **Add to input group**: `sudo usermod -a -G input $USER` then log out/in
- **Wayland issue**: Switch to X11 session if using Wayland
- **Check display server**: Run `echo $XDG_SESSION_TYPE` - should be "x11" not "wayland"

**X11 Display issues:**
- If running remotely, ensure X11 forwarding is enabled
- For headless systems, you may need a virtual display

### General Issues

**"ModuleNotFoundError: No module named 'pynput'":**
- Install dependencies: `pip install -r requirements.txt`
- On Linux, try: `pip3 install -r requirements.txt`

**"ModuleNotFoundError: No module named 'tkinter'":**
- On Ubuntu/Debian: `sudo apt install python3-tk`
- On CentOS/RHEL/Fedora: `sudo dnf install python3-tkinter`
- On Arch Linux: `sudo pacman -S tk`

**Application freezes or crashes:**
- Check that timing values are reasonable (not too small)
- Ensure sufficient system resources
- Try disabling other clickers to isolate the issue

## Technical Details

### Dependencies
- **pynput**: For mouse control and global hotkey detection
- **tkinter**: GUI framework (included with Python)
- **threading**: For concurrent clicker operation (included with Python)

### Architecture
- **GUI**: Tkinter-based interface with 3 identical clicker sections
- **Threading**: Each active clicker runs in its own daemon thread
- **Mouse Control**: Uses pynput to perform left clicks at cursor position
- **Hotkeys**: Global F9 hotkey listener using pynput's GlobalHotKeys

### Timing Accuracy
- Timing is based on Python's `time.sleep()` function
- Actual timing may vary slightly due to system load and thread scheduling
- For high-precision timing requirements, consider the system's timer resolution

## License

This project is provided as-is for educational and personal use. Please use responsibly and in accordance with your local laws and the terms of service of any applications you interact with.

## Contributing

Feel free to submit issues, feature requests, or pull requests to improve this application.
