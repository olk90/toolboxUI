from PyQt6.QtGui import QStandardItemModel
from PyQt6.QtWidgets import QTabWidget, QVBoxLayout, QLabel, QTableView, QPushButton, QHBoxLayout

from logic.button_functions import enter_container


class ContainersTab(QTabWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        containers_layout = QHBoxLayout(self)

        # Left pane with label and table
        left_pane_layout = QVBoxLayout()
        containers_label = QLabel("<b>Containers</b>")
        self.containers_table = QTableView()
        self.containers_model = QStandardItemModel()
        self.containers_table.setModel(self.containers_model)
        left_pane_layout.addWidget(containers_label)
        self.containers_table.verticalHeader().setVisible(False)
        left_pane_layout.addWidget(self.containers_table)

        # Add left pane to main layout (2/3 of width)
        containers_layout.addLayout(left_pane_layout, stretch=2)

        # Right pane with Enter button
        right_pane_layout = QVBoxLayout()
        actions_label = QLabel("<b>Actions</b>")
        right_pane_layout.addWidget(actions_label)

        right_pane_layout.addStretch(1)  # Spacer to push button to the top
        containers_layout.addLayout(right_pane_layout, stretch=1)

        enter_container_button = QPushButton("Enter")
        right_pane_layout.addWidget(enter_container_button)

        enter_container_button.clicked.connect(
            lambda x: enter_container(self.containers_table.selectionModel()))
