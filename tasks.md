# Autoclicker Application Development Tasks

## Project Overview
Create a cross-platform (Windows/Linux) Python autoclicker application with GUI featuring multiple independent clickers with customizable timing and global hotkey activation.

## Requirements Analysis
- **Platform**: Cross-platform (Windows/Linux)
- **Language**: Python
- **GUI**: Tkinter (built-in, cross-platform)
- **Features**:
  - 3 identical, independent clicker paragraphs/sections
  - Each clicker disabled by default
  - Configurable timing: minutes, seconds, milliseconds
  - Global hotkey activation
  - Multiple clickers can run simultaneously with different intervals
  - Clicks at mouse cursor position when hotkey is pressed

## Technical Architecture

### Core Components
1. **GUI Framework**: Tkinter for cross-platform compatibility
2. **Mouse Control**: `pynput` library for mouse clicking and global hotkeys
3. **Threading**: For independent clicker timers
4. **Configuration**: In-memory state management for clicker settings

### Dependencies
- `pynput`: For mouse control and global hotkeys
- `tkinter`: Built-in GUI framework
- `threading`: Built-in for concurrent operations
- `time`: Built-in for timing operations

## Task Breakdown

### Phase 1: Project Setup and Dependencies
- [ ] **Task 1.1**: Create project structure
  - Create main application file (`autoclicker.py`)
  - Create requirements.txt file
  - Create README.md with setup instructions

- [ ] **Task 1.2**: Set up dependencies
  - Install and configure `pynput` library
  - Test cross-platform compatibility

### Phase 2: Core GUI Development
- [ ] **Task 2.1**: Create main window structure
  - Initialize Tkinter main window
  - Set window title, size, and basic properties
  - Make window non-resizable for consistent layout

- [ ] **Task 2.2**: Design clicker section component
  - Create reusable clicker section class
  - Include enable/disable checkbox
  - Add time input fields (minutes, seconds, milliseconds)
  - Add status indicator (active/inactive)

- [ ] **Task 2.3**: Implement 3 clicker sections
  - Instantiate 3 identical clicker sections
  - Arrange them vertically in the main window
  - Label them as "Clicker 1", "Clicker 2", "Clicker 3"

### Phase 3: Timing and Configuration Logic
- [ ] **Task 3.1**: Implement time calculation
  - Create function to convert minutes/seconds/milliseconds to total milliseconds
  - Add input validation for time fields
  - Set reasonable min/max limits for timing values

- [ ] **Task 3.2**: Create clicker state management
  - Track enabled/disabled state for each clicker
  - Store timing configuration for each clicker
  - Implement configuration change handlers

### Phase 4: Mouse Control Implementation
- [ ] **Task 4.1**: Implement mouse clicking functionality
  - Use `pynput` to perform mouse clicks at cursor position
  - Handle potential errors (permissions, etc.)

- [ ] **Task 4.2**: Create independent clicker threads
  - Implement threading for each clicker
  - Ensure each clicker runs on its own schedule
  - Handle thread synchronization and cleanup

### Phase 5: Global Hotkey System
- [ ] **Task 5.1**: Implement global hotkey detection
  - Set up global hotkey listener using `pynput`
  - Choose appropriate hotkey (e.g., F9 or Ctrl+Alt+C)
  - Handle hotkey press events

- [ ] **Task 5.2**: Integrate hotkey with clicker activation
  - When hotkey pressed, activate all enabled clickers
  - Implement start/stop functionality via hotkey
  - Add visual feedback in GUI for active state

### Phase 6: Advanced Features
- [ ] **Task 6.1**: Add global controls
  - "Start All" button
  - "Stop All" button
  - Global enable/disable toggle

- [ ] **Task 6.2**: Implement status display
  - Show current status of each clicker
  - Display next click countdown
  - Add click counter for each clicker

### Phase 7: Cross-Platform Compatibility
- [ ] **Task 7.1**: Test Windows compatibility
  - Test mouse clicking functionality
  - Test global hotkey detection
  - Handle Windows-specific permissions

- [ ] **Task 7.2**: Test Linux compatibility
  - Test X11 mouse control
  - Handle Linux permissions for input devices
  - Test global hotkey in various Linux desktop environments

### Phase 8: Error Handling and Robustness
- [ ] **Task 8.1**: Implement comprehensive error handling
  - Handle permission errors for mouse control
  - Manage thread exceptions
  - Graceful degradation for unsupported features

- [ ] **Task 8.2**: Add input validation
  - Validate time input ranges
  - Prevent invalid configurations
  - User-friendly error messages

### Phase 9: User Experience Improvements
- [ ] **Task 9.1**: Add configuration persistence
  - Save/load clicker configurations
  - Remember window position and settings

- [ ] **Task 9.2**: Improve UI/UX
  - Add tooltips for controls
  - Improve visual feedback
  - Add keyboard shortcuts for common actions

### Phase 10: Testing and Documentation
- [ ] **Task 10.1**: Comprehensive testing
  - Test all timing combinations
  - Test multiple clickers running simultaneously
  - Verify cross-platform functionality

- [ ] **Task 10.2**: Create documentation
  - Update README with usage instructions
  - Add troubleshooting section
  - Include installation guide for both platforms

## Implementation Details

### File Structure
```
Autoclicker/
├── autoclicker.py          # Main application file
├── requirements.txt        # Python dependencies
├── README.md              # Setup and usage instructions
└── tasks.md              # This file
```

### Key Classes and Functions
1. **ClickerSection**: GUI component for individual clicker configuration
2. **AutoClicker**: Main application class managing GUI and logic
3. **ClickerThread**: Threading class for independent clicker execution
4. **HotkeyManager**: Global hotkey handling
5. **MouseController**: Mouse clicking functionality

### Global Hotkey Options
- **Primary**: F9 (commonly unused, easy to reach)
- **Alternative**: Ctrl+Alt+C (modifier combination)
- **Configurable**: Allow user to set custom hotkey

### Timing Logic Example
- Clicker 1: 20 seconds (20000ms intervals)
- Clicker 2: 25 seconds (25000ms intervals)
- Timeline: Click at 20s, 25s, 40s, 50s, 60s, 75s, 80s, 100s...

### Cross-Platform Considerations
- **Windows**: May require running as administrator for global hotkeys
- **Linux**: May require adding user to input group
- **Mouse Control**: Use `pynput.mouse.Button.left` for left clicks
- **Hotkeys**: Test with different desktop environments (GNOME, KDE, etc.)

## Success Criteria
- [x] Application runs on both Windows and Linux
- [x] 3 independent clickers can be configured and enabled separately
- [x] Timing is accurate and configurable (minutes/seconds/milliseconds)
- [x] Global hotkey activates clicking for all enabled clickers
- [x] Multiple clickers can run simultaneously with different intervals
- [x] Clicks occur at current mouse cursor position
- [x] GUI is intuitive and responsive
- [x] No crashes or performance issues during extended use

## Development Order
Execute tasks in numerical order within each phase. Some tasks within a phase can be done in parallel, but phases should generally be completed sequentially to ensure dependencies are met.

## Notes for Implementation
- Start with basic functionality and gradually add features
- Test frequently on both platforms during development
- Keep the GUI simple and functional
- Focus on reliability and accuracy of timing
- Ensure proper cleanup of threads and resources on application exit
