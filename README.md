# Mini Pixel - Batch Image Converter

**Mini Pixel** is a simple and user-friendly GUI-based image converter built using Python and PyQt5. The application allows you to select multiple images, convert them into various formats (PNG, JPEG, BMP), and resize them to custom or predefined resolutions.

## Features
- **Batch Conversion**: Convert multiple images in one go.
- **Format Support**: Supports popular formats like PNG, JPG, JPEG, and BMP.
- **Custom Resolutions**: Resize images to predefined or custom resolutions.
- **Progress Tracking**: Real-time progress bar and percentage display during conversion.
- **Fixed Window Size**: Clean, minimal design with a fixed window size of 600x300 pixels.
- **Icon Support**: The app features custom icons for the window toolbar and buttons.
- **Threaded Execution**: Runs the conversion process in a separate thread to ensure the GUI remains responsive.

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/NSTechBytes/Mini-Pixel.git
   ```
2. Navigate to the project directory:
   ```bash
   cd Mini-Pixel
   ```
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the application:
   ```bash
   python main.py
   ```

## Packaging
- The repository includes an Inno Setup script to create an installer for the application.
- Use **PyInstaller** to compile the app into a standalone `.exe` file.

## How to Use
1. Launch the application.
2. Click on "Select Images" to choose the images you want to convert.
3. Select the desired **format** and **resolution**.
4. Press the "Convert" button, and watch the progress bar fill up as the images are processed.

## Screenshots
![Mini Pixel Screenshot](https://github.com/NSTechBytes/Projects-Templates/blob/main/Applications/Mini%20Pixel/Mini%20Pixel.png)

## Contributing
Feel free to fork the repository, submit issues, or contribute to the project via pull requests!

## License
This project is licensed under the Appache License - see the [LICENSE](LICENSE) file for details.




