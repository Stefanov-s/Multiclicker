# Multi-Clicker Autoclicker

A cross-platform Python autoclicker application with multiple independent clickers and global hotkey support.

## Features

- **3 Independent Clickers**: Each can be configured and enabled separately
- **Flexible Timing**: Configure minutes, seconds, and milliseconds for each clicker
- **Global Hotkey**: F9 to start/stop all enabled clickers
- **Cross-Platform**: Works on Windows and Linux
- **Real-time Status**: See click counts and current status for each clicker
- **Simultaneous Operation**: Multiple clickers can run with different intervals

## Requirements

- Python 3.6 or higher
- pip (Python package installer)

## Download Options

### Option 1: AppImage (Linux - Easiest)
**Self-contained AppImage** for instant use on any Linux distribution:
- **Zero dependencies** - includes Python, tkinter, pynput, xdotool, X11 libraries
- **Works out of the box** on any Linux distro (Ubuntu, Fedora, Arch, etc.)
- **Single file download** - no installation needed
- **Just make executable and run!**
- **Only requirement**: Add user to input group once: `sudo usermod -a -G input $USER`

```bash
# Download the AppImage (build it yourself for now)
python3 build_appimage.py

# Make executable and run
chmod +x MultiClickerAutoclicker-x86_64.AppImage
./MultiClickerAutoclicker-x86_64.AppImage
```

### Option 2: Manual Installation
Follow the installation instructions below for your operating system.

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

# Or use the shell script
./build_appimage.sh
```

This creates `MultiClickerAutoclicker-x86_64.AppImage` - a single file that:
- Contains all dependencies (Python, pynput, tkinter, xdotool, X11 libraries)
- Works on any Linux distribution without installing anything
- Includes bundled xdotool for clicking outside the app window
- Includes X11 libraries for maximum compatibility
- Requires no installation or system dependencies
- Just needs to be made executable: `chmod +x MultiClickerAutoclicker-x86_64.AppImage`
- Still requires adding user to input group: `sudo usermod -a -G input $USER`

## Usage

### Basic Operation

1. **Enable Clickers**: Check the "Enable" checkbox for the clickers you want to use
2. **Set Timing**: Configure minutes, seconds, and milliseconds for each enabled clicker
3. **Start Clicking**: Press F9 or click "Start All Enabled" to begin
4. **Stop Clicking**: Press F9 again or click "Stop All" to stop

### Example Scenarios

**Scenario 1: Single Clicker**
- Enable Clicker 1
- Set to 0 minutes, 5 seconds, 0 milliseconds
- Press F9 - clicks every 5 seconds

**Scenario 2: Multiple Clickers**
- Enable Clicker 1: 0 minutes, 10 seconds, 0 milliseconds
- Enable Clicker 2: 0 minutes, 15 seconds, 0 milliseconds
- Press F9 - clicks at 10s, 15s, 20s, 30s, 40s, 45s...

### Important Notes

- **Mouse Position**: Clicks occur at the current mouse cursor position when the hotkey is pressed
- **Minimum Timing**: The minimum interval is 10 milliseconds
- **Global Hotkey**: F9 works system-wide, even when the application is not in focus
- **Thread Safety**: Each clicker runs independently in its own thread

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
