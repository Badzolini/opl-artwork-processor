# OPL Artwork Processor


## Table of Contents

- [Introduction](#introduction)
- [Installation](#installation)
- [Running the Application](#running-the-application)
  - [Using the GUI](#using-the-gui)
  - [Using the CLI](#using-the-cli)
- [Building the Executable](#building-the-executable)
- [Notes](#notes)
- [Credits](#credits)


## Installation

1. Install [Python 3 and pip](https://python.org).
    ```sh
    sudo apt install -y python3-full python3-pip
    ```

2. Clone the repository:
    ```sh
    git clone https://github.com/EEkebin/opl-artwork-processor.git
    cd opl-artwork-processor
    ```

3. Create and activate a virtual environment:
    - **Windows (Command Prompt / PowerShell):**
      ```sh
      python -m venv venv
      venv\Scripts\activate
      ```
    - **Mac/Linux:**
      ```sh
      python3 -m venv venv
      source venv/bin/activate
      ```

4. Install required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

---


## Running the Application

### **Using the GUI**
1. Run the script:
    ```sh
    python opl-artwork-processor.py
    ```
2. Select the input directory containing the OPL artwork files.
3. Select the output directory where the processed files will be saved.
4. Enter the suffix for the output files.
5. Enter the desired resolution in the format `width x height` (e.g., `512x736`).
6. Click the **"Start"** button to begin processing.

---

### **Using the CLI**
1. Run the script with the required arguments:
    ```sh
    python opl-artwork-processor.py <input_folder> <output_folder> <suffix> <width>x<height>
    ```

2. Example:
    ```sh
    python opl-artwork-processor.py ./artwork ./output 1 512x736
    ```

3. **Abort Process:**  
   - Press **Ctrl+C** to stop processing immediately.

---

## Building the Executable

1. Ensure your virtual environment is activated:
    ```sh
    # Windows
    venv\Scripts\activate

    # Mac/Linux
    source venv/bin/activate
    ```

2. Install **PyInstaller** (if not already installed):
    ```sh
    pip install pyinstaller
    ```

3. Build the standalone executable:
    ```sh
    pyinstaller --onefile --windowed --hidden-import=PIL opl-artwork-processor.py
    ```

4. The compiled executable will be found in the **`dist/`** folder:
    ```sh
    dist/opl-artwork-processor.exe  # Windows
    dist/opl-artwork-processor      # Mac/Linux
    ```

5. **Run the executable:**
    - **GUI Mode:**  
      ```sh
      ./dist/opl-artwork-processor
      ```
    - **CLI Mode:**  
      ```sh
      ./dist/opl-artwork-processor ./artwork ./output "_COV" 512x736
      ```

---

## Notes
- Running the executable does **not** require Python to be installed.
- The **GUI mode** will launch by default if no arguments are provided.
- **CLI mode** allows automation and scripting by passing the required parameters.
- The **Abort button** in the GUI stops processing safely, and **Ctrl+C** works in CLI mode to immediately terminate the process.


## Credits

[EEkebin](https://github.com/EEkebin)

[Badza](https://github.com/Badzolini) - For the idea and help.
