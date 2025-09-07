#!/usr/bin/env python3
"""
Cross-Platform Autoclicker Application
Supports Windows and Linux with multiple independent clickers
"""

import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
from pynput import mouse, keyboard
from pynput.keyboard import GlobalHotKeys
import sys
import os

# Modern Dark Theme Colors (CustomTkinter Style)
COLORS = {
    'bg_main': '#212121',           # Dark gray main background
    'bg_section': '#2b2b2b',        # Slightly lighter gray for sections
    'bg_section_disabled': '#1a1a1a',  # Darker gray for disabled
    'accent_blue': '#1f538d',       # Primary blue accent
    'accent_blue_hover': '#14375e',  # Darker blue for hover
    'accent_blue_light': '#3d7bb8', # Lighter blue
    'text_primary': '#ffffff',      # White text
    'text_secondary': '#b0b0b0',    # Light gray text
    'text_disabled': '#707070',     # Darker gray for disabled
    'button_bg': '#1f538d',         # Blue button background
    'button_hover': '#14375e',      # Darker blue hover
    'button_disabled': '#404040',   # Dark gray for disabled buttons
    'entry_bg': '#404040',          # Dark gray for entry fields
    'entry_disabled': '#2a2a2a',    # Darker for disabled entries
    'border_color': '#404040'       # Border color
}


