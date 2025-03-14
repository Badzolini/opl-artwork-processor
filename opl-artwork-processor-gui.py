#!/usr/bin/env python3

import tkinter as tk
from tkinter import filedialog, scrolledtext
import subprocess
import threading

class OPLArtworkProcessorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("OPL Artwork Processor")
        
        self.process = None  # For tracking the subprocess
        
        # Input Folder
        tk.Label(root, text="Input Folder:").grid(row=0, column=0, sticky='w')
        self.input_folder_entry = tk.Entry(root, width=50)
        self.input_folder_entry.grid(row=0, column=1)
        tk.Button(root, text="Browse", command=self.browse_input_folder).grid(row=0, column=2)
        
        # Output Folder
        tk.Label(root, text="Output Folder:").grid(row=1, column=0, sticky='w')
        self.output_folder_entry = tk.Entry(root, width=50)
        self.output_folder_entry.grid(row=1, column=1)
        tk.Button(root, text="Browse", command=self.browse_output_folder).grid(row=1, column=2)
        
        # Suffix
        tk.Label(root, text="Suffix:").grid(row=2, column=0, sticky='w')
        self.suffix_entry = tk.Entry(root, width=50)
        self.suffix_entry.grid(row=2, column=1)
        
        # Width
        tk.Label(root, text="Width:").grid(row=3, column=0, sticky='w')
        self.width_entry = tk.Entry(root, width=10)
        self.width_entry.grid(row=3, column=1, sticky='w')
        
        # Height
        tk.Label(root, text="Height:").grid(row=4, column=0, sticky='w')
        self.height_entry = tk.Entry(root, width=10)
        self.height_entry.grid(row=4, column=1, sticky='w')
        
        # Log Box
        tk.Label(root, text="Log:").grid(row=5, column=0, sticky='nw')
        self.log_text = scrolledtext.ScrolledText(root, width=60, height=10)
        self.log_text.grid(row=5, column=1, columnspan=2)
        
        # Buttons
        self.start_button = tk.Button(root, text="Start", command=self.start_process)
        self.start_button.grid(row=6, column=1, pady=5)
        
        self.abort_button = tk.Button(root, text="Abort", command=self.abort_process, state=tk.DISABLED)
        self.abort_button.grid(row=6, column=2, pady=5)
    
    def browse_input_folder(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.input_folder_entry.delete(0, tk.END)
            self.input_folder_entry.insert(0, folder_selected)
    
    def browse_output_folder(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.output_folder_entry.delete(0, tk.END)
            self.output_folder_entry.insert(0, folder_selected)
    
    def start_process(self):
        input_folder = self.input_folder_entry.get()
        output_folder = self.output_folder_entry.get()
        suffix = self.suffix_entry.get()
        width = self.width_entry.get()
        height = self.height_entry.get()
        
        if not input_folder or not output_folder or not suffix or not width or not height:
            self.log("Please fill in all fields before starting.")
            return
        
        size_arg = f"{width}x{height}"
        command = ["python", "./opl-artwork-processor.py", input_folder, output_folder, suffix, size_arg]
        
        self.start_button.config(state=tk.DISABLED)
        self.abort_button.config(state=tk.NORMAL)
        
        self.log("Starting process...")
        self.process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        threading.Thread(target=self.monitor_process, daemon=True).start()
    
    def monitor_process(self):
        if self.process:
            try:
                for line in iter(self.process.stdout.readline, ''):
                    if line:
                        self.log(line.strip())
                for line in iter(self.process.stderr.readline, ''):
                    if line:
                        self.log("ERROR: " + line.strip())
                self.process.wait()
            except AttributeError:
                self.log("Process was aborted before completion.")
        
        self.process = None
        self.start_button.config(state=tk.NORMAL)
        self.abort_button.config(state=tk.DISABLED)
        self.log("Process finished.")
    
    def abort_process(self):
        if self.process:
            self.process.terminate()
            self.process = None
            self.log("Process aborted.")
        self.start_button.config(state=tk.NORMAL)
        self.abort_button.config(state=tk.DISABLED)
    
    def log(self, message):
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.yview(tk.END)
        
if __name__ == "__main__":
    root = tk.Tk()
    app = OPLArtworkProcessorApp(root)
    root.mainloop()
