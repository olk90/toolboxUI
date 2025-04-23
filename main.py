import sys

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QStandardItemModel
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout,
                             QTableView, QLabel, QSplitter, QPushButton)

from logic.button_functions import enter_selected_container
from logic.load_data import load_data

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QWidget()

    # Create layout and widgets
    main_layout = QVBoxLayout()

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

    # Add a button below the containers table
    enter_container_button = QPushButton("Enter")
    containers_layout.addWidget(enter_container_button)

    # Add containers to splitter
    splitter.addWidget(images_container)
    splitter.addWidget(containers_container)

    # Add widgets to main layout
    main_layout.addWidget(splitter)
    window.setLayout(main_layout)

    # Connect button click to slot
    enter_container_button.clicked.connect(lambda x: enter_selected_container(containers_table.selectionModel()))

    # load data on app launch
    load_data(images_model, containers_model, images_table, containers_table)

    # Set window properties
    window.setWindowTitle("Toolbox UI")
    window.resize(800, 500)  # Larger size to accommodate two tables
    window.show()
    sys.exit(app.exec())