class ClickerSection:
    """Individual clicker section with its own configuration and controls"""
    
    def __init__(self, parent, section_id, on_config_change):
        self.section_id = section_id
        self.on_config_change = on_config_change
        self.enabled = tk.BooleanVar()
        self.enabled.trace_add('write', self._on_enabled_change)
        
        # Time variables
        self.minutes = tk.StringVar(value="0")
        self.seconds = tk.StringVar(value="1")
        self.milliseconds = tk.StringVar(value="0")
        
        # Status tracking
        self.is_active = False
        self.click_count = 0
        self.next_click_time = 0
        
        self._create_widgets(parent)
        
    def _create_widgets(self, parent):
        """Create the GUI widgets for this clicker section"""
        # Main frame for this section with compact modern styling
        self.frame = tk.Frame(parent, bg=COLORS['bg_section'], relief='flat', bd=1)
        self.frame.pack(fill="x", pady=3, padx=10, ipady=8, ipadx=10)
        
        # Title and checkbox in same row for compactness
        top_frame = tk.Frame(self.frame, bg=COLORS['bg_section'])
        top_frame.pack(fill="x", pady=(0, 8))
        
        title_label = tk.Label(top_frame, text=f"Clicker {self.section_id}", 
                              font=("Segoe UI", 11, "bold"), 
                              fg=COLORS['text_primary'], 
                              bg=COLORS['bg_section'])
        title_label.pack(side="left")
        
        self.enable_cb = tk.Checkbutton(
            top_frame, 
            text="Enable", 
            variable=self.enabled,
            font=("Segoe UI", 9),
            fg=COLORS['text_primary'],
            bg=COLORS['bg_section'],
            activebackground=COLORS['bg_section'],
            selectcolor=COLORS['accent_blue'],
            relief='flat',
            bd=0,
            highlightthickness=0
        )
        self.enable_cb.pack(side="right")
        
        # Time configuration in compact layout
        time_frame = tk.Frame(self.frame, bg=COLORS['bg_section'])
        time_frame.pack(fill="x", pady=(0, 8))
        
        # Minutes
        min_frame = tk.Frame(time_frame, bg=COLORS['bg_section'])
        min_frame.pack(side="left", padx=(0, 12))
        
        self.min_label = tk.Label(min_frame, text="Min:", 
                                 font=("Segoe UI", 8),
                                 fg=COLORS['text_secondary'], 
                                 bg=COLORS['bg_section'])
        self.min_label.pack()
        
        self.min_entry = tk.Entry(min_frame, textvariable=self.minutes, width=5,
                                 font=("Segoe UI", 9), 
                                 relief='flat', bd=0,
                                 bg=COLORS['entry_bg'],
                                 fg=COLORS['text_primary'],
                                 insertbackground=COLORS['text_primary'],
                                 highlightthickness=1,
                                 highlightcolor=COLORS['accent_blue'],
                                 justify='center')
        self.min_entry.pack()
        
        # Seconds
        sec_frame = tk.Frame(time_frame, bg=COLORS['bg_section'])
        sec_frame.pack(side="left", padx=(0, 12))
        
        self.sec_label = tk.Label(sec_frame, text="Sec:", 
                                 font=("Segoe UI", 8),
                                 fg=COLORS['text_secondary'], 
                                 bg=COLORS['bg_section'])
        self.sec_label.pack()
        
        self.sec_entry = tk.Entry(sec_frame, textvariable=self.seconds, width=5,
                                 font=("Segoe UI", 9), 
                                 relief='flat', bd=0,
                                 bg=COLORS['entry_bg'],
                                 fg=COLORS['text_primary'],
                                 insertbackground=COLORS['text_primary'],
                                 highlightthickness=1,
                                 highlightcolor=COLORS['accent_blue'],
                                 justify='center')
        self.sec_entry.pack()
        
        # Milliseconds
        ms_frame = tk.Frame(time_frame, bg=COLORS['bg_section'])
        ms_frame.pack(side="left")
        
        self.ms_label = tk.Label(ms_frame, text="Ms:", 
                                font=("Segoe UI", 8),
                                fg=COLORS['text_secondary'], 
                                bg=COLORS['bg_section'])
        self.ms_label.pack()
        
        self.ms_entry = tk.Entry(ms_frame, textvariable=self.milliseconds, width=5,
                                font=("Segoe UI", 9), 
                                relief='flat', bd=0,
                                bg=COLORS['entry_bg'],
                                fg=COLORS['text_primary'],
                                insertbackground=COLORS['text_primary'],
                                highlightthickness=1,
                                highlightcolor=COLORS['accent_blue'],
                                justify='center')
        self.ms_entry.pack()
        
        # Status display in compact row
        status_frame = tk.Frame(self.frame, bg=COLORS['bg_section'])
        status_frame.pack(fill="x")
        
        self.status_label = tk.Label(status_frame, text="Status: Disabled", 
                                    font=("Segoe UI", 8),
                                    fg=COLORS['text_secondary'], 
                                    bg=COLORS['bg_section'])
        self.status_label.pack(side="left")
        
        self.count_label = tk.Label(status_frame, text="Clicks: 0", 
                                   font=("Segoe UI", 8),
                                   fg=COLORS['text_secondary'], 
                                   bg=COLORS['bg_section'])
        self.count_label.pack(side="right")
        
        # Store all widgets for easy state management
        self.widgets = [
            self.frame, title_label, self.enable_cb, 
            self.min_label, self.min_entry,
            self.sec_label, self.sec_entry, 
            self.ms_label, self.ms_entry,
            self.status_label, self.count_label
        ]
        
        # Bind validation to entry fields
        for entry in [self.min_entry, self.sec_entry, self.ms_entry]:
            entry.bind('<KeyRelease>', self._validate_input)
            entry.bind('<FocusOut>', self._validate_input)
        
        # Initialize disabled state
        self._update_visual_state()
    
    def _update_visual_state(self):
        """Update visual appearance based on enabled/disabled state"""
        if self.enabled.get():
            # Enabled state - normal colors
            bg_color = COLORS['bg_section']
            text_color = COLORS['text_primary']
            text_secondary = COLORS['text_secondary']
            entry_state = 'normal'
            entry_bg = COLORS['entry_bg']
        else:
            # Disabled state - darker/muted
            bg_color = COLORS['bg_section_disabled']
            text_color = COLORS['text_disabled']
            text_secondary = COLORS['text_disabled']
            entry_state = 'disabled'
            entry_bg = COLORS['entry_disabled']
        
        # Update frame background
        self.frame.config(bg=bg_color)
        
        # Update all child frames
        for child in self.frame.winfo_children():
            if isinstance(child, tk.Frame):
                child.config(bg=bg_color)
                # Update grandchildren frames too
                for grandchild in child.winfo_children():
                    if isinstance(grandchild, tk.Frame):
                        grandchild.config(bg=bg_color)
                    elif isinstance(grandchild, tk.Label):
                        # Check if it's a title or secondary text
                        if "Clicker" in grandchild.cget("text"):
                            grandchild.config(bg=bg_color, fg=text_color)
                        else:
                            grandchild.config(bg=bg_color, fg=text_secondary)
        
        # Update entry fields
        for entry in [self.min_entry, self.sec_entry, self.ms_entry]:
            entry.config(state=entry_state, bg=entry_bg, 
                        disabledbackground=entry_bg, 
                        disabledforeground=text_color,
                        fg=text_color)
        
        # Update checkbox
        self.enable_cb.config(bg=bg_color, activebackground=bg_color, fg=text_color)
        
        # Update labels
        self.status_label.config(bg=bg_color, fg=text_secondary)
        self.count_label.config(bg=bg_color, fg=text_secondary)
    
    def _on_enabled_change(self, *args):
        """Handle enable/disable state changes"""
        self._update_visual_state()
        
        if self.enabled.get():
            self.status_label.config(text="Status: Enabled (Waiting for hotkey)")
        else:
            self.status_label.config(text="Status: Disabled")
            self.is_active = False
        self.on_config_change()
    
    def _validate_input(self, event=None):
        """Validate time input fields"""
        try:
            minutes = int(self.minutes.get()) if self.minutes.get() else 0
            seconds = int(self.seconds.get()) if self.seconds.get() else 0
            milliseconds = int(self.milliseconds.get()) if self.milliseconds.get() else 0
            
            # Validate ranges
            if minutes < 0 or minutes > 59:
                self.minutes.set("0")
            if seconds < 0 or seconds > 59:
                self.seconds.set("1")
            if milliseconds < 0 or milliseconds > 999:
                self.milliseconds.set("0")
                
            # Ensure at least some time is set
            total_ms = self.get_total_milliseconds()
            if total_ms < 10:  # Minimum 10ms
                self.milliseconds.set("10")
                
        except ValueError:
            # Reset to default values if invalid
            if not self.minutes.get().isdigit():
                self.minutes.set("0")
            if not self.seconds.get().isdigit():
                self.seconds.set("1")
            if not self.milliseconds.get().isdigit():
                self.milliseconds.set("0")
    
    def get_total_milliseconds(self):
        """Calculate total milliseconds from minutes, seconds, and milliseconds"""
        try:
            minutes = int(self.minutes.get()) if self.minutes.get() else 0
            seconds = int(self.seconds.get()) if self.seconds.get() else 0
            milliseconds = int(self.milliseconds.get()) if self.milliseconds.get() else 0
            
            return (minutes * 60 * 1000) + (seconds * 1000) + milliseconds
        except ValueError:
            return 1000  # Default to 1 second
    
    def update_status(self, is_active, click_count=None):
        """Update the status display"""
        self.is_active = is_active
        if click_count is not None:
            self.click_count = click_count
            
        if not self.enabled.get():
            self.status_label.config(text="Status: Disabled")
        elif is_active:
            self.status_label.config(text="Status: Active (Clicking)", fg=COLORS['accent_blue_light'])
        else:
            self.status_label.config(text="Status: Enabled (Waiting for hotkey)", fg=COLORS['accent_blue'])
            
        self.count_label.config(text=f"Clicks: {self.click_count}")


