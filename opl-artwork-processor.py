#!/usr/bin/env python3

import sys
import os
import re
import PIL.Image
import signal
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed

# Global flag to handle shutdown
graceful_shutdown = False

# Set up logging
LOG_FILE = "LOG.TXT"
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


def log_message(message):
    print(message)
    logging.info(message)


def signal_handler(sig, frame):
    global graceful_shutdown
    log_message("\nShutdown signal received. Exiting gracefully...")
    graceful_shutdown = True


# Register signal handler for Ctrl+C
signal.signal(signal.SIGINT, signal_handler)


def rename_file(filename, suffix):
    """Renames files based on the expected pattern or appends the suffix if the pattern is not matched."""
    name, ext = os.path.splitext(
        filename)  # Extract filename without extension

    # Match expected pattern: PREFIX-NUMBERS (e.g., ALCH-00001, GN-05015, SLES-51046-P)
    match = re.match(r"([A-Za-z]+(?:-[A-Za-z0-9]+)*)-(\d{3})(\d{2})(.*)", name)

    if match:
        region, num3, num2, extras = match.groups()
        return f"{region}_{num3}.{num2}{extras}{suffix}.png"

    # If it doesn't match, just append the suffix
    return f"{name}{suffix}.png"


def convert_image(filename, suffix, size, input_folder, output_folder):
    """Converts and resizes a single image from JPG, JPEG, or PNG to PNG format with renamed output."""
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
                # Convert to 8-bit PNG (only if necessary)
                img = img.convert("P", palette=PIL.Image.ADAPTIVE, colors=256)
                img.save(output_path, "PNG")
            log_message(
                f"Processed {filename} -> {new_filename} (Size: {size})")
        except Exception as e:
            log_message(f"Failed to process {filename}: {e}")


def parse_size(size_str):
    """Parses the size argument into a tuple (width, height) or returns None if not valid."""
    try:
        width, height = map(int, size_str.lower().split('x'))
        return (width, height)
    except Exception:
        return None


def main():
    if len(sys.argv) != 5:
        log_message(
            "Usage: python main.py <path/to/artfolder/> <path/to/outputfolder/> <suffix> <width>x<height>")
        sys.exit(1)

    input_folder = sys.argv[1]
    output_folder = sys.argv[2]
    suffix = sys.argv[3]
    size = parse_size(sys.argv[4])

    log_message(f"Input folder: {input_folder}")
    log_message(f"Output folder: {output_folder}")
    log_message(f"Resize to: {size if size else 'Original Size'}")

    if not os.path.exists(input_folder) or not os.path.isdir(input_folder):
        log_message(
            f"Input folder does not exist or is not a directory: {input_folder}")
        sys.exit(1)

    if not os.path.exists(output_folder) or not os.path.isdir(output_folder):
        os.makedirs(output_folder)
        log_message(f"Created output folder: {output_folder}")

    images_to_process = [f for f in os.listdir(
        input_folder) if f.lower().endswith((".jpg", ".jpeg", ".png"))]
    max_threads = min(8, len(images_to_process))

    with ThreadPoolExecutor(max_threads) as executor:
        future_to_filename = {executor.submit(
            convert_image, f, suffix, size, input_folder, output_folder): f for f in images_to_process}
        try:
            for future in as_completed(future_to_filename):
                if graceful_shutdown:
                    break
                future.result()
        except KeyboardInterrupt:
            log_message("\nProcess interrupted by user. Shutting down...")
        finally:
            executor.shutdown(wait=False)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        log_message("\nProcess interrupted. Exiting.")
    sys.exit(0)
