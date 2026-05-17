#!/usr/bin/env python3
"""
RCA VH226E IR Interface Rotator Control
By Rob VK8FOES
"""

import tkinter as tk
from tkinter import messagebox
import subprocess
import os

# --- Configuration Constants ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TRANSMIT_EXE = os.path.join(BASE_DIR, "transmit.exe")
REMOTE_NAME = "rca_vh226e_antenna_rotator"
DEFAULT_TRANSMIT_COUNT = "10"
WINLIRC_EXE = "winlirc.exe" # Used for the process check

def is_winlirc_running():
    """
    Checks the Windows task list to see if WinLIRC is currently active.
    Uses native Windows commands to avoid requiring external pip libraries.
    """
    try:
        command = f'tasklist /NH /FI "IMAGENAME eq {WINLIRC_EXE}"'
        output = subprocess.check_output(
            command,
            creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0x08000000),
            text=True
        )
        return WINLIRC_EXE.lower() in output.lower()
    except subprocess.CalledProcessError:
        return False
    except Exception as e:
        print(f"Process check failed: {e}")
        return False

def send_ir_command(ir_code):
    """
    Invokes WinLIRC's transmit.exe directly, bypassing the need for .bat files.
    """
    if not is_winlirc_running():
        messagebox.showerror(
            title="WinLIRC Not Found", 
            message="WinLIRC does not appear to be running in the background.\n\nPlease launch WinLIRC before attempting to rotate the antenna."
        )
        return

    command = [TRANSMIT_EXE, REMOTE_NAME, ir_code, DEFAULT_TRANSMIT_COUNT]

    try:
        subprocess.run(
            command,
            cwd=BASE_DIR, 
            check=True,
            creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0x08000000)
        )
    except FileNotFoundError:
        error_msg = (
            f"Could not find transmit.exe at:\n{TRANSMIT_EXE}\n\n"
            "Please download WinLIRC and ensure 'transmit.exe' is copied into "
            "the same folder as this application."
        )
        messagebox.showerror("Missing File", error_msg)
    except subprocess.CalledProcessError as e:
        messagebox.showwarning("Transmission Failed", f"WinLIRC command failed with error code: {e.returncode}")
    except Exception as e:
        messagebox.showerror("Unexpected Error", f"An error occurred:\n{e}")

def main():
    root = tk.Tk()
    root.title("Rotator Control v2.6")
    root.resizable(True, True)  

    # Assign the title to a variable so we can measure it later
    title_label = tk.Label(root, text='RCA VH226E IR Interface', font=('Segoe UI', 12, 'bold'))
    title_label.pack(pady=(10, 0))
    
    tk.Label(root, text='By Rob VK8FOES', font=('Segoe UI', 10)).pack(pady=(0, 10))

    # --- Button Data Structure ---
    buttons_data = [
        ("0 Degrees (Wait 1 Minute)", "000_deg"),
        ("30 Degrees", "030_deg"),
        ("60 Degrees", "060_deg"),
        ("90 Degrees", "090_deg"),
        ("120 Degrees", "120_deg"),
        ("150 Degrees", "150_deg"),
        ("180 Degrees", "180_deg"),
        ("210 Degrees", "210_deg"),
        ("240 Degrees", "240_deg"),
        ("270 Degrees", "270_deg"),
        ("300 Degrees", "300_deg"),
        ("330 Degrees", "330_deg"),
        ("360 Degrees", "360_deg"),
        ("Counter Clockwise Rotation", "ccw_rot"),
        ("Clockwise Rotation", "cw_rot")
    ]

    max_text_length = max(len(text) for text, _ in buttons_data)
    calculated_button_width = max_text_length + 4

    for text, ir_code in buttons_data:
        btn = tk.Button(
            root,
            text=text,
            command=lambda code=ir_code: send_ir_command(code),
            width=calculated_button_width, 
            cursor="hand2"
        )
        # Reduced horizontal padding from 15 to 5 so the buttons don't artificially widen the window
        btn.pack(pady=1, padx=5)

    version_label = tk.Label(root, text="Version: 1.2", font=('Segoe UI', 10))
    version_label.pack(side='bottom', anchor='e', padx=5, pady=5)

    # --- Dynamic Window Sizing ---
    # update_idletasks() forces Tkinter to render the widgets in memory and calculate 
    # their actual physical dimensions before drawing the window on the screen.
    root.update_idletasks()
    
    # Get the exact physical width of the Title text and add 40 pixels of breathing room (20px each side)
    launch_width = title_label.winfo_reqwidth() + 40
    
    # We also check the required width of the window based on the buttons. 
    # We take whichever is larger so we don't accidentally chop the buttons in half.
    final_width = max(launch_width, root.winfo_reqwidth())
    
    # Get the natural height of all the stacked widgets
    launch_height = root.winfo_reqheight()

    # Apply the perfectly calculated geometry
    root.geometry(f"{final_width}x{launch_height}")

    root.mainloop()

if __name__ == "__main__":
    main()
