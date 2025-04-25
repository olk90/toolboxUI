from PyQt6.QtGui import QStandardItemModel
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableView


class ImagesTab(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        images_layout = QVBoxLayout(self)
        images_label = QLabel("<b>Images</b>")
        self.images_table = QTableView()
        self.images_model = QStandardItemModel()
        self.images_table.setModel(self.images_model)
        images_layout.addWidget(images_label)
        self.images_table.verticalHeader().setVisible(False)
        images_layout.addWidget(self.images_table)