class AutoClicker:
    """Main application class"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.setup_window()
        
        # Clicker sections
        self.clickers = []
        self.clicker_threads = {}
        self.active_clickers = set()
        self.global_active = False
        
        # Mouse controller
        self.mouse_controller = mouse.Controller()
        
        # Global hotkey setup
        self.hotkey_listener = None
        self.setup_hotkeys()
        
        self.create_widgets()
        
    def setup_window(self):
        """Configure the main window"""
        self.root.title("Multi-Clicker Autoclicker")
        self.root.geometry("550x580")
        self.root.resizable(False, False)
        self.root.configure(bg=COLORS['bg_main'])
        
        # Handle window closing
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    def create_widgets(self):
        """Create all GUI widgets"""
        # Main container with compact modern styling
        main_frame = tk.Frame(self.root, bg=COLORS['bg_main'], padx=15, pady=15)
        main_frame.pack(fill="both", expand=True)
        
        # Compact header
        header_frame = tk.Frame(main_frame, bg=COLORS['bg_main'])
        header_frame.pack(fill="x", pady=(0, 15))
        
        # Main title with modern style
        title_label = tk.Label(header_frame, text="Multi-Clicker Autoclicker", 
                              font=("Segoe UI", 16, "bold"), 
                              fg=COLORS['text_primary'], 
                              bg=COLORS['bg_main'])
        title_label.pack()
        
        # Compact instructions
        instructions_frame = tk.Frame(main_frame, bg=COLORS['bg_section'], relief='flat', bd=1)
        instructions_frame.pack(fill="x", pady=(0, 12), padx=3)
        
        instructions = ("Enable clickers → Set timing → Press F9 to start/stop → Clicks at mouse position")
        
        instruction_label = tk.Label(instructions_frame, text=instructions, 
                                    justify="center", 
                                    fg=COLORS['text_secondary'], 
                                    bg=COLORS['bg_section'],
                                    font=("Segoe UI", 8))
        instruction_label.pack(pady=6)
        
        # Clickers container
        clickers_frame = tk.Frame(main_frame, bg=COLORS['bg_main'])
        clickers_frame.pack(fill="both", expand=True, pady=(0, 10))
        
        # Create 3 clicker sections
        for i in range(1, 4):
            clicker = ClickerSection(clickers_frame, i, self.on_config_change)
            self.clickers.append(clicker)
        
        # Global controls with compact styling
        control_frame = tk.Frame(main_frame, bg=COLORS['bg_main'])
        control_frame.pack(fill="x", pady=(8, 0))
        
        # Compact buttons
        self.start_all_btn = tk.Button(control_frame, text="Start All", 
                                      command=self.start_all_clickers,
                                      font=("Segoe UI", 10, "bold"),
                                      bg=COLORS['button_bg'],
                                      fg=COLORS['text_primary'],
                                      relief='flat',
                                      bd=0,
                                      padx=20,
                                      pady=6,
                                      cursor='hand2')
        self.start_all_btn.pack(side="left", padx=(0, 10))
        
        self.stop_all_btn = tk.Button(control_frame, text="Stop All", 
                                     command=self.stop_all_clickers,
                                     font=("Segoe UI", 10, "bold"),
                                     bg=COLORS['button_disabled'],
                                     fg=COLORS['text_primary'],
                                     relief='flat',
                                     bd=0,
                                     padx=20,
                                     pady=6,
                                     cursor='hand2')
        self.stop_all_btn.pack(side="left")
        
        # Status and hotkey in one line for compactness
        status_hotkey_frame = tk.Frame(main_frame, bg=COLORS['bg_main'])
        status_hotkey_frame.pack(fill="x", pady=(10, 0))
        
        self.global_status_label = tk.Label(status_hotkey_frame, text="Status: Inactive", 
                                          font=("Segoe UI", 10, "bold"),
                                          fg=COLORS['text_secondary'],
                                          bg=COLORS['bg_main'])
        self.global_status_label.pack(side="left")
        
        hotkey_info = tk.Label(status_hotkey_frame, text="Hotkey: F9", 
                              fg=COLORS['accent_blue'], 
                              bg=COLORS['bg_main'],
                              font=("Segoe UI", 10))
        hotkey_info.pack(side="right")
        
        # Add hover effects to buttons
        self._add_button_effects()
    
    def _add_button_effects(self):
        """Add hover effects to buttons for modern feel"""
        def on_enter_start(event):
            self.start_all_btn.config(bg=COLORS['accent_blue_hover'])
        
        def on_leave_start(event):
            self.start_all_btn.config(bg=COLORS['button_bg'])
        
        def on_enter_stop(event):
            self.stop_all_btn.config(bg=COLORS['accent_blue_hover'])
        
        def on_leave_stop(event):
            self.stop_all_btn.config(bg=COLORS['button_disabled'])
        
        self.start_all_btn.bind("<Enter>", on_enter_start)
        self.start_all_btn.bind("<Leave>", on_leave_start)
        self.stop_all_btn.bind("<Enter>", on_enter_stop)
        self.stop_all_btn.bind("<Leave>", on_leave_stop)
    
    def setup_hotkeys(self):
        """Set up global hotkey listener"""
        try:
            hotkeys = {
                '<f9>': self.toggle_clickers
            }
            self.hotkey_listener = GlobalHotKeys(hotkeys)
            self.hotkey_listener.start()
            print("✅ Global hotkeys enabled")
        except Exception as e:
            print(f"⚠️  Hotkey setup failed: {e}")
            # Show more helpful error message for Linux
            if sys.platform.startswith('linux'):
                error_msg = (f"Could not set up global hotkeys: {e}\n\n"
                           "Linux Solutions:\n"
                           "1. Run with sudo (not recommended)\n"
                           "2. Add user to input group: sudo usermod -a -G input $USER\n"
                           "3. Install xdotool: sudo apt install xdotool\n"
                           "4. Use GUI buttons instead\n\n"
                           "For Wayland: Global hotkeys may not work due to security restrictions.")
            else:
                error_msg = f"Could not set up global hotkeys: {e}\nYou can still use the GUI buttons."
            
            messagebox.showwarning("Hotkey Warning", error_msg)
    
    def on_config_change(self):
        """Handle configuration changes"""
        # This can be extended for real-time config updates
        pass
    
    def toggle_clickers(self):
        """Toggle all enabled clickers on/off"""
        if self.global_active:
            self.stop_all_clickers()
        else:
            self.start_all_clickers()
    
    def start_all_clickers(self):
        """Start all enabled clickers"""
        enabled_clickers = [c for c in self.clickers if c.enabled.get()]
        
        if not enabled_clickers:
            messagebox.showinfo("Info", "No clickers are enabled!\nPlease enable at least one clicker to start.")
            return
        
        self.global_active = True
        self.global_status_label.config(text="Status: ACTIVE", 
                                       fg=COLORS['accent_blue_light'])
        
        for clicker in enabled_clickers:
            if clicker.section_id not in self.clicker_threads:
                thread = threading.Thread(target=self.clicker_worker, 
                                        args=(clicker,), daemon=True)
                self.clicker_threads[clicker.section_id] = thread
                thread.start()
                clicker.update_status(True)
    
    def stop_all_clickers(self):
        """Stop all clickers"""
        self.global_active = False
        self.global_status_label.config(text="Status: Inactive", 
                                       fg=COLORS['text_secondary'])
        
        # Clear active clickers set
        self.active_clickers.clear()
        
        # Update status for all clickers
        for clicker in self.clickers:
            clicker.update_status(False)
        
        # Threads will stop naturally when they check global_active
    
    def clicker_worker(self, clicker):
        """Worker thread for individual clicker"""
        self.active_clickers.add(clicker.section_id)
        
        while self.global_active and clicker.enabled.get():
            try:
                # Get current mouse position
                current_pos = self.mouse_controller.position
                print(f"🖱️  Clicking at position: {current_pos}")
                
                # Perform click with error handling for Linux
                try:
                    self.mouse_controller.click(mouse.Button.left, 1)
                except Exception as click_error:
                    print(f"⚠️  Click failed: {click_error}")
                    # Try alternative method for Linux
                    if sys.platform.startswith('linux'):
                        try:
                            # Alternative: Use xdotool if available
                            import subprocess
                            
                            # Check for bundled xdotool first (AppImage)
                            xdotool_cmd = 'xdotool'
                            if 'APPDIR' in os.environ:
                                bundled_xdotool = os.path.join(os.environ['APPDIR'], 'usr', 'bin', 'xdotool')
                                if os.path.exists(bundled_xdotool):
                                    xdotool_cmd = bundled_xdotool
                                    print("🎯 Using bundled xdotool from AppImage")
                            
                            subprocess.run([xdotool_cmd, 'click', '1'], 
                                         check=True, capture_output=True)
                            print("✅ Used xdotool as fallback")
                        except (subprocess.CalledProcessError, FileNotFoundError):
                            print("❌ xdotool not available")
                            # Show error in UI
                            self.root.after(0, lambda: messagebox.showerror(
                                "Click Error", 
                                "Cannot click outside app window.\n\n"
                                "Linux Solutions:\n"
                                "1. Install xdotool: sudo apt install xdotool\n"
                                "2. Add user to input group: sudo usermod -a -G input $USER\n"
                                "3. Run with sudo (not recommended)\n"
                                "4. Switch from Wayland to X11 if using Wayland"))
                            break
                
                # Update click count
                clicker.click_count += 1
                
                # Update UI in main thread
                self.root.after(0, lambda c=clicker: c.update_status(True, c.click_count))
                
                # Wait for the specified interval
                interval_ms = clicker.get_total_milliseconds()
                time.sleep(interval_ms / 1000.0)
                
            except Exception as e:
                print(f"❌ Error in clicker {clicker.section_id}: {e}")
                # Show error in UI
                self.root.after(0, lambda: messagebox.showerror(
                    "Clicker Error", 
                    f"Clicker {clicker.section_id} encountered an error:\n{e}\n\n"
                    "This may be due to Linux security restrictions."))
                break
        
        # Clean up when stopping
        if clicker.section_id in self.active_clickers:
            self.active_clickers.remove(clicker.section_id)
        
        if clicker.section_id in self.clicker_threads:
            del self.clicker_threads[clicker.section_id]
        
        # Update UI
        self.root.after(0, lambda c=clicker: c.update_status(False))
    
    def on_closing(self):
        """Handle application closing"""
        self.stop_all_clickers()
        
        if self.hotkey_listener:
            self.hotkey_listener.stop()
        
        # Wait a moment for threads to clean up
        time.sleep(0.1)
        
        self.root.destroy()
    
    def run(self):
        """Start the application"""
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            self.on_closing()


def main():
    """Main entry point"""
    try:
        app = AutoClicker()
        app.run()
    except Exception as e:
        print(f"Error starting application: {e}")
        if hasattr(e, '__class__'):
            print(f"Error type: {e.__class__.__name__}")
        sys.exit(1)


if __name__ == "__main__":
    main()
