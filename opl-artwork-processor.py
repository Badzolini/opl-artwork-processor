#!/usr/bin/env python3

import sys
import tkinter as tk
from tkinter import filedialog, scrolledtext
import threading
import os
import re
import PIL.Image
import signal
import logging
from concurrent.futures import ThreadPoolExecutor

# Set up logging
LOG_FILE = "LOG.TXT"
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

# Global shutdown flag
graceful_shutdown = False


def signal_handler(sig, frame):
    """Handles Ctrl+C to gracefully shut down the CLI process."""
    global graceful_shutdown
    graceful_shutdown = True
    print("\nCtrl+C detected! Stopping process...")
    sys.exit(0)  # Ensures an immediate exit in CLI mode


# Register Ctrl+C signal handler
signal.signal(signal.SIGINT, signal_handler)


def log_message(gui, message):
    """Log message to file and update GUI log box (if available)."""
    print(message)
    logging.info(message)

    if gui:
        gui.log_text.config(state=tk.NORMAL)
        gui.log_text.insert(tk.END, message + "\n")
        gui.log_text.yview(tk.END)
        gui.log_text.config(state=tk.DISABLED)


def rename_file(filename, suffix):
    """Renames files based on a pattern or appends a suffix."""
    name, ext = os.path.splitext(filename)
    match = re.match(r"([A-Za-z]+(?:-[A-Za-z0-9]+)*)-(\d{3})(\d{2})(.*)", name)
    if match:
        region, num3, num2, extras = match.groups()
        return f"{region}_{num3}.{num2}{extras}{suffix}.png"
    return f"{name}{suffix}.png"


def convert_image(gui, filename, suffix, size, input_folder, output_folder):
    """Converts and resizes a single image."""
    global graceful_shutdown
    if graceful_shutdown:
        return

    if filename.lower().endswith((".jpg", ".jpeg", ".png")):
        input_path = os.path.join(input_folder, filename)
        new_filename = rename_file(filename, suffix)
        output_path = os.path.join(output_folder, new_filename)

        try:
            with PIL.Image.open(input_path) as img:
                if size:
                    img = img.resize(size, PIL.Image.LANCZOS)
                img = img.convert("P", palette=PIL.Image.ADAPTIVE, colors=256)
                img.save(output_path, "PNG")
            log_message(
                gui, f"Processed {filename} -> {new_filename} (Size: {size})")
        except Exception as e:
            log_message(gui, f"Failed to process {filename}: {e}")


def parse_size(size_str):
    """Parses the size argument into a tuple (width, height)."""
    try:
        width, height = map(int, size_str.lower().split('x'))
        return (width, height)
    except Exception:
        return None


def run_processor(gui, input_folder, output_folder, suffix, size_str):
    """Processes images inside the GUI or CLI."""
    global graceful_shutdown
    graceful_shutdown = False  # Reset shutdown flag

    size = parse_size(size_str)
    log_message(gui, f"Input folder: {input_folder}")
    log_message(gui, f"Output folder: {output_folder}")
    log_message(gui, f"Resize to: {size if size else 'Original Size'}")

    if not os.path.exists(input_folder) or not os.path.isdir(input_folder):
        log_message(gui, f"Input folder does not exist: {input_folder}")
        return

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        log_message(gui, f"Created output folder: {output_folder}")

    images_to_process = [f for f in os.listdir(
        input_folder) if f.lower().endswith((".jpg", ".jpeg", ".png"))]
    max_threads = min(8, len(images_to_process))

    with ThreadPoolExecutor(max_threads) as executor:
        futures = []
        for filename in images_to_process:
            if graceful_shutdown:
                log_message(gui, "Processing aborted by user.")
                return
            futures.append(executor.submit(convert_image, gui,
                           filename, suffix, size, input_folder, output_folder))

        for future in futures:
            if graceful_shutdown:
                log_message(gui, "Processing aborted by user.")
                return
            future.result()

    if gui:
        gui.start_button.config(state=tk.NORMAL)
        gui.abort_button.config(state=tk.DISABLED)
    log_message(gui, "Processing complete.")


class OPLArtworkProcessorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("OPL Artwork Processor")

        # Input Folder
        tk.Label(root, text="Input Folder:").grid(row=0, column=0, sticky='w')
        self.input_folder_entry = tk.Entry(root, width=50)
        self.input_folder_entry.grid(row=0, column=1)
        tk.Button(root, text="Browse", command=self.browse_input_folder).grid(
            row=0, column=2)

        # Output Folder
        tk.Label(root, text="Output Folder:").grid(row=1, column=0, sticky='w')
        self.output_folder_entry = tk.Entry(root, width=50)
        self.output_folder_entry.grid(row=1, column=1)
        tk.Button(root, text="Browse", command=self.browse_output_folder).grid(
            row=1, column=2)

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
        self.log_text = scrolledtext.ScrolledText(
            root, width=60, height=10, state=tk.DISABLED)
        self.log_text.grid(row=5, column=1, columnspan=2)

        # Buttons
        self.start_button = tk.Button(
            root, text="Start", command=self.start_process)
        self.start_button.grid(row=6, column=1, pady=5)

        self.abort_button = tk.Button(
            root, text="Abort", command=self.abort_process, state=tk.DISABLED)
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
        global graceful_shutdown
        graceful_shutdown = False

        input_folder = self.input_folder_entry.get()
        output_folder = self.output_folder_entry.get()
        suffix = self.suffix_entry.get()
        size = f"{self.width_entry.get()}x{self.height_entry.get()}"

        self.start_button.config(state=tk.DISABLED)
        self.abort_button.config(state=tk.NORMAL)

        threading.Thread(target=run_processor, args=(
            self, input_folder, output_folder, suffix, size), daemon=True).start()

    def abort_process(self):
        global graceful_shutdown
        graceful_shutdown = True
        self.abort_button.config(state=tk.DISABLED)
        log_message(self, "Abort signal sent. Stopping processing...")


if __name__ == "__main__":
    if len(sys.argv) == 5:
        run_processor(None, sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
    else:
        root = tk.Tk()
        app = OPLArtworkProcessorApp(root)
        root.mainloop()
