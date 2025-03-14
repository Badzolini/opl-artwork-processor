# OPL Artwork Processor


## Installation

1. Install [python3 and pip3](https://python.org).

2. Clone the repository:
    ```sh
    git clone https://github.com/EEkebin/opl-artwork-processor.git
    ```

3. Install the required packages:
    ```sh
    pip3 install -r requirements.txt
    ```


## Running using the GUI
1. Run the script:
    Open the executable or run the script:
    ```sh
    python3 opl-artwork-processor.py
    ```
2. Select the input directory containing the OPL artwork files.
3. Select the output directory where the processed files will be saved.
4. Enter the suffix for the output files.
5. Enter the desired resolution in the format `width x height` (e.g., `512x736`).
6. Click the "Start" button to start processing the files.


## Running the script using CLI

1. Run the script:
    ```sh
    python3 opl-artwork-processor.py <path_to_opl_artwork> <path_to_output_directory> <suffix> <width>x<height>
    ```

2. Example:
    ```sh
    python3 opl-artwork-processor.py ./artwork ./output 1 512x736
    ```


## Building the executable

1. Install [pyinstaller](https://pyinstaller.readthedocs.io/en/stable/):
    ```sh
    pip3 install pyinstaller
    ```

2. Build the executable:
    ```sh
    pyinstaller --onefile --windowed --hidden-import=PIL opl-artwork-processor.py
    ```
