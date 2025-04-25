from PyQt6.QtGui import QStandardItemModel
from PyQt6.QtWidgets import QTabWidget, QVBoxLayout, QLabel, QTableView, QPushButton

from logic.button_functions import enter_selected_container


class ContainersTab(QTabWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        containers_layout = QVBoxLayout(self)
        containers_label = QLabel("<b>Containers</b>")
        self.containers_table = QTableView()
        self.containers_model = QStandardItemModel()
        self.containers_table.setModel(self.containers_model)
        containers_layout.addWidget(containers_label)
        self.containers_table.verticalHeader().setVisible(False)
        containers_layout.addWidget(self.containers_table)

        # Add a button below the containers table
        enter_container_button = QPushButton("Enter")
        containers_layout.addWidget(enter_container_button)

        # Connect button click to slot
        enter_container_button.clicked.connect(lambda x: enter_selected_container(self.containers_table.selectionModel()))