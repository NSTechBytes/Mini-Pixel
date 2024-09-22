import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel,
    QProgressBar, QComboBox, QHBoxLayout, QLineEdit
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QIcon
from PIL import Image
import os


class ConversionThread(QThread):
    progress_update = pyqtSignal(int)
    status_update = pyqtSignal(str)

    def __init__(self, images, output_dir, output_format, output_resolution):
        super().__init__()
        self.images = images
        self.output_dir = output_dir
        self.output_format = output_format
        self.output_resolution = output_resolution

    def run(self):
        total_images = len(self.images)
        for i, img_path in enumerate(self.images):
            try:
                # Log which image is being processed
                self.status_update.emit(f"Processing {os.path.basename(img_path)}...")

                # Open and convert the image
                img = Image.open(img_path)
                img = img.resize(self.output_resolution)  # Resize the image

                # Create the new file name
                base_name = os.path.basename(img_path)
                new_file_name = os.path.splitext(base_name)[0] + f"_converted.{self.output_format}"
                save_path = os.path.join(self.output_dir, new_file_name)

                # Save the image in the specified format
                img.save(save_path, format=self.output_format.upper())

                # Update progress
                progress = int(((i + 1) / total_images) * 100)
                self.progress_update.emit(progress)

            except Exception as e:
                # If there's an error, log it but continue with the next image
                self.status_update.emit(f"Error with {os.path.basename(img_path)}: {str(e)}")
                continue  # Skip to the next image

        self.status_update.emit("Conversion complete!")


class MiniPixelApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Set fixed window size
        self.setFixedSize(500, 400)
        self.setWindowTitle('Mini Pixel')

        # Set window toolbar icon
        self.setWindowIcon(QIcon('icons/window_icon.png'))

        # Layout
        layout = QVBoxLayout()

        # Label to display status
        self.status_label = QLabel("Select images to convert", self)
        layout.addWidget(self.status_label)

        # Button to select images with icon
        self.select_button = QPushButton('Select Images', self)
        self.select_button.setIcon(QIcon('icons/select_images.png'))
        self.select_button.clicked.connect(self.select_images)
        layout.addWidget(self.select_button)

        # Dropdown to select resolution
        self.resolution_label = QLabel("Select Resolution", self)
        layout.addWidget(self.resolution_label)

        self.resolution_combo = QComboBox(self)
        self.resolution_combo.addItems([
            "800x600", "1024x768", "1280x720", "1920x1080", "Custom"
        ])
        layout.addWidget(self.resolution_combo)

        # Custom resolution input fields
        self.custom_res_layout = QHBoxLayout()

        self.width_input = QLineEdit(self)
        self.width_input.setPlaceholderText("Width")
        self.custom_res_layout.addWidget(self.width_input)

        self.height_input = QLineEdit(self)
        self.height_input.setPlaceholderText("Height")
        self.custom_res_layout.addWidget(self.height_input)

        layout.addLayout(self.custom_res_layout)

        # Dropdown to select format
        self.format_label = QLabel("Select Format", self)
        layout.addWidget(self.format_label)

        self.format_combo = QComboBox(self)
        self.format_combo.addItems([
            "PNG", "JPG", "JPEG", "BMP"
        ])
        layout.addWidget(self.format_combo)

        # Button to convert images with icon
        self.convert_button = QPushButton('Convert Images', self)
        self.convert_button.setIcon(QIcon('icons/convert_images.png'))
        self.convert_button.setEnabled(False)  # Disabled until images are selected
        self.convert_button.clicked.connect(self.convert_images)
        layout.addWidget(self.convert_button)

        # Progress bar
        self.progress_bar = QProgressBar(self)
        layout.addWidget(self.progress_bar)

        # Label to show percentage
        self.percentage_label = QLabel("0%", self)
        layout.addWidget(self.percentage_label)

        # Set the layout
        self.setLayout(layout)

        # Store selected images
        self.selected_images = []

    def select_images(self):
        # Open file dialog to select multiple images
        options = QFileDialog.Options()
        files, _ = QFileDialog.getOpenFileNames(self, "Select Images", "", "Images (*.png *.jpg *.jpeg *.bmp)", options=options)
        if files:
            self.selected_images = files
            self.status_label.setText(f"{len(files)} images selected")
            self.convert_button.setEnabled(True)

    def convert_images(self):
        if not self.selected_images:
            return

        # Ask the user to select an output directory
        output_dir = QFileDialog.getExistingDirectory(self, "Select Output Directory")
        if not output_dir:
            return  # If the user cancels, do nothing

        # Check if custom resolution is selected
        if self.resolution_combo.currentText() == "Custom":
            try:
                # Get the custom width and height
                custom_width = int(self.width_input.text())
                custom_height = int(self.height_input.text())
                output_resolution = (custom_width, custom_height)
            except ValueError:
                # If input is invalid, show an error
                self.status_label.setText("Error: Invalid custom resolution values.")
                return
        else:
            # Get selected resolution from dropdown
            selected_resolution = self.resolution_combo.currentText()
            width, height = map(int, selected_resolution.split('x'))
            output_resolution = (width, height)

        # Get selected format
        output_format = self.format_combo.currentText().lower()

        # Create and start the conversion thread
        self.thread = ConversionThread(self.selected_images, output_dir, output_format, output_resolution)
        self.thread.progress_update.connect(self.update_progress)
        self.thread.status_update.connect(self.update_status)
        self.thread.start()

    def update_progress(self, value):
        # Update progress bar and percentage
        self.progress_bar.setValue(value)
        self.percentage_label.setText(f"{value}%")

    def update_status(self, message):
        # Update status label
        self.status_label.setText(message)
        if message == "Conversion complete!":
            self.convert_button.setEnabled(False)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MiniPixelApp()
    ex.show()
    sys.exit(app.exec_())
