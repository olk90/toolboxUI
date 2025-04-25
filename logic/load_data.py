import subprocess

from PyQt6.QtGui import QStandardItem
from PyQt6.QtWidgets import QTableView, QHeaderView


def load_data(images_model, containers_model, images_table, containers_table):
    try:
        # Clear the previous data
        images_model.clear()
        containers_model.clear()

        # Run the command
        result = subprocess.run(["toolbox", "list"], text=True, capture_output=True, check=True)

        # Parse the output
        lines = result.stdout.strip().split("\n")

        # Process Images section
        image_headers = ["IMAGE ID", "IMAGE NAME", "CREATED"]
        image_data_lines = []

        # Process Containers section
        container_headers = ["CONTAINER ID", "CONTAINER NAME", "CREATED", "STATUS", "IMAGE NAME"]
        container_data_lines = []

        current_section = None

        for line in lines:
            line = line.strip()
            if not line:
                continue

            # # Check if this is a header line
            if line.startswith("IMAGE ") or line.startswith("IMAGE\t"):
                current_section = "images"
                continue

            if line.startswith("CONTAINER ") or line.startswith("CONTAINER\t"):
                current_section = "containers"
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
        images_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        images_table.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)

        containers_table.resizeColumnsToContents()
        containers_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        containers_table.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)

    except subprocess.CalledProcessError as e:
        # Clear tables and show error
        images_model.clear()
        containers_model.clear()

        images_model.setHorizontalHeaderLabels(["Error"])
        error_item = QStandardItem(f"Error: {e.stderr}")
        images_model.appendRow([error_item])


def parse_line(line, expected_columns):
    columns = []
    current_word = ""
    space_count = 0

    for char in line:
        if char == " ":
            space_count += 1
            if space_count >= 2:  # Use 2+ spaces as column delimiter
                if current_word:
                    columns.append(current_word)
                    current_word = ""
                space_count = 1  # Reset counter but keep track of current space
            elif current_word:  # Add single spaces to current word
                current_word += " "
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
