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
        
        # Coordinate variables
        self.coordinates = None  # (x, y) tuple
        self.coordinates_text = tk.StringVar(value="No coordinates set")
        
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
        
        # Coordinate selection frame
        coord_frame = tk.Frame(self.frame, bg=COLORS['bg_section'])
        coord_frame.pack(fill="x", pady=(8, 8))
        
        coord_label = tk.Label(coord_frame, text="Coordinates:", 
                              font=("Segoe UI", 8),
                              fg=COLORS['text_secondary'], 
                              bg=COLORS['bg_section'])
        coord_label.pack(side="left")
        
        self.coord_display = tk.Label(coord_frame, textvariable=self.coordinates_text,
                                     font=("Segoe UI", 8),
                                     fg=COLORS['text_primary'], 
                                     bg=COLORS['bg_section'])
        self.coord_display.pack(side="left", padx=(8, 0))
        
        self.choose_coord_btn = tk.Button(coord_frame, text="Choose Coordinates",
                                         command=self.choose_coordinates,
                                         font=("Segoe UI", 8),
                                         bg=COLORS['accent_blue'],
                                         fg=COLORS['text_primary'],
                                         relief='flat',
                                         bd=0,
                                         padx=12,
                                         pady=4,
                                         cursor='hand2')
        self.choose_coord_btn.pack(side="right", padx=(0, 5))
        
        # Test coordinates button
        self.test_coord_btn = tk.Button(coord_frame, text="Test",
                                       command=self.test_coordinates,
                                       font=("Segoe UI", 8),
                                       bg=COLORS['accent_blue_light'],
                                       fg=COLORS['text_primary'],
                                       relief='flat',
                                       bd=0,
                                       padx=8,
                                       pady=4,
                                       cursor='hand2')
        self.test_coord_btn.pack(side="right", padx=(0, 5))
        
        # Reset button for this clicker
        self.reset_btn = tk.Button(coord_frame, text="Reset",
                                  command=self.reset_clicker,
                                  font=("Segoe UI", 8),
                                  bg=COLORS['button_disabled'],
                                  fg=COLORS['text_primary'],
                                  relief='flat',
                                  bd=0,
                                  padx=8,
                                  pady=4,
                                  cursor='hand2')
        self.reset_btn.pack(side="right")
        
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
            coord_label, self.coord_display, self.choose_coord_btn, self.test_coord_btn, self.reset_btn,
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
        
        # Update coordinate buttons
        if self.enabled.get():
            self.choose_coord_btn.config(state='normal', bg=COLORS['accent_blue'])
            # Test button enabled only if coordinates are set
            if self.coordinates is not None:
                self.test_coord_btn.config(state='normal', bg=COLORS['accent_blue_light'])
                self.reset_btn.config(state='normal', bg=COLORS['button_disabled'])
            else:
                self.test_coord_btn.config(state='disabled', bg=COLORS['button_disabled'])
                self.reset_btn.config(state='disabled', bg=COLORS['button_disabled'])
        else:
            self.choose_coord_btn.config(state='disabled', bg=COLORS['button_disabled'])
            self.test_coord_btn.config(state='disabled', bg=COLORS['button_disabled'])
            self.reset_btn.config(state='disabled', bg=COLORS['button_disabled'])
        
        # Update labels
        self.status_label.config(bg=bg_color, fg=text_secondary)
        self.count_label.config(bg=bg_color, fg=text_secondary)
        self.coord_display.config(bg=bg_color, fg=text_color)
    
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
    
    def choose_coordinates(self):
        """Start coordinate selection process"""
        if hasattr(self, 'parent_app') and self.parent_app:
            self.parent_app.start_coordinate_selection(self)
        else:
            # Fallback if parent_app is not set
            messagebox.showinfo("Coordinate Selection", 
                              "Click anywhere on the screen to set coordinates.\n"
                              "The coordinates will be captured automatically.")
    
    def set_coordinates(self, x, y):
        """Set the coordinates for this clicker"""
        self.coordinates = (x, y)
        self.coordinates_text.set(f"({x}, {y})")
        print(f"📍 Clicker {self.section_id} coordinates set to: ({x}, {y})")
        # Update visual state to enable test button
        self._update_visual_state()
    
    def test_coordinates(self):
        """Test the current coordinates by performing a single click"""
        if self.coordinates is None:
            messagebox.showwarning("No Coordinates", "Please set coordinates first by clicking 'Choose Coordinates'.")
            return
        
        if hasattr(self, 'parent_app') and self.parent_app:
            self.parent_app.test_click_at_coordinates(self.coordinates, self.section_id)
        else:
            messagebox.showinfo("Test Click", f"Would click at coordinates: {self.coordinates}")
    
    def reset_clicker(self):
        """Reset this clicker to default values"""
        # Reset time values
        self.minutes.set("0")
        self.seconds.set("1")
        self.milliseconds.set("0")
        
        # Reset coordinates
        self.coordinates = None
        self.coordinates_text.set("No coordinates set")
        
        # Reset click count
        self.click_count = 0
        
        # Update status
        self.update_status(False, 0)
        
        # Update visual state
        self._update_visual_state()
        
        print(f"🔄 Clicker {self.section_id} reset to defaults")


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
        
        # Recording variables
        self.recorded_clicks = []
        self.recording = False
        self.recording_start_time = None
        self.recording_listener = None
        self.replaying = False
        self.replay_count = 0
        self.max_replays = 1
        
        # Global hotkey setup
        self.hotkey_listener = None
        self.setup_hotkeys()
        
        self.create_widgets()
        
    def setup_window(self):
        """Configure the main window"""
        self.root.title("Advanced Autoclicker")
        self.root.geometry("600x700")
        self.root.resizable(False, False)
        self.root.configure(bg=COLORS['bg_main'])
        
        # Handle window closing
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    def create_widgets(self):
        """Create all GUI widgets with tab interface"""
        # Main container
        main_frame = tk.Frame(self.root, bg=COLORS['bg_main'], padx=15, pady=15)
        main_frame.pack(fill="both", expand=True)
        
        # Header
        header_frame = tk.Frame(main_frame, bg=COLORS['bg_main'])
        header_frame.pack(fill="x", pady=(0, 15))
        
        title_label = tk.Label(header_frame, text="Advanced Autoclicker", 
                              font=("Segoe UI", 16, "bold"), 
                              fg=COLORS['text_primary'], 
                              bg=COLORS['bg_main'])
        title_label.pack()
        
        # Create notebook for tabs
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TNotebook', background=COLORS['bg_main'], borderwidth=0)
        style.configure('TNotebook.Tab', background=COLORS['bg_section'], 
                       foreground=COLORS['text_primary'], padding=[12, 8])
        style.map('TNotebook.Tab', background=[('selected', COLORS['accent_blue'])])
        
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill="both", expand=True, pady=(0, 10))
        
        # Create tabs
        self.create_multi_clicker_tab()
        self.create_recorder_tab()
        
        # Global status at bottom
        status_frame = tk.Frame(main_frame, bg=COLORS['bg_main'])
        status_frame.pack(fill="x")
        
        self.global_status_label = tk.Label(status_frame, text="Status: Ready", 
                                          font=("Segoe UI", 10, "bold"),
                                          fg=COLORS['text_secondary'],
                                          bg=COLORS['bg_main'])
        self.global_status_label.pack(side="left")
        
        hotkey_info = tk.Label(status_frame, text="Hotkeys: F9 (Multi-Clicker), F10 (Record/Stop)", 
                              fg=COLORS['accent_blue'], 
                              bg=COLORS['bg_main'],
                              font=("Segoe UI", 9))
        hotkey_info.pack(side="right")
    
    def create_multi_clicker_tab(self):
        """Create the multi-clicker tab"""
        # Create tab frame
        multi_frame = tk.Frame(self.notebook, bg=COLORS['bg_main'])
        self.notebook.add(multi_frame, text="Multi-Clicker")
        
        # Instructions
        instructions_frame = tk.Frame(multi_frame, bg=COLORS['bg_section'], relief='flat', bd=1)
        instructions_frame.pack(fill="x", pady=(0, 12), padx=3)
        
        instructions = ("Enable clickers → Set timing → Choose coordinates → Press F9 to start/stop")
        
        instruction_label = tk.Label(instructions_frame, text=instructions, 
                                    justify="center", 
                                    fg=COLORS['text_secondary'], 
                                    bg=COLORS['bg_section'],
                                    font=("Segoe UI", 8))
        instruction_label.pack(pady=6)
        
        # Clickers container
        clickers_frame = tk.Frame(multi_frame, bg=COLORS['bg_main'])
        clickers_frame.pack(fill="both", expand=True, pady=(0, 10))
        
        # Create 3 clicker sections
        for i in range(1, 4):
            clicker = ClickerSection(clickers_frame, i, self.on_config_change)
            clicker.parent_app = self
            self.clickers.append(clicker)
        
        # Controls
        control_frame = tk.Frame(multi_frame, bg=COLORS['bg_main'])
        control_frame.pack(fill="x", pady=(8, 0))
        
        self.start_all_btn = tk.Button(control_frame, text="Start All", 
                                      command=self.start_all_clickers,
                                      font=("Segoe UI", 10, "bold"),
                                      bg=COLORS['button_bg'],
                                      fg=COLORS['text_primary'],
                                      relief='flat', bd=0, padx=20, pady=6, cursor='hand2')
        self.start_all_btn.pack(side="left", padx=(0, 10))
        
        self.stop_all_btn = tk.Button(control_frame, text="Stop All", 
                                     command=self.stop_all_clickers,
                                     font=("Segoe UI", 10, "bold"),
                                     bg=COLORS['button_disabled'],
                                     fg=COLORS['text_primary'],
                                     relief='flat', bd=0, padx=20, pady=6, cursor='hand2')
        self.stop_all_btn.pack(side="left", padx=(0, 15))
        
        self.reset_all_btn = tk.Button(control_frame, text="Reset All", 
                                      command=self.reset_all_clickers,
                                      font=("Segoe UI", 10, "bold"),
                                      bg=COLORS['button_disabled'],
                                      fg=COLORS['text_primary'],
                                      relief='flat', bd=0, padx=20, pady=6, cursor='hand2')
        self.reset_all_btn.pack(side="left")
    
    def create_recorder_tab(self):
        """Create the click recorder tab"""
        # Create tab frame
        recorder_frame = tk.Frame(self.notebook, bg=COLORS['bg_main'])
        self.notebook.add(recorder_frame, text="Click Recorder")
        
        # Instructions
        instructions_frame = tk.Frame(recorder_frame, bg=COLORS['bg_section'], relief='flat', bd=1)
        instructions_frame.pack(fill="x", pady=(0, 15), padx=3)
        
        instructions = ("Record clicks → Set replay count → Press F10 to record/stop → Replay sequence")
        
        instruction_label = tk.Label(instructions_frame, text=instructions, 
                                    justify="center", 
                                    fg=COLORS['text_secondary'], 
                                    bg=COLORS['bg_section'],
                                    font=("Segoe UI", 8))
        instruction_label.pack(pady=6)
        
        # Recording controls
        record_frame = tk.Frame(recorder_frame, bg=COLORS['bg_section'], relief='flat', bd=1)
        record_frame.pack(fill="x", pady=(0, 15), padx=3, ipady=15)
        
        record_title = tk.Label(record_frame, text="Recording Controls", 
                               font=("Segoe UI", 12, "bold"),
                               fg=COLORS['text_primary'], 
                               bg=COLORS['bg_section'])
        record_title.pack(pady=(0, 10))
        
        record_btn_frame = tk.Frame(record_frame, bg=COLORS['bg_section'])
        record_btn_frame.pack()
        
        self.record_btn = tk.Button(record_btn_frame, text="Start Recording", 
                                   command=self.toggle_recording,
                                   font=("Segoe UI", 11, "bold"),
                                   bg=COLORS['accent_blue'],
                                   fg=COLORS['text_primary'],
                                   relief='flat', bd=0, padx=25, pady=8, cursor='hand2')
        self.record_btn.pack(side="left", padx=(0, 15))
        
        self.clear_record_btn = tk.Button(record_btn_frame, text="Clear Recording", 
                                         command=self.clear_recording,
                                         font=("Segoe UI", 11, "bold"),
                                         bg=COLORS['button_disabled'],
                                         fg=COLORS['text_primary'],
                                         relief='flat', bd=0, padx=25, pady=8, cursor='hand2')
        self.clear_record_btn.pack(side="left")
        
        # Recording status
        self.record_status = tk.Label(record_frame, text="Status: Ready to record", 
                                     font=("Segoe UI", 10),
                                     fg=COLORS['text_secondary'], 
                                     bg=COLORS['bg_section'])
        self.record_status.pack(pady=(10, 0))
        
        # Replay controls
        replay_frame = tk.Frame(recorder_frame, bg=COLORS['bg_section'], relief='flat', bd=1)
        replay_frame.pack(fill="x", pady=(0, 15), padx=3, ipady=15)
        
        replay_title = tk.Label(replay_frame, text="Replay Controls", 
                               font=("Segoe UI", 12, "bold"),
                               fg=COLORS['text_primary'], 
                               bg=COLORS['bg_section'])
        replay_title.pack(pady=(0, 10))
        
        # Replay count setting
        count_frame = tk.Frame(replay_frame, bg=COLORS['bg_section'])
        count_frame.pack(pady=(0, 10))
        
        count_label = tk.Label(count_frame, text="Replay count:", 
                              font=("Segoe UI", 10),
                              fg=COLORS['text_secondary'], 
                              bg=COLORS['bg_section'])
        count_label.pack(side="left", padx=(0, 10))
        
        self.replay_count_var = tk.StringVar(value="1")
        self.replay_count_entry = tk.Entry(count_frame, textvariable=self.replay_count_var, width=8,
                                          font=("Segoe UI", 10), 
                                          relief='flat', bd=0,
                                          bg=COLORS['entry_bg'],
                                          fg=COLORS['text_primary'],
                                          insertbackground=COLORS['text_primary'],
                                          highlightthickness=1,
                                          highlightcolor=COLORS['accent_blue'],
                                          justify='center')
        self.replay_count_entry.pack(side="left")
        
        # Replay buttons
        replay_btn_frame = tk.Frame(replay_frame, bg=COLORS['bg_section'])
        replay_btn_frame.pack(pady=(10, 0))
        
        self.replay_btn = tk.Button(replay_btn_frame, text="Start Replay", 
                                   command=self.start_replay,
                                   font=("Segoe UI", 11, "bold"),
                                   bg=COLORS['button_disabled'],
                                   fg=COLORS['text_primary'],
                                   relief='flat', bd=0, padx=25, pady=8, cursor='hand2')
        self.replay_btn.pack(side="left", padx=(0, 15))
        
        self.stop_replay_btn = tk.Button(replay_btn_frame, text="Stop Replay", 
                                        command=self.stop_replay,
                                        font=("Segoe UI", 11, "bold"),
                                        bg=COLORS['button_disabled'],
                                        fg=COLORS['text_primary'],
                                        relief='flat', bd=0, padx=25, pady=8, cursor='hand2')
        self.stop_replay_btn.pack(side="left")
        
        # Replay status
        self.replay_status = tk.Label(replay_frame, text="Status: No recording to replay", 
                                     font=("Segoe UI", 10),
                                     fg=COLORS['text_secondary'], 
                                     bg=COLORS['bg_section'])
        self.replay_status.pack(pady=(10, 0))
        
        # Recording info display
        info_frame = tk.Frame(recorder_frame, bg=COLORS['bg_section'], relief='flat', bd=1)
        info_frame.pack(fill="both", expand=True, padx=3, ipady=10)
        
        info_title = tk.Label(info_frame, text="Recording Information", 
                             font=("Segoe UI", 12, "bold"),
                             fg=COLORS['text_primary'], 
                             bg=COLORS['bg_section'])
        info_title.pack(pady=(0, 10))
        
        self.recording_info = tk.Text(info_frame, height=8, width=50,
                                     font=("Segoe UI", 9),
                                     bg=COLORS['entry_bg'],
                                     fg=COLORS['text_primary'],
                                     relief='flat', bd=0,
                                     wrap=tk.WORD,
                                     state='disabled')
        self.recording_info.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        # Initial info text
        self.recording_info.config(state='normal')
        self.recording_info.insert('1.0', "No recording yet. Click 'Start Recording' or press F10 to begin recording clicks.")
        self.recording_info.config(state='disabled')
    
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
        
        def on_enter_reset(event):
            self.reset_all_btn.config(bg=COLORS['accent_blue_hover'])
        
        def on_leave_reset(event):
            self.reset_all_btn.config(bg=COLORS['button_disabled'])
        
        self.start_all_btn.bind("<Enter>", on_enter_start)
        self.start_all_btn.bind("<Leave>", on_leave_start)
        self.stop_all_btn.bind("<Enter>", on_enter_stop)
        self.stop_all_btn.bind("<Leave>", on_leave_stop)
        self.reset_all_btn.bind("<Enter>", on_enter_reset)
        self.reset_all_btn.bind("<Leave>", on_leave_reset)
    
    def setup_hotkeys(self):
        """Set up global hotkey listener"""
        try:
            hotkeys = {
                '<f9>': self.toggle_clickers,
                '<f10>': self.toggle_recording
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
        
        # Check if all enabled clickers have coordinates set
        clickers_without_coords = [c for c in enabled_clickers if c.coordinates is None]
        if clickers_without_coords:
            clicker_numbers = [str(c.section_id) for c in clickers_without_coords]
            messagebox.showwarning("Missing Coordinates", 
                                 f"Clicker(s) {', '.join(clicker_numbers)} have no coordinates set!\n"
                                 f"Please click 'Choose Coordinates' to set click positions before starting.")
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
    
    def reset_all_clickers(self):
        """Reset all clickers to default values"""
        # Stop all clickers first
        self.stop_all_clickers()
        
        # Reset each clicker
        for clicker in self.clickers:
            clicker.reset_clicker()
        
        print("🔄 All clickers reset to defaults")
        messagebox.showinfo("Reset Complete", "All clickers have been reset to default values.")
    
    def clicker_worker(self, clicker):
        """Worker thread for individual clicker"""
        self.active_clickers.add(clicker.section_id)
        
        while self.global_active and clicker.enabled.get():
            try:
                # Check if coordinates are set
                if clicker.coordinates is None:
                    print(f"⚠️  Clicker {clicker.section_id}: No coordinates set, skipping...")
                    # Update UI to show warning
                    self.root.after(0, lambda c=clicker: c.update_status(False))
                    break
                
                # Use stored coordinates
                target_x, target_y = clicker.coordinates
                print(f"🖱️  Clicking at coordinates: ({target_x}, {target_y})")
                
                # Move mouse to target position and click with improved multi-monitor handling
                try:
                    # First, try to set position and verify it worked
                    self.mouse_controller.position = (target_x, target_y)
                    time.sleep(0.02)  # Slightly longer delay for multi-monitor setups
                    
                    # Verify the position was set correctly
                    actual_pos = self.mouse_controller.position
                    print(f"🎯 Target: ({target_x}, {target_y}), Actual: {actual_pos}")
                    
                    # If position is significantly off, try alternative approach
                    pos_diff = abs(actual_pos[0] - target_x) + abs(actual_pos[1] - target_y)
                    if pos_diff > 5:  # If more than 5 pixels off
                        print(f"⚠️  Position offset detected: {pos_diff} pixels")
                        # Try setting position again
                        self.mouse_controller.position = (target_x, target_y)
                        time.sleep(0.01)
                    
                    # Perform the click
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
                            
                            subprocess.run([xdotool_cmd, 'mousemove', str(target_x), str(target_y), 'click', '1'], 
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
    
    def start_coordinate_selection(self, clicker_section):
        """Start coordinate selection for a specific clicker"""
        self.coordinate_selection_clicker = clicker_section
        
        # Minimize the main window
        self.root.iconify()
        
        # Show instruction dialog
        instruction_window = tk.Toplevel()
        instruction_window.title("Select Coordinates")
        instruction_window.geometry("400x200")
        instruction_window.configure(bg=COLORS['bg_main'])
        instruction_window.resizable(False, False)
        instruction_window.attributes('-topmost', True)
        
        # Center the instruction window
        instruction_window.update_idletasks()
        x = (instruction_window.winfo_screenwidth() // 2) - (400 // 2)
        y = (instruction_window.winfo_screenheight() // 2) - (200 // 2)
        instruction_window.geometry(f"400x200+{x}+{y}")
        
        # Create instruction content
        main_frame = tk.Frame(instruction_window, bg=COLORS['bg_main'], padx=20, pady=20)
        main_frame.pack(fill="both", expand=True)
        
        title_label = tk.Label(main_frame, 
                              text=f"Setting Coordinates for Clicker {clicker_section.section_id}",
                              font=("Segoe UI", 12, "bold"),
                              fg=COLORS['text_primary'],
                              bg=COLORS['bg_main'])
        title_label.pack(pady=(0, 15))
        
        instruction_label = tk.Label(main_frame,
                                   text="Click anywhere on your screen to set the coordinates.\n"
                                        "The coordinates will be captured automatically.\n\n"
                                        "Close this window to cancel.",
                                   font=("Segoe UI", 10),
                                   fg=COLORS['text_secondary'],
                                   bg=COLORS['bg_main'],
                                   justify='center')
        instruction_label.pack(pady=(0, 20))
        
        # Cancel button
        cancel_btn = tk.Button(main_frame, text="Cancel",
                              command=lambda: self.cancel_coordinate_selection(instruction_window),
                              font=("Segoe UI", 10),
                              bg=COLORS['button_disabled'],
                              fg=COLORS['text_primary'],
                              relief='flat',
                              bd=0,
                              padx=20,
                              pady=8,
                              cursor='hand2')
        cancel_btn.pack()
        
        # Set up mouse listener for coordinate capture
        self.coordinate_listener = mouse.Listener(on_click=self.on_coordinate_click)
        self.coordinate_listener.start()
        
        # Store reference to instruction window
        self.coordinate_instruction_window = instruction_window
        
        # Handle window close
        instruction_window.protocol("WM_DELETE_WINDOW", 
                                   lambda: self.cancel_coordinate_selection(instruction_window))
    
    def on_coordinate_click(self, x, y, button, pressed):
        """Handle mouse click during coordinate selection"""
        if pressed and button == mouse.Button.left:
            # Stop the listener
            if hasattr(self, 'coordinate_listener'):
                self.coordinate_listener.stop()
            
            # Set coordinates for the clicker with improved handling
            if hasattr(self, 'coordinate_selection_clicker'):
                # Convert to int and add debug info
                coord_x, coord_y = int(x), int(y)
                print(f"🎯 Captured coordinates: ({coord_x}, {coord_y})")
                
                # Validate coordinates are within reasonable bounds
                try:
                    # Test if we can get current mouse position for validation
                    current_pos = self.mouse_controller.position
                    print(f"🖱️  Current mouse position: {current_pos}")
                    
                    # Set the coordinates
                    self.coordinate_selection_clicker.set_coordinates(coord_x, coord_y)
                    
                except Exception as e:
                    print(f"⚠️  Coordinate validation warning: {e}")
                    # Still set coordinates even if validation fails
                    self.coordinate_selection_clicker.set_coordinates(coord_x, coord_y)
            
            # Close instruction window and restore main window
            self.root.after(0, self.complete_coordinate_selection)
            
            return False  # Stop the listener
    
    def complete_coordinate_selection(self):
        """Complete the coordinate selection process"""
        # Close instruction window
        if hasattr(self, 'coordinate_instruction_window'):
            self.coordinate_instruction_window.destroy()
            delattr(self, 'coordinate_instruction_window')
        
        # Restore main window
        self.root.deiconify()
        self.root.lift()
        self.root.focus_force()
        
        # Clean up
        if hasattr(self, 'coordinate_selection_clicker'):
            delattr(self, 'coordinate_selection_clicker')
        if hasattr(self, 'coordinate_listener'):
            delattr(self, 'coordinate_listener')
    
    def cancel_coordinate_selection(self, instruction_window):
        """Cancel coordinate selection"""
        # Stop the listener
        if hasattr(self, 'coordinate_listener'):
            self.coordinate_listener.stop()
            delattr(self, 'coordinate_listener')
        
        # Close instruction window
        instruction_window.destroy()
        
        # Restore main window
        self.root.deiconify()
        self.root.lift()
        self.root.focus_force()
        
        # Clean up
        if hasattr(self, 'coordinate_selection_clicker'):
            delattr(self, 'coordinate_selection_clicker')
    
    def test_click_at_coordinates(self, coordinates, clicker_id):
        """Test click at specific coordinates"""
        target_x, target_y = coordinates
        print(f"🧪 Testing click for Clicker {clicker_id} at ({target_x}, {target_y})")
        
        try:
            # Store current mouse position to restore later
            original_pos = self.mouse_controller.position
            
            # Move to target position
            self.mouse_controller.position = (target_x, target_y)
            time.sleep(0.02)
            
            # Verify position
            actual_pos = self.mouse_controller.position
            pos_diff = abs(actual_pos[0] - target_x) + abs(actual_pos[1] - target_y)
            
            print(f"🎯 Test - Target: ({target_x}, {target_y}), Actual: {actual_pos}, Diff: {pos_diff}")
            
            # Perform test click
            self.mouse_controller.click(mouse.Button.left, 1)
            
            # Show result
            if pos_diff <= 2:
                messagebox.showinfo("Test Result", f"✅ Test click successful!\n"
                                   f"Target: ({target_x}, {target_y})\n"
                                   f"Actual: {actual_pos}\n"
                                   f"Precision: {pos_diff} pixels off")
            else:
                messagebox.showwarning("Test Result", f"⚠️  Test click with offset!\n"
                                      f"Target: ({target_x}, {target_y})\n"
                                      f"Actual: {actual_pos}\n"
                                      f"Offset: {pos_diff} pixels\n\n"
                                      f"This may be due to multi-monitor setup.\n"
                                      f"Try recapturing coordinates if needed.")
            
            # Restore original mouse position
            time.sleep(0.1)
            self.mouse_controller.position = original_pos
            
        except Exception as e:
            print(f"❌ Test click failed: {e}")
            messagebox.showerror("Test Failed", f"Test click failed: {e}\n\n"
                               f"This may be due to system restrictions or multi-monitor issues.")
    
    # Recording Methods
    def toggle_recording(self):
        """Toggle recording on/off"""
        if self.recording:
            self.stop_recording()
        else:
            self.start_recording()
    
    def start_recording(self):
        """Start recording clicks"""
        if self.replaying:
            messagebox.showwarning("Recording Error", "Cannot record while replaying. Stop replay first.")
            return
        
        self.recorded_clicks = []
        self.recording = True
        self.recording_start_time = time.time()
        
        # Update UI
        self.record_btn.config(text="Stop Recording", bg=COLORS['accent_blue_hover'])
        self.record_status.config(text="Status: Recording... (Press F10 to stop)", fg=COLORS['accent_blue_light'])
        self.global_status_label.config(text="Status: Recording clicks", fg=COLORS['accent_blue_light'])
        
        # Start mouse listener
        self.recording_listener = mouse.Listener(on_click=self.on_recording_click)
        self.recording_listener.start()
        
        # Update recording info
        self.update_recording_info("Recording started. Click anywhere to record clicks...")
        
        print("🎬 Recording started")
    
    def stop_recording(self):
        """Stop recording clicks"""
        if not self.recording:
            return
        
        self.recording = False
        
        # Stop listener
        if self.recording_listener:
            self.recording_listener.stop()
            self.recording_listener = None
        
        # Update UI
        self.record_btn.config(text="Start Recording", bg=COLORS['accent_blue'])
        click_count = len(self.recorded_clicks)
        
        if click_count > 0:
            duration = time.time() - self.recording_start_time
            self.record_status.config(text=f"Status: Recorded {click_count} clicks in {duration:.1f}s", 
                                     fg=COLORS['text_secondary'])
            self.replay_btn.config(bg=COLORS['accent_blue'], state='normal')
            self.clear_record_btn.config(bg=COLORS['accent_blue_hover'])
            self.replay_status.config(text=f"Status: Ready to replay {click_count} clicks")
            
            # Update recording info with details
            info_text = f"Recording completed!\n\n"
            info_text += f"Total clicks: {click_count}\n"
            info_text += f"Duration: {duration:.1f} seconds\n\n"
            info_text += "Click sequence:\n"
            
            for i, (x, y, delay) in enumerate(self.recorded_clicks, 1):
                info_text += f"{i}. Click at ({x}, {y}) after {delay:.2f}s\n"
            
            self.update_recording_info(info_text)
        else:
            self.record_status.config(text="Status: No clicks recorded", fg=COLORS['text_disabled'])
            self.update_recording_info("Recording stopped. No clicks were recorded.")
        
        self.global_status_label.config(text="Status: Ready", fg=COLORS['text_secondary'])
        print(f"🎬 Recording stopped. Captured {click_count} clicks")
    
    def on_recording_click(self, x, y, button, pressed):
        """Handle mouse click during recording"""
        if pressed and button == mouse.Button.left and self.recording:
            current_time = time.time()
            delay = current_time - self.recording_start_time
            
            # Store click with coordinates and timing
            self.recorded_clicks.append((int(x), int(y), delay))
            
            click_num = len(self.recorded_clicks)
            print(f"📹 Recorded click {click_num}: ({int(x)}, {int(y)}) at {delay:.2f}s")
            
            # Update status
            self.root.after(0, lambda: self.record_status.config(
                text=f"Status: Recording... {click_num} clicks recorded"))
    
    def clear_recording(self):
        """Clear the current recording"""
        if self.recording:
            self.stop_recording()
        
        self.recorded_clicks = []
        self.record_status.config(text="Status: Ready to record", fg=COLORS['text_secondary'])
        self.replay_btn.config(bg=COLORS['button_disabled'], state='disabled')
        self.clear_record_btn.config(bg=COLORS['button_disabled'])
        self.replay_status.config(text="Status: No recording to replay")
        
        self.update_recording_info("Recording cleared. Click 'Start Recording' or press F10 to begin recording clicks.")
        print("🗑️ Recording cleared")
    
    def start_replay(self):
        """Start replaying recorded clicks"""
        if not self.recorded_clicks:
            messagebox.showwarning("Replay Error", "No recording to replay. Record some clicks first.")
            return
        
        if self.recording:
            messagebox.showwarning("Replay Error", "Cannot replay while recording. Stop recording first.")
            return
        
        try:
            self.max_replays = int(self.replay_count_var.get())
            if self.max_replays <= 0:
                raise ValueError()
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid positive number for replay count.")
            return
        
        self.replaying = True
        self.replay_count = 0
        
        # Update UI
        self.replay_btn.config(text="Replaying...", bg=COLORS['accent_blue_hover'], state='disabled')
        self.stop_replay_btn.config(bg=COLORS['accent_blue'], state='normal')
        self.record_btn.config(state='disabled')
        self.global_status_label.config(text="Status: Replaying clicks", fg=COLORS['accent_blue_light'])
        
        # Start replay in separate thread
        replay_thread = threading.Thread(target=self.replay_worker, daemon=True)
        replay_thread.start()
        
        print(f"▶️ Starting replay of {len(self.recorded_clicks)} clicks, {self.max_replays} times")
    
    def stop_replay(self):
        """Stop replaying"""
        self.replaying = False
        
        # Update UI
        self.replay_btn.config(text="Start Replay", bg=COLORS['accent_blue'], state='normal')
        self.stop_replay_btn.config(bg=COLORS['button_disabled'], state='disabled')
        self.record_btn.config(state='normal')
        self.global_status_label.config(text="Status: Ready", fg=COLORS['text_secondary'])
        
        if self.replay_count > 0:
            self.replay_status.config(text=f"Status: Stopped after {self.replay_count} replays")
        else:
            self.replay_status.config(text=f"Status: Ready to replay {len(self.recorded_clicks)} clicks")
        
        print("⏹️ Replay stopped")
    
    def replay_worker(self):
        """Worker thread for replaying clicks"""
        try:
            for replay_num in range(self.max_replays):
                if not self.replaying:
                    break
                
                self.replay_count = replay_num + 1
                
                # Update status
                self.root.after(0, lambda: self.replay_status.config(
                    text=f"Status: Replaying... {self.replay_count}/{self.max_replays}"))
                
                # Replay each click
                start_time = time.time()
                
                for i, (x, y, original_delay) in enumerate(self.recorded_clicks):
                    if not self.replaying:
                        break
                    
                    # Wait for the original delay
                    elapsed = time.time() - start_time
                    wait_time = original_delay - elapsed
                    
                    if wait_time > 0:
                        time.sleep(wait_time)
                    
                    if not self.replaying:
                        break
                    
                    # Perform click
                    try:
                        self.mouse_controller.position = (x, y)
                        time.sleep(0.01)
                        self.mouse_controller.click(mouse.Button.left, 1)
                        print(f"🔄 Replay {self.replay_count}: Click {i+1} at ({x}, {y})")
                    except Exception as e:
                        print(f"❌ Replay click failed: {e}")
                        # Try Linux xdotool fallback
                        if sys.platform.startswith('linux'):
                            try:
                                import subprocess
                                
                                # Check for bundled xdotool first (AppImage)
                                xdotool_cmd = 'xdotool'
                                if 'APPDIR' in os.environ:
                                    bundled_xdotool = os.path.join(os.environ['APPDIR'], 'usr', 'bin', 'xdotool')
                                    if os.path.exists(bundled_xdotool):
                                        xdotool_cmd = bundled_xdotool
                                        print("🎯 Using bundled xdotool from AppImage for replay")
                                
                                subprocess.run([xdotool_cmd, 'mousemove', str(x), str(y), 'click', '1'], 
                                             check=True, capture_output=True)
                                print(f"✅ Replay {self.replay_count}: Click {i+1} at ({x}, {y}) via xdotool")
                            except (subprocess.CalledProcessError, FileNotFoundError):
                                print(f"❌ xdotool fallback failed for replay click {i+1}")
                        else:
                            # Non-Linux systems - break on click failure
                            break
                
                # Small delay between replays
                if self.replaying and replay_num < self.max_replays - 1:
                    time.sleep(0.5)
            
            # Replay completed
            if self.replaying:
                self.root.after(0, self.replay_completed)
                
        except Exception as e:
            print(f"❌ Replay error: {e}")
            self.root.after(0, self.stop_replay)
    
    def replay_completed(self):
        """Handle replay completion"""
        self.replaying = False
        
        # Update UI
        self.replay_btn.config(text="Start Replay", bg=COLORS['accent_blue'], state='normal')
        self.stop_replay_btn.config(bg=COLORS['button_disabled'], state='disabled')
        self.record_btn.config(state='normal')
        self.global_status_label.config(text="Status: Ready", fg=COLORS['text_secondary'])
        self.replay_status.config(text=f"Status: Completed {self.replay_count} replays")
        
        print(f"✅ Replay completed: {self.replay_count} replays finished")
    
    def update_recording_info(self, text):
        """Update the recording information display"""
        self.recording_info.config(state='normal')
        self.recording_info.delete('1.0', tk.END)
        self.recording_info.insert('1.0', text)
        self.recording_info.config(state='disabled')
    
    def on_closing(self):
        """Handle application closing"""
        self.stop_all_clickers()
        
        # Stop recording if active
        if self.recording:
            self.stop_recording()
        
        # Stop replay if active
        if self.replaying:
            self.stop_replay()
        
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
