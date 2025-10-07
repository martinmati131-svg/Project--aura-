
    
 import platform

# Detect the OS and import the correct libraries
if platform.system() == "Darwin": # macOS
    from AppKit import NSWorkspace
elif platform.system() == "Windows":
    import win32gui
    import win32process
    import psutil
elif platform.system() == "Linux":
    from Xlib import display
    import psutil

# Then, define the correct version of the function
def get_active_app_name():
    os_name = platform.system()
    if os_name == "Darwin":
        # macOS code here...
    elif os_name == "Windows":
        # Windows code here...
    elif os_name == "Linux":
        # Linux code here...
    else:
        return "Unsupported OS"

       
