import subprocess
import sys

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.QtWidgets import (QApplication, QWidget, QPushButton, QVBoxLayout,
                             QTableView, QLabel, QSplitter)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QWidget()

    # Create layout and widgets
    main_layout = QVBoxLayout()
    button = QPushButton("Show Toolboxes")

    # Create a splitter to hold both tables
    splitter = QSplitter(Qt.Orientation.Horizontal)

    # Container for images table
    images_container = QWidget()
    images_layout = QVBoxLayout(images_container)
    images_label = QLabel("<b>Images</b>")
    images_table = QTableView()
    images_model = QStandardItemModel()
    images_table.setModel(images_model)
    images_layout.addWidget(images_label)
    images_layout.addWidget(images_table)

    # Container for containers table
    containers_container = QWidget()
    containers_layout = QVBoxLayout(containers_container)
    containers_label = QLabel("<b>Containers</b>")
    containers_table = QTableView()
    containers_model = QStandardItemModel()
    containers_table.setModel(containers_model)
    containers_layout.addWidget(containers_label)
    containers_layout.addWidget(containers_table)

    # Add containers to splitter
    splitter.addWidget(images_container)
    splitter.addWidget(containers_container)

    # Add widgets to main layout
    main_layout.addWidget(button)
    main_layout.addWidget(splitter)
    window.setLayout(main_layout)


    # Function to parse toolbox output and populate tables
    def show_toolboxes():
        try:
            # Clear the previous data
            images_model.clear()
            containers_model.clear()

            # Run the command
            result = subprocess.run(["toolbox", "list"], text=True, capture_output=True, check=True)

            # Parse the output
            lines = result.stdout.strip().split('\n')

            # Process Images section
            image_headers = []
            image_data_lines = []

            # Process Containers section
            container_headers = []
            container_data_lines = []

            current_section = None

            for line in lines:
                line = line.strip()
                if not line:
                    continue

                # Check if this is a header line
                if line.startswith('IMAGE ') or line.startswith('IMAGE\t'):
                    current_section = "images"
                    image_headers = [h.strip() for h in line.split() if h.strip()]
                    continue

                if line.startswith('CONTAINER ') or line.startswith('CONTAINER\t'):
                    current_section = "containers"
                    container_headers = [h.strip() for h in line.split() if h.strip()]
                    continue

                # Add data lines to appropriate section
                if current_section == "images":
                    image_data_lines.append(line)
                elif current_section == "containers":
                    container_data_lines.append(line)

            # Set headers for images table
            if image_headers:
                images_model.setHorizontalHeaderLabels(image_headers)

            # Set headers for containers table
            if container_headers:
                containers_model.setHorizontalHeaderLabels(container_headers)

            # Helper function to parse a line into columns
            def parse_line(line, expected_columns):
                columns = []
                current_word = ""
                space_count = 0

                for char in line:
                    if char == ' ':
                        space_count += 1
                        if space_count >= 2:  # Use 2+ spaces as column delimiter
                            if current_word:
                                columns.append(current_word)
                                current_word = ""
                            space_count = 1  # Reset counter but keep track of current space
                        elif current_word:  # Add single spaces to current word
                            current_word += ' '
                    else:
                        current_word += char
                        space_count = 0

                # Add the last word
                if current_word:
                    columns.append(current_word)

                # Make sure we have exactly the expected number of columns
                if expected_columns > 0 and len(columns) < expected_columns:
                    # If we have fewer columns than expected, add empty values
                    columns.extend([""] * (expected_columns - len(columns)))

                return columns

            # Populate images table
            for line in image_data_lines:
                row_data = parse_line(line, len(image_headers))
                row_items = [QStandardItem(item.strip()) for item in row_data]
                images_model.appendRow(row_items)

            # Populate containers table
            for line in container_data_lines:
                row_data = parse_line(line, len(container_headers))
                row_items = [QStandardItem(item.strip()) for item in row_data]
                containers_model.appendRow(row_items)

            # Resize columns to content
            images_table.resizeColumnsToContents()
            containers_table.resizeColumnsToContents()

        except subprocess.CalledProcessError as e:
            # Clear tables and show error
            images_model.clear()
            containers_model.clear()

            images_model.setHorizontalHeaderLabels(["Error"])
            error_item = QStandardItem(f"Error: {e.stderr}")
            images_model.appendRow([error_item])


    # Connect button to function
    button.clicked.connect(show_toolboxes)

    # Set window properties
    window.setWindowTitle("Toolbox UI")
    window.resize(800, 500)  # Larger size to accommodate two tables
    window.show()
    sys.exit(app.exec())
