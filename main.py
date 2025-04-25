import sys

from PyQt6.QtGui import QStandardItemModel
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout,
                             QTableView, QLabel, QPushButton, QTabWidget)

from logic.button_functions import enter_selected_container
from logic.load_data import load_data

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QWidget()

    # Create layout and widgets
    main_layout = QVBoxLayout()

    # Create a tab widget to hold both tables
    tab_widget = QTabWidget()
    tab_widget.setTabPosition(QTabWidget.TabPosition.West)

    # Tab for images table
    images_tab = QWidget()
    images_layout = QVBoxLayout(images_tab)
    images_label = QLabel("<b>Images</b>")
    images_table = QTableView()
    images_model = QStandardItemModel()
    images_table.setModel(images_model)
    images_layout.addWidget(images_label)
    images_layout.addWidget(images_table)
    tab_widget.addTab(images_tab, "Images")

    # Tab for containers table
    containers_tab = QWidget()
    containers_layout = QVBoxLayout(containers_tab)
    containers_label = QLabel("<b>Containers</b>")
    containers_table = QTableView()
    containers_model = QStandardItemModel()
    containers_table.setModel(containers_model)
    containers_layout.addWidget(containers_label)
    containers_layout.addWidget(containers_table)

    # Add a button below the containers table
    enter_container_button = QPushButton("Enter")
    containers_layout.addWidget(enter_container_button)
    tab_widget.addTab(containers_tab, "Containers")

    # Add widgets to main layout
    main_layout.addWidget(tab_widget)
    window.setLayout(main_layout)

    # Connect button click to slot
    enter_container_button.clicked.connect(lambda x: enter_selected_container(containers_table.selectionModel()))

    # load data on app launch
    load_data(images_model, containers_model, images_table, containers_table)

    # Set window properties
    window.setWindowTitle("Toolbox UI")
    window.resize(1600, 900)
    window.show()
    sys.exit(app.exec())
