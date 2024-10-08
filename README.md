# Image Labeling App for AI Training

This desktop application, built with Python using the Tkinter package, provides a user-friendly interface for labeling images, and the files with same names as images to prepare datasets for AI model training. The tool simplifies the manual process of assigning labels to images by offering an intuitive, customizable interface.

## Features

- **Image Display:** The app displays images from a selected directory, allowing you to view them one at a time.
- **Labeling Functionality:** Users can define multiple labels, which are represented as buttons in the interface. Clicking a button assigns the corresponding label to the image.
- **Directory Selection:** Easily select the directory containing the images to be labeled from the settings section.
- **File Renaming:** When a label is chosen, the application renames the image file by appending the corresponding label ID to the filename.
- **Customizable Labels:** Users can define their own labels through the settings section, making the tool adaptable for various AI training scenarios.
- **Settings Section:** Modify labels, choose directories, and configure the tool to fit different workflows.

## Installation

1. **Clone the Repository:**
   Clone this repository to your local machine:
   ```bash
   git clone HTTP_REPOSITORY_URL
   cd image-labeling
   ```

2. **Install Dependencies:**
   Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Application:**
   Run the application with the following command:
   ```bash
   python main.py
   ```

## Building the Executable with PyInstaller

To build the app as a standalone executable, follow these steps:

1. **Install PyInstaller:**
   Install PyInstaller via pip:
   ```bash
   pip install pyinstaller
   ```

2. **Build the Executable:**
   In the project directory, run the following command:
   ```bash
   pyinstaller --onefile --windowed --icon=static/img/icon.ico main.py
   ```
   - `--onefile`: Bundles the app into a single executable.
   - `--windowed`: Ensures the app runs without a terminal window.
   - `--icon`: Adds a custom icon for the executable (use `.ico` format).

3. **Locate the Executable:**
   After building, the executable will be in the `dist` folder.

### How to Use

To run the application as a standalone desktop app:

1. **Create a Folder:**
   - Create a folder, for example, `AILabeling`, where you will place all the necessary files.

2. **Move Files:**
   - Copy the generated executable (`dist/main.exe`) into the `AILabeling` folder.
   - Include the `database` directory (if your app uses a database) and the `static` directory (for any static resources like images and icons).

3. **Run the App:**
   - Once the files are in the folder, you can move the folder anywhere on your system and run the app by double-clicking `main.exe`.

Here’s what the folder structure should look like after setting it up:

```bash
AILabeling/
│
├── database/              # Directory for storing database files (if used)
│   └── image_labeling.db  # Example of a database file
├── static/                # Directory for static resources (images, icons, etc.)
│   └── img/*              # Images dir
└── main.exe               # The executable file generated by PyInstaller
```

This folder structure keeps all necessary components organized in one place, allowing you to easily run and manage the application as a portable desktop app.

## Customization

The app is highly customizable. You can modify:
- **Labels:** Add or remove label options through the settings section in the interface.
- **Directories:** Use the settings to switch between different image directories for labeling.
- **File Handling:** The app automatically modifies filenames to include the label ID when a label is applied.

## Contributing

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Open a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
